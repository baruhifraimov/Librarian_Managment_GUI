import hashlib


class Encryption:

    @staticmethod
    def encrypt_password(password):
        hash_object = hashlib.sha256(str(password).encode())
        return hash_object.hexdigest()

