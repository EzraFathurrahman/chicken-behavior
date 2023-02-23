import pandas as pd

def split_object_id(file_path):
    df = file_path

    columns = df.columns.values.tolist()
    columns_list = list(columns)

    indx_val = columns_list.index("Object_ID")
    column_to_split = columns[indx_val]
    unique_values = df[column_to_split].unique()

    labels = []
    df_by_object = []

    for label in unique_values:
        df_label = df[df[column_to_split] == label]
        df_label = df_label.iloc[:, 3:]
        labels.append(label)
        df_by_object.append(df_label)
    
    return labels, df_by_object