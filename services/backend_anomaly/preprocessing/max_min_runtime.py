import pandas as pd

def max_min_runtime(file_path):
    hasil = pd.DataFrame()
    data = file_path

    ID = data["Object_ID"]
    last_occ = data.groupby("Object_ID")["runtime"].transform('max')
    first_occ = data.groupby("Object_ID")["runtime"].transform('min')

    hasil["ID"] = ID
    hasil["last_occurrence"] = last_occ
    hasil["first_occurrence"] = first_occ
    hasil["period_detected"] = last_occ-first_occ

    result = hasil.drop_duplicates()

    return result

