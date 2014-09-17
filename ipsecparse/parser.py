from ply import yacc
from collections import OrderedDict

from ipsecparse.structures import IpsecConf
from ipsecparse.lexer import Lexer
from ipsecparse.exceptions import ConfSyntaxError

__all__ = ['loads']
    
class Parser(object):

    def p_conf(self, p):
        " conf : parts "
        p[0] = IpsecConf(p[1])
    
    def p_parts(self, p):
        " parts : parts part "
        p[0] = p[1] + (p[2],)
        
    def p_parts_empty(self, p):
        " parts : " 
        p[0] = ()
        
    def p_part(self, p):
        """ part : include 
            part : section """
        p[0] = p[1]
        
    def p_include(self, p):
        """ include : INCLUDE VALUE """
        p[0] = (('include', p[2]), True)

    def p_section(self, p):
        """ section : SECTION_TYPE VALUE key_value_list """
        p[0] = ((p[1], p[2]), OrderedDict(p[3]))    
            
    def p_key_value_list(self, p):
        " key_value_list : key_value_list key_value "
        p[0] = p[1] + (p[2],)
        
    def p_key_value_list_empty(self, p):
        " key_value_list : "
        p[0] = ()
        
    def p_key_value(self, p):
        """ key_value : KEY DOUBLE_QUOTED_VALUE
            key_value : KEY VALUE """
        p[0] = (p[1], p[2])
           
    def p_key_empty_value(self, p):
        """ key_value : KEY """
        p[0] = (p[1], '')       
  
    def p_error(self, p):
        raise ConfSyntaxError(repr(p))
        
    def __init__(self, lexer = None):
        lexer = lexer or Lexer()
        self.tokens = lexer.tokens
        self._lexer = lexer
        self._parser = yacc.yacc(module=self, debug=False, write_tables=0)
    
    def parse(self, entry):
        return self._parser.parse(
            entry,
            lexer = self._lexer.lexer
        )
        
loads = Parser().parse
