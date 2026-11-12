import os

import yaml
 
DEFAULT_CONFIG_PATH = "config.yaml"
 
def load_config(path: str = DEFAULT_CONFIG_PATH) -> dict:

    with open(path, "r") as f:

        return yaml.safe_load(f)
 