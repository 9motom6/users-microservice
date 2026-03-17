from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app import models, schemas


def get_user(db: Session, user_id: str) -> models.User | None:
    """
    Retrieves a user from the database by their unique external ID.

    Args:
        db (Session): The database session.
        user_id (str): The unique external identifier of the user to retrieve.

    Returns:
        models.User | None: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.external_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Retrieves a user from the database by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.

    Returns:
        models.User | None: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user data to create.

    Returns:
        models.User: The newly created user object.

    Raises:
        SQLAlchemyError: If there is an error during the database transaction.
    """
    db_user = models.User(
        email=user.email,
        name=user.name,
        date_of_birth=user.date_of_birth,
        external_id=str(user.external_id),
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError:
        db.rollback()
        raise
    return db_user
