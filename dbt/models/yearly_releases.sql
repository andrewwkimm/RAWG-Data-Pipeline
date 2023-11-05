-- Queries number of games released per year.


WITH yearly_releases AS (
    SELECT
        year,
        COUNT(game_id) AS games_released
    FROM
        rawg_staging_area.rawg_staging_table
    GROUP BY
        year
    ORDER BY
        year
)

SELECT year, games_released
FROM yearly_releases
