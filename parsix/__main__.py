import argparse
import main
from config import REGIONS, OUTPUT_DIR_NAME, SHOW_CHROME


parser = argparse.ArgumentParser(
    prog="parsix",
    description="Election commissions parser",
)
parser.add_argument("--output-dir", "-o", default=OUTPUT_DIR_NAME, nargs='?',
                    help="path to the directory where to put results")
parser.add_argument("--region", "-r", required=True,
                    choices=REGIONS,
                    help="which regions to work with")
parser.add_argument("--show-chrome", default=SHOW_CHROME, action="store_true",
                    help="use to display Chrome window while parsing initial page")

args = parser.parse_args()

main.run(region=args.region,
         out_dir=args.output_dir,
         show_chrome=args.show_chrome)
