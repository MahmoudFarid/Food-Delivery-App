import os

from functools import wraps
from django.utils import crypto


def media_file_name(directory, container_id_field):
    @wraps(media_file_name)
    def wrapped(instance, filename):
        name, ext = os.path.splitext(filename)
        file_path = '{directory}/container_{user_id}/{name}-{suffix}{ext}'.format(
            directory=directory,
            user_id=getattr(instance, container_id_field),
            name=name,
            suffix=crypto.get_random_string(5),
            ext=ext
        )
        return file_path
    return wrapped
