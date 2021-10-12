import yaml

config_path = "config.yaml"

def get_config():
    with open(config_path) as f:
        dict = yaml.safe_load(f)
        dict["add_subtitles"] = dict["add_subtitles"] == 1

    return dict
