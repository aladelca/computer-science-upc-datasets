# Playlist2vec Acquisition and Ingestion Workflow

## Goal

- Dejar implementado y documentado un flujo completo, reproducible y verificable para:
  - descargar `Playlist2vec` desde la fuente oficial
  - importar el SQL dump en MySQL o MariaDB
  - exportar los CSV que el repo necesita bajo `data/raw/playlist2vec/`
  - ejecutar el build del curso para generar `playlist_events`, `playlist_stats`, `track_popularity` y `song_graph_edges`
  - reconciliar la discrepancia entre el esquema oficial de `Playlist2vec` y la expectativa actual del repo sobre `position`
- Mantener la narrativa del curso en `music / Spotify recommendation` para Weeks `9-12`.

## Request Snapshot

- User request: "crea todo el proceso para hacer esto, haz un plan detallado"
- Owner or issue: `None`
- Plan file: `plans/20260321-1722-playlist2vec-acquisition-and-ingestion.md`

## Current State

- El repo ya soporta `Playlist2vec` como fuente de comportamiento en:
  - `src/pachamix_data/builders/playlist_events.py`
  - `src/pachamix_data/pipeline.py`
  - `src/upc_datasets/catalog.py`
- El flujo documentado actual está en:
  - `runbooks/06-playlist2vec-prep.md`
  - `runbooks/03-build-course-datasets.md`
  - `README.md`
- El builder de `Playlist2vec` actualmente:
  - lee `playlist.csv`, `track.csv`, `track_playlist1.csv`
  - tolera ausencia de `position` en `track_playlist1.csv`
  - si no existe `position`, crea una con `with_row_index(name="position")`
- La documentación local todavía exige `position` como columna mínima en `track_playlist1.csv`.
- El esquema oficial de Zenodo para `Playlist2vec` describe `track_playlist1` solo con:
  - `track_id`
  - `playlist_id`
- No existe hoy en el repo:
  - script de descarga
  - script SQL de exportación para producir los CSV esperados
  - explicitación contractual de qué significa `position` cuando el origen es `Playlist2vec`
  - configuración de `ruff`
  - configuración de `mypy`

## Findings

- La fuente oficial confirmada es `Zenodo record 5002584`, con:
  - `spotifydbdumpschemashare.sql`
  - `spotifydbdumpshare.sql`
  - tamaño aproximado de descarga: `10.7 GB`
  - tamaño de base poblada: `~35 GB`
- El esquema oficial publicado en Zenodo dice que `track_playlist1` contiene solo `track_id` y `playlist_id`, sin `position`.
- `runbooks/06-playlist2vec-prep.md` y la expectativa mínima actual del repo están desalineadas con la fuente oficial, porque exigen `position`.
- El builder actual no falla si `position` falta, pero la posición sintética creada con `with_row_index()`:
  - no representa orden real dentro de cada playlist
  - puede inducir un uso incorrecto en labs que asumen secuencia real o holdout de “últimos k tracks”
- `tests/test_playlist2vec_builder.py` y `tests/fixtures/playlist2vec/track_playlist1.csv` hoy solo cubren el caso con `position` presente.
- `pyproject.toml` no tiene secciones `[tool.ruff]` ni `[tool.mypy]`, y el `optional-dependencies.dev` solo incluye `pytest`.
- El runner real del proyecto hoy es `.venv/bin/python` y `.venv/bin/pytest`, según `Makefile`, `README.md` y `runbooks/04-test-and-verify.md`.

## Scope

### In scope

- Actualizar el flujo técnico y documental para obtener `Playlist2vec` desde Zenodo.
- Definir exportaciones SQL exactas para producir:
  - `playlist.csv`
  - `track.csv`
  - `track_playlist1.csv`
- Ajustar el builder y/o el contrato del dataset para soportar oficialmente `Playlist2vec` sin `position` observada.
- Hacer explícita la semántica de `position` cuando la fuente no la provee.
- Cubrir con tests:
  - export layout esperado
  - ausencia de `position`
  - build end-to-end con `Playlist2vec`
