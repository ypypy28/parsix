import argparse
import main


parser = argparse.ArgumentParser(description="Parse uiks from state izbirkoms' webpage")
parser.add_argument("url", metavar="URL", type=str, nargs='?',
                    help="link to the state izbirkoms' webpage with uiks")
parser.add_argument("-o", default="out", type=str, nargs='?',
                    help="path to the directory where to put result")

args = parser.parse_args()

main.run(start_url=args.url, out_dir=args.o)
