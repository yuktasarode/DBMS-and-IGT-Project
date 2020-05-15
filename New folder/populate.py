import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","trial.settings")

import django
django.setup()


from django.contrib.auth.models import User
from faker import Faker
fake = Faker()
def populate():
    for i in range(1,2801):
        username = "bb"+str(i)
        user = User.objects.create_user(username, password=username)
        user.is_superuser = True
        user.is_staff = True
        user.email = username + "@gmail"  + ".com"
        user.save()



if __name__ == '__main__':
    print("populating!")
    populate()
    print("done")
