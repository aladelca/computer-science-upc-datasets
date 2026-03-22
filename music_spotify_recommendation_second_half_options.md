# Music / Spotify Recommendation Dataset Options for the Second Half of the Course

## Scope of This Note

This note answers a narrower question than the general dataset viability report:

> If the second half of the course must remain in the `music / Spotify recommendation` domain, which datasets should be used?

The focus is therefore on:

- Weeks `9-10`: collaborative filtering, playlist continuation, matrix factorization, hybrid recommendation
- Weeks `11-12`: graph analytics, random walks, PageRank on music networks
- Weeks `13-14`: pipelines, serving, monitoring, and final productization in the same narrative

---

## Core Clarification

The missing dataset in your current course stack is `not only` for network analytics.

It is primarily the missing `behavior layer`.

That behavior layer is needed for:

- collaborative filtering
- popularity baselines
- playlist continuation
- matrix factorization
- hybrid recommendation
- song co-occurrence graph construction
- graph analytics and PageRank

So the real gap is:

> `a music listening / playlist interaction dataset`

The graph dataset should ideally be `derived from that same behavior dataset`, not introduced as a disconnected external graph source.

That is the cleanest way to preserve the `PachaMix` story and the mathematical continuity of the course.

---

## Current Recommendation

If you want to stay fully in the `music / Spotify recommendation` world, the best ordering is:

1. `Playlist2vec`
2. `ListenBrainz / MLHD+`
3. `Spotify MPD` only if you already have legitimate access
4. `LFM-2b` is not a dependable core option today

---

## Decision Matrix

| Option | Domain fit | Best for Weeks | Current availability status | Fit to current repo | Overall verdict |
| --- | --- | --- | --- | --- | --- |
| `Playlist2vec` | Excellent | 9-12, 13-14 | publicly downloadable on Zenodo | Excellent | `Best choice` |
| `ListenBrainz / MLHD+` | Excellent | 9-12, 13-14 | official dumps and MLHD+ docs available | Medium | `Best open alternative if you can adapt the pipeline` |
| `Spotify MPD` | Perfect in theory | 9-12, 13-14 | not directly downloadable from AIcrowd as of March 21, 2026 | Medium | `Use only if you already have access` |
| `LFM-2b` | Very strong in theory | 9-12, 13-14 | not available for download anymore | Low | `No-go as a core dependency` |

---

## Option 1. Playlist2vec

## Why it fits

This is the best match to your current repository and course narrative.

The official Zenodo record describes it as:

- a `Spotify Million Playlist Dataset`
- `1 million playlists`
- `3 million unique tracks`
- `3 million unique albums`
- `1.3 million artists`
- delivered as a SQL dump with tables including:
  - `track`
  - `playlist`
  - `track_playlist1`

That matches your codebase very closely.

## Why it is the best engineering fit

Your current repo already expects exactly the exported structure that Playlist2vec can provide:

- `playlist.csv`
- `track.csv`
- `track_playlist1.csv`

The current builder in `src/pachamix_data/builders/playlist_events.py` already supports this path directly.

That means the least invasive course-completion strategy is:

1. obtain Playlist2vec
2. export the three required CSVs
3. place them under `data/raw/playlist2vec/`
4. run the existing build pipeline

## What it gives you pedagogically

### Weeks 9-10

- playlist-track interaction matrix
- popularity baselines
- item-item collaborative filtering
- playlist continuation
- matrix factorization

### Weeks 11-12

- song-song co-occurrence graph
- weighted degree
- transition probabilities
- PageRank

### Weeks 13-14

- complete behavior-to-graph pipeline
- realistic artifact lineage
- deployment and monitoring examples

## Main limitations

- it requires SQL-dump preparation work
- it is still not a natural join with your `FMA` or `musiXmatch/MSD` layers
- a fully valid hybrid recommender still needs cross-catalog matching if you want content plus behavior on the same items

## Verdict

> `This is the best dataset for the second half of the course if you want to stay in Spotify-style playlist recommendation and preserve your current repo architecture.`

## Official source

- Playlist2vec Zenodo record: https://zenodo.org/records/5002584

---

## Option 2. ListenBrainz / MLHD+

## Why it fits

If you want the second half to remain in `music recommendation`, but you prefer a more open and actively maintained ecosystem than Spotify-challenge data, this is the best alternative.

MusicBrainz documents `MLHD+` as an improved listening-history dataset with corrected and canonicalized MusicBrainz identifiers.
The official documentation explicitly recommends using the `-complete` archives when you want verified MBIDs.

The MusicBrainz FTP index also shows active ListenBrainz dump infrastructure, including:

- `fullexport/`
- `incremental/`
- `mlhd/`
- `sample/`
- `spark/`

As of `March 21, 2026`, the dump index shows ongoing incremental exports through `January` and `February 2026`, which is strong evidence that the ecosystem remains active.

## What it gives you pedagogically

### Strengths

- real music listening events
- canonical identifiers
- richer long-term path into MusicBrainz-linked metadata
- better long-term research value than challenge-only playlist datasets

### Good second-half fit

It supports:

- user-item or user-track collaborative filtering
- playcount aggregation
- implicit-feedback recommendation
- item-item co-listening graphs
- graph analytics and PageRank

## Why it is not the easiest option for your current repo

Your current builders are playlist-centric:

- `playlist_id`
- `track_uri`
- playlist-event grain

ListenBrainz / MLHD+ is closer to:

