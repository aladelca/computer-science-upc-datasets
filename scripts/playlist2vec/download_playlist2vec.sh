#!/usr/bin/env bash

set -euo pipefail

DEST_DIR="${1:-data/external/playlist2vec}"
SCHEMA_URL="https://zenodo.org/records/5002584/files/spotifydbdumpschemashare.sql?download=1"
DUMP_URL="https://zenodo.org/records/5002584/files/spotifydbdumpshare.sql?download=1"

mkdir -p "${DEST_DIR}"

echo "Downloading Playlist2vec schema to ${DEST_DIR}/spotifydbdumpschemashare.sql"
curl -L "${SCHEMA_URL}" -o "${DEST_DIR}/spotifydbdumpschemashare.sql"

echo "Downloading Playlist2vec dump to ${DEST_DIR}/spotifydbdumpshare.sql"
curl -L "${DUMP_URL}" -o "${DEST_DIR}/spotifydbdumpshare.sql"

echo "Download complete."
echo "Files:"
echo "- ${DEST_DIR}/spotifydbdumpschemashare.sql"
echo "- ${DEST_DIR}/spotifydbdumpshare.sql"
