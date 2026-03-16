from __future__ import annotations

from pathlib import Path

import pytest

from pachamix_data.builders.audio_core import build_audio_core


FIXTURES = Path(__file__).parent / "fixtures" / "fma"


def test_build_audio_core_joins_tracks_and_features(tmp_path: Path) -> None:
    output_path = tmp_path / "audio_core.parquet"

    frame = build_audio_core(
        tracks_csv=FIXTURES / "tracks.csv",
        features_csv=FIXTURES / "features.csv",
        output_parquet=output_path,
    )

    assert output_path.exists()
    assert frame.shape == (2, 7)
    assert frame.columns == [
        "track_id",
        "title",
        "genre_top",
        "artist_name",
        "chroma_mean_01",
        "chroma_std_01",
        "mfcc_mean_01",
    ]
    rows = frame.sort("track_id").to_dicts()
    assert rows[0]["title"] == "Song A"
    assert rows[1]["artist_name"] == "Artist B"
    assert rows[0]["chroma_mean_01"] == pytest.approx(0.10)


def test_build_audio_core_requires_track_identifier(tmp_path: Path) -> None:
    bad_features = tmp_path / "bad_features.csv"
    bad_features.write_text(
        "feature,chroma\n"
        "name,mean\n"
        "kind,01\n"
        "1,0.1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="track_id"):
        build_audio_core(
            tracks_csv=FIXTURES / "tracks.csv",
            features_csv=bad_features,
            output_parquet=tmp_path / "ignored.parquet",
        )


def test_build_audio_core_supports_real_fma_three_row_track_header(
    tmp_path: Path,
) -> None:
    tracks_csv = tmp_path / "tracks_real_shape.csv"
    tracks_csv.write_text(
        ",track,track,artist\n"
        ",title,genre_top,name\n"
        "track_id,,,\n"
        "1,Song A,Rock,Artist A\n"
        "2,Song B,Jazz,Artist B\n",
        encoding="utf-8",
    )
    output_path = tmp_path / "audio_core_real_shape.parquet"

    frame = build_audio_core(
        tracks_csv=tracks_csv,
        features_csv=FIXTURES / "features.csv",
        output_parquet=output_path,
    )

    assert output_path.exists()
    assert frame.shape == (2, 7)
    assert frame.sort("track_id").get_column("track_id").to_list() == [1, 2]