- listening-event grain
- timestamped user-track histories
- MBID-based canonical music entities

So it is a strong conceptual fit, but it requires:

- an adapter or new builder
- a redesign of the interaction schema
- likely a different graph-construction logic

## Best use case

Use this if:

- you want to stay in music recommendation
- you are willing to invest in a slightly more serious data engineering path
- you value open, canonical music identifiers

## Verdict

> `Best open music-behavior alternative if you are willing to adapt the pipeline beyond the current Playlist2vec-first design.`

## Official sources

- MLHD+ documentation: https://musicbrainz.org/doc/MLHD%2B
- ListenBrainz dump index: https://ftp.musicbrainz.org/pub/musicbrainz/listenbrainz/
- ListenBrainz incremental exports: https://ftp.musicbrainz.org/pub/musicbrainz/listenbrainz/incremental/

---

## Option 3. Spotify MPD

## Why it fits in theory

Conceptually, this is the perfect thematic continuation if you want the second half to remain explicitly tied to `Spotify recommendation`.

Spotify Research describes the remastered Million Playlist Dataset as:

- `1 million playlists`
- `over 2 million unique tracks`
- `nearly 300,000 artists`

and the task is exactly:

- automatic playlist continuation

Pedagogically, this is ideal for:

- collaborative filtering
- ranking
- matrix factorization
- graph derivation from playlist co-occurrence

## Why it is not safe as a core course dependency

As of `March 21, 2026`, the official AIcrowd challenge page states:

- `the dataset associated with this challenge is not available for download anymore`
- it asks users to reach out directly to Spotify Research for access

So even though Spotify Research announced the remastered release on `September 28, 2020`, the current operational state is not dependable for a course that needs frictionless access.

## Practical interpretation

This means:

- if you already have legitimate institutional access, it is a very strong option
- if you do not already have access, you should not build the semester around it

## Verdict

> `Excellent in theory, risky in practice. Use only if access is already secured before the course starts.`

## Official sources

- Spotify Research announcement: https://research.atspotify.com/the-million-playlist-dataset-remastered
- AIcrowd challenge page: https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

---

## Option 4. LFM-2b

## Why it is attractive

This dataset would be academically strong for the second half:

- `~2 billion` listening events
- `120,322` users
- explicit music listening history structure
- track-level and artist-level recommendation views
- official additional files such as:
  - `listening-events`
  - `listening-counts`
  - `spotify-uris`
  - lyrics features
  - tags

It would support:

- implicit recommendation
- playcount-based modeling
- graph construction from co-listening
- music recommendation at substantial scale

## Why it is not dependable now

The official dataset page explicitly says:

> `The dataset is not available for download anymore due to license issues.`

That makes it unsuitable as a required course dependency today.

## Verdict

> `Excellent historical benchmark, but a no-go for a course that needs reproducible current access.`

## Official source

- LFM-2b official dataset page: https://www.cp.jku.at/datasets/LFM-2b/

---

## What the Missing Dataset Should Look Like

For your current course and repo, the second-half dataset should ideally satisfy all of these:

1. `music recommendation domain`
2. `playlist or listening interaction structure`
3. `track-level identifiers`
4. `enough scale for collaborative filtering`
5. `natural graph derivation from co-occurrence`
6. `stable enough access to prepare the semester in advance`

That means the target data model should be one of:

- `playlist_id, track_id, position`
- `user_id, track_id, timestamp`
- optionally, `playcount` or repeated listening events

From there you can derive:

- user-item matrices
- item-item similarity
- train/test continuation splits
- song co-occurrence graphs
- transition matrices for PageRank

---

## Best Strategy for Your Course

## Recommended final choice

### Best practical choice

`Playlist2vec`

Why:

- closest to current code
- clearly Spotify-like playlist recommendation
- easiest route to complete Weeks `9-12`
- preserves the PachaMix playlist narrative

### Best open long-term alternative

`ListenBrainz / MLHD+`

Why:

- still music recommendation
- more open and canonical
- good if you want a more research-oriented future version of the course

### Only use if already obtained

`Spotify MPD`

Why:

- perfect thematic fit
- bad operational predictability as of `March 21, 2026`

### Do not use as a core dependency now

`LFM-2b`

Why:

- official page says it is no longer downloadable

---

## Recommended Course Mapping

If you adopt `Playlist2vec`, the second half becomes:

| Weeks | Topic | Data object |
| --- | --- | --- |
| 9 | Collaborative filtering | playlist-track interaction table |
| 10 | Matrix factorization / hybrid logic | playlist-track matrix, optional matched subset |
| 11 | Graph analytics foundations | song-song co-occurrence graph derived from playlists |
| 12 | PageRank | directed transition graph derived from the co-occurrence graph |
| 13 | Pipelines | end-to-end raw playlist exports -> processed events -> graph |
| 14 | Serving and monitoring | ranking, freshness, popularity drift, graph drift |

This is the cleanest continuation of your current first-half stack.

---

## Final Answer

If everything from Week `9` onward must remain tied to `music / Spotify recommendation`, then:

> `The missing dataset is primarily a music-behavior dataset, not merely a graph dataset.`

The graph layer should be derived from that behavior layer.

The best choice for your current repository is:

> `Playlist2vec`

The best open alternative, if you are willing to adapt the pipeline more deeply, is:

> `ListenBrainz / MLHD+`

And the option that sounds most perfect conceptually but is too risky to depend on operationally is:

> `Spotify MPD`
