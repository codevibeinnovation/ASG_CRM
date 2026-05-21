from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import (
    engine,
    Base,
    SessionLocal
)

from models import *
from schemas import *
from crud import * 
from auth_config import verify_password

from jwt_token import create_access_token
from authlib.integrations.starlette_client import OAuth

from fastapi.responses import RedirectResponse

from auth import (
    CLIENT_ID,
    CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    SECRET_KEY,
    ALGORITHM,
    ADMIN_EMAIL, 
    ADMIN_PASSWORD
)

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)
oauth = OAuth()

oauth.register(
    name="google",

    client_id=CLIENT_ID,

    client_secret=CLIENT_SECRET,

    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",

    client_kwargs={
        "scope": "openid email profile"
    }
)

Base.metadata.create_all(bind=engine, checkfirst=True)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/")
def home():

    return {
        "message": "ASG CRM Running"
    }


@app.post("/signup")
def signup(
    user: SignupSchema,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    create_user(db, user)

    return {
        "message": "User created successfully"
    }

@app.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    users = get_all_users(db)

    return users

@app.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/login/google")
async def login_google(request: Request):

    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@app.get("/auth/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    email = user_info["email"]

    name = user_info["name"]

    user = db.query(User).filter(User.email == email).first()

    # Create user if not exists
    if not user:

        user = User(
            name=name,
            email=email,
            phone="",
            password=""
        )

        db.add(user)

        db.commit()

        db.refresh(user)

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@app.post("/clients", response_model=ClientResponse)
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@app.get("/clients", response_model=list[ClientResponse])
def all_clients(db: Session = Depends(get_db)):
    return get_clients(db)

@app.get("/clients/search/")
def search_client(name: str, db: Session = Depends(get_db)):

    clients = search_clients(db, name)

    if not clients:
        raise HTTPException(
            status_code=404,
            detail="No clients found"
        )

    return clients

@app.put("/clients/{client_id}")
def edit_client(
    client_id: int,
    client: ClientCreate,
    db: Session = Depends(get_db)
):

    updated_client = update_client(
        db,
        client_id,
        client
    )

    if not updated_client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return {
        "message": "Client updated successfully",
        "client": updated_client
    }

@app.delete("/clients/{client_id}")
def remove_client(
    client_id: int,
    db: Session = Depends(get_db)
):

    client = delete_client(db, client_id)

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return {
        "message": "Client deleted successfully"
    }

@app.post("/admin/login")
def admin_login(admin: AdminLogin):

    if (
        admin.email != ADMIN_EMAIL
        or
        admin.password != ADMIN_PASSWORD
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )

    access_token = create_access_token(
        data={
            "sub": admin.email,
            "role": "admin"
        }
    )

    return {
        "message": "Admin login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/admin/cities", response_model=CityResponse)
def add_city(city: CityCreate, db: Session = Depends(get_db)):

    new_city = City(name=city.name)

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city

@app.put("/admin/cities/{city_id}")
def update_city(
    city_id: int,
    city: CityCreate,
    db: Session = Depends(get_db)
):

    existing_city = db.query(City).filter(City.id == city_id).first()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    existing_city.name = city.name

    db.commit()

    return {"message": "City updated successfully"}

@app.delete("/admin/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()

    return {"message": "City deleted successfully"}

@app.post("/admin/areas", response_model=AreaResponse)
def add_area(area: AreaCreate, db: Session = Depends(get_db)):

    city = db.query(City).filter(City.id == area.city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    new_area = Area(
        name=area.name,
        city_id=area.city_id
    )

    db.add(new_area)
    db.commit()
    db.refresh(new_area)

    return new_area

@app.put("/admin/areas/{area_id}")
def update_area(
    area_id: int,
    area: AreaCreate,
    db: Session = Depends(get_db)
):

    existing_area = db.query(Area).filter(Area.id == area_id).first()

    if not existing_area:
        raise HTTPException(status_code=404, detail="Area not found")

    existing_area.name = area.name
    existing_area.city_id = area.city_id

    db.commit()

    return {"message": "Area updated successfully"}

@app.delete("/admin/areas/{area_id}")
def delete_area(area_id: int, db: Session = Depends(get_db)):

    area = db.query(Area).filter(Area.id == area_id).first()

    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    db.delete(area)
    db.commit()

    return {"message": "Area deleted successfully"}

@app.post("/admin/products")
def add_product(
    product: ExistingProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = db.query(ExistingProduct).filter(
        ExistingProduct.product_name == product.product_name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = ExistingProduct(
        product_name=product.product_name
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product added successfully",
        "data": new_product
    }

@app.get(
    "/admin/products",
    response_model=list[ExistingProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    products = db.query(ExistingProduct).all()

    return products

@app.put(
    "/admin/products/{product_id}",
    response_model=ExistingProductResponse
)
def update_product(
    product_id: int,
    product: ExistingProductCreate,
    db: Session = Depends(get_db)
):
    existing_product = db.query(ExistingProduct).filter(
        ExistingProduct.id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_product.product_name = product.product_name


    db.commit()
    db.refresh(existing_product)

    return existing_product

@app.delete("/admin/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(ExistingProduct).filter(
        ExistingProduct.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }

@app.post(
    "/call-logs",
    response_model=CallLogResponse
)

def create_call_log(
    call_log: CallLogCreate,
    db: Session = Depends(get_db)
):

    client = db.query(Client).filter(
        Client.id == call_log.client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    new_log = CallLog(
        **call_log.dict()
    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return new_log

@app.get(
    "/clients/{client_id}/history",
    response_model=list[CallLogResponse]
)

def get_client_history(
    client_id: int,
    db: Session = Depends(get_db)
):

    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    history = db.query(CallLog).filter(
        CallLog.client_id == client_id
    ).all()

    return history