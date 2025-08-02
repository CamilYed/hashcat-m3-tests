import yaml

def load_algorithms(path="config/algorithms.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)["algorithms"]
