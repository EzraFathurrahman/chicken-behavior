import pandas as pd
from sklearn.ensemble import IsolationForest

<<<<<<< HEAD
def isolation_forest(file_path):
    data = file_path

    model = IsolationForest(n_estimators = 100, max_samples = 'auto', contamination = float(0.1))
    model.fit(data['period_detected'].values.reshape(-1, 1))
    
    data['scores'] = model.decision_function(data['period_detected'].values.reshape(-1, 1))
    data['anomaly_score'] = model.predict(data['period_detected'].values.reshape(-1, 1))
    
    return data
=======
class IForest:
    def __init__(self):
        self.model = IsolationForest(n_estimators = 100, max_samples = 'auto', contamination = float(0.1))

    def find_max_min_runtime(self, file_path):
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

    def detect_anomaly(self, file_path):
        data = file_path

        self.model.fit(data['period_detected'].values.reshape(-1, 1))
        
        data['scores'] = self.model.decision_function(data['period_detected'].values.reshape(-1, 1))
        data['anomaly_score'] = self.model.predict(data['period_detected'].values.reshape(-1, 1))
        data['anomaly_score'] = data['anomaly_score'].apply(lambda x : 'Anomaly' if x == -1 else 'Normal')
        
        return data
>>>>>>> a8fe885d4563f15b993d8dfc3e2937954829c7e5
