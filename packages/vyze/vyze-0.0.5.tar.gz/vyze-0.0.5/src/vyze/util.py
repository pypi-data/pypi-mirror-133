from random import randbytes


def new_id():
    return randbytes(16).hex()
