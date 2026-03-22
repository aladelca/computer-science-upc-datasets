SELECT
  t.id AS track_id,
  t.name AS track_name,
  COALESCE(artists.artist_name, '') AS artist_name,
  COALESCE(al.name, '') AS album_name
FROM track AS t
LEFT JOIN album AS al
  ON al.id = t.album_id
LEFT JOIN (
  SELECT
    ta.track_id,
    GROUP_CONCAT(ar.name ORDER BY ar.name SEPARATOR ' | ') AS artist_name
  FROM track_artist1 AS ta
  LEFT JOIN artist AS ar
    ON ar.id = ta.artist_id
  GROUP BY ta.track_id
) AS artists
  ON artists.track_id = t.id
ORDER BY t.id;
