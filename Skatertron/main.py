from fastapi import FastAPI
from routers import competition_router


app = FastAPI(title="Skatertron", docs_url="/api/docs")
app.include_router(competition_router.router)


@app.get("/")
def root():
    return {"Hello": "Skaters"}
