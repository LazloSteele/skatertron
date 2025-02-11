from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from pathlib import Path
from typing import Annotated, List, Dict

from Skatertron.models.file import File as FileDBModel
from Skatertron.schemas.file import File as FileSchema
from Skatertron.schemas.upload_item import UploadItem
from Skatertron.database import get_db_session

import shutil

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
def create_file(competition: Annotated[str, Form()],
                event: Annotated[str, Form()],
                skater: Annotated[str, Form()],
                skate_id: Annotated[str, Form()],
                request: Request,
                uploaded_file: UploadFile = File(...)
                ):

    file_name = f"{competition} - {event} - {skater} - {uploaded_file.filename}"
    file_path = f"static/media/{competition}/{event}/"
    path = Path(f"{file_path}{file_name}")
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'wb') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    try:
        file = FileDBModel(skate_id=int(skate_id),
                           file_name=file_name,
                           file_path=file_path,
                           file_type=uploaded_file.content_type
                           )

        with get_db_session().__next__() as session:
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
