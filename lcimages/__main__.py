import numpy as np
import os.path
import pandas as pd
import pickle
import sys

import images

CATEGORY = "Var_Type"
ID = "Numerical_ID"

def main():
    data_file = sys.argv[1]
    source_curves_dir = sys.argv[2]
    target_curves_dir = sys.argv[3]
    bins_file = sys.argv[4]

    data = pd.read_csv(data_file)

    ids = data[ID]

    def process_curve(i):
        curve_file = source_curves_dir + "/" + str(i) + ".csv"

        if os.path.isfile(curve_file):
            curve = pd.read_csv(curve_file)
            curve = curve.sort_values(by="time")

            bins = images.bin_lc(
                np.array(curve["time"]),
                np.array(curve["mag"])
            )

            img = images.bins_to_image(bins)
            img.save(target_curves_dir + "/" + str(i) + ".png", "PNG")

            return bins

    bin_sets = [process_curve(i) for i in ids]

    with open(bins_file, "wb") as f:
        pickle.dump(bin_sets, f)

if __name__ == "__main__":
    main()
