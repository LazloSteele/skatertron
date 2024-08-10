from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers import competition, event, skate, file
from mq.mq_worker import MQWorker
from mq.mq_task import MQTask

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


def get_mq():
    return MQWorker()


worker = get_mq()


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


'''
@app.post("/mq")
async def send_message(message: str | bytes, background_tasks: BackgroundTasks, task_rabbit: MQTask):
    # Publish the message to RabbitMQ
    background_tasks.add_task(task_rabbit.new_task(worker.connection, message))
    return {"status": "Message sent"}


@app.on_event("shutdown")
def shutdown_event(worker: MQWorker = Depends(get_mq)):
    # Ensure the RabbitMQ connection is closed when the app shuts down
    worker.close_connection()
'''
