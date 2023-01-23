import pandas as pd

def max_min_runtime(file_path):
    hasil = pd.DataFrame()
    data = pd.read_csv(file_path, header = 0)

    ID = data["Object_ID"]
    #cari nilai runtime maksimum masing-masing objek
    last_occ = data.groupby("Object_ID")["runtime"].transform('max')
    #cari nilai runtime minimum masing-masing objek
    first_occ = data.groupby("Object_ID")["runtime"].transform('min')

    hasil["ID"] = ID
    hasil["last_occurence"] = last_occ
    hasil["first_occurence"] = first_occ
    hasil["period_detected"] = last_occ-first_occ

    bersih = hasil.drop_duplicates()

    bersih.to_csv("D:/Read Paper/Program/chicken_behaviour/results/max_min_runtime.csv", index = False)

