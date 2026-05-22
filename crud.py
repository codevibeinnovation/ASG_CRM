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


# def create_user(
#     db: Session,
#     user
# ):

#     new_user = User(
#     name=user.name,
#     email=user.email,
#     password=hash_password(user.password)
# )

#     db.add(new_user)

#     db.commit()

#     db.refresh(new_user)

#     return new_user

# def create_user(db: Session, user: User):
#     # Truncate password to 72 bytes BEFORE hashing
#     truncated_password = user.password[:72]
#     password = hash_password(truncated_password)
    
#     db_user = User(
#         email=user.email,
#         password=hashed_password,  # ✅ CORRECT
#         # ... other fields
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
def create_user(db: Session, user: User):
    truncated_password = user.password[:72]
    hashed_password = hash_password(truncated_password)
    
    db_user = User(
        email=user.email,
        password=hashed_password,
        name=user.name,  # ✅ ADD THIS - make sure UserCreate has a name field
        # ... other fields
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_all_users(db: Session):

    return db.query(User).all()

def create_client(db, client):

    new_client = Client(
        pharmacy_name=client.pharmacy_name,
        contact_person=client.contact_person,
        Mobile_No=client.Mobile_No,
        email=client.email,
        lead_source=client.lead_source,
        address=client.address,
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
    client.lead_source = updated_data.lead_source
    client.address = updated_data.address
    client.city_id = updated_data.city_id
    client.area_id = updated_data.area_id

    db.commit()

    db.refresh(client)

    return client

def delete_client(db, client_id: int):

    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if not client:
        return None

    db.delete(client)
    db.commit()

    return client