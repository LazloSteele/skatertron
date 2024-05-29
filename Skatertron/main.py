from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import competition, event, skate, file

app = FastAPI(title="Skatertron", docs_url="/api/docs")
app.include_router(competition.router)
app.include_router(event.router)
app.include_router(skate.router)
app.include_router(file.router)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

current_competition = 0


@app.get("/", response_class=HTMLResponse)
def root(request: Request):

    competitions_list = competition.get_all_competitions()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "competitions_list": competitions_list
        }
    )


@app.get("/new_event_modal/{competition_id}", response_class=HTMLResponse)
def new_event_modal(request: Request, competition_id: int):
    return templates.TemplateResponse(
        request=request,
        name="new_event_modal.html",
        context={
            "competition_id": competition_id
        }
    )
