import sys

class _Error(): # Generic error class
    def __init__(self, type, message):
        self.type = type # Error type
        self.message = message # Message
    def throw(self):
        '''
        Throws the error
        '''
        sys.stderr.write(f'{self.type}: {self.message}\n') # Put a message to stderr
        sys.exit(1) # Exit

class _ArityError(_Error): # Thrown when the wrong arity is given
    def __init__(self, message):
        super().__init__('ArityError', message)

class _UndefinedError(_Error): # Thrown when a name is undefined
    def __init__(self, message):
        super().__init__('UndefinedError', message)

class _TypeError(_Error): # Like a Python TypeError
    def __init__(self, message):
        super().__init__('TypeError', message)

class _UseError(_Error): # Thrown when a use function fails
    def __init__(self, message):
        super().__init__('UseError', message)

class _SyntaxError(_Error): # Thrown by the parser
    def __init__(self, message):
        super().__init__('SyntaxError', message)

class _FileError(_Error): # Thrown when a file cannot be found
    def __init__(self, message):
        super().__init__('FileError', message)
