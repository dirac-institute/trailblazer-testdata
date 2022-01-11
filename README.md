# trailblazer-testdata

``trailblazer-testdata`` provides a sample input and output data sufficient to test the functionality of ``trailblazer``.

This repository provides the configuration files required by ``trailblazer`` to use the data.

Thumbnails displayed in the ``trailblazer`` gallery can be found in the ``media/`` directory. 
The data that was used to produce the thumbnails is located in the ``static/upload/fits`` directory. The collection of FITS files that can be found there have been resized in order to keep the total size of this repository reasonable, while being sufficient in their role as placeholder files for download or any other ``trailblazer`` functionality that depends on their existence. The raw, original, unresized data is provided in the same directory as a ``.tar.bz2`` archive. If untampered data is required for a particular purpose, extract the archive in the same directory.

A database, also required for ``trailblazer`` to work correctly, is provided in the root directory of the repository as ``db.sqlite3``. 

There are no guarantees the current iteration of the thumbnails, test data or the database matches the exact state of the [trailblazer](https://github.com/dirac-institute/trailblazer) repository main branch, even though we are trying to be as up to date as possible. Open an Issue here or in the [trailblazer](https://github.com/dirac-institute/trailblazer) repository if the current version is too far out of sync with the main repo.

## Obtaining the test data

The data is stored using [Git LFS](https://git-lfs.github.com/).

## Using the test data

Set the env variable `TRAILBLAZER_CONFIG_DIR` to point to the `config` directory of this package. 

```export TRAILBLAZER_CONFIG_DIR=<local_path>/trailblazer-testdata/config/```
