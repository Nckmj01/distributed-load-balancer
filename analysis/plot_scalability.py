import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)

df = pd.read_csv(os.path.join(BASE_DIR, "scalability.csv"))

plt.figure(figsize=(8,5))

plt.plot(
    df["Servers"],
    df["AverageLoad"],
    marker="o",
    linewidth=2
)

plt.title("Measured Average Requests per Server")
plt.xlabel("Number of Servers")
plt.ylabel("Average Requests")

plt.grid(True)

plt.savefig(os.path.join(BASE_DIR, "modified_scalability.png"), dpi=300)

plt.show()