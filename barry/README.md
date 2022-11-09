I ran the following queries on https://gea.esac.esa.int/archive/ and uploading the results in both ESA's native .vot.gz format (which includes the query) and compressed CSV format (which is easier to handle)

I've created this separate subdirectory so void4 can decide how to handle these files.

1667986137685O: Ran query "SELECT FLOOR(ra*6) AS ra, FLOOR(dec*6) AS dec, SUM(POWER(100, 2-phot_g_mean_mag/5)) AS brightness FROM gaiadr3.gaia_source_lite GROUP BY 1, 2 ORDER BY brightness DESC" to find the brightest region of the sky down to 1/6th degree increments. There are 360*6*180*6 or 2,332,800 regions of the sky with 1/6th degree increments, but there are actually 2,327,256 results because the other 5,544 1/6th degree regions of the sky contain no stars in GAIA3. Note that these regions are very close to the poles and thus very small, so it's not surprising they contain no stars in GAIA3.

1667988501590O: Ran query "SELECT FLOOR(ra*6) AS ra, FLOOR(dec*6) AS dec, COUNT(*) FROM gaiadr3.gaia_source_lite GROUP BY 1, 2" to count the number of stars in each 1/6th degree region of the sky as a sanity check to finding the darkest regions.

An attempt to run a query with 1/10th degree "squares" returned 3,000,000 rows but the results appear to have hit a row limit and thus are unlikely to be accurate and are thus not included here.

Note that running this query:

SELECT * FROM gaiadr3.gaia_source_lite WHERE ra >= 246.66666666 and ra <= 246.833333333 AND dec >= -24.66666666666 AND dec <= -24.5

yields only 5 stars of magnitudes 19 and 20, a potential candidate for darkest region, even though it's in Scorpio and surrounded by significantly brighter regions
