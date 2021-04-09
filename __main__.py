import main
from uik_ids import parse_ids


START_URL = 'http://www.ivanovo.vybory.izbirkom.ru/region/ivanovo?action=ik'
urls = [f'{START_URL}&vrn={i}' for i in parse_ids(START_URL)]
main.run(urls)
