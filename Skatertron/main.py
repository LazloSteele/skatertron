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


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )
