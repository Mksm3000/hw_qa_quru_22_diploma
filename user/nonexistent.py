class NonExistentUser:

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


non_existent_user = NonExistentUser(
    first_name='user',
    last_name='non_existent',
    email='non_existent_user@@wrong.com',
    password='******'
)
