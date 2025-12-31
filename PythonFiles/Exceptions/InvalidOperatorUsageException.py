class InvalidOperatorUsageException(Exception):
    #Used When a valid operator recieves invalid inputs either to its left or it's right
    def __init__(self, message: str):
        self.message = message
        # Pass the message to the base Exception class
        super().__init__(self.message)