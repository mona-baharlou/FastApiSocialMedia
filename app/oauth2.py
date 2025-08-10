from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret_KEY
# Algo
# Expiration

SECRET_KEY = "dnfsdifw8y834yfmscmsdfq23416792402425464ejrwurt267tva54q23" \
"dfjkgdgh56523972047204254687987FHGIWWWFNSFNNE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MIN = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MIN)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    return encoded_jwt



