from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by email.

    :param email: The email to find a user by.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if it does not exist.
    :rtype : User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user with provided parameters.

    :param body: The data for the user to create.
    :type body: UsertModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the token of the user.

    :param user: The user to update the token for.
    :type user: User
    :param token: A new token.
    :type token: str
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype : None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Returns the flag which indicates if the user's email is confirmed.

    :param email: The email to find a user by.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype : None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the user's avatar, for which email is provided.

    :param email: The email to find a user by.
    :type email: str
    :param url: The link to the new avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if it does not exist.
    :rtype : User | None
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
