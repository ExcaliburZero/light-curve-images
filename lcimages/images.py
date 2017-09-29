from scipy.misc import toimage

import numpy as np

def bin_lc(times, magnitudes):
    deltas = get_deltas(times, magnitudes)

    time_bins = np.array([0.0, 1 / 145.0, 2 / 145.0, 3 / 145.0, 4 / 145.0,
        1 / 25.0, 2 / 25.0, 3 / 25.0, 1.5, 2.5, 3.5, 4.5, 5.5, 7.0, 10.0, 20.0,
        30.0, 60.0, 90.0, 120.0, 240.0, 600.0, 960.0, 2000.0, 4000.0])
    mag_bins = np.array([0.0, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 8.0])
    mag_bins = np.concatenate((mag_bins[1:] * -1, mag_bins))

    time_bins = np.sort(time_bins)[::-1]
    mag_bins = np.sort(mag_bins)[::-1]

    def count_bin(i, j):
        return np.sum(
            (deltas[:,0] < time_bins[i]) * \
            (deltas[:,0] >= time_bins[i + 1]) * \
            (deltas[:,1] < mag_bins[j]) * \
            (deltas[:,1] >= mag_bins[j + 1])
        )

    bins = np.array([[count_bin(j, i) for j in range(len(time_bins) - 1)] for i in range(len(mag_bins) - 1)])

    return bins / np.sum(bins)

def get_deltas(times, magnitudes):
    delta_times = times[1:] - times[:-1]
    delta_mags = magnitudes[1:] - magnitudes[:-1]

    deltas = np.column_stack((delta_times, delta_mags))

    return deltas

def bins_to_image(bins):
    bins_2d = bins.reshape(22, 24)

    return toimage(bins_2d)
