import hashlib
import string
import random

from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer
from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.orm import validates

from racings.db import BaseModel


#From: https://eve-sqlalchemy.readthedocs.io/en/latest/tutorial.html#authentication-example
class UserBase:


    def generate_auth_token(self, expiration=24*60*60):
        """Generates token for given expiration
        and user login."""
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'login': self.login })

    @staticmethod
    def verify_auth_token(token):
        """Verifies token and eventually returns
        user login.
        """
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        return data['login']

    def isAuthorized(self, role_names):
        """Checks if user is related to given role_names.
        """
        allowed_roles = set([r.id for r in self.roles])\
            .intersection(set(role_names))
        return len(allowed_roles) > 0

    def generate_salt(self):
        return ''.join(random.sample(string.letters, 12))

    def encrypt(self, password):
        """Encrypt password using hashlib and current salt.
        """
        return str(hashlib.sha1(password + str(self.salt))\
            .hexdigest())

    @validates('password')
    def _set_password(self, key, value):
        """Using SQLAlchemy validation makes sure each
        time password is changed it will get encrypted
        before flushing to db.
        """
        self.salt = self.generate_salt()
        return self.encrypt(value)

    def check_password(self, password):
        if not self.password:
            return False
        return self.encrypt(password) == self.password
