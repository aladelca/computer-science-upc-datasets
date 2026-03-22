from __future__ import annotations

from typing import Any, Literal, cast

from upc_datasets.catalog import get_dataset_definition, list_datasets

Language = Literal["en", "es", "bilingual"]

LABELS = {
    "dataset": {"en": "Dataset", "es": "Conjunto de datos"},
    "path": {"en": "Path", "es": "Ruta"},
    "asset_name": {"en": "Asset Name", "es": "Nombre del asset"},
    "status": {"en": "Status", "es": "Estado"},
    "grain": {"en": "Grain", "es": "Granularidad"},
    "description": {"en": "Description", "es": "Descripcion"},
    "source": {"en": "Sources", "es": "Fuentes"},
    "primary_key": {"en": "Primary Key", "es": "Clave primaria"},
    "columns": {"en": "Columns", "es": "Columnas"},
    "feature_families": {"en": "Feature Families", "es": "Familias de variables"},
}

STATUS_LABELS = {
    "generated": {"en": "generated", "es": "generado"},
    "optional": {"en": "optional", "es": "opcional"},
}

TRANSLATIONS = {
    "pachamix_audio_core": {
        "grain_es": "una fila por pista de FMA",
        "description_es": "Tabla estructurada de caracteristicas de audio con metadatos de FMA y descriptores precalculados.",
        "columns": {
            "track_id": "Identificador de pista de FMA.",
            "title": "Titulo de la pista segun los metadatos de FMA.",
            "genre_top": "Etiqueta de genero principal segun los metadatos de FMA.",
            "artist_name": "Nombre del artista segun los metadatos de FMA.",
        },
        "feature_families": {
            "chroma_cens": "Caracteristicas cromaticas de la representacion CENS.",
            "chroma_cqt": "Caracteristicas cromaticas de la transformada de Q constante.",
            "chroma_stft": "Caracteristicas cromaticas de la representacion STFT.",
            "mfcc": "Coeficientes cepstrales en frecuencias Mel.",
            "rmse": "Resumen de energia RMS.",
            "spectral_bandwidth": "Resumen del ancho de banda espectral.",
            "spectral_centroid": "Resumen del centroide espectral.",
            "spectral_contrast": "Resumenes por banda del contraste espectral.",
            "spectral_rolloff": "Resumen del rolloff espectral.",
            "tonnetz": "Caracteristicas de centroide tonal.",
            "zcr": "Resumen de la tasa de cruces por cero.",
        },
    },
    "pachamix_lyrics_long": {
        "grain_es": "una fila por (msd_track_id, token)",
        "description_es": "Conteos de tokens liricos en formato largo enriquecidos con metadatos de MSD cuando track_metadata.db esta disponible.",
        "columns": {
            "msd_track_id": "Identificador de pista de MSD; se une con songs.track_id.",
            "title": "Titulo de la pista segun los metadatos de MSD.",
            "song_id": "Identificador de cancion de MSD / Echo Nest.",
            "release": "Nombre del lanzamiento o album segun MSD.",
            "artist_id": "Identificador de artista de MSD / Echo Nest.",
            "artist_mbid": "Identificador de artista de MusicBrainz.",
            "artist_name": "Nombre del artista segun los metadatos de MSD.",
            "duration": "Duracion de la pista en segundos.",
            "artist_familiarity": "Puntaje de familiaridad del artista en Echo Nest.",
            "artist_hotttnesss": "Puntaje de hotttnesss del artista en Echo Nest.",
            "year": "Ano de lanzamiento; suele ser 0 cuando no esta disponible.",
            "track_7digitalid": "Identificador de pista de 7digital en MSD.",
            "shs_perf": "Identificador de interpretacion de SecondHandSongs o valor centinela.",
            "shs_work": "Identificador de obra de SecondHandSongs o valor centinela.",
            "token": "Token lirico del vocabulario oficial de musiXmatch/MSD.",
            "count": "Frecuencia del token para la pista.",
        },
    },
    "pachamix_playlist_events": {
        "grain_es": "una fila por (playlist_id, track_uri, position)",
        "description_es": "Tabla de pertenencia a playlists usada para filtrado colaborativo y construccion de grafos. Cuando la fuente no provee orden observado, la posicion se sintetiza de forma determinista por playlist y se marca con position_observed=false.",
        "columns": {
            "playlist_id": "Identificador nativo de la playlist segun la fuente; en Playlist2vec suele ser texto y en MPD suele ser entero.",
            "playlist_name": "Nombre de la playlist.",
            "track_uri": "Identificador canonico de la pista segun la fuente de playlists.",
            "track_name": "Titulo de la pista segun la fuente de playlists.",
            "artist_name": "Nombre del artista segun la fuente de playlists.",
            "album_name": "Nombre del album segun la fuente de playlists.",
            "position": "Orden de la pista dentro de la playlist.",
            "position_observed": "Indica si la posicion proviene de la fuente original (true) o si fue sintetizada de forma determinista durante la ingesta (false).",
        },
    },
    "pachamix_playlist_stats": {
        "grain_es": "una fila por playlist",
        "description_es": "Tabla resumen al nivel de playlist.",
        "columns": {
            "playlist_id": "Identificador nativo de la playlist segun la fuente; en Playlist2vec suele ser texto y en MPD suele ser entero.",
            "playlist_name": "Nombre de la playlist.",
            "track_count": "Numero de pistas en la playlist.",
        },
    },
    "pachamix_track_popularity": {
        "grain_es": "una fila por track_uri",
        "description_es": "Resumen de popularidad de pistas basado en el numero de playlists distintas donde aparecen.",
        "columns": {
            "track_uri": "Identificador de pista segun la fuente de playlists.",
            "playlist_count": "Numero de playlists distintas que contienen la pista.",
        },
    },
    "pachamix_song_graph_edges": {
        "grain_es": "una fila por par no dirigido de canciones",
        "description_es": "Aristas ponderadas de coocurrencia entre canciones para analitica de grafos y PageRank.",
        "columns": {
            "src_track_uri": "Primera cancion del par de coocurrencia.",
            "dst_track_uri": "Segunda cancion del par de coocurrencia.",
            "weight": "Numero de playlists donde el par coocurre.",
        },
    },
}


