from fastapi import FastAPI
from routers import competition, event, skate, file


app = FastAPI(title="Skatertron", docs_url="/api/docs")
app.include_router(competition.router)
app.include_router(event.router)
app.include_router(skate.router)
app.include_router(file.router)


@app.get("/")
def root():
    return {"Hello": "Skaters"}
