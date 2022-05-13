import sys
import time
import csv
from pathlib import Path
from random import randrange
from uik_obj import Uik_obj
from uik_ids import parse_ids, SLEEP_RANDOM_RANGE


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


def run(region: str = None, out_dir: str = "out"):

    if not region:
        region = "ivanovo"

    start_url = f'http://www.{region}.vybory.izbirkom.ru/region/{region}?action=ik'

    out_dir = Path().cwd() / out_dir
    out_dir.mkdir(exist_ok=True)

    urls = [f'{start_url}&vrn={i}' for i in parse_ids(url=start_url, out_dir=out_dir)]
    if not urls:
        print("Parsing from site went wrong")
        sys.exit(1)

    uiks, hqiks = [], []

    print(f':: {len(urls)} election commisions in total\n'
          'Parsing will complete in around'
          f'{len(urls)*SLEEP_RANDOM_RANGE[1]//60} minutes')
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

    filename = f'{region}_{time.strftime('%Y%m%d', time.localtime())}'

    write_to_csv(out_dir / f'uiks_{filename}.csv', uiks)
    write_to_csv(out_dir / f'hqiks_{filename}.csv', hqiks)

    # remove temporary files
    for f in out_dir.iterdir():
        if f.stem.startswith('tmp'):
            f.unlink()


if __name__ == "__main__":
    run()
