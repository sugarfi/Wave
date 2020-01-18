import eval # Imports
import data
import errors
import os
import importlib

data.init() # Set up data

def setup(env):
    @eval.proc(env, 'useg', eval.ARITY_1, data.str_t) # useg procedure - like from module import *
    def useg(env, *args):
        args = eval.parse_args(args, env) # Parse args
        for arg in args:
            try: # Try to open a local file first
                import_env = eval.Env(arg + '.wave')
                for name in env.getscope():
                    import_env.setval(name, env.getscope()[name])
                import_env.run()
                env.pyvars.update(import_env.pyvars)
                for name in import_env.getscope():
                    env.setval(name, import_env.getscope()[name])
            except FileNotFoundError: # If we can't do that then try to import a Python module
                try:
                    try:
                        importlib.import_module(arg).setup(env)
                    except AttributeError:
                        lib = importlib.import_module(arg)
                        env.pyvars[arg] = lib
                except ImportError: # If we can't do that then try to open a standard library file
                    try:
                        import_env = eval.Env(os.path.abspath('lib/' + arg + '.wave'))
                        for name in env.getscope():
                            import_env.setval(name, env.getscope()[name])
                        import_env.run()
                        env.pyvars.update(import_env.pyvars)
                        for name in import_env.getscope():
                            env.setval(name, import_env.getscope()[name])
                    except FileNotFoundError: # If we can't do that then give up
                        errors._UseError(f'Could not find {arg}.wave or {arg}.py').throw()

    @eval.proc(env, 'use', eval.ARITY_1, data.str_t) # use procedure - like import module
    def use(env, *args):
        args = eval.parse_args(args, env) # Same process as useg
        for arg in args:
            try:
                import_env = eval.Env(arg + '.wave')
                for name in env.getscope():
                    import_env.setval(name, env.getscope()[name])
                import_env.run()
                ldict = import_env.getscope()
                env.setval(arg, ldict)
                env.pyvars.update(import_env.pyvars)
            except FileNotFoundError:
                try:
                    try:
                        import_env = eval.Env(None)
                        importlib.import_module(arg).setup(import_env)
                        env.pyvars[arg] = import_env.getscope()
                    except AttributeError:
                        lib = importlib.import_module(arg)
                        env.pyvars[arg] = lib
                except ImportError:
                    try:
                        import_env = eval.Env(os.path.abspath('lib/' + arg + '.wave'))
                        for name in env.getscope():
                            import_env.setval(name, env.getscope()[name])
                        import_env.run()
                        ldict = import_env.getscope()
                        env.setval(arg, ldict)
                        env.pyvars.update(import_env.pyvars)
                    except FileNotFoundError:
                        errors._UseError(f'Could not find {arg}.wave or {arg}.py').throw()

    @eval.proc(env, 'py', 1, data.str_t) # py procedure - runs Python code
    def py(env, *args):
        pyvars = env.getscope() # Set up globals()
        pyvars['env'] = env
        pyvars['eval'] = eval
        pyvars['data'] = data
        pyvars.update(env.pyvars)
        args = eval.parse_args(args, env)
        exec(f'_ = {args[0]}', pyvars) # Yes, this is insecure, but if the user does something bad, it only harms their computer
        p = env.getscope().keys()
        for key in p:
            if key in env.pyvars:
                del env.pyvars[key]
        return pyvars['_'] # Return the output

    @eval.proc(env, '\'', eval.ARITY_1, eval.ANY) # quote procedure - creates a node
    def quote(env, *args):
        args = list(args)
        return eval.Node(args) # Make a node

    @eval.proc(env, 'list', eval.ARITY_0, eval.ANY) # list procedure - creates a list
    def _list(env, *args):
        args = eval.parse_args(args, env)
        return data.array(args) # Make a list

    @eval.proc(env, 'eval', 1, [data.node_t, data.str_t]) # eval procedure - evaluates a string or node
    def _eval(env, *args):
        args = eval.parse_args(args, env)
        arg = args[0]
        if isinstance(arg, eval.Node): # If it is a node, evaluate that
            return arg.eval(env)
        else: # Otherwise, run a string
            eval_env = eval.Env(code=str(arg))
            setup(eval_env)
            eval_env.run()
            env.scopes[env.scope].update(eval_env.getscope())

    @eval.proc(env, 'var', 2, eval.ANY, eval.ANY) # var procedure - variable assignment
    def var(env, *args):
        name = str(args[0])
        args = eval.parse_args(args, env)
        value = args[1]
        env.setval(name, value)

    @eval.proc(env, 'if', 3, eval.ANY, data.node_t, data.node_t) # if procedure - if-else
    def _if(env, *args):
        args = eval.parse_args(args, env) # Parse the args
        t = args[1] # True code
        f = args[2] # False code
        if isinstance(t, str): # Format strings correctly
            t = '"' + t + '"'
        if isinstance(f, str):
            f = '"' + f + '"'
        expr = args[0] # Get the expression
        if expr: # Choose some code to evaluate
            return _eval(env, t)
        return _eval(env, f)

    @eval.proc(env, 'while', 2, eval.ANY, data.node_t) # while procedure - while loop
    def _while(env, *args):
        args = eval.parse_args(args, env)
        expr = args[0] # Get the expression and body
        body = args[1]
        if isinstance(body, str): # Format strings
            body = '"' + body + '"'
        while _eval(env, expr): # Go
            _eval(env, body)

    @eval.proc(env, 'for', 3, eval.ANY, data.arr_t) # for procedure - for-in loop
    def _for(env, *args):
        var = args[0] # Get the variable, iterable, and body
        args = eval.parse_args(args, env)
        iter = args[1]
        body = args[2]
        if isinstance(body, str): # Format strings
            body = '"' + body + '"'
        for item in iter: # Go
            env.setval(var, item)
            _eval(env, body)

    @eval.proc(env, 'func', 3, eval.ANY, data.arr_t, data.node_t)
    def func(env, *args):
        name = args[0]
        os = env.getscope() # Get the old scope
        ns = {}
        for item in env.getscope():
            if isinstance(env.getval(item), eval.Proc):
                ns[item] = env.getval(item) # Save procedures in the new scope
        env.scopes[env.scope] = ns
        args = eval.parse_args(args, env) # Parse arguments
        need = args[1] # Get the arguments needed
        env.scopes[env.scope] = os # Restore the old scope
        args = eval.parse_args(args, env) # Parse arguments again
        body = args[2] # Get the body
        @eval.proc(env, name, len(need), *[eval.ANY] * len(need)) # Create a procedure
        def run(env, *args):
            args = eval.parse_args(args, env) # Parse arguments
            env.scopes.append({}) # Create a new scope
            env.scope += 1
            i = 0
            env.scopes[env.scope].update(env.scopes[env.scope - 1]) # Add the old scope to it
            for var in need: # Set up arguments
                env.setval(str(var), args[i])
                i += 1
            env.setval(name, run) # Allow recursion
            out = _eval(env, body) # Run the code
            env.scope -= 1
            env.scopes.pop() # Delete our scope
            return out
        return run

    @eval.proc(env, 'switch', 3, eval.ANY, data.arr_t, data.arr_t) # switch procedure - switch-case
    def switch(env, *args):
        args = eval.parse_args(args, env) # Get the expression, values, and outputs
        expr = args[0]
        vals = args[1]
        outs = args[2]
        i = 0
        for val in vals:
            if expr == val: # If we find a match, run that
                return _eval(env, outs[i])
            i += 1
        return _eval(env, outs[-1]) # Run the last thing

    @eval.proc(env, 'object', 1, data.arr_t) # object procedure - creates an object
    def _object(env, *args):
        args = eval.parse_args(args, env)
        out = {}
        l = args[0]
        for i in range(0, len(l), 2): # Set up keys and values
            out[l[i]] = l[i + 1]
        return out
