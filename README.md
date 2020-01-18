![The Great Wave](https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg)
# Wave
Wave is a Lisp-like language implemented in Python. Built on top of Numpy and Sympy,
Wave is both powerful and simple. It can be easily extended to your needs, and is very
versatile. Sound interesting? Read on to get started.
---
## Installation

Wave is simple to install. Just clone this repository, `cd` into the Wave directory,
and run `pip3 install -r requirements.txt`. Then, you can run `./wave` in this directory.
---
## Basic Usage
First, run `./wave` to open a REPL. You should see a `>` prompt. Obviously, you will want
to run a "Hello, world!" program now. That can be accomplished in 2 simple lines:  
```
(useg "wio")
(println "Hello, world!")
```
You should see the words "Hello, world!" on screen. But what did you just do? We'll go through
it line by line:

- The first line imports, or `use`s the `wio` library, which gives us access to the `println`
procedure. You might wonder why we use `useg` instead of `use`. That is because just `use` will
import the `wio` library, but put it in its own object. If we did that, we would have to use
`wio.println`, not `println`. `useg` does not put the library in its own object. It is like Python's
`import module` vs `from module import *`.
- The second line is simple. It calls the procedure `println` from `wio`. `println` simple takes
a string as input and outputs it the screen, with a trailing newline. There is a `print` procedure,
but it does not print with a newline.
---
## The Wave Philosophy
That was a pretty minimal example, but it shows off one of the core principles of Wave:  
`Functions should not assume anything.`  
The `useg` function did not assume you wanted to import the module globally; you had to add the `g`.
The `println` function did not assume you wanted a newline; you had to use the function that uses one.
There are a few principles like this in the Wave Philosophy:

- `Functions should not assume anything.`
- `Neither should anything else.`
- `Syntax should be uniform; no special cases at all.`
- `Thus, there is nothing besides functions to not assume anything.`
- `Code should be readable and simple, but powerful.`
---
## The Standard Library
Obviously, Wave has more functions than just `println`. The standard library is small at the moment,
comprising just `wcore`, `wio`, `wmath`, and `wtypes`. These all have to be imported, except `wcore`,
which is imported by default. The names of these libraries are pretty self-explanatory: `wio` is I/O,
`wtypes` is type operations, and `wmath` is math. The standard library functions, albeit described briefly,
are as follows:

### `wcore`

- `(useg <module: string>)` Imports a module and adds it to the current scope.
- `(use <module: string>)` Imports a module and adds it to its own object.
- `(py <code: string>)` Evaluates Python code.
- `(' *<node: any>)` The same as the Lisp quote procedure. Can also be written `'(*<node>)`.
- `(list *<values: any>)` Creates a list from arguments.
- `(eval <code: node | string>)` Evaluates a node or string as Wave code.
- `(var <name: name> <value: any>)` Sets a variable to a name.
- `(if <expr: any> <true: node | string> <false: node | string>)` Evaluates `true` if `expr` is true, otherwise evaluates `false`.
- `(while <expr: any> <body: node | string>)` Evaluates `body` while `expr` is true.
- `(for <var: name> <iter: list> <body: node | string>)` Evaluates `body` on every `var` in `iter`.
- `(func <name: name> <args: list> <body: node>)` Defines a new function with the given body and arguments.
- `(switch <expr: any> <vals: list> <outs: list>)` A switch-case statement. Selects the matching output to `expr`. Uses
the last value as the default.
- `(object <pairs: list>)` Creates an object with the given keys and values. `pairs` is of the format: `[key val key val]`, where key
is always a string.

### `wio`

- `(list-print <val: list>)` Prints a list.
- `(list-print <val: number>)` Prints a number.
- `(list-print <val: string>)` Prints a string.
- `(list-print <val: bool>)` Prints a boolean.
- `(list-print <val: object>)` Prints an object.
- `(list-print <val: node>)` Prints a node.
- `(list-print <val: nil>)` Prints nil.
- `(print <val: any>)` Prints a value based on its type.
- `(println <val: any>)` Prints a value with a newline after it.
- `(read <prompt: any> <type: node>)` Reads a value and converts it to `type`.
- `(newline)` Prints a newline.

### `wtypes`

- `(number <val: any>)` Converts `val` to a number.
- `(string <val: any>)` Converts `val` to a string.
- `(bool <val: any>)` Converts `val` to a boolean.
- `(nil)` Returns `nil`.
- `(typeof <val: any>)` Returns the type of `val` as a string.

### `wmath`

- `(+ <a: any> <b: any>)` Returns `a` + `b`.
- `(- <a: number | bool | list> <b: number | bool | list>)` Returns `a` - `b`.
- `(* <a: number | bool | list> <b: number | bool | list>)` Returns `a` * `b`.
- `(/ <a: number | bool | list> <b: number | bool | list>)` Returns `a` / `b`.
- `(^ <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` ** `b`.
- `(% <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` % `b`.
- `(> <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` > `b`.
- `(< <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` < `b`.
- `(>= <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` >= `b`.
- `(<= <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` <= `b`.
- `(== <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` == `b`.
- `(!= <a: number | string | object | bool> <b: number | string | object | bool>)` Returns `a` != `b`.
---
## Extending
Wave can be easily extended to do whatever you would like. For example, let's say you want to create a library
`hello` that has a function `hi` that prints out the text `hi there`. You could do this in Wave like so:
```
(useg "wio")
(func hi (list) '(
    (println "hi there")
))
```
Then, from another file, just do `(use hello)` and then you can call this new function. Easy! But what if you
wanted to do this in Python? There is a basic API for that. First, in the Wave directory, make a new file
`hello.py`. In it, type:
```
import eval
import data

def setup(env):
    @eval.proc(env, 'hi', 0, eval.ANY)
    def hi(env, *args):
        print('hi there')
```
See? Simple. Whenever Wave loads a Python module, it calls its `setup` method, the argument being the
`eval.Env` object the program is running in. To create procedures, simple import `eval` and `data` and
use the `eval.proc` decorator. The arguments to it are the `Env` object, the procedure name, the arity,
or number of arguments, and the type of the arguments. This is one reason to use Python over Wave for
writing libraries: type checking. If you want a procedure that takes 0 or more or 1 or more arguments,
use the `eval.ARITY_0` and `eval.ARITY_1` constants respectively. The valid values for types are really any
class, but it is reccomened to use those in `data`: `data.num_t`, `data.arr_t`, `data.str_t`, `data.node_t`,
`data.bool_t`, `data.obj_t`, and `data.nil_t`. If you do not care what type something uses, you can use the
`eval.ANY` constant. As well, most of the time, you will want to call
```
args = eval.parse_args(args, env)
```
on you arguments. This just parses the arguments to that something like `(myfunc (+ 5 5))` would become
`(myfunc 10)`, not the literal `(+ 5 5)`.
---
## License
You can do whatever you want with this software. If you write a library, please submit a pull request
and it could be added to the standard library. Feel free to contribute any code, as long as it is tested.
