class Credentials:
    def __init__(self, user_name, password, domain):
        self.user_name = user_name
        self.password = password
        self.domain = domain

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, new_name):
        if not isinstance(new_name, str):
            raise RuntimeError('user_name should be a string!')

        self._user_name = new_name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        if not isinstance(new_password, str):
            raise RuntimeError('password should be a string!')

        self._password = new_password

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, new_domain):
        if not isinstance(new_domain, str):
            raise RuntimeError('domain should be a string!')

        self._domain = new_domain

    def __eq__(self, other):
        return self.user_name == other.user_name and \
               self.password == other.password and \
               self.domain == other.domain