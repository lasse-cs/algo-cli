class AlgoCliException(Exception):
    pass


class InvalidBaseDirectory(AlgoCliException):
    pass


class MalformedProblemDirectory(AlgoCliException):
    pass


class ProblemDoesNotExist(AlgoCliException):
    pass


class MalformedAttemptDirectory(AlgoCliException):
    pass


class AttemptDoesNotExist(AlgoCliException):
    pass
