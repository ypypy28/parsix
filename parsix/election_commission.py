import sys
from urllib.request import urlopen, Request
from urllib.error import URLError
from bs4 import BeautifulSoup
from parsix.coords_helper import make_unique_coordinates

HEADERS = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"}


class Uik_obj:

    _page = ''
    link = ''
    name = ''
    address = ''
    address_voteroom = ''
    chairman = ''
    vice_chairman = ''
    secretary = ''
    members = ''
    coords = ()
    _staff = []

    def _get_page(self, link):
        try:
            p = urlopen(Request(link, headers=HEADERS)).read()
        except URLError as e:
            print("\nSomething happend while trying to parse:",
                  link,
                  e.reason,
                  sep='\n')
            sys.exit(1)

        return p.decode('cp1251').encode('utf-8')

    def _get_coords(self, s: BeautifulSoup) -> str:

        if map_voteroom := s.find('span', {'id': 'view_in_map_voteroom'}):
            lat = map_voteroom['coordlat']
            lon = map_voteroom['coordlon']

            if lat and lon:
                lat, lon = make_unique_coordinates(lat, lon)
                return f'{lat}, {lon}'

        return ''

    def _get_staff(self, s: BeautifulSoup) -> list:

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
                    persons['Член'].append({name: org_from})
                else:
                    persons[position] = {name: org_from}

        return persons

    def _build_name_pos(self, o: object) -> str:
        return '\n'.join(list(x + ', ' + o[x] for x in o))

    def _build_members_str(self, m: list) -> str:
        return '\n'.join(self._build_name_pos(x) for x in m)

    def __getitem__(self, field):
        return self.__getattribute__(field)

    def __init__(self, link):
        self.link = link
        self._page = self._get_page(link)
        soup = BeautifulSoup(self._page, 'lxml')
        self.name = soup.find_all('h2')[1].text
        # make uik's full name into short
        # Участковая избирательная комиссия №X → УИК №X
        if self.name[0] == 'У':
            _, _, num = self.name.rpartition(' ')
            self.name = f"УИК {num}"

        self.address = soup.find('span', {'id': 'address_ik'}).text
        if pre := soup.find('span', {'id': 'address_voteroom'}):
            self.address_voteroom = pre.text
        self.coords = self._get_coords(soup)
        self._staff = self._get_staff(soup)

        if 'Председатель' in self._staff:
            self.chairman = self._build_name_pos(self._staff['Председатель'])
        if 'Зам.председателя' in self._staff:
            self.vice_chairman = self._build_name_pos(self._staff['Зам.председателя'])
        if 'Секретарь' in self._staff:
            self.secretary = self._build_name_pos(self._staff['Секретарь'])
        self.members = self._build_members_str(self._staff['Член'])

    def keys(self):
        return('link',
               'name',
               'address',
               'address_voteroom',
               'coords',
               'chairman',
               'vice_chairman',
               'secretary',
               'members')
