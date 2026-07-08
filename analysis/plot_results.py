import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)

df = pd.read_csv(os.path.join(BASE_DIR, "modified_results.csv"))

plt.figure(figsize=(7,5))

bars = plt.bar(df["Server"], df["Requests"])

plt.xticks(df["Server"])

plt.title("Load Distribution")

plt.xlabel("Server")

plt.ylabel("Number of Requests")

plt.bar_label(bars, padding=2)

plt.savefig(os.path.join(BASE_DIR, "modified_load_distribution.png"), dpi=300)

plt.show()