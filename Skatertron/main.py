from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import competition, event, skate, file

# this is the app
app = FastAPI(title="Skatertron", docs_url="/api/docs")

# include fastapi routers to the data model endpoints
app.include_router(competition.router)
app.include_router(event.router)
app.include_router(skate.router)
app.include_router(file.router)

# Mount a directory for serving static files like CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# initialize html templating engine
templates = Jinja2Templates(directory="templates")


# root path for main app frame
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
