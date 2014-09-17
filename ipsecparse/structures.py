from collections import OrderedDict

__all__ = ['IpsecConf']

class IpsecConf(OrderedDict):

    @classmethod
    def display_value(cls, value):
        try:
            next(c for c in value if c in ' \t')
        except StopIteration:
            return value
        else:
            #  from http://linux.die.net/man/5/ipsec.conf :
            #  "A value may contain white space only if the
            #  entire value is enclosed in double quotes (");
            #  a value cannot itself contain a double quote, 
            #  nor may it be continued across more than one line.
            return '"' + value + '"'
            
    def dumps(self, indent = '\t'):
        result = []
        for (tpe, name), content in self.items():
            result.append('%s %s' % (tpe, name))
            if tpe != 'include':
                for key, value in content.items():
                    result.append(
                        '%s%s=%s' % (
                            indent, key,
                            self.__class__.display_value(value)
                        )
                    )
            result.append('')
        return '\n'.join(result)
        
        
    def conn_filter(self, func):
        return [
            (name, content) for (tpe, name), content in self.items()
            if tpe == 'conn' and func(content)
        ]
