from __future__ import annotations

from pathlib import Path

from pachamix_data.builders.lyrics_core import build_lyrics_core


FIXTURES = Path(__file__).parent / "fixtures" / "lyrics" / "official"


def test_build_lyrics_core_parses_official_musixmatch_format_from_directory(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "lyrics_core.parquet"

    frame = build_lyrics_core(
        lyrics_txt=FIXTURES,
        output_parquet=output_path,
    )

    assert output_path.exists()
    assert frame.columns == ["msd_track_id", "token", "count"]
    assert frame.shape == (8, 3)
    rows = frame.sort(["msd_track_id", "token"]).to_dicts()
    assert rows[0] == {"msd_track_id": "TR001", "token": "bright", "count": 2}
    assert rows[-1] == {"msd_track_id": "TR003", "token": "calm", "count": 6}
