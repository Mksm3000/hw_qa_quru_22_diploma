from faker import Faker

fake = Faker("en_US")


class RandomUser:

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


FIRST_NAME = fake.first_name()
LAST_NAME = fake.last_name()
EMAIL = f'{FIRST_NAME}_{LAST_NAME}@gmail.com'
PASSWORD = fake.password(length=10,
                         special_chars=True,
                         digits=True,
                         upper_case=True,
                         lower_case=True)

random_user = RandomUser(
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
    email=EMAIL,
    password=PASSWORD
)
