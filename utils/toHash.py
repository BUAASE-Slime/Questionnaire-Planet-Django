import hashlib


def hash_code(s, salt='OnlinePublish'):  # generate s+salt into hash_code (default: salt=online publish)
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update method get bytes(type)
    return h.hexdigest()
