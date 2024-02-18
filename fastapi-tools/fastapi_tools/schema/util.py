def ensure_update(update_object: object, fields: list[str], error_message: str = 'nothing to update'):
    update: bool = False
    for field in fields:
        value = getattr(update_object, field)
        update |= value is not None
    if not update:
        raise ValueError(error_message)


def ensure_mutually_exclusive(data_object: object, fields: list[str], error_message: str = None):
    count: int = 0
    for field in fields:
        value = getattr(data_object, field)
        if value:
            count += 1
    if count < 1 or count > 1:
        default_error_message = f'fields are mutually exclusive: {fields}'
        raise ValueError(error_message or default_error_message)
