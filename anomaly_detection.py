import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("server_metrics_log.csv")

features = ["cpu_usage_percent" , "ram_usage_percent" , "response_time_ms"]
X = df[features]

model = IsolationForest( contamination = 'auto' , random_state = 36)

df["anomaly_prediction"] = model.fit_predict(X)
anomalies = df[df["anomaly_prediction"] == -1]

print(anomalies[["test_iteration", "cpu_usage_percent", "ram_usage_percent", "response_time_ms", "is_anomaly"]])

df["State"] = df["anomaly_prediction"].map({1 : "Normal Data" , -1 : "Anomaly"})

plt.figure(figsize = (10,6))

colours = {"Normal Data" : "#1f77b4" , "Anomaly" : "#d62728" }

sns.scatterplot(
    data=df,
    x="cpu_usage_percent",
    y="response_time_ms",
    hue="State",
    palette=colours,
    s=100,       
    alpha=0.8    
)

plt.title("Server Metrics and Observed Anomalies (Isolation Forest)", fontsize=14, fontweight='bold')
plt.xlabel("CPU Usage (%)", fontsize=12)
plt.ylabel("Response Time (ms)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Data Class")
plt.savefig("pipeline_3d_result.png")

plt.show()