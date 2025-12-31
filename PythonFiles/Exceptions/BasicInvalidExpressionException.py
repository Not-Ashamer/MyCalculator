class BasicInvalidExpressionException(Exception):
    def __init__(self, message : str):
        self.expression = message
        super().__init__(message)