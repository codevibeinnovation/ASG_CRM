from xmlrpc import client

from sqlalchemy.orm import Session

from models import User,Client

from auth_config import hash_password
from database import SessionLocal
from auth import ADMIN_EMAIL, ADMIN_PASSWORD

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

        name=user.name,

        role=user.role
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

def create_default_admin():

    db = SessionLocal()

    existing_admin = db.query(User).filter(
        User.email == ADMIN_EMAIL
    ).first()

    if not existing_admin:

        admin_user = User(
            name="Admin",
            email=ADMIN_EMAIL,
            password=hash_password(ADMIN_PASSWORD),
            role="admin"
        )

        db.add(admin_user)

        db.commit()

        print("✅ Default admin created")

    else:

        print("✅ Admin already exists")

    db.close()


def create_deal(db: Session, deal: schemas.DealCreate):

    new_deal = models.Deal(

        client_id=deal.client_id,

        deal_person_name=deal.deal_person_name,

        deal_name=deal.deal_name,

        contact_person_name=deal.contact_person_name,

        amount=deal.amount,

        closing_date=deal.closing_date,

        description=deal.description,

        number_of_devices=deal.number_of_devices,

        software_type=deal.software_type,

    )

    db.add(new_deal)

    db.commit()

    db.refresh(new_deal)

    return new_deal

def get_deals(db: Session):

    return db.query(models.Deal).all()

def get_deal(db: Session, deal_id: int):

    return db.query(models.Deal).filter(
        models.Deal.id == deal_id
    ).first()

def update_deal(
    db: Session,
    deal_id: int,
    deal: schemas.DealCreate
):

    existing_deal = db.query(models.Deal).filter(
        models.Deal.id == deal_id
    ).first()

    if not existing_deal:

        return None

    existing_deal.client_id = deal.client_id
    existing_deal.deal_person_name = deal.deal_person_name
    existing_deal.deal_name = deal.deal_name
    existing_deal.contact_person_name = deal.contact_person_name
    existing_deal.amount = deal.amount
    existing_deal.closing_date = deal.closing_date
    existing_deal.description = deal.description
    existing_deal.number_of_devices = deal.number_of_devices
    existing_deal.software_type = deal.software_type


    db.commit()

    db.refresh(existing_deal)

    return existing_deal

def delete_deal(db: Session, deal_id: int):

    deal = db.query(models.Deal).filter(
        models.Deal.id == deal_id
    ).first()

    if not deal:

        return None

    db.delete(deal)

    db.commit()

    return deal