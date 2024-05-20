import jwt
from datetime import datetime, timedelta
from django.conf import settings

from user.repositories import UserRepository

from .models import UserEntity


def authenticate(username, password):
    repository = UserRepository(collection_name="user")
    user = repository.getUserByNameAndPassword(username, password)
    return user


def generateToken(user_id, username):
    payload = {
        "id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=5),
    }
    return jwt.encode(
        payload=payload, key=getattr(settings, "SECRET_KEY"), algorithm="HS256"
    )


def refreshToken(user_id, username):
    return generateToken(user_id, username)


def verifyToken(token):
    error_code = 0
    payload = None
    try:
        payload = jwt.decode(
            jwt=token, key=getattr(settings, "SECRET_KEY"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2

    return [error_code, payload]


def getAuthenticatedUser(token):
    _, payload = verifyToken(token)

    if payload is not None:
        # recuperar o usuario no banco
        return UserEntity(username=payload["username"])
