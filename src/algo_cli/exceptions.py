class AlgoCliException(Exception):
    pass


class InvalidBaseDirectory(AlgoCliException):
    pass


class MalformedProblemDirectory(AlgoCliException):
    pass