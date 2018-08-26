from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    @staticmethod
    def authenticate(uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    @staticmethod
    def get_user(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
