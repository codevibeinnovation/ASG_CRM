from jose import jwt
from jose import JWTError

from datetime import (
    datetime,
    timedelta
)

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database import SessionLocal,get_db

from models import User

from auth import (
    SECRET_KEY,
    ALGORITHM
)


# =========================
# OAUTH
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =========================
# CREATE ACCESS TOKEN
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=24
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return token


# =========================
# GET CURRENT USER
# =========================

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(

        status_code=401,

        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        role = payload.get("role")

        user_id = payload.get("user_id")

        if email is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise credentials_exception

    return user


# =========================
# ADMIN ONLY
# =========================

def admin_only(

    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.role != "admin":

        raise HTTPException(

            status_code=403,

            detail="Only admin allowed"
        )

    return current_user