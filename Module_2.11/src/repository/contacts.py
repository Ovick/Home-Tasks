from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.database.models import Contact
from src.schemas import ContactModel
from src.repository.utils import days_to_birthday

from datetime import datetime


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contacts_with_birthday(period_in_days: int, skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).filter(days_to_birthday(Contact.born_date) <= period_in_days).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contact_by_name(contact_name: str, db: Session) -> Contact:
    return db.query(Contact).filter(or_(Contact.first_name == contact_name, Contact.last_name == contact_name)).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        born_date=body.born_date,
        email=body.email,
        phone_number=body.phone_number
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.born_date = body.born_date,
        contact.email = body.email,
        contact.phone_number = body.phone_number
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
