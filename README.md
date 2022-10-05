# lowestflux

to find the darkest regions in the night sky

## Getting the code

`git clone https://github.com/void4/lowestflux.git`

## Install code requirements

`python -m pip install -r requirements.txt`

## Data dependencies

In this case I used Gaia Data Release 1 (DR1), because even though DR2 and (E)DR3 are more complete, they require more than a terabyte of data, too much for me to download, store and process.

## Downloading the data

The DR1 files are around 200 Gigabytes, so may take a while

### On Windows

Download VisualWget:

https://sites.google.com/site/visualwget/a-download-manager-gui-based-on-wget-for-windows

and set this as the source URL:

http://cdn.gea.esac.esa.int/Gaia/gdr1/gaia_source/csv/

then enable the Advanced->Recursive Retrieval->--recursive and Advanced->Recursive Accept/Reject->--no-parent flag

as visually documented here: https://stackoverflow.com/questions/23446635/how-to-download-http-directory-with-all-files-and-sub-directories-as-they-appear/24247715#24247715

## On Linux

should be (not tested)

`wget --recursive --no-parent --no-host-directories http://cdn.gea.esac.esa.int/Gaia/gdr1/gaia_source/csv/`

## Put the data in the right place

Then copy the downloaded GaiaSource_000-xxx-yyy.csv.gz files into this repository folder, so they are at the same level as the main.py file.

## Usage

`python main.py`

This first generates an index ("sourcemeta.json") of the minimum and maximum right ascension and declination values, so that when a region (given by min/max ra/dec itself) is queried, it only loads a subset of the files (going through *all* files every time, filtering for stars of that region would take too long).

Given that the DR1 data is not expected to change, and so you do not have to generate it yourself, I have included my generated sourcemeta.json in this repository. If you do want to recreate it yourself, set recreate = True on the first run only.

Once it has loaded or generated/extended that file, it opens the files (possibly) containing stars in that queried region, and filters them down to the ones that are definitely contained within it, generating:

- a plot of subregion brightness in that region (where subregion granularity is given by a field of view size (fov_ra, fov_dec, and the fov_? divisor achieve a more fine grained sliding window)
- a histogram/distribution of subregion brightness
- a list of the n brightest and n darkest subregions (hmsdms + sum of mean flux)
