from fastapi import FastAPI
import uvicorn
from requests import Request
from starlette.responses import JSONResponse

from rest import workloads, migrations

app = FastAPI()


@app.get("/")
def index():
    return "Hi, I'm ready! Based on FastAPI"


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc} did something. There goes a rainbow..."},
    )


if __name__ == "__main__":
    app.include_router(workloads.router)
    app.include_router(migrations.router)

    uvicorn.run(app, host="0.0.0.0", port=8001)
