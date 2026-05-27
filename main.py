from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database import (
    SessionLocal,
    engine,
    Base,
    get_db
)

import models
import schemas
import crud

from models import User

from auth_config import (
    verify_password
)

from jwt_token import (
    create_access_token,
    get_current_user,
    admin_only
)
from datetime import date


# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# APP
# =========================

app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)
# =========================
# ROOT
# =========================

@app.get("/")

def root():

    return {
        "message": "CRM Running Successfully"
    }
# =========================
# SIGNUP
# =========================

@app.post(
    "/signup",
    response_model=schemas.UserResponse
)

def signup(

    user: schemas.UserCreate,

    db: Session = Depends(get_db)
):

    # CHECK EMAIL EXISTS

    existing_user = crud.get_user_by_email(

        db,

        user.email
    )

    if existing_user:

        raise HTTPException(

            status_code=400,

            detail="Email already exists"
        )

    # CREATE USER

    new_user = crud.create_user(

        db,

        user
    )

    return new_user

# =========================
# LOGIN
# =========================

@app.post("/login")

def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(

        db,

        form_data.username
    )

    if not user:

        raise HTTPException(

            status_code=401,

            detail="Invalid Email"
        )

    if not verify_password(

        form_data.password,

        user.password
    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid Password"
        )

    access_token = create_access_token(

        data={

            "sub": user.email,

            "role": user.role,

            "user_id": user.id
        }
    )

    return {

        "access_token": access_token,

        "token_type": "bearer"
    }
    
@app.get("/me")
def get_me(

    current_user: User = Depends(get_current_user)

):

    return {

        "id": current_user.id,

        "name": current_user.name,

        "email": current_user.email,

        "role": current_user.role

    }
# =========================
# CREATE USER
# ADMIN ONLY
# =========================

@app.post(
    "/users",
    response_model=schemas.UserResponse
)

def create_user(

    user: schemas.UserCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_user(
        db,
        user
    )


# =========================
# GET USERS
# ADMIN ONLY
# =========================

@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)

