from application.common.interfaces.validator import Validator


class ValidationBehaviour:
    def validate[TRequest](self, request: TRequest, validator: Validator[TRequest] | None) -> None:
        if validator is not None:
            validator.validate(request)
