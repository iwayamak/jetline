copy (
{%- filter indent %}
{{sql_str}}
{%- endfilter -%}
)
    to stdout
    with
        delimiter as '{{delimiter}}'
        {{-' null \'' ~ null_str ~ '\'' if null_str != none}}
        csv {{-' header' if header}}
            quote as '{{quote}}'
            escape as '{{escape}}'
            {{'force quote ' ~ force_quote if force_quote != none}}
