import sys
import getopt
import time
import csv
from pathlib import Path
from random import randrange
from uik_obj import Uik_obj
from uik_ids import parse_ids

SLEEP_RANDOM_RANGE = (0, 2)


def write_to_csv(pathname: Path, all_uiks: list):

    fieldnames = list(all_uiks[0].keys())
    with pathname.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for uik in all_uiks:
            writer.writerow({field: uik[field] for field in fieldnames})


def run(start_url: str = None, out_dir: str = "out"):

    if not start_url:
        start_url = 'http://www.ivanovo.vybory.izbirkom.ru/region/pskov/?action=ik'

    out_dir = Path().cwd() / out_dir
    if not out_dir.is_dir():
        out_dir.mkdir()

    urls = [f'{start_url}&vrn={i}' for i in parse_ids(start_url)]
    if not urls:
        print("Parsing from site went wrong")
        sys.exit(1)

    uiks, hqiks = [], []

    for link in urls:
        u = Uik_obj(link)

        if u.name[0] == 'У':
            uiks.append(u)
        else:
            hqiks.append(u)

        sleep_time = randrange(*SLEEP_RANDOM_RANGE)
        print(f'working on {u.name}')
        print(f'sleep for {sleep_time} seconds')
        time.sleep(sleep_time)

    filename = time.strftime('%Y%m%d', time.localtime())

    write_to_csv(out_dir / f'uiks_{filename}.csv', uiks)
    write_to_csv(out_dir / f'hqiks_{filename}.csv', hqiks)


if __name__ == "__main__":
    run()
