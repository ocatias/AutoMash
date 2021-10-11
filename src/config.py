import yaml

config_path = "config.yaml"

def get_config():
    with open(config_path) as f:
        dict = yaml.safe_load(f)
    return dict
