import pandas as pd
from sklearn.ensemble import IsolationForest

def isolation_forest(file_path):
    data = pd.read_csv(file_path)
    
    random_state = 42
    model = IsolationForest(n_estimators = 100, max_samples = 'auto', contamination = float(0.1), random_state = random_state)
    model.fit(data['period_detected'].values.reshape(-1, 1))
    
    data['scores'] = model.decision_function(data['period_detected'].values.reshape(-1, 1))
    data['anomaly_score'] = model.predict(data['period_detected'].values.reshape(-1, 1))
    data.to_csv("D:/Read Paper/Program/chicken_behaviour/results/anomaly_detection_result.csv", index = False)