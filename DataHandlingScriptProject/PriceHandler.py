from bs4 import BeautifulSoup

with open('sample.xml', 'r') as f:
    data = f.read()


bs_data = BeautifulSoup(data, 'html.parser')

from_tags_in_file = bs_data.find_all('from')

print(from_tags_in_file)

