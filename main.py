from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import (
    engine,
    Base,
    SessionLocal
)

from models import User
 
from schemas import (
    SignupSchema , UserResponse , LoginSchema,ClientCreate, ClientResponse)

from crud import (
    create_user,
    get_user_by_email,
    get_all_users,
    create_client,
    get_clients,
    search_clients,
    update_client,
    delete_client
    
)
from auth_config import verify_password

from jwt_token import create_access_token
from authlib.integrations.starlette_client import OAuth

from fastapi.responses import RedirectResponse

from auth import (
    CLIENT_ID,
    CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    SECRET_KEY,
    ALGORITHM
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

Base.metadata.create_all(bind=engine)


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