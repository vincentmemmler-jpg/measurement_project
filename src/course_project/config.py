"""Load, validate, and resolve a YAML configuration."""
import math
from pathlib import Path

# pip install PyYAML
# PyYAML: from yaml file to python format
import yaml

# print(Path('config/base.yaml'))
# print(Path('config/base.yaml').resolve())
# print(Path('~/config/base.yaml').expanduser())

def load_config(config_path):
    """Read a YAML file and return (absolute path of the file, config dict)."""
    path = Path(config_path).expanduser().resolve()
    with path.open(encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    if not isinstance(cfg, dict):
        raise ValueError("Configuration must be a mapping")
    return path, cfg

#  "  abc  ".strip()   →  "abc"
#  "   ".strip()       →  ""       
#  "".strip()          →  ""

def validate_config(cfg):
    """Fail early, before any data is read, if a setting has the wrong type."""
    for key in ("input_path", "output_dir"):
        value = cfg.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
    analysis = cfg.get("analysis")
    if not isinstance(analysis, dict):
        raise ValueError("analysis must be a mapping")
    column = analysis.get("column") # column name
    if not isinstance(column, str) or not column.strip():
        raise ValueError("column must be a non-empty string")
    # type(...) instead of isinstance(...): bool is a subclass of int
    if type(analysis.get("threshold")) not in (int, float): # .inf and .nan all belong to float
        raise ValueError("threshold must be numeric")
    if not math.isfinite(analysis["threshold"]): # Semantic check
        raise ValueError("threshold must be finite")


def resolve_paths(cfg, config_path):
    """Interpret YAML paths relative to the YAML file, not the terminal."""
    base = config_path.parent
    source = (base / cfg["input_path"]).resolve()
    target = (base / cfg["output_dir"]).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    target.mkdir(parents=True, exist_ok=True)
    return source, target
