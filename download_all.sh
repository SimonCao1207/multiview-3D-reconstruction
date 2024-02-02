#!/usr/bin/env bash

# Check if the DATASET_ROOT argument is provided
: ${1?"Usage: $0 DATASET_ROOT"}

# Assign the provided argument to dataset_root variable
dataset_root=$1

# Create dataset root directory if it doesn't exist
mkdir -p ${dataset_root}
cd ${dataset_root}

wget https://phototour.cs.washington.edu/datasets/NotreDame.zip
unzip NotreDame.zip && rm NotreDame.zip
