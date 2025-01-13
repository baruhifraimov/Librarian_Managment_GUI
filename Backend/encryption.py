import hashlib

class Encryption:

    @staticmethod
    def encrypt_password(password):
        """
        Encrypt the password using sha256 algorithm and return the hash value in hexadecimal format
        :param password:  The password to encrypt
        :return:  The hash value in hexadecimal format
        """
        hash_object = hashlib.sha256(str(password).encode())
        return hash_object.hexdigest()

