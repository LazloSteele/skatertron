import os
import tempfile

from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from pathlib import Path
from typing import Annotated, List

from Skatertron.models.file import File as FileDBModel
from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.models.event import Event as EventDBModel
from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.schemas.file import File as FileSchema
from Skatertron.database import get_db_session
from Skatertron.database import session_manager
from Skatertron.utils import extract_metadata
from Skatertron.utils.video_formatter import VideoFormatter

import aiofiles
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
    external_drive_tmp = r"S:\2025 Omaha Winterfest\tmp"

    os.makedirs(external_drive_tmp, exist_ok=True)

    context = await get_file_path_from_skate_id(skate_id, file_name)

    file_type = await get_file_type(await uploaded_file.read(20 * 1024))

    '''
    if file_type.startswith("video/"):
        # Create a temporary file for the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mov", dir=external_drive_tmp) as temp_video_file:
            temp_video_path = temp_video_file.name

        async with aiofiles.open(temp_video_path, "wb") as out_file:
            while True:
                chunk = await uploaded_file.read(1024 * 1024)
                if not chunk:
                    break

                await out_file.write(chunk)

        try:
            processed_video_path = await VideoFormatter.format_video(temp_video_path)

        except Exception as e:
            os.remove(temp_video_path)
            raise HTTPException(status_code=500, detail=f"Video Processing failed: {e}")

        try:
            await asyncio.to_thread(os.rename, processed_video_path, context["path"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error moving file: {e}")

        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

        print(f"Video uploaded and processed successfully. Saved to {context['path']}")
    
    else:
        async with aiofiles.open(context["path"], 'wb') as dest:
            while True:
                chunk = await uploaded_file.read(1024 * 1024)
                if not chunk:
                    break
                await dest.write(chunk)
    '''
    # Delete this next block when reimplementing the converter!!!
    async with aiofiles.open(context["path"], 'wb') as dest:
        while True:
            chunk = await uploaded_file.read(1024 * 1024)
            if not chunk:
                break
            await dest.write(chunk)

    try:
        file = FileDBModel(skate_id=int(skate_id),
                           file_name=file_name,
                           file_path=context["path"],
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

        event_path = f"{current_event.event_number}_{current_event.event_name}"

    except IntegrityError:
        raise HTTPException(404, "Data not found.")

    new_file_name = f"{current_skate.skater_name}_{file_name}".replace(' ', '_').replace('/', '-').replace('&', '_and_')
    file_path = f"{event_path}".replace(' ', '_').replace('/', '-').replace('&', '_and_')
    path = Path(f"S:/2025 Omaha Winterfest/{file_path}/{new_file_name}")
    path.parent.mkdir(parents=True, exist_ok=True)

    context = {
        "file_name": new_file_name,
        "file_path": file_path,
        "path": fr"{path}"
    }

    return context
