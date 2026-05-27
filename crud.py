from sqlalchemy.orm import Session

from datetime import (
    datetime,
    date,
    timedelta
)

import models
import schemas

from models import (
    User,
    Client,
    Demo,
    Deal,
    Reminder
)

from auth_config import hash_password


from auth import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD
)


# =========================
# USER SECTION
# =========================

def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db: Session,
    user: schemas.UserCreate
):

    hashed_password = hash_password(
        user.password[:72]
    )

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_all_users(db: Session):

    return db.query(User).all()


# =========================
# DEFAULT ADMIN
# =========================

def create_default_admin():

    from database import SessionLocal

    db = SessionLocal()

    if not ADMIN_EMAIL or not ADMIN_PASSWORD:

        print("❌ ADMIN_EMAIL or ADMIN_PASSWORD missing")

        return

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

# =========================
# CLIENT SECTION
# =========================

def create_client(
    db: Session,
    client: schemas.ClientCreate,
    user_id: int
):

    new_client = Client(

        pharmacy_name=client.pharmacy_name,

        contact_person=client.contact_person,

        Mobile_No=client.Mobile_No,

        email=client.email,

        lead_source=client.lead_source,

        address=client.address,

        city_id=client.city_id,

        area_id=client.area_id,

        created_by=user_id
    )

    db.add(new_client)

    db.commit()

    db.refresh(new_client)

    return new_client


def get_clients(db: Session):

    return db.query(Client).all()


def get_my_clients(
    db: Session,
    user_id: int
):

    return db.query(Client).filter(
        Client.created_by == user_id
    ).all()


def search_clients(
    db: Session,
    name: str
):

    return db.query(Client).filter(
        Client.pharmacy_name.ilike(
            f"%{name}%"
        )
    ).all()


def update_client(
    db: Session,
    client_id: int,
    updated_data
):

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


def delete_client(
    db: Session,
    client_id: int
):

    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if not client:

        return None

    db.delete(client)

    db.commit()

    return client

# =========================
# CITY SECTION
# =========================

def create_city(

    db: Session,

    city: schemas.CityCreate
):

    new_city = models.City(

        name=city.name
    )

    db.add(new_city)

    db.commit()

    db.refresh(new_city)

    return new_city


def get_cities(db: Session):

    return db.query(
        models.City
    ).all()

def update_city(

    db: Session,

    city_id: int,

    city: schemas.CityCreate
):

    existing_city = db.query(
        models.City
    ).filter(

        models.City.id == city_id

    ).first()

    if not existing_city:

        return None

    existing_city.name = city.name

    db.commit()

    db.refresh(existing_city)

    return existing_city

def delete_city(

    db: Session,

    city_id: int
):

    city = db.query(
        models.City
    ).filter(

        models.City.id == city_id

    ).first()

    if not city:

        return None

    db.delete(city)

    db.commit()

    return city

# =========================
# AREA SECTION
# =========================

def create_area(

    db: Session,

    area: schemas.AreaCreate
):

    new_area = models.Area(

        name=area.name,

        city_id=area.city_id
    )

    db.add(new_area)

    db.commit()

    db.refresh(new_area)

    return new_area


def get_areas(db: Session):

    return db.query(
        models.Area
    ).all()

def update_area(

    db: Session,

    area_id: int,

    area: schemas.AreaCreate
):

    existing_area = db.query(
        models.Area
    ).filter(

        models.Area.id == area_id

    ).first()

    if not existing_area:

        return None

    existing_area.name = area.name

    existing_area.city_id = area.city_id

    db.commit()

    db.refresh(existing_area)

    return existing_area

def delete_area(

    db: Session,

    area_id: int
):

    area = db.query(
        models.Area
    ).filter(

        models.Area.id == area_id

    ).first()

    if not area:

        return None

    db.delete(area)

    db.commit()

    return area

# =========================
# EXISTING PRODUCT SECTION
# =========================

