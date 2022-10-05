import os
import sys
from math import log
from glob import glob
from collections import Counter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.coordinates import SkyCoord

sourcefiles = glob("GaiaSource_*")

recreate = False
extend = True
# TODO GAIA is epoch 2015!
if not os.path.exists("sourcemeta.json") or recreate or extend:
	print("Creating sourcemeta.json")
	sourcemeta = {}

	if extend and os.path.exists("sourcemeta.json"):
		with open("sourcemeta.json") as f:
			sourcemeta = json.loads(f.read())		

	try:
		for filepath in sourcefiles:#[:10]
			if filepath in sourcemeta and not recreate:
				continue

			try:
				df = pd.read_csv(filepath)
			except Exception as e:
				print(filepath, e)
				continue

			# TODO make relative
			sourcemeta[filepath] = {
				"ra_min": df["ra"].min(),
				"ra_max": df["ra"].max(),
				"dec_min": df["dec"].min(),
				"dec_max": df["dec"].max()
			}
			print(filepath, sourcemeta[filepath])
	except KeyboardInterrupt:
		pass

	with open("sourcemeta.json", "w+") as f:
		f.write(json.dumps(sourcemeta, indent=4))
else:
	print("Reading sourcemeta.json")
	with open("sourcemeta.json") as f:
		sourcemeta = json.loads(f.read())

min_ra = 0#5*360/24#hours
max_ra = 40#7*360/24

min_dec = -80
max_dec = -60

fov_ra = 360/24/60
fov_dec = 1

fov_div = 1

df = pd.read_csv(sourcefiles[0])
print(df)

regions = []
#print("sourcemeta", sourcemeta)
checked = 0
try:
	for filepath in sourcefiles:#[:10]
		if filepath in sourcemeta:
			meta = sourcemeta[filepath]
			if meta["ra_min"] > max_ra or meta["ra_max"] < min_ra or meta["dec_min"] > max_dec or meta["dec_max"] < min_dec:
				continue
		else:
			print(filepath, "not in sourcemeta")
		print(filepath)
		try:
			df = pd.read_csv(filepath)
		except Exception as e:
			print(e)
			continue
		checked += 1
		region = df.loc[(df["ra"] >= min_ra) & (df["ra"] <= max_ra) & (df["dec"] >= min_dec) & (df["dec"] <= max_dec)]
		region = region[["ra", "dec", "phot_g_mean_flux"]]
		print(region)
		if len(region) > 0:
			regions.append(region)
		print(len(regions))
except KeyboardInterrupt:
	pass

print(checked, "files checked")
print(len(regions), "files matched")


if len(regions) == 0:
	exit(0)

df = pd.concat(regions)

print("dataframe size:", sys.getsizeof(df))

print("stars:", len(df))



cnt = Counter()

rarange = list(np.arange(min_ra, max_ra, fov_ra/fov_div))
decrange = np.arange(min_dec, max_dec, fov_dec/fov_div)
print(len(rarange), len(decrange), len(rarange)*len(decrange))

img = []
for x, ra in enumerate(rarange):
	print(ra)
	img.append([])
	for y, dec in enumerate(decrange):
		rectsum = df.loc[(df["ra"] >= ra) & (df["ra"] <= ra+fov_ra) & (df["dec"] >= dec) & (df["dec"] <= dec+fov_dec)]["phot_g_mean_flux"].sum()
		cnt[(ra,dec)] = rectsum
		img[-1].append(rectsum)

print(len(cnt), "subfields")

mostcommon = list([(k,v) for k,v in cnt.most_common()])# if v!=0

for key, value in mostcommon[:10] + mostcommon[-20:]:
	c = SkyCoord(ra=key[0]*u.degree, dec=key[1]*u.degree)
	print(c.to_string("hmsdms"), str(int(round(value))).rjust(12))

fig, axes = plt.subplots(1, 2)

axes[0].imshow(img)
axes[1].hist([log(1+v) for v in cnt.values()])

plt.show()
