import sly
import sys
import errors

class Lexer(sly.Lexer):
    tokens = {NUMBER, NAME, STRING} # The tokens we need to match
    literals = {'(', ')'} # Parentheses

    ignore = ' \t\n' # Ignore whitespace
    ignore_comment = ';.*\n' # Comments

    NUMBER = r'-?[0-9]+(\.[0-9]+)?' # Numbers regex
    STRING = r'\"(\\.|[^\"])*\"' # String literal regex
    NAME = r'[^ \t\n()]+' # Names, really anything but the other stuff

class Parser(sly.Parser):
    tokens = Lexer.tokens # Sly requires this

    def error(self, p): # Syntax error handler
        if p:
            errors._SyntaxError(f'Bad token {p.value} at index {p.index}').throw()
        else:
            errors._SyntaxError('EOF').throw()
        sys.exit(1)

    @_('expr line') # Allow joint expressions
    def line(self, p):
        return [p.expr, *p.line]

    @_('expr') # One expression counts as a line
    def line(self, p):
        return [p.expr]

    @_('"(" NAME arg ")"') # A name with arguments is an expression
    def expr(self, p):
        return [p.NAME, *p.arg]

    @_('"(" expr ")"') # An expression is an expression
    def expr(self, p):
        return p.expr

    @_('"(" expr expr ")"') # Joint expressions are allowed
    def expr(self, p):
        return [p.expr0, p.expr1]

    @_('"(" ")"') # An empty node is allowed
    def expr(self, p):
        return []

    @_('expr') # An expression counts as an argument
    def arg(self, p):
        return [p.expr]

    @_('NUMBER') # A number is also an argument
    def arg(self, p):
        return [p.NUMBER]

    @_('NAME') # So is a name
    def arg(self, p):
        return [p.NAME]

    @_('STRING') # Also a string
    def arg(self, p):
        return [p.STRING]

    @_('arg arg') # Jointed arguments are allowed
    def arg(self, p):
        return [*p.arg0, *p.arg1]

    @_('') # No arguments are allowed too
    def arg(self, p):
        return []