def _validate_language(language: Language) -> None:
    if language not in {"en", "es", "bilingual"}:
        raise ValueError(f"unsupported language: {language}")


def _label(key: str, language: Language) -> str:
    if language == "en":
        return LABELS[key]["en"]
    if language == "es":
        return LABELS[key]["es"]
    return f"{LABELS[key]['en']} / {LABELS[key]['es']}"


def _value(english: str, spanish: str, language: Language) -> str:
    if language == "en":
        return english
    if language == "es":
        return spanish
    return f"{english} / {spanish}"


def show_dataset_definition(name: str, language: Language = "bilingual") -> str:
    _validate_language(language)
    dataset = get_dataset_definition(name)
    translation = cast(dict[str, Any], TRANSLATIONS.get(name, {}))

    status_en = str(dataset["status"])
    status_es = STATUS_LABELS.get(status_en, {}).get("es", status_en)
    grain_en = str(dataset["grain"])
    grain_es = translation.get("grain_es", grain_en)
    description_en = str(dataset["description"])
    description_es = translation.get("description_es", description_en)

    lines = [
        f"{_label('dataset', language)}: {dataset['name']}",
        f"{_label('path', language)}: {dataset['path']}",
        f"{_label('asset_name', language)}: {dataset.get('asset_name', dataset['path'].split('/')[-1])}",
        f"{_label('status', language)}: {_value(status_en, status_es, language)}",
        f"{_label('grain', language)}: {_value(grain_en, grain_es, language)}",
        f"{_label('description', language)}: {_value(description_en, description_es, language)}",
        f"{_label('source', language)}: {', '.join(dataset['source'])}",
        f"{_label('primary_key', language)}: {', '.join(dataset['primary_key'])}",
        f"{_label('columns', language)}:",
    ]

    column_translations = cast(dict[str, str], translation.get("columns", {}))
    for column in dataset["columns"]:
        description_en = str(column["description"])
        description_es = column_translations.get(column["name"], description_en)
        lines.append(
            f"- {column['name']} ({column['dtype']}): "
            f"{_value(description_en, description_es, language)}"
        )

    feature_families = dataset.get("feature_families", [])
    if feature_families:
        lines.append(f"{_label('feature_families', language)}:")
        family_translations = cast(
            dict[str, str], translation.get("feature_families", {})
        )
        for family in feature_families:
            description_en = str(family["description"])
            description_es = family_translations.get(family["family"], description_en)
            family_shape_en = (
                f"{family['column_count']} columns, "
                f"{family['components']} components, "
                f"stats={', '.join(family['stats'])}"
            )
            family_shape_es = (
                f"{family['column_count']} columnas, "
                f"{family['components']} componentes, "
                f"estadisticas={', '.join(family['stats'])}"
            )
            lines.append(
                f"- {family['family']}: "
                f"{_value(family_shape_en, family_shape_es, language)}; "
                f"{_value(description_en, description_es, language)}"
            )

    return "\n".join(lines)


def show_data_dictionary(language: Language = "bilingual") -> str:
    _validate_language(language)
    sections = [
        show_dataset_definition(name, language=language) for name in list_datasets()
    ]
    separator = "\n\n" + ("=" * 80) + "\n\n"
    return separator.join(sections)
