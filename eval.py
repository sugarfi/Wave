import parser # Imports
import errors
import data
import re

ARITY_0 = 'ARITY_0' # Arity and typechecking values
ARITY_1 = 'ARITY_1'
ANY = 'ANY'

class Proc(): # Procedure class
    def __init__(self, env, name, arity, function, *types):
        self.name = name # Procedure name
        self.arity = arity # Arity
        self.function = function # Function to call
        self.types = types # Type checking params
        env.setval(self.name, self) # Store ourself
    def __call__(self, env, *args):
        '''
        Calls a procedure.
        '''
        p = [data.parse(arg, env) for arg in args] # Parse our arguments
        if self.arity == ARITY_1 or self.arity == ARITY_0: # If we have no set arity, assign our types as such
            self.types = [self.types[0]] * len(p)
        if isinstance(self.arity, int): # If we have an arity, check for arity errors
            if len(args) != self.arity:
                errors._ArityError(f'{self.name} expected {self.arity} arguments, got {len(args)}').throw()
        else:
            if self.arity == ARITY_1: # Check if we have no arguments
                if len(args) == 0:
                    errors._ArityError(f'{self.name} expected at least 1 argument, got 0').throw()
        for i in range(len(p)): # Typechecking
            arg = p[i] # Get the current arguments
            if not isinstance(arg, list): # If it is not a function, parse it
                want = self.types[i] # Get the needed type
                if want != ANY: # If we care what it is, then check
                    if isinstance(want, list): # Check for multiple types
                        o = True # No errors
                        for w in want:
                            if w != ANY:
                                o = not isinstance(arg, w) # Update o
                        if not o:
                            errors._TypeError(f'{self.name} argument {i + 1} must be one of {list(map(lambda x: data.names[x], want))}').throw()
                    else: # Check for errors
                        if not isinstance(arg, want):
                            errors._TypeError(f'{self.name} argument {i + 1} must be {data.names[want]}').throw()
        return data.parse(self.function(env, *args), env) # Return the output

def proc(env, name, arity, *types):
    '''
    Decorator to create procedures.
    '''
    def new(function): # Return a procedure factory
        return Proc(env, name, arity, function, *types)
    return new

class Env(): # Environment to run code in
    def __init__(self, file=None, code=''):
        self.scope = 0 # The current scope
        self.scopes = [{}] # All scopes
        self.lexer = parser.Lexer() # Lexer an parser
        self.parser = parser.Parser()
        self.file = file # File to read
        self.pyvars = {} # Python variables
        if file: # Try to read from file
            self.code = open(file).read()
        else: # Read from code
            self.code = code
        self.code = self.code.replace('\'(', '(\' ') # Replace '(x) with (' x)
    def run(self):
        '''
        Runs the code.
        '''
        tree = self.parser.parse(self.lexer.tokenize(self.code)) # Get an AST
        out = []
        for node in tree:
            this = Node(node).eval(self) # Evaluate every node
            if isinstance(this, list): # Store the output
                out += this
            else:
                out.append(this)
        return out # Return the output
    def getval(self, name, e=True):
        '''
        Gets a variable from the current scope.
        '''
        objs, name = name.split('.')[:-1], name.split('.')[-1] # Get the objects tree
        if objs:
            if objs[0].lstrip('-').isdigit(): # Decimals are not objects!
                return None
        scope = self.getscope() # Set up a scope to search
        scope.update(self.pyvars)
        for obj in objs: # Loop over all objects
            try:
                scope = scope[obj] # Get the object from the scope
            except KeyError:
                if e: # Throw an error if we want to
                    errors._UndefinedError(f'No such object {obj}').throw()
                else:
                    return None
        try:
            return scope.get(name) # For Wave objects
        except AttributeError:
            return getattr(scope, name) # For Python objects
    def setval(self, name, value):
        '''
        Sets a name to a value.
        '''
        self.scopes[self.scope][name] = value
    def getscope(self):
        '''
        Returns the current scope.
        '''
        return self.scopes[self.scope]

class Node():
    def __init__(self, node):
        self.node = node # Save the node
        if len(self.node) == 0:
            errors._SyntaxError('Empty node evaluated').throw() # We don't like empty nodes
        self.proc = self.node[0] # Get procedure and args
        self.args = self.node[1:]
    def __repr__(self):
        return 'Node ' + str(self.node)
    def eval(self, env):
        e = False # Do we need to call eval?
        out = []
        if isinstance(self.proc, list): # If our procedure is a list, then we messed up and need to fix it
            for item in self.node:
                out.append(Node(item).eval(env))
            return out
        if data.isval(self.proc): # If our procedure is a value, we need to just return it
            new_env = env
            new_env.scopes[new_env.scope] = {}
            return data.parse(self.proc, new_env)
        var = env.getval(self.proc) # Get the procedure
        if not isinstance(var, Proc) and not hasattr(var, '__call__'): # If it is not a procedure, return it
            if var:
                return var
        if not isinstance(var, Proc) and hasattr(var, '__call__'): # If it is a Python thing, we need to call eval
            e = True
        mods = self.proc.split('.') # Get the list of modules - same idea as the objects in getval
        mods, proc = mods[:-1], mods[-1]
        lib = env.getscope()
        while mods:
            m = mods.pop(0) # Get the current module
            lib = lib[m]
            if not lib:
                try:
                    lib = env.pyvars[m] # Get the next level from it
                except KeyError:
                    errors._UndefinedError(f'No such library {m}').throw() # Yell at people if we can't find it
        try:
            proc = lib[proc] # Get our procedure
        except: # Uh oh
            try:
                e = True # Try to call a Python procedure
                proc = getattr(lib, proc)
            except: # This is bad
                try:
                    e = True # Try to call eval
                    proc = eval(proc)
                except (SyntaxError, NameError): # Yell at the user
                    errors._UndefinedError(f'No such procedure {proc}').throw()
        if e:
            try:
                return proc(*parse_args(self.args, env)) # Call the procedure
            except TypeError:
                errors._ArityError(f'Wrong arity for procedure {self.proc}').throw()
        return proc(env, *self.args) # Call the procedure

def parse_args(args, env):
    '''
    Parses a list of arguments.
    '''
    args = list(args) # Nobody likes tuples
    for i in range(len(args)):
        arg = args[i] # Get the current argument
        if isinstance(arg, list):
            arg = Node(arg).eval(env) # If it is a node, evaluate it
        try:
            var = env.getval(arg, e=False) # Try and get it as a variable
            if isinstance(var, data.arr_t): # If it is a list, then save it, or Numpy will throw TypeErrors
                arg = var
            else: # Otherwise, do type checking
                if var == None:
                    arg = data.parse(arg, env)
                else:
                    arg = var
        except:
            pass
        if isinstance(arg, list): # If it is a list with length 1, then it doesn't need to be a list
            if len(arg) == 1:
                arg = arg[0]
        args[i] = arg # Save it
    return args
