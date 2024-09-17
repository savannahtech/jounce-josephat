from flask_restful import Resource

from src.infrastructure.utils.exceptions import exception_handle


class BaseAPIResource(Resource):
    method_decorators = [exception_handle]
