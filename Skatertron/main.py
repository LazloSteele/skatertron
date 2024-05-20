from fastapi import FastAPI
from models import Base, Competition
from database import session_manager, get_db_session

app = FastAPI()


@app.get("/")
def root():
    all_competitions = get_db_session().__next__().query(Competition).all()

    return all_competitions
