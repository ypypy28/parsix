from selenium import webdriver
from re import findall
from time import sleep
from pathlib import Path


START_URL = 'http://www.ivanovo.vybory.izbirkom.ru/region/ivanovo?action=ik'


def get_src(url: str) -> str:
    driver = webdriver.Chrome()
    driver.get(url)

    arrows = driver.find_elements_by_class_name('jstree-ocl')[1:]
    for arrow in arrows:
        arrow.click()
        sleep(1)

    src = driver.page_source
    driver.quit()

    return src


def parse_ids(url: str = START_URL) -> list:
    src = get_src(url)
    return findall('id="(\d+)"', src)


if __name__ == '__main__':
    from time import (strftime, localtime)

    ids = parse_ids(START_URL)

    filename = (Path().cwd() / "out" /
                'uiks_' + strftime('%Y%m%d', localtime()) + '.txt'
                )

    with open(filename, 'w') as f:
        f.writelines((START_URL + f'%vrn={i}' for i in ids))
