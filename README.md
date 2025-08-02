# Hashcat 7.0 on Apple M3 – Benchmark & Feature Tests

This project provides a scientific and automated approach to benchmarking the newly released [Hashcat v7.0.0](https://github.com/hashcat/hashcat) on Apple Silicon (M3). It focuses on real-world performance, feature testing (such as auto hash detection and Python Bridge), and visualization of results.

## 🔧 Installing Hashcat v7.0.0 on macOS (Apple Silicon)

```bash
brew install cmake git

git clone https://github.com/hashcat/hashcat.git
cd hashcat
make -j$(sysctl -n hw.ncpu)

sudo cp ./hashcat /usr/local/bin/hashcat

hashcat --version
# should output v7.0.0-4-g9727714cf


python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## 🧪 Project Goals

- Test performance of popular hash modes (MD5, SHA1, bcrypt, scrypt, Argon2, WPA2, etc.)
- Compare CPU vs GPU utilization on M3 hardware
- Evaluate new features like:
  - Auto hash identification (`--identify`)
  - Python Bridge
  - Assimilation Bridge
- Automate result collection and plotting

## 📁 Structure

```
.
├── run_tests.py          # Main test runner
├── config/
│   └── algorithms.yaml   # List of hash modes to test
├── data/
│   └── results.csv       # Collected results from tests
├── plots/
│   └── performance.png   # Output graphs
├── scripts/
│   └── parse_output.py
│   └── plot_results.py
└── requirements.txt      # Python dependencies
```

## ⚙️ Setup

```bash
git clone https://github.com/CamilYed/hashcat-m3-tests.git
cd hashcat-m3-tests
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure you have Hashcat 7.0 installed:
```bash
brew install hashcat
# or build from source
```

## 🚀 Run Benchmarks

```bash
python run_tests.py
python scripts/plot_results.py
```

## 📊 Outputs

- CSV file with speeds and durations
- PNG chart comparing average performance per hash mode

## 🛡️ Security Reminder

- Use strong, unique passwords
- Enable 2FA wherever possible
- Store credentials in a secure password manager

---

> Work in progress – contributions and feedback welcome!
