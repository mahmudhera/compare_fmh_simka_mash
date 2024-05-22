"""
In this script, we investigate why using abundances, we get a mismatch between
sourmash sketch and fracKmcSketch.
"""

import json

sketch_name_frackmcsketch = 'test'
sketch_name_sourmash = 'test2'

# these two sketches are json files
frackmc_data = json.load(open(sketch_name_frackmcsketch, 'r'))
sourmash_data = json.load(open(sketch_name_sourmash, 'r'))

# get the min hashes
frackmc_mins = frackmc_data[0]['signatures'][0]['mins']
sourmash_mins = sourmash_data[0]['signatures'][0]['mins']

# assert that the counts are the same
assert len(frackmc_mins) == len(sourmash_mins)

# assert that the min hashes are the same
assert set(frackmc_mins) == set(sourmash_mins)

# obviously, there is a mismatch in the abundances
# let us now investigate the abundances

frackmc_abundances = frackmc_data[0]['signatures'][0]['abundances']
sourmash_abundances = sourmash_data[0]['signatures'][0]['abundances']

# create dictionary keyed by min hashes and values are the abundances
frackmc_abundance_dict = dict(zip(frackmc_mins, frackmc_abundances))
sourmash_abundance_dict = dict(zip(sourmash_mins, sourmash_abundances))

# show the min hashes whose abundances are not the same
for min_hash in frackmc_mins:
    if frackmc_abundance_dict[min_hash] != sourmash_abundance_dict[min_hash]:
        print(min_hash, frackmc_abundance_dict[min_hash], sourmash_abundance_dict[min_hash])

# after investigating manually, it is obvious that the counts are not correct in fracKmcSketch when
# the value is > 255