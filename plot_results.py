import pandas as pd
import matplotlib.pyplot as plt
import os

filename = "results.csv"

if not os.path.exists(filename):
    print(f"[!] File '{filename}' not found.")
    exit(1)

df = pd.read_csv(filename)

# Fix types
df["speed_hps"] = pd.to_numeric(df["speed_hps"], errors="coerce")
df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
df = df.dropna(subset=["speed_hps", "duration"])

summary = df.groupby("name").agg(
    avg_speed_hps=("speed_hps", "mean"),
    avg_duration=("duration", "mean")
).reset_index()

print("\n[+] Summary statistics:")
print(summary.round(2).to_string(index=False))

plt.figure(figsize=(10, 5))
bars = plt.bar(summary["name"], summary["avg_speed_hps"])
plt.yscale("log")  # Optional but useful for large speed ranges
plt.title("Average Cracking Speed (H/s)")
plt.ylabel("Speed [H/s] (log scale)")
plt.xlabel("Hash Algorithm")
plt.xticks(rotation=45)

# Annotate bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height,
             f'{height:.1e}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()
