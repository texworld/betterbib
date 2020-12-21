import argparse
import csv
import json


def _main():
    args = _parse_cmd_arguments()

    # read input file into dictionary
    # only take the first two entries per row
    with open(args.infile) as f:
        out = {
            row[0]: row[1] for row in csv.reader(f, delimiter=";")
        }

    with open(args.outfile, "w") as f:
        json.dump(out, f, indent=2)


def _parse_cmd_arguments():
    parser = argparse.ArgumentParser(description="Update journals.json.")
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', type=str)
    return parser.parse_args()


if __name__ == "__main__":
    _main()
