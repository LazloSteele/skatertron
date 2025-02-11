from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)


templates = Jinja2Templates(directory="templates")


@router.get("/staged", response_class=HTMLResponse)
def get_staged_message(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="staged.html"
    )


@router.get("/upload_queue", response_class=HTMLResponse)
def upload_queue(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload_queue.html"
    )
