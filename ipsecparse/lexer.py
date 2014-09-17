from ply import lex
from re import MULTILINE
from ipsecparse.exceptions import ConfTokenError

class Lexer(object):
    tokens = (
        'INCLUDE',
        'SECTION_TYPE',
        'KEY',
        'VALUE',
        'DOUBLE_QUOTED_VALUE',
    )
    
    _name = '[a-zA-Z][-_.a-zA-Z0-9]*'
    
    def t_ignore_NEW_LINE(self, token):
        r'\n'
        
    def t_ignore_COMMENT(self, token):
        r'\#.*'

    def t_SECTION_TYPE(self, token):
        if token.value == 'include':
            token.type = 'INCLUDE'
        return token
        
    t_SECTION_TYPE.__doc__ = '^' + _name
     
    def t_KEY(self, token):
        token.value = token.value.strip()[:-1].rstrip()
        return token
    
    t_KEY.__doc__ = r'^[ \t]+' + _name + r'[ \t]*=[ \t]*'
    
    def t_VALUE(self, token):
        r'[^ \t\n\#"]+'
        return token
    
    def t_DOUBLE_QUOTED_VALUE(self, token):
        #  from http://linux.die.net/man/5/ipsec.conf :
        #  "A value may contain white space only if the
        #  entire value is enclosed in double quotes (");
        #  a value cannot itself contain a double quote, 
        #  nor may it be continued across more than one line."
        r'"[^"\n\#]*"'
        token.value = token.value[1:-1]
        return token

    t_ignore_SPACE = r'[ \t]+'
    
    def t_error(self, token):
        raise ConfTokenError(
            "Illegal character '%s', line %s" % (
                token.value[0],
                token.lineno
            )
        )
        
    def __init__(self):
        self.lexer = lex.lex(object = self, debug = 0,reflags = MULTILINE)
        
    def input(self, text):
        self.lexer.input(text + "\n")
