class ValidationException(Exception):

    def __init__(self, message='Generic validation exception'):
        self.message = message

    def __str__(self):
        return f'Validation failed! - {self.message}'


class SliceException(Exception):

    def __init__(self, message='Generic slice exception'):
        self.message = message

    def __str__(self):
        return f'Slice failed! - {self.message}'


class MissingGlobalConfigException(Exception):

    def __init__(self, message='Generic missing global config exception'):
        self.message = message


    def __str__(self):
        return f'Finding a global config failed! - {self.message}'