def create_existing_product(

    db: Session,

    product: schemas.ExistingProductCreate
):

    new_product = models.ExistingProduct(

        product_name=product.product_name
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product


def get_existing_products(db: Session):

    return db.query(
        models.ExistingProduct
    ).all()

def update_existing_product(

    db: Session,

    product_id: int,

    product: schemas.ExistingProductCreate
):

    existing_product = db.query(
        models.ExistingProduct
    ).filter(

        models.ExistingProduct.id == product_id

    ).first()

    if not existing_product:

        return None

    existing_product.product_name = product.product_name

    db.commit()

    db.refresh(existing_product)

    return existing_product

def delete_existing_product(

    db: Session,

    product_id: int
):

    product = db.query(
        models.ExistingProduct
    ).filter(

        models.ExistingProduct.id == product_id

    ).first()

    if not product:

        return None

    db.delete(product)

    db.commit()

    return product

# =========================
# DEMO SECTION
# =========================

def create_demo(
    db: Session,
    demo: schemas.DemoCreate
):

    expiry_date = None

    if demo.installation_date:

        expiry_date = (
            demo.installation_date
            + timedelta(days=demo.trial_days)
        )

    new_demo = Demo(

        client_id=demo.client_id,

        assigned_employee_id=demo.assigned_employee_id,

        demo_date=demo.demo_date,

        demo_time=demo.demo_time,

        demo_feedback=demo.demo_feedback,

        meeting_notes=demo.meeting_notes,

        demo_status=demo.demo_status,

        demo_location=demo.demo_location,

        demo_installed=demo.demo_installed,

        installation_date=demo.installation_date,

        trial_days=demo.trial_days,

        trial_expiry_date=expiry_date,

        trial_status="active"
    )

    db.add(new_demo)

    db.commit()

    db.refresh(new_demo)

    return new_demo


def get_demos(db: Session):

    return db.query(Demo).all()


def get_my_demos(
    db: Session,
    user_id: int
):

    return db.query(Demo).filter(
        Demo.assigned_employee_id == user_id
    ).all()


def check_expired_trials(
    db: Session
):

    demos = db.query(Demo).all()

    today = date.today()

    for demo in demos:

        if (
            demo.trial_expiry_date
            and demo.trial_expiry_date < today
        ):

            demo.trial_status = "expired"

    db.commit()


# =========================
# DEAL SECTION
# =========================

def create_deal(
    db: Session,
    deal: schemas.DealCreate
):

    renewal_date = (
        deal.end_date - timedelta(days=30)
    )

    new_deal = Deal(

        client_id=deal.client_id,

        deal_owner_id=deal.deal_owner_id,

        deal_name=deal.deal_name,

        software_type=deal.software_type,

        amount=deal.amount,

        number_of_devices=deal.number_of_devices,

        start_date=deal.start_date,

        end_date=deal.end_date,

        renewal_reminder_date=renewal_date,

        notes=deal.notes
    )

    db.add(new_deal)

    db.commit()

    db.refresh(new_deal)

    return new_deal


def get_deals(db: Session):

    return db.query(Deal).all()


def get_deal(
    db: Session,
    deal_id: int
):

    return db.query(Deal).filter(
        Deal.id == deal_id
    ).first()


def update_deal(
    db: Session,
    deal_id: int,
    deal: schemas.DealCreate
):

    existing_deal = db.query(Deal).filter(
        Deal.id == deal_id
    ).first()

    if not existing_deal:

        return None

    existing_deal.deal_name = deal.deal_name

    existing_deal.amount = deal.amount

    existing_deal.software_type = deal.software_type

    existing_deal.number_of_devices = deal.number_of_devices

    existing_deal.start_date = deal.start_date

    existing_deal.end_date = deal.end_date

    existing_deal.notes = deal.notes

    db.commit()

    db.refresh(existing_deal)

    return existing_deal


def delete_deal(
    db: Session,
    deal_id: int
):

    deal = db.query(Deal).filter(
        Deal.id == deal_id
    ).first()

    if not deal:

        return None

    db.delete(deal)

    db.commit()

    return deal


def create_reminder(
    db: Session,
    reminder: schemas.ReminderCreate
):

    new_reminder = Reminder(

        client_id=reminder.client_id,

        user_id=reminder.user_id,

        reminder_date=reminder.reminder_date,

        reminder_time=reminder.reminder_time,

        description=reminder.description,

        status="pending"
    )

    db.add(new_reminder)

    db.commit()

    db.refresh(new_reminder)

    return new_reminder

def create_renewal_reminders(
    db: Session
):

    today = date.today()

    deals = db.query(Deal).filter(
        Deal.renewal_reminder_date == today
    ).all()

    for deal in deals:

        reminder = Reminder(

            client_id=deal.client_id,

            user_id=deal.deal_person_id,

            reminder_date=today,

            description="Software renewal due in 30 days",

            status="pending"
        )

        db.add(reminder)

    db.commit()

def create_renewal_reminders(
    db: Session
):

    today = date.today()

    deals = db.query(Deal).filter(
        Deal.renewal_reminder_date == today
    ).all()

    for deal in deals:

        reminder = Reminder(

            client_id=deal.client_id,

            user_id=deal.deal_person_id,

            reminder_date=today,

            description="Software renewal due in 30 days",

            status="pending"
        )

        db.add(reminder)

    db.commit()
def create_trial_expiry_reminders(
    db: Session
):

    today = date.today()

    demos = db.query(Demo).filter(
        Demo.trial_end_date == today
    ).all()

    for demo in demos:

        reminder = Reminder(

            client_id=demo.client_id,

            user_id=demo.assigned_to,

            reminder_date=today,

            description="Demo trial expired",

            status="pending"
        )

        db.add(reminder)

    db.commit()