"""
    pygments.lexers.elpi
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for the `Elpi <http://github.com/LPCIC/elpi>`_ programming language.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import \
    Text, Comment, Operator, Keyword, Name, String, Number

__all__ = ['ElpiLexer']

class ElpiLexer(RegexLexer):
    """
    Lexer for the `Elpi <http://github.com/LPCIC/elpi>`_ programming language.

    .. versionadded::2.11
    """

    name = 'Elpi'
    aliases = ['elpi']
    filenames = ['*.elpi']
    mimetypes = ['text/x-elpi']
    
    lcase_re = r"[a-z]"
    ucase_re = r"[A-Z]"
    digit_re = r"[0-9]"
    schar2_re = r"([+*^?/<>`'@#~=&!])"
    schar_re = r"({}|-|\$|_)".format(schar2_re)
    idchar_re = r"({}|{}|{}|{})".format(lcase_re,ucase_re,digit_re,schar_re)
    idcharstarns_re = r"({}+|(?=\.[a-z])\.{}+)".format(idchar_re,idchar_re)
    symbchar_re = r"({}|{}|{}|{}|:)".format(lcase_re, ucase_re, digit_re, schar_re)
    constant_re = r"({}{}*|{}{}*|{}{}*|_{}+)".format(ucase_re, idchar_re, lcase_re, idcharstarns_re,schar2_re, symbchar_re,idchar_re)
    symbol_re=r"(,|<=>|->|:-|;|\?-|->|&|=>|\bas\b|\buvar\b|<|=<|=|==|>=|>|\bi<|\bi=<|\bi>=|\bi>|\bis\b|\br<|\br=<|\br>=|\br>|\bs<|\bs=<|\bs>=|\bs>|@|::|\[\]|`->|`:|`:=|\^|-|\+|\bi-|\bi\+|r-|r\+|/|\*|\bdiv\b|\bi\*|\bmod\b|\br\*|~|\bi~|\br~)"
    escape_re=r"\(({}|{})\)".format(constant_re,symbol_re)
    const_sym_re = r"({}|{}|{})".format(constant_re,symbol_re,escape_re)

    tokens = {
        'root': [ include('elpi') ],

        'elpi': [

            include('_elpi-comment'),

            (r"(:before|:after|:if|:name)(\s*)(\")",bygroups(Keyword.Mode,Text.Whitespace,String.Double),'elpi-string'),
            (r"(:index)(\s*\()",bygroups(Keyword.Mode,Text.Whitespace),'elpi-indexing-expr'),
            (r"\b(external pred|pred)(\s+)({})".format(const_sym_re),bygroups(Keyword.Declaration,Text.Whitespace,Name.Function),'elpi-pred-item'),
            (r"\b(external type|type)(\s+)(({}(,\s*)?)+)".format(const_sym_re),bygroups(Keyword.Declaration,Text.Whitespace,Name.Function),'elpi-type'),
            (r"\b(kind)(\s+)(({}|,)+)".format(const_sym_re),bygroups(Keyword.Declaration,Text.Whitespace,Name.Function),'elpi-type'),
            (r"\b(typeabbrev)(\s+)({})".format(const_sym_re),bygroups(Keyword.Declaration,Text.Whitespace,Name.Function),'elpi-type'),
            (r"\b(accumulate)(\s+)(\")",bygroups(Keyword.Declaration,Text.Whitespace,String.Double),'elpi-string'),
            (r"\b(accumulate|namespace|local)(\s+)({})".format(constant_re),bygroups(Keyword.Declaration,Text.Whitespace,Text)),
            (r"\b(shorten)(\s+)({}\.)".format(constant_re),bygroups(Keyword.Declaration,Text.Whitespace,Text)),
            (r"\b(pi|sigma)(\s+)([a-zA-Z][A-Za-z0-9_ ]*)(\\)",bygroups(Keyword.Declaration,Text.Whitespace,Name.Variable,Text)),
            (r"\b(constraint)(\s+)(({}(\s+)?)+)".format(const_sym_re),bygroups(Keyword.Declaration,Text.Whitespace,Name.Function),'elpi-chr-rule-start'),

            (r"(?=[A-Z_]){}".format(constant_re),Name.Variable),
            (r"(?=[a-z_]){}\\".format(constant_re),Name.Variable),
            (r"_",Name.Variable),
            (r"({}|!|=>|;)".format(symbol_re),Keyword.Declaration),
            (constant_re,Text),
            (r"\[|\]|\||=>",Keyword.Declaration),
            (r'"', String.Double, 'elpi-string'),
            (r'`', String.Double, 'elpi-btick'),
            (r'\'', String.Double, 'elpi-tick'),
            (r'\{[^\{]', Text, 'elpi-spill'),
            (r"\(",Text,'elpi-in-parens'),
            (r'\d[\d_]*', Number.Integer),
            (r'-?\d[\d_]*(.[\d_]*)?([eE][+\-]?\d[\d_]*)', Number.Float),
            (r"[\+\*\-/\^\.]", Operator),
        ],
        '_elpi-comment': [
            (r'%[^\n]*\n',Comment),
            (r'/\*',Comment,'elpi-multiline-comment'),
            (r"\s+",Text.Whitespace),
        ],
        'elpi-multiline-comment': [
            (r'\*/',Comment,'#pop'),
            (r'.',Comment)
        ],
        'elpi-indexing-expr':[
            (r'[0-9 _]+',Number.Integer),
            (r'\)',Text,'#pop'),
        ],
        'elpi-type': [
            (r"(ctype\s+)(\")",bygroups(Keyword.Type,String.Double),'elpi-string'),
            (r'->',Keyword.Type),
            (constant_re,Keyword.Type),
            (r"\(|\)",Keyword.Type),
            (r"\.",Text,'#pop'),
            include('_elpi-comment'),
        ],
        'elpi-chr-rule-start': [
            (r"\{",Text,'elpi-chr-rule'),
            include('_elpi-comment'),
        ],
        'elpi-chr-rule': [
           (r"\brule\b",Keyword.Declaration),
           (r"\\",Keyword.Declaration),
           (r"\}",Text,'#pop:2'),
           include('elpi'),
        ],
        'elpi-pred-item': [
            (r"[io]:",Keyword.Mode,'elpi-ctype'),
            (r"\.",Text,'#pop'),
            include('_elpi-comment'),
        ],
        'elpi-ctype': [
            (r"(ctype\s+)(\")",bygroups(Keyword.Type,String.Double),'elpi-string'),
            (constant_re,Keyword.Type),
            (r"\(|\)",Keyword.Type),
            (r",",Text,'#pop'),
            (r"\.",Text,'#pop:2'),
            include('_elpi-comment'),
        ],
        'elpi-btick': [
            (r'[^` ]+', String.Double),
            (r'`', String.Double, '#pop'),
        ],
        'elpi-tick': [
            (r'[^\' ]+', String.Double),
            (r'\'', String.Double, '#pop'),
        ],
        'elpi-string': [
            (r'[^\"]+', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'elpi-spill': [
            (r'\{[^\{]', Text, '#push'),
            (r'\}[^\}]', Text, '#pop'),
            include('elpi'),
        ],
        'elpi-in-parens': [
            (r"\(", Operator, '#push'),
            (r"\)", Operator, '#pop'),
            include('elpi'),
        ],

    }
