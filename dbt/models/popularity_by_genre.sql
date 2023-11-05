-- Queries number of games released by genre.


WITH game_counts AS (
    SELECT
        genre,
        COUNT(game_id) AS games_count
    FROM
        rawg_staging_area.rawg_staging_table
    GROUP BY
        genre
    ORDER BY
        games_count DESC
)

SELECT genre, games_count
FROM game_counts
