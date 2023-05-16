import uvicorn
from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr, BaseModel
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis


from src.services import auth
from src.services.email import conf
from src.routes import contacts, auth, users


origins = [
    "http://localhost:3000"
]


app = FastAPI()
app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailSchema(BaseModel):
    email: EmailStr


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def index():
    return {"msg": "Hello World"}


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Volodymyr Kuznetsov"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message,
                              template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == "__main__":
    uvicorn.run("main:app", headers=[
                ("localhost:8000", "rest_app")], reload=True)
