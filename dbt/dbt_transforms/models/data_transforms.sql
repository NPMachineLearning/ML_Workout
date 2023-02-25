{{ config(
    materialized="view",
    alias="ml_workout_transform"
) }}

with dataset as (
    select id, image  
    from ml_workout 
),

label as (
    select id as label_id, choice
    from ml_workout
),

final as (
    select id, image, choice
    from dataset
    left join label on dataset.id = label.label_id
)

select * from final