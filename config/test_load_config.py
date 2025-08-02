from config_loader import load_algorithms

def test_load_algorithms():
    algos = load_algorithms("config/algorithms.yaml")
    assert isinstance(algos, list)
    assert algos[0]["name"] == "MD5"
    assert algos[1]["mode"] == 3200
