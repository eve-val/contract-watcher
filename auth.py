from binascii import hexlify

class Character(object):
    def __init__(self):
        self.auth_id = auth_id
        self.user_values = user_values
        self.tokens = {}

    @classmethod
    def get_by_auth_id(cls, auth_id):
        pass

    @classmethod
    def get_by_auth_token(cls, user_id, token):
        pass

    @classmethod
    def get_by_auth_password(cls, auth_id, password):
        pass

    @classmethod
    def create_user(cls, auth_id, unique_properties=None, **user_values):
        pass

    @classmethod
    def validate_token(cls, user_id, subject, token):
        pass

    @classmethod
    def create_auth_token(cls, user_id):
        bytes = ""
        with open('/dev/random') as f:
            while len(bytes) != 16:
                bytes += f.read(16 - len(bytes))
        return hexlify(bytes)

    @classmethod
    def delete_auth_token(cls, user_id, token):
        pass
