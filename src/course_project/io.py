"""Read measurement CSV files and write result files.

Why the standard-library csv module instead of pandas?
- Day 1 is about fundamentals: here you can see every step that
  pandas.read_csv would hide (header, rows as dicts, str -> float).
- No extra dependency: pandas (plus numpy) is a large install for four rows.
- Explicit rules: pandas silently turns "nan" or empty cells into NaN, and
  Series.mean() skips NaN by default. Here a non-finite value raises an error.

The pandas version, for comparison (pandas would have to be added to
pyproject.toml, and the checks above would still be needed):

    import pandas as pd
    values = pd.read_csv(path)[column].astype(float).tolist()

For larger tables, grouping, or joins, pandas is the right tool (later days).
"""

import csv
import json
import math


def read_values(path, column): # column: column name we get from the config file
    """Return one column of a CSV file as a list of finite floats."""
    values = []
    with path.open(newline="", encoding="utf-8") as handle:
        """ newline="":
        This is the requirement for the csv module in Python's official documentation, 
        which means "the newline character is left to the csv module to handle itself." 
        Line breaks vary between systems (\r\n for Windows, \n for Mac and Linux), 
        and CSV cells may contain line breaks. 
        Without this parameter, 
        in some cases extra blank lines will be read, 
        or a cell will be split incorrectly.
        """
        reader = csv.DictReader(handle)  # The first line is used as the header
        # each row becomes a dict keyed by the header
        # reader.fieldnames = ['sample_id', 'value']
        if column not in (reader.fieldnames or []):
            # why " or [] "? try an empty csv file, then reader.fieldnames is None,
            # value in None -> TypeError ; value in [] -> False
            raise ValueError(f"Missing column: {column}")
        for row in reader:
            value = float(row[column])  # CSV cells are always strings
            if not math.isfinite(value):
                raise ValueError("Values must be finite")
            values.append(value)
    return values


def write_result(result, output_path): # result -> a dictionary, summarize()
    # e.g. {"n": 4, "mean": 11.0, "n_above": 2, "threshold": 10.0}
    """Write a result dict as indented JSON."""
    text = json.dumps(result, indent=2) # from dict -> JSON; dumps = dump string
    # without indent: {"n": 4, "mean": 11.0, "n_above": 2, "threshold": 10.0}
    # with indent:
#     {
#        "n": 4,
#        "mean": 11.0,
#        "n_above": 2,
#        "threshold": 10.0
#      }
    output_path.write_text(text + "\n", encoding="utf-8")


# homework: why not pandas? try pandas.