# import libraries to read .nc files
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# read .nc file
fp = "photon_counting_data/20220928_1a_eps_0_02.nc"
dataset = nc.Dataset(fp)

# select 2 microsecond scale
for key, var in dataset.variables.items():
    try:
        if var.units == "2 [us]":
            datapoints = var[:]
    except AttributeError:
        pass

print(datapoints.shape)
