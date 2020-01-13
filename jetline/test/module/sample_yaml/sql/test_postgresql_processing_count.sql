select
    count(*)
from (
    select
        current_timestamp
    union all
    select
        current_timestamp
    union all
    select current_timestamp
) t
