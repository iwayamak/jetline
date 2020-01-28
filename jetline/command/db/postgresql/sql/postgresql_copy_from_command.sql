copy
    {{schema}}.{{table_name}}
from stdin
    with
        delimiter as '{{delimiter}}'
        {{-' null \'' ~ null_str ~ '\'' if null_str != none}}
        csv {{-' header' if header}}
            quote as '{{quote}}'
            escape as '{{escape}}'
