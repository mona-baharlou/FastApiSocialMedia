from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret_KEY
# Algo
# Expiration

SECRET_KEY = "dnfsdifw8y834yfmscmsdfq23416792402425464ejrwurt267tva54q23" \
"dfjkgdgh56523972047204254687987FHGIWWWFNSFNNE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MIN = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MIN)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: str = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token,
                               credentials_exception=credentials_exception)
                     