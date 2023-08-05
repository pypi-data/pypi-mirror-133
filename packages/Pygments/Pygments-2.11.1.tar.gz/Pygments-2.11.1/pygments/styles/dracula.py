"""
    pygments.styles.dracula
    ~~~~~~~~~~~~~~~~~~~~~~~

    Pygments version of `Dracula` from https://github.com/dracula/dracula-theme.

    Based on the Dracula Theme for pygments by Chris Bracco.
    See https://github.com/dracula/pygments/tree/fee9ed5613d1086bc01b9d0a5a0e9867a009f571

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import (
    Keyword, Name, Comment, String, Error, Literal, Number, Operator, Other,
    Punctuation, Text, Generic, Whitespace,
)


class DraculaStyle(Style):

    default_style = ""
    background_color = "#282a36"
    highlight_color = "#44475a"
    line_number_color = "#f1fa8c"
    line_number_background_color = "#44475a"
    line_number_special_color = "#50fa7b"
    line_number_special_background_color = "#6272a4"

    styles = {
        Whitespace: "#f8f8f2",

        Comment: "#6272a4",
        Comment.Hashbang: "#6272a4",
        Comment.Multiline: "#6272a4",
        Comment.Preproc: "#ff79c6",
        Comment.Single: "#6272a4",
        Comment.Special: "#6272a4",

        Generic: "#f8f8f2",
        Generic.Deleted: "#8b080b",
        Generic.Emph: "#f8f8f2 underline",
        Generic.Error: "#f8f8f2",
        Generic.Heading: "#f8f8f2 bold",
        Generic.Inserted: "#f8f8f2 bold",
        Generic.Output: "#44475a",
        Generic.Prompt: "#f8f8f2",
        Generic.Strong: "#f8f8f2",
        Generic.Subheading: "#f8f8f2 bold",
        Generic.Traceback: "#f8f8f2",

        Error: "#f8f8f2",
        Keyword: "#ff79c6",
        Keyword.Constant: "#ff79c6",
        Keyword.Declaration: "#8be9fd italic",
        Keyword.Namespace: "#ff79c6",
        Keyword.Pseudo: "#ff79c6",
        Keyword.Reserved: "#ff79c6",
        Keyword.Type: "#8be9fd",
        Literal: "#f8f8f2",
        Literal.Date: "#f8f8f2",
        Name: "#f8f8f2",
        Name.Attribute: "#50fa7b",
        Name.Builtin: "#8be9fd italic",
        Name.Builtin.Pseudo: "#f8f8f2",
        Name.Class: "#50fa7b",
        Name.Constant: "#f8f8f2",
        Name.Decorator: "#f8f8f2",
        Name.Entity: "#f8f8f2",
        Name.Exception: "#f8f8f2",
        Name.Function: "#50fa7b",
        Name.Label: "#8be9fd italic",
        Name.Namespace: "#f8f8f2",
        Name.Other: "#f8f8f2",
        Name.Tag: "#ff79c6",
        Name.Variable: "#8be9fd italic",
        Name.Variable.Class: "#8be9fd italic",
        Name.Variable.Global: "#8be9fd italic",
        Name.Variable.Instance: "#8be9fd italic",
        Number: "#ffb86c",
        Number.Bin: "#ffb86c",
        Number.Float: "#ffb86c",
        Number.Hex: "#ffb86c",
        Number.Integer: "#ffb86c",
        Number.Integer.Long: "#ffb86c",
        Number.Oct: "#ffb86c",
        Operator: "#ff79c6",
        Operator.Word: "#ff79c6",
        Other: "#f8f8f2",
        Punctuation: "#f8f8f2",
        String: "#bd93f9",
        String.Backtick: "#bd93f9",
        String.Char: "#bd93f9",
        String.Doc: "#bd93f9",
        String.Double: "#bd93f9",
        String.Escape: "#bd93f9",
        String.Heredoc: "#bd93f9",
        String.Interpol: "#bd93f9",
        String.Other: "#bd93f9",
        String.Regex: "#bd93f9",
        String.Single: "#bd93f9",
        String.Symbol: "#bd93f9",
        Text: "#f8f8f2",
    }
