import sys
import time
import csv
from pathlib import Path
from random import randrange
from uik_obj import Uik_obj
from uik_ids import parse_ids
from config import SLEEP_RANGE


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


def run(region: str, out_dir: str = "out", show_chrome: bool = False):

    start_url = f'http://www.{region}.vybory.izbirkom.ru/region/{region}?action=ik'

    out_dir = Path().cwd() / out_dir
    out_dir.mkdir(exist_ok=True)

    print("Parsing uik ids form the base page of the region. It may take a while.")
    urls = [f'{start_url}&vrn={i}'
            for i in parse_ids(url=start_url,
                               out_dir=out_dir,
                               show_chrome=show_chrome)]
    if not urls:
        print("Parsing from site went wrong")
        sys.exit(1)


    print(f':> {len(urls)} election commissions in total\n'
          'Parsing will be completed in around '
          f'{len(urls)*(SLEEP_RANGE[1]-1)//60} minutes')

    uiks, hqiks = [], []
    for link in urls:
        u = Uik_obj(link)

        if u.name[0] == 'У':
            uiks.append(u)
        else:
            hqiks.append(u)

        sleep_time = randrange(*SLEEP_RANGE)
        print(f'working on {u.name}, sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)

    today = time.strftime('%Y%m%d', time.localtime())

    write_to_csv(out_dir / f'{region}_uiks_{today}.csv', uiks)
    write_to_csv(out_dir / f'{region}_hqiks_{today}.csv', hqiks)

    # remove temporary files
    for f in out_dir.iterdir():
        if f.stem.startswith('tmp'):
            f.unlink()


if __name__ == "__main__":
    run()
