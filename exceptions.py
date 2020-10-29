class BaseException(Exception):
    def __init__(self, dic):
        self.dic = dic


class DatabaseException(BaseException):
    pass


class DuplicationException(BaseException):
    pass


class InvalidEntryException(BaseException):
    pass
