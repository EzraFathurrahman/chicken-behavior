import pandas as pd
from sklearn.ensemble import IsolationForest

def isolation_forest(file_path):
    data = file_path

    model = IsolationForest(n_estimators = 100, max_samples = 'auto', contamination = float(0.1))
    model.fit(data['period_detected'].values.reshape(-1, 1))
    
    data['scores'] = model.decision_function(data['period_detected'].values.reshape(-1, 1))
    data['anomaly_score'] = model.predict(data['period_detected'].values.reshape(-1, 1))
    
    return data