from xmlrpc import client

from sqlalchemy.orm import Session

from models import User,Client

from auth_config import hash_password


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db: Session,
    user
):

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

def get_all_users(db: Session):

    return db.query(User).all()

def create_client(db, client):
    new_client = Client(
        pharmacy_name=client.pharmacy_name,
        contact_person=client.contact_person,
        Mobile_No=client.Mobile_No,
        email=client.email,
        city_id=client.city_id,
        area_id=client.area_id
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client

def get_clients(db):
    return db.query(Client).all()

def search_clients(db, name: str):
    return db.query(Client).filter(
        Client.pharmacy_name.ilike(f"%{name}%")
    ).all()

def update_client(db, client_id: int, updated_data):

    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if not client:
        return None

    client.pharmacy_name = updated_data.pharmacy_name
    client.contact_person = updated_data.contact_person
    client.Mobile_No = updated_data.Mobile_No
    client.email = updated_data.email
    client.city_id = updated_data.city_id
    client.area_id = updated_data.area_id

    db.commit()
    db.refresh(client)

    return client

from models import Client

def delete_client(db, client_id: int):

    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if not client:
        return None

    db.delete(client)
    db.commit()

    return client