- Actualizar README, runbooks y material de datos para que el proceso sea ejecutable sin ambigüedades.
- Introducir configuración mínima de `ruff` y `mypy` aplicable a este cambio en Python.

### Out of scope

- Descargar y versionar en Git el SQL dump real de `Playlist2vec`.
- Subir a release assets del repo los parquets derivados.
- Resolver matching completo entre:
  - `Playlist2vec`
  - `FMA`
  - `musiXmatch/MSD`
- Reescribir la segunda mitad del curso para depender de secuencia real cuando la fuente no la provee.
- Introducir Spark como camino principal de ejecución.

## File Plan

| Path | Action | Details |
| --- | --- | --- |
| `README.md` | modify | Alinear la sección de `Playlist2vec` con la fuente oficial, dejar claro que la fuente primaria es un SQL dump, documentar el flujo soportado y la semántica de `position` faltante. |
| `runbooks/06-playlist2vec-prep.md` | modify | Convertirlo en runbook ejecutable con pasos exactos de descarga, importación SQL, exportación a CSV, staging y build. Corregir la expectativa mínima de columnas. |
| `runbooks/03-build-course-datasets.md` | modify | Ajustar la sección de `Playlist2vec` para que no asuma `position` observada y remita al contrato real del export. |
| `runbooks/05-troubleshooting.md` | modify | Agregar troubleshooting específico para: descarga incompleta, importación SQL fallida, columnas esperadas faltantes y `position` no observada. |
| `big_data_dataset_generation_plan.md` | modify | Aclarar que `Playlist2vec` sirve para recommendation y graph analytics, pero no debe presentarse como fuente secuencial real salvo adaptación explícita. |
| `data_dictionary.md` | modify | Documentar la procedencia de `position` en `playlist_events` cuando venga de `Playlist2vec` sin orden real. |
| `src/pachamix_data/builders/playlist_events.py` | modify | Formalizar el soporte a `Playlist2vec` sin `position`, evitar ambigüedad contractual y producir una representación estable y explícitamente etiquetada. |
| `src/upc_datasets/catalog.py` | modify | Ajustar descripciones del dataset de playlists si cambia el contrato o si se agrega una columna indicadora de posición observada/sintética. |
| `src/upc_datasets/presentation.py` | modify | Mantener sincronizado el texto del data dictionary si cambia el contrato de `playlist_events`. |
| `tests/test_playlist2vec_builder.py` | modify | Cubrir el caso oficial sin `position` y validar el comportamiento esperado del builder. |
| `tests/test_course_dataset_pipeline_playlist2vec.py` | modify | Asegurar que el pipeline completo sigue funcionando con exportaciones alineadas al esquema oficial. |
| `tests/fixtures/playlist2vec/track_playlist1.csv` | keep or modify | Evaluar si se conserva como fixture “con posición” para compatibilidad o se reemplaza por un fixture más fiel al oficial. |
| `tests/fixtures/course_raw_playlist2vec/playlist2vec/track_playlist1.csv` | keep or modify | Igual que arriba, según la estrategia de fixtures. |
| `tests/fixtures/playlist2vec_no_position/track_playlist1.csv` | create | Nuevo fixture alineado al esquema oficial sin `position`. |
| `tests/fixtures/course_raw_playlist2vec_no_position/...` | create | Nuevo set end-to-end para probar el flujo completo con exportaciones fieles a Zenodo. |
| `scripts/playlist2vec/download_playlist2vec.sh` | create | Helper script para descargar `spotifydbdumpschemashare.sql` y `spotifydbdumpshare.sql` desde Zenodo con `curl -L`, validando nombres y rutas destino. |
| `scripts/playlist2vec/export_playlist.sql` | create | SQL de export para `playlist.csv` con aliases acordes al repo. |
| `scripts/playlist2vec/export_track.sql` | create | SQL de export para `track.csv`, resolviendo `track_name`, `artist_name`, `album_name` desde `track`, `track_artist1`, `artist`, `album`. |
| `scripts/playlist2vec/export_track_playlist1.sql` | create | SQL de export para `track_playlist1.csv`, sin asumir `position` si el origen no la tiene. |
| `scripts/playlist2vec/README.md` | create | Instrucciones breves para ejecutar los scripts SQL en MySQL/MariaDB o desde un cliente. |
| `pyproject.toml` | modify | Agregar configuración mínima de `ruff` y `mypy`, y dependencias de desarrollo necesarias para ejecutarlos desde `.venv`. |

