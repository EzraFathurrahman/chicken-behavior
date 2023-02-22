import matplotlib.pyplot as plt
import pandas as pd
import csv
from mpl_toolkits import mplot3d
import numpy as np

def sort(file_path):
    colnames = ["time", "runtime", "Object_ID", "Frame", "cX", "cY"]
    data = pd.read_csv(file_path, names = colnames)
    data.columns = colnames

    runtime = data["runtime"].tolist()
    frame = [0]
    count = 0
    for i in range(len(data) - 1):
        t0 = runtime[i]
        t1 = runtime[i+1]

        if t0 == t1:
            pass
        elif t0 < t1:
            count += 1
        frame.append(count)

    count += 1

    data["Frame"] = frame
    #data.insert(3, "Frame", frame)
    data.sort_values(by = ["Object_ID", "Frame"], inplace=True)

    return data