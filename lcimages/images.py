from PIL import Image

from scipy.misc import toimage

import colorsys
import numpy as np

def bin_lc(times, magnitudes):
    deltas = get_deltas(times, magnitudes)

    time_bins = np.array([1 / 145.0, 2 / 145.0, 3 / 145.0, 4 / 145.0, 1 / 25.0,
        2 / 25.0, 3 / 25.0, 1.5, 2.5, 3.5, 4.5, 5.5, 7.0, 10.0, 20.0, 30.0,
        60.0, 90.0, 120.0, 240.0, 600.0, 960.0, 2000.0, 4000.0])
    mag_bins = np.array([0.0, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 8.0])

    #def is_in_bin(i, j, x):
        #return x[0] >= time_bins[i] and x[0] < time_bins[i + 1] and x[1] >= mag_bins[j] and x[1] < mag_bins[j + 1]

        #t_lower = time_bins[i]
        #t_upper = time_bins[i + 1]
        #m_lower = mag_bins[j]
        #m_upper = mag_bins[j + 1]
        #return x[0] >= t_lower and x[0] < t_upper and x[1] >= m_lower and x[1] < m_upper

    def count_bin(i, j):
        #return np.sum([is_in_bin(i, j, x) for x in deltas])
        return np.sum(
            (deltas[:,0] >= time_bins[i]) * \
            (deltas[:,0] < time_bins[i + 1]) * \
            (deltas[:,1] >= mag_bins[j]) * \
            (deltas[:,1] < mag_bins[j + 1])
        )

        #in_bin = lambda x: is_in_bin(time_bins[i], time_bins[i + 1], mag_bins[j], mag_bins[j + 1], x)
        #bin_elements = [is_in_bin(i, j, x) for x in deltas]
        #bin_count = np.sum(bin_elements)

        #return bin_count

    bins = [[count_bin(i, j) for j in range(len(mag_bins) - 1)] for i in range(len(time_bins) - 1)]

    return np.array(bins)

def get_deltas(times, magnitudes):
    delta_times = times[1:] - times[:-1]
    delta_mags = magnitudes[1:] - magnitudes[:-1]

    deltas = np.column_stack((delta_times, delta_mags))

    return deltas

def get_color(value):
    h, s, v = (value * 360.0, value, value)
    r, g, b = tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    return [r, g, b]

def bins_to_image(bins):
    #bins_2d = bins[0:252].reshape(21, 12) # drop last bin (?)
    bins_2d = bins.reshape(23, 11) # drop last bin (?)

    #bins_2d = np.vstack((bins_2d[::-1], bins_2d))
    #bins_2d = np.fliplr(bins_2d)

    bins_2d = (bins_2d / np.max(bins_2d))
    bins_2d = np.array([[get_color(x) for x in row] for row in bins_2d])
    #img = Image.fromarray(formatted)
    img = toimage(bins_2d)
    #img.putpalette(Image.ADAPTIVE)
    #img.putpalette([0, 0, 0, # black background
    #  255, 0, 0, # index 1 is red
    #  255, 255, 0, # index 2 is yellow
    #  255, 153, 0, # index 3 is orange
    #  ])
    img = img.convert("P", palette = Image.ADAPTIVE, colors = 16)
    #img = img.resize((11 * 2 * 16, 23 * 16))

    #img = img.resize((23 * 64, 11 * 2 * 64))
    #img.save("image.png", "PNG")

    return img
