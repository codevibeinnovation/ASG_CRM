from passlib.context import CryptContext



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    # Truncate to 72 bytes (bcrypt limit)
    truncated = password[:72]
    return pwd_context.hash(truncated)

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )