from django.contrib.auth.models import User


def auth(func):
    '''аутентификация'''
    def wrapper(self):
        USERNAME = 'test'
        PASSWORD = '123123'
        self.user = User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        self.client.login(
            username=USERNAME,
            password=PASSWORD
        )
        func(self)

    return wrapper

