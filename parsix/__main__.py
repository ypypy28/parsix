import argparse
import main
from config import REGIONS, OUTPUT_DIR_NAME


parser = argparse.ArgumentParser(
    prog="parsix",
    description="Parser izbiratelnyh komissyi",
)
parser.add_argument("--output_dir", default=OUTPUT_DIR_NAME, nargs='?',
                    help="path to the directory where to put results")
parser.add_argument("--region", nargs='?',
                    choices=REGIONS,
                    help="which regions to work with")

args = parser.parse_args()

main.run(region=args.region, out_dir=args.output_dir)
