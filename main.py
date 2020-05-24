from fastapi import FastAPI
import uvicorn

from rest import workloads

app = FastAPI()


@app.route("/")
def index():
    return "Hi, I'm ready! Based on FastAPI"


if __name__ == "__main__":
    app.include_router(workloads.router)

    uvicorn.run(app, host="0.0.0.0", port=8001)