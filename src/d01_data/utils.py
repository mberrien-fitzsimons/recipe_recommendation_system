import pandas as pd
import numpy as np
import glob
import functools

def read_multiple_csv_and_concat(file_location_pattern_and_name_pattern):

    """
    EXAMPLE: file_location_pattern_and_name_pattern = '../../data/01_raw/Kickstarter_201*/Kickstarter*'
    """

    files = glob.glob(file_location_pattern_and_name_pattern)

    li = []
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    return frame
    # frame.to_csv(file_save_path+new_file_name, index=False)
