SELECT
  tp.playlist_id AS playlist_id,
  tp.track_id AS track_id
FROM track_playlist1 AS tp
ORDER BY tp.playlist_id, tp.track_id;
