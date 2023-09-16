-- Queries number of games released per year.


WITH yearly_releases AS (
    SELECT
        year,
        COUNT(game_id) AS games_released
    FROM
        video_game_dataset.video_game_data
    GROUP BY
        year
    ORDER BY
        year
)

SELECT year, games_released
FROM yearly_releases
