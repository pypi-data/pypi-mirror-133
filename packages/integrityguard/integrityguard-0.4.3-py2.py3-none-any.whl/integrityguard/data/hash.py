import hashlib

def hash_file(file, method="md5", blocksize=65536):

    # Preset supported methods by hashlib
    supportedMethods = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

    # Handle error if a method requested is not supported
    if method not in supportedMethods:
        raise ValueError("Hash type *" + method + "* not supported.")

    # Dynamically set method
    hashIt = getattr(hashlib, method)

    # Initiate Hashlib method
    hasher = hashIt()

    # Open file to read content and generate the proper hash
    with open(file, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)

    # Return hash in digested mode, not in bytes-like object
    return hasher.hexdigest()