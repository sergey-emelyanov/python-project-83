import validators


def validate(url):
    errors = {}
    if len(url) > 255:
        errors['to_mach'] = 'URL превышает 255 символов'
    elif not url:
        errors['blank_url'] = 'URL обязателен'
    elif not validators.url(url):
        errors['unccorect_url'] = 'Некорректный URL'

    return errors


