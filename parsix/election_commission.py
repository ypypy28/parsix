from bs4 import BeautifulSoup

from dataclasses import dataclass, fields
from urllib.error import URLError
from urllib.request import urlopen, Request
import sys

from parsix.coords_helper import make_unique_coordinates


_HEADERS = {'User-Agent':
            "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"}


@dataclass(slots=True)
class Commission:
    """Representation of Russian election commission"""

    link: str
    name: str
    address: str = ''
    address_voteroom: str = ''
    chairman: str = ''
    vice_chairman: str = ''
    secretary: str = ''
    members: str = ''
    coords: str = ''

    def keys(self):
        return tuple(field.name for field in fields(self))


def _get_page(link: str) -> str:
    try:
        p = urlopen(Request(link, headers=_HEADERS)).read()
    except URLError as e:
        print("\nSomething happend while trying to parse:",
              link,
              e.reason,
              sep='\n')
        sys.exit(1)

    return p.decode('cp1251').encode('utf-8')


def _get_staff(s: BeautifulSoup) -> dict[str, str | list[dict[str, str]]]:

    table = s.find('div', {'class': 'table'})
    rows = table.find_all('tr')
    persons = {'Член': []}
    for row in rows:
        tds = row.find_all('td')
        if len(tds) > 1:
            name = tds[1].text
            position = tds[2].text
            org_from = tds[3].text
            if position == 'Член':
                persons['Член'].append((name, org_from))
            else:
                persons[position] = (name, org_from)

    return persons


def _get_coords(s: BeautifulSoup) -> str:

    if map_voteroom := s.find('span', {'id': 'view_in_map_voteroom'}):
        lat = map_voteroom['coordlat']
        lon = map_voteroom['coordlon']

        if lat and lon:
            lat, lon = make_unique_coordinates(lat, lon)
            return f'{lat}, {lon}'

    return ''


# TODO make simplier
def _build_name_organization(member: tuple[str]) -> str:
    return ', '.join(member)


def _build_members_str(members: list[tuple[str]]) -> str:
    return '\n'.join(_build_name_organization(member) for member in members)


def get_commission_from(link: str) -> Commission:
    page = _get_page(link)
    soup = BeautifulSoup(page, 'lxml')

    name = soup.find_all('h2')[1].text

    # turn full name into short name for "УИК"
    # Участковая избирательная комиссия №X → УИК №X
    if name.startswith('У'):
        _, _, num = name.rpartition(' ')
        name = f"УИК {num}"

    address = soup.find('span', {'id': 'address_ik'}).text

    address_voteroom = ''
    if voteroom := soup.find('span', {'id': 'address_voteroom'}):
        address_voteroom = voteroom.text

    staff = _get_staff(soup)

    chairman, vice_chairman, secretary = '', '', ''
    if 'Председатель' in staff:
        chairman = _build_name_organization(staff['Председатель'])
    if 'Зам.председателя' in staff:
        vice_chairman = _build_name_organization(staff['Зам.председателя'])
    if 'Секретарь' in staff:
        secretary = _build_name_organization(staff['Секретарь'])

    regular_members = _build_members_str(staff['Член'])

    coords = _get_coords(soup)

    return Commission(link=link,
                      name=name,
                      address=address,
                      address_voteroom=address_voteroom,
                      chairman=chairman,
                      vice_chairman=vice_chairman,
                      secretary=secretary,
                      members=regular_members,
                      coords=coords,
                      )
