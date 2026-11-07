"""Connect config, io, and analysis; provide the command-line entry point."""
import argparse
# The argparse module is Python's standard library tool for building user-friendly command-line interfaces (CLIs)
import logging

from .analysis import summarize
from .config import load_config, resolve_paths, validate_config
from .io import read_values, write_result


def run(config_path):
    """Run the whole analysis for one YAML file and return the result dict."""
    path, cfg = load_config(config_path)                        # 1. read YAML
    validate_config(cfg)                                        # 2. check it
    source, target = resolve_paths(cfg, path)                   # 3. real paths
    values = read_values(source, cfg["analysis"]["column"])     # 4. read CSV
    result = summarize(values, cfg["analysis"]["threshold"])    # 5. compute
    write_result(result, target / "summary.json")               # 6. save JSON
    return result


def parse_args():
    """Declare which command-line arguments the program accepts."""
    parser = argparse.ArgumentParser(description="Summarize a measurement CSV")
    parser.add_argument(
        "--config",
        default="config/base.yaml",
        help="Path to a YAML configuration file",
    )
    # parser.add_argument("--output-dir", default=None)
    # parser.add_argument("--threshold", type=float, default=None)
    # parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main():
    """Entry point for the terminal. In a notebook, call run() instead."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    result = run(args.config)
    logging.info("Result: %s", result)


# True only when started as a program (python -m course_project.pipeline),
# False when another file imports this module.
if __name__ == "__main__":
    main()


# python -m course_project.pipeline --config config/base.yaml
# # INFO: Result: {'n': 4, 'mean': 11.0, 'n_above': 2, 'threshold': 10.0}  
# python -m course_project.pipeline --config config/high_threshold.yaml
# # INFO: Result: {'n': 4, 'mean': 11.0, 'n_above': 1, 'threshold': 12.0} 