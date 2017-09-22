import numpy as np
import os.path
import pandas as pd
import sys

import images

CATEGORY = "Var_Type"
ID = "Numerical_ID"

def main():
    data_file = sys.argv[1]
    source_curves_dir = sys.argv[2]
    target_curves_dir = sys.argv[3]

    data = pd.read_csv(data_file)

    ids = data[ID]

    for i in ids:
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

if __name__ == "__main__":
    main()
