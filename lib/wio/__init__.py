import eval
import data

def setup(env):
    @eval.proc(env, 'list-print', 1, data.arr_t) # list-print procedure - prints an array
    def list_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        print('[', end='') # Opening bracket
        for item in arg:
            _print(env, item)
            print(' ', end='') # Print items
        print('\x08]', end='') # Remove the last space and print a bracket

    @eval.proc(env, 'number-print', 1, data.num_t) # number-print procedure - prints a number
    def number_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        print(str(arg).rstrip('.'), end='') # Remove trailing .

    @eval.proc(env, 'string-print', 1, data.str_t) # string-print procedure - prints a string
    def string_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        print(arg, end='') # Literally just print

    @eval.proc(env, 'bool-print', 1, data.bool_t) # bool-print procedure - prints a boolean
    def bool_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        if arg: # Print as a boolean
            print('true', end='')
        else:
            print('false', end='')

    @eval.proc(env, 'object-print', 1, data.obj_t) # object-print procedure - prints an object
    def object_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        print('{', end='') # Just like list-print
        for key in arg:
            value = arg[key]
            print(key, end=':')
            _print(env, value) # Prints key and value
            print(' ', end='')
        print('\x08}', end='')

    @eval.proc(env, 'node-print', 1, data.nil_t) # node-print procedure - prints a node
    def node_print(env, *args):
        args = eval.parse_args(args, env) # Just like list-print
        arg = args[0]
        print('(', end='')
        for item in arg.node:
            if isinstance(item, list):
                node_print(env, Node(item)) # Recursive printing
            else:
                print(item, end=' ')
        print('\x08)', end='')

    @eval.proc(env, 'nil-print', 1, data.nil_t) # nil-print procedure - prints nil
    def nil_print(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        print('nil', end='') # just print nil

    @eval.proc(env, 'print', eval.ARITY_1, eval.ANY) # print procedure - prints an object based on type
    def _print(env, *args):
        args = eval.parse_args(args, env)
        methods = {
            data.num_t: number_print,
            data.arr_t: list_print,
            data.str_t: string_print,
            data.node_t: node_print,
            data.bool_t: bool_print,
            data.obj_t: object_print,
            data.nil_t: nil_print,
        }
        for arg in args:
            for type in methods:
                if isinstance(arg, type):
                    methods[type](env, arg) # Call the correct method

    @eval.proc(env, 'println', eval.ARITY_1, eval.ANY) # println procedure - prints with a newline
    def println(env, *args):
        _print(env, *args, '\n')

    @eval.proc(env, 'read', 2, eval.ANY, data.node_t) # read procedure - reads a value
    def read(env, *args):
        args = eval.parse_args(args, env)
        out = input(args[0]) # Read a value
        args[1].args = [out]
        out = args[1].eval(env) # Convert it to the given type
        return out

    @eval.proc(env, 'newline', 0, eval.ANY) # newline procedure - prints a newline
    def newline(env, *args):
        print()
