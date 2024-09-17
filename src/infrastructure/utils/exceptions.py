from functools import wraps
from http import HTTPStatus

from flask import current_app as app
from flask_jwt_extended.exceptions import (InvalidHeaderError, NoAuthorizationError,
                                           RevokedTokenError)
from jwt import DecodeError


class AuthenticationException(Exception):
    pass


def exception_handle(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as e:
            app.logger.error(str(e), exc_info=True)
            return {"message": str(e)}, HTTPStatus.BAD_REQUEST
        except (
            NoAuthorizationError,
            RevokedTokenError,
            DecodeError,
            InvalidHeaderError,
            AuthenticationException,
        ) as e:
            app.logger.error(str(e), exc_info=True)
            return {"message": str(e)}, HTTPStatus.FORBIDDEN
        except Exception as exc:
            app.logger.error(exc)
            return {"message": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return wrapper
