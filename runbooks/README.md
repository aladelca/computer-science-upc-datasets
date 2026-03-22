# UPC Datasets Runbooks

This folder contains the operational runbooks for the local `upc_datasets` toolkit.

Use these in order:

1. [01-setup.md](./01-setup.md)
   Environment setup and dependency installation
2. [02-run-sample-data.md](./02-run-sample-data.md)
   Fast local verification using the included fixtures
3. [03-build-course-datasets.md](./03-build-course-datasets.md)
   How to run the toolkit on real course datasets
4. [04-test-and-verify.md](./04-test-and-verify.md)
   How to validate the toolkit and outputs
5. [05-troubleshooting.md](./05-troubleshooting.md)
   Common issues and how to resolve them
6. [06-playlist2vec-prep.md](./06-playlist2vec-prep.md)
   How to prepare Playlist2vec exports for the one-command course build
7. [07-package-and-publish.md](./07-package-and-publish.md)
   How to build and publish the `upc-datasets` Python package
8. [08-how-the-package-works.md](./08-how-the-package-works.md)
   How the package is structured, how dataset resolution works, and how publication channels are split

The toolkit is intentionally focused on:

- structured metadata
- audio-feature tables
- lyrics token/count data
- playlist event tables
- graph edge tables

It intentionally does **not** process:

- mp3 files
- waveform data
- spectrograms
- raw audio extraction pipelines
