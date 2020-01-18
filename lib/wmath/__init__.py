import eval
import data

def setup(env):
    @eval.proc(env, '+', 2, eval.ANY, eval.ANY) # + procedure - addition
    def add(env, *args):
        args = eval.parse_args(args, env)
        return args[0] + args[1]

    @eval.proc(env, '-', 2, [data.num_t, data.bool_t, data.arr_t], [data.num_t, data.bool_t, data.arr_t]) # - procedure - subtraction
    def sub(env, *args):
        args = eval.parse_args(args, env)
        return args[0] - args[1]

    @eval.proc(env, '*', 2, eval.ANY, eval.ANY) # * procedure - multiplication
    def mul(env, *args):
        args = eval.parse_args(args, env)
        return args[0] * args[1]

    @eval.proc(env, '/', 2, [data.num_t, data.bool_t, data.arr_t], [data.num_t, data.bool_t, data.arr_t]) # / procedure - division
    def div(env, *args):
        args = eval.parse_args(args, env)
        return args[0] / args[1]

    @eval.proc(env, '^', 2, [data.num_t, data.bool_t, data.arr_t], [data.num_t, data.bool_t, data.arr_t]) # ^ procedure - exponentiation
    def pow(env, *args):
        args = eval.parse_args(args, env)
        return args[0] ** args[1]

    @eval.proc(env, '%', 2, [data.num_t, data.bool_t, data.arr_t], [data.num_t, data.bool_t, data.arr_t]) # % procedure - modulus
    def mod(env, *args):
        args = eval.parse_args(args, env)
        return args[0] % args[1]

    @eval.proc(env, '>', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # > procedure - greater than
    def gt(env, *args):
        args = eval.parse_args(args, env)
        return args[0] > args[1]

    @eval.proc(env, '<', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # < procedure - less than
    def lt(env, *args):
        args = eval.parse_args(args, env)
        return args[0] < args[1]

    @eval.proc(env, '>=', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # >= procedure - greater than or equal to
    def ge(env, *args):
        args = eval.parse_args(args, env)
        return args[0] >= args[1]

    @eval.proc(env, '<=', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # <= procedure - less than or equal to
    def le(env, *args):
        args = eval.parse_args(args, env)
        return args[0] <= args[1]

    @eval.proc(env, '==', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # == procedure - equal to
    def le(env, *args):
        args = eval.parse_args(args, env)
        return args[0] == args[1]

    @eval.proc(env, '!=', 2, [data.num_t, data.str_t, data.obj_t, data.bool_t], [data.num_t, data.str_t, data.obj_t, data.bool_t]) # != procedure - not equal to
    def le(env, *args):
        args = eval.parse_args(args, env)
        return args[0] != args[1]
