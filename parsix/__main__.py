import argparse
import signal
import sys
from parsix import main
from parsix.config import REGIONS, OUTPUT_DIR_NAME, SHOW_CHROME
from shutil import which


def exit_gracefully(signal, frame):
    print("\nProgram was interrupted")
    sys.exit(1)


def start():

    signal.signal(signal.SIGINT, exit_gracefully)
    if not which('chromedriver'):
        print("You need to install chromedriver, "
            "download it from here https://chromedriver.chromium.org/home")

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


if __name__ == "__main__":
    start()
