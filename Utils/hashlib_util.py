from hashlib import sha256


def sha(o):
    if not isinstance(o,(bytes,bytearray)):
        try:
            o = o.encode()
        except AttributeError:
            try:
                o = str(o).encode()
            except ValueError:
                raise AttributeError("Don't know how to handle {}, isn't bytes and doesn't have encode".format(o))
    hexdigest = sha256(o).hexdigest()
    as_int = int(hexdigest, 16)
    return as_int


def hash_to_bin(o, num_digits=256):
    data = sha(o)
    data = int(data, 16)
    format_code = '#0{}b'.format(num_digits+2)
    return format(data, format_code)
