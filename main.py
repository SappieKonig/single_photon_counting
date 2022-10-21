# import libraries to read .nc files
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# read .nc file
fp = "photon_counting_data/20221018_1b_eps_6.nc"
# fp = "photon_counting_data/20220928_1a_eps_0_1.nc"
# fp = "photon_counting_data/20220929_1a_eps_0_02.nc"
dataset = nc.Dataset(fp)

# select 2 microsecond scale
for key, var in dataset.variables.items():
    try:
        if var.units == "2 [us]":
            datapoints = var[:]
    except AttributeError:
        pass

# get data with zeroes for masked values
data = np.ma.filled(datapoints, 0)[0]
# remove leading zeroes
max = np.argmax(data)
data = data[max:]
# ignore first 10 data points, as they are not representative
data = data / np.max(data)

# fit negative exponential to data, to get half-life
def func(x, a, b):
    return np.exp(-a * (x - b))

popt, pcov = curve_fit(func, np.arange(len(data)), data, p0=(1, 1))
print("Half-life: ", np.log(2) / popt[0] * 2, "us")

# plot data and curve
plt.plot(np.arange(len(data)), data, "b-", label="data")
plt.plot(np.arange(len(data)), func(np.arange(len(data)), *popt), "r-", label="fit")
plt.xlabel("Time [2 us]")
plt.ylabel("Normalized counts")
plt.legend()
plt.show()
