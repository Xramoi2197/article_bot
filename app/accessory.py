import validators


def is_url(url_string: str) -> bool:
    result = validators.url(url_string)
    if isinstance(result, validators.ValidationFailure):
        return False
    return result
