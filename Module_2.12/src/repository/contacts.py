from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import extract, or_, and_

from src.database.models import Contact, User
from src.schemas import ContactModel

from datetime import date, timedelta


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contacts_with_birthday(period_in_days: int, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    bdays_up_to_date = date.today() + timedelta(days=period_in_days)
    return db.query(Contact).filter(
        or_(  # spans across two months
            and_(and_(extract("month", Contact.born_date) == bdays_up_to_date.month, extract("day", Contact.born_date) <= bdays_up_to_date.day),
                 and_(extract("month", Contact.born_date) == date.today().month, extract(
                     "day", Contact.born_date) >= date.today().day),
                 date.today().month < bdays_up_to_date.month
                 ),  # within one month
            and_(and_(extract("day", Contact.born_date) >= date.today().day, extract("day", Contact.born_date) <= bdays_up_to_date.day),
                 date.today().month == bdays_up_to_date.month
                 )
        )
    ).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_name(contact_name: str, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.user_id == user.id, or_(Contact.first_name == contact_name, Contact.last_name == contact_name))).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        born_date=body.born_date,
        email=body.email,
        phone_number=body.phone_number,
        user=user
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.born_date = body.born_date,
        contact.email = body.email,
        contact.phone_number = body.phone_number
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
