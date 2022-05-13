from selenium import webdriver
from re import findall
from time import sleep
from pathlib import Path
from random import randrange


START_URL = 'http://www.ivanovo.vybory.izbirkom.ru/region/ivanovo?action=ik'
SLEEP_RANDOM_RANGE = (2, 4)

def get_src(url: str) -> str:
    driver = webdriver.Chrome()
    driver.get(url)

    arrows = driver.find_elements_by_class_name('jstree-ocl')[1:]
    for arrow in arrows:
        arrow.click()
        sleep(randrange(*SLEEP_RANDOM_RANGE))

    src = driver.page_source
    driver.quit()

    return src


def parse_ids(url: str = START_URL, out_dir: Path=None) -> list:

    src = ''
    if out_dir is None:
        src = get_src(url)
    else:
        tmp = out_dir.joinpath("tmp_base.html")
        if tmp.is_file():
            src = tmp.read_text(encoding='utf-8')
        else:
            src = get_src(url)
            out_dir.joinpath("tmp_base.html").write_text(src, encoding='utf-8')

    return findall('id="(\d+)"', src)


if __name__ == '__main__':
    from time import (strftime, localtime)

    ids = parse_ids(START_URL)

    filename = (Path().cwd() / "out" /
                'uiks_' + strftime('%Y%m%d', localtime()) + '.txt'
                )

    with open(filename, 'w') as f:
        f.writelines((START_URL + f'%vrn={i}' for i in ids))
