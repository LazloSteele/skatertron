from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from typing import Annotated
from tempfile import NamedTemporaryFile
import subprocess

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from Skatertron.models.skate import Skate as SkateDBModel
from Skatertron.schemas.skate import Skate as SkateSchema
from Skatertron.models.event import Event as EventDBModel
from Skatertron.models.competition import Competition as CompetitionDBModel
from Skatertron.models.file import File as FileDBModel
from Skatertron.database import get_db_session
from Skatertron.utils import extract_metadata

router = APIRouter(
    prefix="/skates",
    tags=["skates"]
)

templates = Jinja2Templates(directory="templates")


@router.post("/", status_code=201, response_class=HTMLResponse)
def create_skate(event_id: Annotated[int, Form()],
                 skater_name: Annotated[str, Form()],
                 request: Request):
    try:
        skate = SkateDBModel(event_id=event_id,
                             skater_name=skater_name
                             )

        with get_db_session().__next__() as session:
            session.add(skate)
            session.commit()

        return templates.TemplateResponse(
            request=request,
            name="new_skate.html",
            context={
                "skate": skate
            }
        )

    except IntegrityError:
        raise HTTPException(422, "Missing data from skate model.")


@router.get("/{skate_id}", response_model=SkateSchema)
def get_skate_by_id(skate_id: int):
    try:
        with get_db_session().__next__() as session:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()

            return skate
    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")


@router.get("/{skate_id}/details", response_class=HTMLResponse)
def get_context_by_skate_id(skate_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            current_skate = get_skate_by_id(skate_id)
            current_event = session.query(EventDBModel).filter_by(id=current_skate.event_id).first()
            current_competition = session.query(CompetitionDBModel).filter_by(id=current_event.competition_id).first()

        return templates.TemplateResponse(
            request=request,
            name="file_browser_context.html",
            context={
                "skate_id": skate_id,
                "current_skate": current_skate.skater_name,
                "current_event": f"{current_event.event_number} {current_event.event_name}",
                "current_competition": f"{current_competition.competition_year} {current_competition.competition_name}"
            }
        )

    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")


@router.get("/{skate_id}/details/json", response_class=JSONResponse)
def get_context_by_skate_id_json(skate_id: int, request: Request):
    try:
        with get_db_session().__next__() as session:
            current_skate = get_skate_by_id(skate_id)

        content = {
            "id": skate_id,
            "event_id": current_skate.event_id,
            "skater_name": current_skate.skater_name,
            "footage_exceptions": current_skate.footage_exceptions,
            "skate_position": current_skate.skate_position
        }
        print(content)
        return JSONResponse(
            content=content,
            status_code=200
        )

    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")
@router.get("/{skate_id}/files", response_class=HTMLResponse)
def get_files_by_skate_id(request: Request, skate_id: int):
    try:
        with get_db_session().__next__() as session:
            files_list = session.query(FileDBModel).filter_by(skate_id=skate_id).all()
            current_skate = get_skate_by_id(skate_id)
            current_event = session.query(EventDBModel).filter_by(id=current_skate.event_id).first()
            current_competition = session.query(CompetitionDBModel).filter_by(id=current_event.competition_id).first()

        return templates.TemplateResponse(
            request=request,
            name="files_by_skate.html",
            context={
                "files_list": files_list,
                "current_skate": current_skate,
                "current_event": current_event,
                "current_competition": current_competition
            }
        )

    except IntegrityError:
        raise HTTPException(404, f"Skate with id #{skate_id} not found.")


@router.put("/{skate_id}")
def update_event(skate_id: int,
                 new_event_id: int | None = None,
                 new_skater_name: str | None = None,
                 ):
    with get_db_session().__next__() as session:
        try:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()
            if new_event_id:
                skate.event_id = new_event_id
            if new_skater_name:
                skate.skater_name = new_skater_name

            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Skate with id: #{skate_id} not found.")


@router.delete("/{skate_id}")
def delete_event(skate_id: int):
    with get_db_session().__next__() as session:
        try:
            skate = session.query(SkateDBModel).filter_by(id=skate_id).first()

            session.delete(skate)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"Skate with id: #{skate_id} not found.")


@router.post("/{skate_id}/stage_file")
async def stage_file(skate_id: int, file: UploadFile = File(...)):
    # Save a temporary file
    with open("temp_file", "wb") as temp:
        temp.write(await file.read(1024 * 100))  # Read only the first 100 KB

    # Use ffprobe to extract metadata
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format_tags=creation_time", "-of", "default=nw=1", "temp_file"],
        capture_output=True,
        text=True,
    )

    return {
        "skate_id": skate_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "creation_time": result.stdout.strip()[18:],
    }
