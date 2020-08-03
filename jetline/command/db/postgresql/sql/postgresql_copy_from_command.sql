copy
    {{table_name}}
    {%- if column_list != none -%}
    (
        {%- for column in column_list %}
        {{column}}{% if not loop.last %},{% endif %}
        {%- endfor %}
    )
    {%- endif %}
    from stdin
    with
        delimiter as '{{delimiter}}'
        {{-' null \'' ~ null_str ~ '\'' if null_str != none}}
        csv {{-' header' if header}}
            quote as '{{quote}}'
            escape as '{{escape}}'
