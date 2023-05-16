from fastapi import FastAPI
import uvicorn

from src.routes import contacts

app = FastAPI()
app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Contacts Book"}


if __name__ == "__main__":
    uvicorn.run("main:app", headers=[("localhost:8000", "rest_app")])
