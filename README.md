# Comparing FracMinHash, Mash, and SIMKA

This repository compares the following tools:

1. FracMinHash based tool
1. All k-mer based tool (SIMKA)
1. MinHash based tool (Mash)

## What we want to show

Hopefully, after running the experiments, we will observe the following:

1. FMH should be more accurate than Mash
1. FMH should be less resource intensive than SIMKA

Thus, with evidence of both of these results, we can argue that FMH should be a good balance in resources and accuracy, bringing together the good of both worlds.

## Datasets

Currently we plan to compare the tools using the following dataset:

1. One metagenomic dataset: HMP data
1. One genomic dataset (not yet decided what this should be)
1. One TODO dataset (not yet decided what this should be)

### TODO

1. Download the dataset
1. Write wrapper tools for all of these
1. Run all tools to record results and resource usages
1. Plot results


### Requirements
1. FracKmcSketch -- needs to be in path