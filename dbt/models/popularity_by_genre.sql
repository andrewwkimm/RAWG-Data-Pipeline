-- Queries number of games released by genre.


WITH game_counts AS (
    SELECT
        genre,
        COUNT(game_id) AS games_count
    FROM
        video_game_dataset.video_game_data
    GROUP BY
        genre
    ORDER BY
        games_count DESC
)

SELECT genre, games_count
FROM game_counts
