-- Queries number of games released per month.


WITH monthly_releases AS (
    SELECT
        month,
        year,
        COUNT(game_id) AS games_released
    FROM
        rawg_staging_area.rawg_staging_table
    GROUP BY
        month, year
    ORDER BY
        month, year
)

SELECT month, year, games_released
FROM monthly_releases