## Data and Contract Changes

- `Playlist2vec` oficial no provee `position` observada en `track_playlist1`.
- El contrato actual del repo para `playlist_events` necesita una decisión explícita. Recomendación:
  - mantener la columna `position` por compatibilidad de grain y orden estable
  - agregar una columna booleana como `position_observed` o `position_is_synthetic`
  - cuando `Playlist2vec` no provea orden, generar `position` solo como orden técnico estable dentro de cada playlist, no como secuencia semántica
- Documentar que con `Playlist2vec`:
  - collaborative filtering, popularity, matrix factorization y song graph sí son válidos
  - playlist continuation secuencial basada en “últimos k tracks” no debe presentarse como señal real de orden
- Si se decide no agregar columna nueva, el plan debe al menos:
  - fijar una estrategia determinista por playlist
  - documentar que `position` no es observada
  - evitar que la documentación la venda como orden real

## Implementation Steps

1. Confirmar y fijar el contrato de ingestión de `Playlist2vec`.
   - Tomar como referencia el esquema oficial de Zenodo.
   - Decidir cómo se representará la ausencia de `position`.
   - Reconciliar builder, docs, data dictionary y tests con esa decisión.

2. Crear el toolkit operativo para adquisición y exportación.
   - Crear `scripts/playlist2vec/download_playlist2vec.sh`.
   - Crear `scripts/playlist2vec/export_playlist.sql`.
   - Crear `scripts/playlist2vec/export_track.sql`.
   - Crear `scripts/playlist2vec/export_track_playlist1.sql`.
   - Crear `scripts/playlist2vec/README.md` con ejemplos de ejecución.

3. Actualizar el builder de playlists.
   - Ajustar `src/pachamix_data/builders/playlist_events.py` para manejar formalmente el caso sin `position`.
   - Si se agrega `position_observed` o equivalente, propagar la columna al output.
   - Garantizar orden estable por `playlist_id` y criterio determinista cuando no haya secuencia observada.

4. Sincronizar los contratos públicos del dataset.
   - Actualizar `data_dictionary.md`.
   - Actualizar `src/upc_datasets/catalog.py`.
   - Actualizar `src/upc_datasets/presentation.py`.
   - Revisar que `README.md` y runbooks no contradigan la implementación.

5. Reescribir la documentación operacional.
   - En `runbooks/06-playlist2vec-prep.md`, dejar:
     - descarga exacta desde Zenodo
     - importación en MySQL/MariaDB
     - exportación con SQL
     - staging bajo `data/raw/playlist2vec/`
     - build del curso
     - verificación de outputs
   - En `runbooks/03-build-course-datasets.md`, dejar claro el flujo real.
   - En `runbooks/05-troubleshooting.md`, documentar fallas comunes del proceso.

6. Alinear fixtures y tests.
   - Crear fixtures fieles al esquema oficial sin `position`.
   - Mantener o ajustar fixtures con `position` explícita si se quiere conservar backward compatibility.
   - Actualizar tests unitarios e integrales para ambos caminos:
     - exportación con `position`
     - exportación sin `position`

7. Introducir validación estática mínima del repo para este cambio.
   - Agregar `ruff` y `mypy` al entorno de desarrollo.
   - Configurar reglas mínimas en `pyproject.toml`.
   - Dejar comandos claros en docs y plan para ejecutarlos desde `.venv`.

