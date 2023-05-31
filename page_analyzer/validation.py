import validators


def validate(url):
    errors = {}
    if not url:
        errors['blank_url'] = 'URL обязателен'
    elif not validators.url(url):
        errors['unccorect_url'] = 'Некорректный URL'

    return errors


