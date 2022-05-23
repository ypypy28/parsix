from dataclasses import asdict
from pathlib import Path
from random import randrange
import csv
import sys
import time

from parsix.config import SLEEP_RANGE
from parsix.commissions_id_parser import parse_ids
from parsix.election_commission import get_commission_from, Commission


def write_to_csv(pathname: Path, election_commissions: list[Commission]) -> None:
    fieldnames = list(asdict(election_commissions[0]).keys())
    with pathname.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for commission in election_commissions:
            writer.writerow(asdict(commission))


def clean_workdir(wd: Path) -> None:
    for f in wd.iterdir():
        if f.stem.startswith('tmp'):
            f.unlink()


def run(region: str, out_dir: str = "out", show_chrome: bool = False) -> None:

    start_url = f'http://www.{region}.vybory.izbirkom.ru/region/{region}?action=ik'

    out_dir = Path().cwd() / out_dir
    out_dir.mkdir(exist_ok=True)

    print("Parsing ids of commissions form the base page of the region. It may take a while.")
    urls = [f'{start_url}&vrn={i}'
            for i in parse_ids(url=start_url,
                               out_dir=out_dir,
                               show_chrome=show_chrome)]
    if not urls:
        print("Parsing from site went wrong. Maybe you were banned.",
              "Or perhaps the election commissions site changed its structure.",
              f"Try to open base link in your browser {start_url}",
              sep='\n')
        clean_workdir(out_dir)
        sys.exit(1)

    print(f':> {len(urls)} election commissions in total\n'
          'Parsing will be completed in around '
          f'{len(urls)*(SLEEP_RANGE[1]-1)//60} minutes')

    uiks, hqiks = [], []
    for link in urls:
        commission = get_commission_from(link)
        print(f'Got the {commission.name}', end='')

        if commission.name.startswith('У'):
            uiks.append(commission)
        else:
            hqiks.append(commission)

        sleep_time = randrange(*SLEEP_RANGE)
        print(f', sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)

    today = time.strftime('%Y%m%d', time.localtime())

    write_to_csv(out_dir / f'{region}_uiks_{today}.csv', uiks)
    write_to_csv(out_dir / f'{region}_hqiks_{today}.csv', hqiks)

    # remove temporary files
    clean_workdir(out_dir)


if __name__ == "__main__":
    run()