8. Validar end-to-end con sample data y, luego, con datos reales.
   - Ejecutar tests con fixtures.
   - Probar el flujo documental usando fixtures de `course_raw_playlist2vec`.
   - Cuando el usuario tenga el dump real, validar el flujo completo en `data/raw/playlist2vec`.

## Tests

- Unit: `tests/test_playlist2vec_builder.py` cubrir:
  - lectura de export oficial sin `position`
  - generación estable de `position` técnica o columna indicadora
  - join correcto con `playlist.csv` y `track.csv`
- Integration: `tests/test_course_dataset_pipeline_playlist2vec.py` validar:
  - preferencia por `playlist2vec/`
  - escritura de `playlist_events`, `playlist_stats`, `track_popularity`, `song_graph_edges`
  - contrato correcto del output cuando `position` es sintética
- Regression: `tests/test_playlist_builder.py` confirmar que el flujo MPD sigue intacto
- Regression: agregar o ajustar fixture con `position` presente para no romper el caso ya soportado
- Docs smoke check: ejecutar los comandos documentados contra fixtures y verificar que produzcan outputs válidos

## Validation

- Format: `.venv/bin/ruff format --check src tests scripts`
- Lint: `.venv/bin/ruff check src tests scripts`
- Types: `.venv/bin/mypy src`
- Tests:
  - `.venv/bin/pytest`
  - `.venv/bin/pytest tests/test_playlist2vec_builder.py`
  - `.venv/bin/pytest tests/test_course_dataset_pipeline_playlist2vec.py`
  - `.venv/bin/pytest tests/test_playlist_builder.py`

Si `ruff` y `mypy` todavía no están disponibles en `.venv`, el cambio debe incluir:

- dependencia de desarrollo en `pyproject.toml`
- configuración mínima en `pyproject.toml`
- actualización de la documentación para su uso

## Risks and Mitigations

- `Zenodo cambia URL o disponibilidad` -> usar DOI oficial y documentar fallback manual desde navegador.
- `MySQL/MariaDB import falla por espacio o timeout` -> documentar requerimientos mínimos de disco y usar runbook de troubleshooting.
- `Playlist2vec sin position rompe expectativas del curso` -> hacer explícito que el dataset soporta recommendation set-based y graph analytics, no secuencia real.
- `Se mantiene position sintética y alguien la usa como orden real` -> agregar columna indicadora y advertencias visibles en docs y data dictionary.
- `Export SQL produce duplicados por join track-artist` -> definir una estrategia explícita de selección de artista principal o agregación estable en `export_track.sql`.
- `Introducir ruff/mypy agrega fricción` -> usar configuración mínima y acotada al alcance del repo, no un set estricto arbitrario.

## Open Questions

- `position` debe modelarse como:
  - columna obligatoria técnica con orden sintético estable, o
  - columna nullable más una bandera de observación real.

Recomendación:

- mantener `position` por compatibilidad
- agregar `position_observed` o `position_is_synthetic`
- tratar `Playlist2vec` como no secuencial en docs y labs

## Acceptance Criteria

- Existe un proceso documentado, ejecutable y verificable para bajar `Playlist2vec`, importarlo y exportar los CSV que este repo consume.
- El repo deja de asumir falsamente que `Playlist2vec` provee `position`.
- El builder soporta oficialmente el esquema real de `Playlist2vec`.
- La documentación pública del repo queda alineada entre:
  - README
  - runbooks
  - data dictionary
  - catalog presentation
- Los tests cubren tanto el caso oficial sin `position` como el caso ya tolerado con `position`.
- El repo tiene una ruta clara para ejecutar `ruff`, `mypy` y `pytest` desde `.venv`.

## Definition of Done

- Scripts de descarga y exportación creados en `scripts/playlist2vec/`
- Builder de `Playlist2vec` actualizado y con contrato explícito
- README, runbooks y data dictionary actualizados
- Fixtures y tests actualizados o añadidos
- `ruff`, `mypy` y `pytest` configurados y documentados para el alcance del cambio
- Plan actualizado si cambia el alcance durante la implementación
