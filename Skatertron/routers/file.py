import tempfile

from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio
from datetime import datetime

from sqlalchemy.orm import aliased

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from pathlib import Path
from typing import Annotated, List, Dict

from Skatertron.models.file import File as FileDBModel
from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.models.event import Event as EventDBModel
from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.schemas.file import File as FileSchema
from Skatertron.schemas.upload_item import UploadItem
from Skatertron.database import get_db_session
from Skatertron.database import session_manager
from Skatertron.utils import extract_metadata
from Skatertron.utils.video_formatter import VideoFormatter

import shutil
import magic


router = APIRouter(
    prefix="/files",
    tags=["files"]
)


templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
async def create_file(
                skate_id: Annotated[str, Form()],
                file_name: Annotated[str, Form()],
                creation_datetime: Annotated[datetime, Form()],
                request: Request,
                uploaded_file: UploadFile = File(...)
                ):
    context = await get_file_path_from_skate_id(skate_id, file_name)

    file_type = uploaded_file.content_type

    if file_type.startswith("video/"):
        # Create a temporary file for the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            # Save the uploaded video content into the temporary file
            shutil.copyfileobj(uploaded_file.file, temp_video_file)

            # Get the temporary file path
            video_path = temp_video_file.name

            processed_path = VideoFormatter.format_video(video_path)

            shutil.move(processed_path, context["path"])

    else:
        with open(context["path"], 'wb') as file:
            shutil.copyfileobj(uploaded_file.file, file)

    try:
        file = FileDBModel(skate_id=int(skate_id),
                           file_name=file_name,
                           file_path=context["file_path"],
                           file_type=uploaded_file.content_type,
                           creation_time=creation_datetime,
                           )

        with session_manager.session() as session:
            session.add(file)
            session.commit()

        return templates.TemplateResponse(
            request=request,
            name="file.html",
            context={
                "file": file
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from file model.")


@router.get("/{file_id}/status")
def get_file_status_by_id(file_id: int):
    pass


@router.get("/", response_model=list[FileSchema])
def get_all_files():
    all_files = get_db_session().__next__().query(FileDBModel).all()

    return all_files


@router.get("/{file_id}", response_model=FileSchema)
def get_file_by_id(file_id: int):
    try:
        with get_db_session().__next__() as session:
            file = session.query(FileDBModel).filter_by(id=file_id).first()

            return file
    except IntegrityError:
        raise HTTPException(404, f"File with id #{file_id} not found.")


@router.get("/{file_id}/media", response_class=HTMLResponse)
def get_media_by_id(file_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            file = session.query(FileDBModel).filter_by(id=file_id).first()
            path = f"{file.file_path}{file.file_name}"

            '''
            # noinspection PyTypeChecker
            return StreamingResponse(iterfile(), media_type=file.file_type)
            '''
            return templates.TemplateResponse(
                request=request,
                name="media_player.html",
                context={
                    "path": path,
                    "file_type": file.file_type,
                    "file_name": file.file_name
                }

            )
    except IntegrityError:
        raise HTTPException(404, f"File with id #{file_id} not found.")


@router.get("/files_by_skate/{skate_id}", response_class=HTMLResponse)
def get_files_by_skate(request: Request, skate_id: int):
    try:
        with get_db_session().__next__() as session:
            files_list = session.query(FileDBModel).filter_by(skate_id=skate_id).all()

        return templates.TemplateResponse(
            request=request,
            name="files_by_skate.html",
            context={
                "files_list": files_list,
                "current_skate_id": skate_id
            }
        )

    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")


@router.put("/{file_id}")
def update_file(file_id: int,
                new_skate_id: int | None = None,
                new_file_name: str | None = None
                ):
    with get_db_session().__next__() as session:
        try:
            file = session.query(FileDBModel).filter_by(id=file_id).first()
            if new_skate_id:
                file.skate_id = new_skate_id
            if new_file_name:
                file.file_name = new_file_name

            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"File with id: #{file_id} not found.")


@router.delete("/{file_id}")
def delete_file(file_id: int):
    with get_db_session().__next__() as session:
        try:
            file = session.query(FileDBModel).filter_by(id=file_id).first()

            session.delete(file)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"File with id: #{file_id} not found.")


@router.post("/{file_id}/stage")
def stage_file(
        upload_request: dict
):
    pass


@router.post("/bulk_upload")
async def upload_from_queue(
        files: List[UploadFile] = File(...),
        skate_ids: str = Form(...),
):
    skate_ids_list = json.loads(skate_ids)  # Deserialize skate_ids from JSON string
    for file, skate_id in zip(files, skate_ids_list):
        contents = await file.read()  # Read the contents of the file
        print(f"Received file: {file.filename} with skate_id: {skate_id}")

    return {"message": "Upload successful"}


@router.post("/get_creation_datetime")
async def get_creation_datetime(file_slice: UploadFile = File(...)):
    file_contents = await file_slice.read()

    file_type = await get_file_type(file_contents)

    if file_type.startswith("image/"):
        print("MARKED AS IMAGE!!!")
        metadata = await extract_metadata.get_image_metadata(file_contents)
    elif file_type.startswith("video/"):
        metadata = await extract_metadata.get_video_metadata(file_contents)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type!")

    return JSONResponse(content=metadata)


async def get_file_type(file_path):
    loop = asyncio.get_event_loop()
    mime = await loop.run_in_executor(None, lambda: magic.Magic(mime=True).from_buffer(file_path))
    return mime


async def get_skate_details(skate_id):
    try:
        with session_manager.session() as session:
            current_skate = session.query(SkateDBModel).filter_by(id=int(skate_id)).first()
            current_event = session.query(EventDBModel).filter_by(id=current_skate.event_id).first()
            current_competition = session.query(CompetitionDBModel).filter_by(id=current_event.competition_id).first()

            context = {
                "current_skate": current_skate,
                "current_event": current_event,
                "current_competition": current_competition
            }

            return context

    except UnmappedInstanceError:
        raise HTTPException(404, f"Skate with id#{skate_id} not found!")


async def get_file_path_from_skate_id(skate_id, file_name):
    try:
        context = await get_skate_details(skate_id)
        current_competition = context["current_competition"]
        current_event = context["current_event"]
        current_skate = context["current_skate"]

        competition_path = f"{current_competition.competition_year}_{current_competition.competition_name}"
        event_path = f"{current_event.event_number}_{current_event.event_name}"

    except IntegrityError:
        raise HTTPException(404, "Data not found.")

    file_name = f"{current_skate.skater_name.replace(' ', '_')}_{file_name.replace(' ', '_')}"
    file_path = f"static/media/{competition_path.replace(' ', '_')}/{event_path.replace(' ', '_')}/"
    path = Path(f"{file_path}{file_name}")
    path.parent.mkdir(parents=True, exist_ok=True)

    context = {
        "file_name": file_name,
        "file_path": file_path,
        "path": path
    }

    return context
