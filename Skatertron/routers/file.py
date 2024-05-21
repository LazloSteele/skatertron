from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from Skatertron.models.file import File as FileDBModel
from Skatertron.schemas.file import File as FileSchema
from Skatertron.database import get_db_session

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


@router.post("/")
def create_file(file_schema: FileSchema):
    try:
        file = FileDBModel(skate_id=file_schema.skate_id,
                           file_name=file_schema.file_name
                           )
    except IntegrityError:
        raise HTTPException(422, "Missing data from file model.")

    with get_db_session().__next__() as session:
        session.add(file)
        session.commit()


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


@router.put("/{file_id}")
def update_file(file_id: int,
                new_skate_id: int | None = None,
                new_file_name: str | None = None,
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
def delete_skate(file_id: int):
    with get_db_session().__next__() as session:
        try:
            file = session.query(FileDBModel).filter_by(id=file_id).first()

            session.delete(file)
            session.commit()
        except UnmappedInstanceError:
            raise HTTPException(404, f"File with id: #{file_id} not found.")
