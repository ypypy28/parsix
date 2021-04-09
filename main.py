import time
import csv
# import os
from random import randrange
from Uik_obj import Uik_obj

SLEEP_RANDOM_RANGE = (0, 2)


def write_to_csv(pathname: str, all_uiks: list):

    fieldnames = list(all_uiks[0].keys())
    with open(pathname, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for uik in all_uiks:
            writer.writerow({field: uik[field] for field in fieldnames})


def run(urls: list):
    all_uiks = []

    for link in urls:
        u = Uik_obj(link)
        all_uiks.append(u)

        sleep_time = randrange(*SLEEP_RANDOM_RANGE)
        print(f'working on {u.name}')
        print(f'sleep for {sleep_time} seconds')
        time.sleep(sleep_time)

    filename = time.strftime('%Y%m%d', time.localtime())

    write_to_csv(f'./out/{filename}.csv', all_uiks)


if __name__ == "__main__":
    urls = []
    all_uiks = []
    with open('uiks.txt', encoding='utf-8') as uu:
        urls = uu.read().split()

    run(urls)
