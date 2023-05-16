from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import extract, or_, and_

from src.database.models import Contact, User
from src.schemas import ContactModel

from datetime import date, timedelta


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contacts_with_birthday(period_in_days: int, skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts with burthday date in the next specified number of days with specified pagination parameters.

    :param period_in_days: The number of days forward.
    :type period_in_days: int
    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
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
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_name(contact_name: str, user: User, db: Session) -> Contact:
    """
    Retrieves a specific contact with match by first or last name.

    :param contact_name: The contact first or last name.
    :type contact_name: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.user_id == user.id, or_(Contact.first_name == contact_name, Contact.last_name == contact_name))).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
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
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
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
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
