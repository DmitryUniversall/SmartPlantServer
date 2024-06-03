from http import HTTPStatus

from .generic_base import GenericApplicationJsonResponse


class SuccessResponse(GenericApplicationJsonResponse):
    default_ok = True
    default_status_code = HTTPStatus.OK
    default_status_info_path = "GENERICS.SUCCESS"


class CreatedResponse(GenericApplicationJsonResponse):
    default_ok = True
    default_status_code = HTTPStatus.CREATED
    default_status_info_path = "GENERICS.CREATED"


class UpdatedResponse(GenericApplicationJsonResponse):
    default_ok = True
    default_status_code = HTTPStatus.OK
    default_status_info_path = "GENERICS.UPDATED"
