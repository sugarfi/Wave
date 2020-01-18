import sympy as sp # Imports
import numpy as np
import re
import eval

NUMBER = r'-?[0-9]+(\.[0-9]+)?' # We need the basic tokens
STRING = r'"[^"]*"'
tokens = [NUMBER, STRING]
num_t = sp.Float # We need the type classes
arr_t = np.ndarray
node_t = None # This gets setup later to prevent circular imports
str_t = str
bool_t = bool
obj_t = dict
nil_t = type(None)
names = { # Type names
    num_t: 'number',
    arr_t: 'list',
    str_t: 'string',
    node_t: 'node',
    bool_t: 'bool',
    obj_t: 'object',
    nil_t: 'nil',
}

def init():
    '''
    Sets up the node type.
    '''
    global node_t
    node_t = eval.Node
    names[node_t] = 'node'

def parse(string, env):
    '''
    Parses a value.
    '''
    if isinstance(string, bool): # If it is already a boolean, just edit it
        return sp.nfloat(int(string))
    if isinstance(string, str): # If it is a string, parse it
        if '"' in string or '\'' in string:
            return string.strip('"').strip('\'') # Strip quotes and parse strings
        else:
            var = env.getval(string) # If it is a variable, try and get its value
            try:
                if var:
                    return var
            except ValueError: # Numpy throws this if you try to use if on an array
                return var
            try:
                return sp.Float(string, '') # Make it into a number
            except:
                return string # Give up
    return string # Give up again

def number(arg): # Type conversion functions
    return sp.Float(arg, '')

def array(args):
    return np.array(args)

def symbol(args):
    return sp.Symbol(str(args))

def string(args):
    return [str(args)]

def isval(arg):
    '''
    Checks if a string is a valuable.
    '''
    return any([re.match(token, arg) for token in tokens])
