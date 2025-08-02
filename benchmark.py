import subprocess
import time
import os
import sys
import yaml
import csv

CONFIG_PATH = "config/algorithms.yaml"
REPEATS = 3
RESULTS_CSV = "results.csv"

def load_algorithms():
    if not os.path.exists(CONFIG_PATH):
        print(f"[!] Config not found: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f)
        return data.get("algorithms", [])

def parse_speed(speed_line):
    if not speed_line:
        return ("N/A", None)

    parts = speed_line.split(":")
    if len(parts) < 2:
        return ("N/A", None)

    raw = parts[1].strip()
    try:
        val, unit = raw.split()[:2]
        value = float(val)
    except ValueError:
        return (raw, None)

    # Normalize unit (e.g. MH/s)
    multipliers = {
        "H/s": 1,
        "kH/s": 1e3,
        "MH/s": 1e6,
        "GH/s": 1e9,
        "TH/s": 1e12
    }

    multiplier = multipliers.get(unit, 1)
    return (raw, round(value * multiplier, 2))


def convert_to_hps(value, unit):
    units = {"H/s": 1, "kH/s": 1e3, "MH/s": 1e6, "GH/s": 1e9}
    return round(value * units.get(unit, 1), 2)

def run_benchmark(mode, name):
    print(f"\n[+] Benchmarking {name} (mode {mode}) – {REPEATS} repeats")
    results = []
    for i in range(REPEATS):
        print(f"  [>] Run {i + 1}...")
        start = time.time()
        try:
            proc = subprocess.run(
                ["hashcat", "-b", "-m", str(mode), "--force"],
                capture_output=True,
                text=True,
                timeout=90
            )
            duration = round(time.time() - start, 2)
            output = proc.stdout
            print(proc.stdout)
            speed_line = next((l for l in output.splitlines() if "Speed.#" in l), None)
            raw_speed, hps = parse_speed(speed_line)
            print(f"      -> {raw_speed} in {duration}s")
        except Exception as e:
            raw_speed, hps, duration = "Error", None, None
            print(f"      [!] Error: {e}")

        results.append({
            "name": name,
            "mode": mode,
            "speed_raw": raw_speed,
            "speed_hps": hps,
            "duration": duration
        })
    return results

def write_csv(results):
    header = ["name", "mode", "speed_raw", "speed_hps", "duration"]
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[✔] Results saved to {RESULTS_CSV}")

if __name__ == "__main__":
    print("[#] Hashcat Benchmark Tool\n==========================\n")
    algos = load_algorithms()

    print("[?] Select algorithms to benchmark:")
    for idx, algo in enumerate(algos, 1):
        print(f"  {idx}. {algo['name']} (mode {algo['mode']})")
    choice = input("\n[?] Enter numbers (e.g. 1,3) or press Enter for all: ").strip()

    if choice:
        indices = {int(i.strip()) - 1 for i in choice.split(",")}
        algos = [algo for i, algo in enumerate(algos) if i in indices]

    all_results = []
    for algo in algos:
        all_results.extend(run_benchmark(algo["mode"], algo["name"]))

    write_csv(all_results)