def get_users(

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    return crud.get_all_users(db)


# =========================
# CREATE CLIENT
# =========================

@app.post(
    "/clients",
    response_model=schemas.ClientResponse
)

def create_client(

    client: schemas.ClientCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.create_client(

        db,

        client,

        current_user.id
    )


# =========================
# GET CLIENTS
# =========================

@app.get(
    "/clients",
    response_model=list[schemas.ClientResponse]
)

def get_clients(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.get_clients(db)


# =========================
# SEARCH CLIENTS
# =========================

@app.get("/search-clients")

def search_clients(

    name: str,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.search_clients(
        db,
        name
    )


# =========================
# UPDATE CLIENT
# =========================

@app.put(
    "/clients/{client_id}",
    response_model=schemas.ClientResponse
)

def update_client(

    client_id: int,

    client: schemas.ClientCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    updated_client = crud.update_client(

        db,

        client_id,

        client
    )

    if not updated_client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return updated_client


# =========================
# DELETE CLIENT
# ADMIN ONLY
# =========================

@app.delete("/clients/{client_id}")

def delete_client(

    client_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    deleted_client = crud.delete_client(
        db,
        client_id
    )

    if not deleted_client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return {
        "message": "Client deleted successfully"
    }

# =========================
# CREATE CITY
# ADMIN ONLY
# =========================

@app.post(

    "/cities",

    response_model=schemas.CityResponse
)

def create_city(

    city: schemas.CityCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    return crud.create_city(
        db,
        city
    )


# =========================
# GET CITIES
# =========================

@app.get(

    "/cities",

    response_model=list[schemas.CityResponse]
)

def get_cities(

    db: Session = Depends(get_db)

):

    return crud.get_cities(db)

@app.put(

    "/cities/{city_id}",

    response_model=schemas.CityResponse
)

def update_city(

    city_id: int,

    city: schemas.CityCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    updated_city = crud.update_city(

        db,

        city_id,

        city
    )

    if not updated_city:

        raise HTTPException(

            status_code=404,

            detail="City not found"
        )

    return updated_city

@app.delete("/cities/{city_id}")

def delete_city(

    city_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    deleted_city = crud.delete_city(
        db,
        city_id
    )

    if not deleted_city:

        raise HTTPException(

            status_code=404,

            detail="City not found"
        )

    return {
        "message": "City deleted successfully"
    }

# =========================
# CREATE AREA
# ADMIN ONLY
# =========================

@app.post(

    "/areas",

    response_model=schemas.AreaResponse
)

def create_area(

    area: schemas.AreaCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    return crud.create_area(
        db,
        area
    )


# =========================
# GET AREAS
# =========================

@app.get(

    "/areas",

    response_model=list[schemas.AreaResponse]
)

def get_areas(

    db: Session = Depends(get_db)

):

    return crud.get_areas(db)

@app.put(

    "/areas/{area_id}",

    response_model=schemas.AreaResponse
)

def update_area(

    area_id: int,

    area: schemas.AreaCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    updated_area = crud.update_area(

        db,

        area_id,

        area
    )

    if not updated_area:

        raise HTTPException(

            status_code=404,

            detail="Area not found"
        )

    return updated_area

@app.delete("/areas/{area_id}")

def delete_area(

    area_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    deleted_area = crud.delete_area(
        db,
        area_id
    )

    if not deleted_area:

        raise HTTPException(

            status_code=404,

            detail="Area not found"
        )

    return {
        "message": "Area deleted successfully"
    }
# =========================
# GET AREAS BY CITY
# =========================

@app.get(
    "/areas-by-city/{city_id}",
    response_model=list[schemas.AreaResponse]
)

def get_areas_by_city(

    city_id: int,

    db: Session = Depends(get_db)
):

    return db.query(models.Area).filter(
        models.Area.city_id == city_id
    ).all()
# =========================
# CREATE EXISTING PRODUCT
# ADMIN ONLY
# =========================

@app.post(

    "/existing-products",

    response_model=schemas.ExistingProductResponse
)

def create_existing_product(

    product: schemas.ExistingProductCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    return crud.create_existing_product(
        db,
        product
    )


# =========================
# GET EXISTING PRODUCTS
# =========================

@app.get(

    "/existing-products",

    response_model=list[
        schemas.ExistingProductResponse
    ]
)

def get_existing_products(

    db: Session = Depends(get_db)

):

    return crud.get_existing_products(db)

@app.put(

    "/existing-products/{product_id}",

    response_model=schemas.ExistingProductResponse
)

def update_existing_product(

    product_id: int,

    product: schemas.ExistingProductCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    updated_product = crud.update_existing_product(

        db,

        product_id,

        product
    )

    if not updated_product:

        raise HTTPException(

            status_code=404,

            detail="Product not found"
        )

    return updated_product

@app.delete("/existing-products/{product_id}")

def delete_existing_product(

    product_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    deleted_product = crud.delete_existing_product(
        db,
        product_id
    )

    if not deleted_product:

        raise HTTPException(

            status_code=404,

            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }

# =========================
# CREATE DEMO
# =========================

@app.post(
    "/demos",
    response_model=schemas.DemoResponse
)

def create_demo(

    demo: schemas.DemoCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.create_demo(
        db,
        demo
    )


# =========================
# GET DEMOS
# =========================

@app.get(
    "/demos",
    response_model=list[schemas.DemoResponse]
)

def get_demos(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    crud.check_expired_trials(db)

    return crud.get_demos(db)


# =========================
# CREATE DEAL
# =========================

@app.post(
    "/deals",
    response_model=schemas.DealResponse
)

def create_deal(

    deal: schemas.DealCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.create_deal(
        db,
        deal
    )


# =========================
# GET DEALS
# =========================

@app.get(
    "/deals",
    response_model=list[schemas.DealResponse]
)

def get_deals(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.get_deals(db)


# =========================
# GET SINGLE DEAL
# =========================

@app.get(
    "/deals/{deal_id}",
    response_model=schemas.DealResponse
)

def get_deal(

    deal_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    deal = crud.get_deal(
        db,
        deal_id
    )

    if not deal:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return deal


# =========================
# UPDATE DEAL
# =========================

@app.put(
    "/deals/{deal_id}",
    response_model=schemas.DealResponse
)

def update_deal(

    deal_id: int,

    deal: schemas.DealCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    updated_deal = crud.update_deal(

        db,

        deal_id,

        deal
    )

    if not updated_deal:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return updated_deal


# =========================
# DELETE DEAL
# ADMIN ONLY
# =========================

@app.delete("/deals/{deal_id}")

def delete_deal(

    deal_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(admin_only)
):

    deleted_deal = crud.delete_deal(
        db,
        deal_id
    )

    if not deleted_deal:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return {
        "message": "Deal deleted successfully"
    }


# =========================
# CREATE REMINDER
# =========================

@app.post(
    "/reminders",
    response_model=schemas.ReminderResponse
)

def create_reminder(

    reminder: schemas.ReminderCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    return crud.create_reminder(
        db,
        reminder
    )


# =========================
# TODAY REMINDERS
# =========================

@app.get(
    "/today-reminders",
    response_model=list[schemas.ReminderResponse]
)

def today_reminders(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    crud.create_trial_expiry_reminders(db)

    crud.create_renewal_reminders(db)

    return crud.get_today_reminders(db)