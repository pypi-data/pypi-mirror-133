"""
    pygments.styles.sas
    ~~~~~~~~~~~~~~~~~~~

    Style inspired by SAS' enhanced program editor. Note This is not
    meant to be a complete style. It's merely meant to mimic SAS'
    program editor syntax highlighting.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Comment
from pygments.token import Error
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import Name
from pygments.token import Number
from pygments.token import Other
from pygments.token import String
from pygments.token import Whitespace


class SasStyle(Style):
    """
    Style inspired by SAS' enhanced program editor. Note This is not
    meant to be a complete style. It's merely meant to mimic SAS'
    program editor syntax highlighting.
    """

    default_style = ''

    styles = {
        Whitespace:            '#bbbbbb',
        Comment:               'italic #008800',
        String:                '#800080',
        Number:                'bold #2e8b57',
        Other:                 'bg:#ffffe0',
        Keyword:               '#2c2cff',
        Keyword.Reserved:      'bold #353580',
        Keyword.Constant:      'bold',
        Name.Builtin:          '#2c2cff',
        Name.Function:         'bold italic',
        Name.Variable:         'bold #2c2cff',
        Generic:               '#2c2cff',
        Generic.Emph:          '#008800',
        Generic.Error:         '#d30202',
        Error:                 'bg:#e3d2d2 #a61717'
    }
