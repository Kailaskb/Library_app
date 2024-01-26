from datetime import datetime

from django.template.defaultfilters import slugify


def success(data=None):
    return_data = {
        'status': True,
        "message": "success"
    }
    if data is not None:
        return_data['data'] = data
    return return_data


def fail(error):
    return_data = {
        'status': False,
        'message': 'fail',
        'error': error
    }
    return return_data


def slug_generate(key: str = 'slug'):
    return slugify(f'{key}-{datetime.now().timestamp()}')
