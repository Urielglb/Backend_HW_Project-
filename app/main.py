from fastapi import FastAPI
from sqlmodel import Session, select
from pydantic import BaseModel
from enum import Enum
from app.core.db import init_db, get_session
from app.core.config import settings
from app.api.routes.main import api_router
from app.models.user import User
from faker import Faker
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.title = "ATM Simple API"
app.version = "0.1"

fake = Faker()


class CardTypeEnum(str, Enum):
    star = "star"
    pulse = "pulse"
    maestro = "maestro"
    mastercard = "mastercard"
    visa = "visa"
    plus = "plus"


def populate_data(session: Session):
    for _ in range(50):
        fake_user = User(
            name=fake.name(),
            pin=fake.bothify(text="####"),
            balance=fake.pyfloat(left_digits=3, right_digits=2, positive=True),
            card_type=fake.random_element(elements=[card for card in CardTypeEnum]),
            bank_account=fake.bothify(text="######"),
        )
        session.add(fake_user)
    session.commit()


@app.on_event("startup")
def startup_event():
    init_db()
    with next(get_session()) as session:
        user_count = session.exec(select(User)).all()
        if len(user_count) == 0:
            populate_data(session)
            print("Base de datos poblada con datos dummy.")
        else:
            print("La base de datos ya tiene datos.")


class CamelModel(BaseModel):
    class Config:
        alias_generator = lambda string: "".join(
            word.capitalize() if i else word for i, word in enumerate(string.split("_"))
        )
        allow_population_by_field_name = True


@app.get("/")
def read_root():
    return "Backend is running"


if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGIN
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)
