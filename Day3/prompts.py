import os

import yaml
 
DEFAULT_CONFIG_PATH = "prompt.yaml"
 
def load_prompts(path: str = DEFAULT_CONFIG_PATH) -> dict:

    with open(path, "r") as f:

        return yaml.safe_load(f)
 
def get_prmpt(name: str, version: int)-> dict:

    prompt_func = load_prompts()

    prompt_entry = prompt_func[name]
 
    system_text = prompt_entry["versions"][version]["system"]
 
    return {"name": name, "version": version, "system": system_text}
 