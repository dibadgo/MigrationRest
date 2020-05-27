from fastapi import FastAPI
from requests import Request
from starlette.responses import JSONResponse

from rest import workloads, migrations

app = FastAPI()
app.include_router(workloads.router)
app.include_router(migrations.router)


@app.get("/")
def index():
    return "Hi, I'm ready! Based on FastAPI"


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": f"Heads up! Something went wrong: {exc}"},
    )
