with dbt_ml_workout as (
    select
        id,
        image  

    from ml_workout 
)

select
    id,
    choice

from ml_workout

left join dbt_ml_workout using(id)