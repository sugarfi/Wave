import eval
import data

def setup(env):
    @eval.proc(env, 'number', 1, eval.ANY) # number procedure - converts to a number
    def number(env, *args):
        args = eval.parse_args(args, env)
        return data.number(args[0])

    @eval.proc(env, 'string', 1, eval.ANY) # string procedure - converts to a string
    def number(env, *args):
        args = eval.parse_args(args, env)
        return data.string(args[0])

    @eval.proc(env, 'bool', 1, eval.ANY) # bool procedure - converts to a boolean
    def number(env, *args):
        args = eval.parse_args(args, env)
        return data.bool(args[0])

    @eval.proc(env, 'nil', 0, eval.ANY) # nil procedure - returns nil
    def nil(env, *args):
        return None

    @eval.proc(env, 'typeof', 1, eval.ANY) # typeof procedure - gets the type of an object
    def typeof(env, *args):
        args = eval.parse_args(args, env)
        return data.string(data.names[args[0].__class__])
