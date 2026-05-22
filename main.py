from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

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

from fastapi.responses import RedirectResponse

from auth import (
    SECRET_KEY,
    ADMIN_EMAIL, 
    ADMIN_PASSWORD
)

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.post("/admin/users")
def create_employee(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = create_user(db, user)

    return {
        "message": "Employee created successfully",
        "user": new_user
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

@app.get("/cities", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()

@app.get("/cities/{city_id}/areas",response_model=list[AreaResponse])
def get_areas_by_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Area)
        .filter(Area.city_id == city_id)
        .all()
    )
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
@app.get("/clients/{client_id}/latest-call-log")
def get_latest_call_log(
    client_id: int,
    db: Session = Depends(get_db)
):
    latest_log = (
        db.query(CallLog)
        .filter(CallLog.client_id == client_id)
        .order_by(CallLog.id.desc())
        .first()
    )

    if not latest_log:
        raise HTTPException(
            status_code=404,
            detail="No call logs found"
        )

    return latest_log

@app.post(
    "/demos",
    response_model=DemoResponse
)
def create_demo(
    demo: DemoCreate,
    db: Session = Depends(get_db)
):

    new_demo = Demo(
        client_id=demo.client_id,
        assigned_employee=demo.assigned_employee,
        demo_date=demo.demo_date,
        demo_time=demo.demo_time,
        demo_feedback=demo.demo_feedback,
        meeting_notes=demo.meeting_notes,
        demo_status=demo.demo_status
    )

    db.add(new_demo)

    db.commit()

    db.refresh(new_demo)

    return new_demo

@app.get(
    "/demos",
    response_model=list[DemoResponse]
)
def get_demos(
    db: Session = Depends(get_db)
):

    return db.query(Demo).all()

@app.get(
    "/demos/{demo_id}",
    response_model=DemoResponse
)
def get_demo(
    demo_id: int,
    db: Session = Depends(get_db)
):

    demo = (
        db.query(Demo)
        .filter(Demo.id == demo_id)
        .first()
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return demo

@app.put(
    "/demos/{demo_id}",
    response_model=DemoResponse
)
def update_demo(
    demo_id: int,
    updated_demo: DemoCreate,
    db: Session = Depends(get_db)
):

    demo = (
        db.query(Demo)
        .filter(Demo.id == demo_id)
        .first()
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    demo.client_id = updated_demo.client_id

    demo.assigned_employee = (
        updated_demo.assigned_employee
    )

    demo.demo_date = updated_demo.demo_date

    demo.demo_time = updated_demo.demo_time

    demo.demo_feedback = (
        updated_demo.demo_feedback
    )

    demo.meeting_notes = (
        updated_demo.meeting_notes
    )

    demo.demo_status = updated_demo.demo_status

    db.commit()

    db.refresh(demo)

    return demo

@app.delete("/demos/{demo_id}")
def delete_demo(
    demo_id: int,
    db: Session = Depends(get_db)
):

    demo = (
        db.query(Demo)
        .filter(Demo.id == demo_id)
        .first()
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    db.delete(demo)

    db.commit()

    return {
        "message": "Demo deleted successfully"
    }

@app.get(
    "/clients/{client_id}/demos",
    response_model=list[DemoResponse]
)
def get_client_demos(
    client_id: int,
    db: Session = Depends(get_db)
):

    demos = (
        db.query(Demo)
        .filter(Demo.client_id == client_id)
        .all()
    )

    return demos