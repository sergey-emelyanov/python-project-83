import validators


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('URL превышает 255 символов')
    elif not url:
        errors.extend(['URL обязателен','Некорректный URL'])
    elif not validators.url(url):
        errors.append('Некорректный URL')

    return errors


