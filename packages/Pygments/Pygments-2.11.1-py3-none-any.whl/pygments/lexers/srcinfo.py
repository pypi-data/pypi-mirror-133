"""
    pygments.lexers.srcinfo
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for .SRCINFO files used by Arch Linux Packages.

    The description of the format can be found in the wiki: https://wiki.archlinux.org/title/.SRCINFO

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import Text, Comment, Keyword, Name, Operator, Whitespace

__all__ = ['SrcinfoLexer']

keywords = (
    'pkgbase', 'pkgname',
    'pkgver', 'pkgrel', 'epoch',
    'pkgdesc', 'url', 'install', 'changelog',
    'arch', 'groups', 'license', 'noextract', 'options', 'backup', 'validpgpkeys',
)

architecture_dependent_keywords = (
    'source', 'depends', 'checkdepends', 'makedepends', 'optdepends',
    'provides', 'conflicts', 'replaces',
    'md5sums', 'sha1sums', 'sha224sums', 'sha256sums', 'sha384sums', 'sha512sums'
)

class SrcinfoLexer(RegexLexer):
    """Lexer for .SRCINFO files used by Arch Linux Packages.

    .. versionadded:: 2.11
    """

    name = 'Srcinfo'
    aliases = ['srcinfo']
    filenames = ['.SRCINFO']

    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'#.*', Comment.Single),
            (words(keywords), Keyword, 'assignment'),
            (words(architecture_dependent_keywords, suffix=r'_\w+'), Keyword, 'assignment'),
            (r'\w+', Name.Variable, 'assignment'),
        ],
        'assignment': [
            (r' +', Whitespace),
            (r'=', Operator, 'value'),
        ],
        'value': [
            (r' +', Whitespace),
            (r'.*', Text, '#pop:2'),
        ],
    }
