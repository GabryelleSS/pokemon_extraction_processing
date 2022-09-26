import scrapy
import logging
import pandas

POKEMON_TYPES = [
  'normal',
  'fire',
  'water',
  'electric',
  'grass',
  'ice',
  'fighting',
  'poison',
  'ground',
  'flying',
  'psychc',
  'bug',
  'rock',
  'ghost',
  'dragon'
]

class PokemonSpider(scrapy.Spider):
  name = 'pokemonSpider'
  start_urls = ['https://www.serebii.net/pokedex/']

  def __init__(self):
    logger = logging.getLogger('scrapy.core.engine')
    logger.setLevel(logging.INFO)
    self.pokemon_info = []

  def parse(self, response):
    for type_link in response.css('#content > main > div:nth-child(4) > div > div:nth-child(5) table tr td a'):
      page_url = type_link.attrib['href']
      yield response.follow(page_url, self.get_pokemon_links)

  def get_pokemon_links(self, response):
    for table in response.css('.dextable tr td:nth-child(3) a'):
      page_url = table.attrib.get('href')
      yield response.follow(page_url, self.get_pokemon_info)

  def get_pokemon_info(self, response):
    pokemon = {
      'number': int(response.url.split('/')[4].split('.')[0]),
      'name': response.css('#content > main > div > div > table:nth-child(5) tr:nth-child(2) .fooinfo:first-child::text').get(),
      'height': response.css('#content > main > div > div > table:nth-child(5) > tr:nth-child(4) > td:nth-child(2)::text').get(),
      'weight': response.css('#content > main > div > div > table:nth-child(5) > tr:nth-child(4) > td:nth-child(3)::text').get(),
      'type': response.css('#content > main > div > div > table:nth-child(5) > tr:nth-child(2) > td.cen > a').attrib['href'],
      'damage_taken': {},
      'next_evolution_number': 0,
    }

    pokemon['height'] = round(float(pokemon['height'].replace("'", '').replace('"', '')) / 39.370, 1)
    pokemon['weight'] = round(float(pokemon['weight'].replace('lbs', '')) / 2.2046, 1)
    pokemon['type'] = pokemon['type'].split('/')[2].split('.')[0]

    damages_taken_by_type = response.css('#content > main > div > div > table:nth-child(7) > tr:nth-child(3) td::text')

    for i, _type in enumerate(POKEMON_TYPES):
      pokemon['damage_taken'][_type] = damages_taken_by_type[i].get().replace('*', '')
      pokemon['damage_taken'][_type] = round(float(pokemon['damage_taken'][_type]), 1)
    
    evolutions = response.css('#content > main > div > div > table:nth-child(8) > tr:nth-child(2) > td > table tr td a')
    
    evolutions_numbers = []

    for evolution in evolutions:
      try:
        evolutions_numbers.append(
          int(evolution.attrib['href'].split('/')[2].split('.')[0])
        )
      except ValueError:
        self.logger.error(
          "ERROR WHILE CONVERTING '{}' TO POKEMON NUMBER".format(
            evolution.attrib['href'].split('/')[2].split('.')[0]
          ),
        )
        return
    for evolution_number in evolutions_numbers:
      if (evolution_number - pokemon['number']) == 1:
        pokemon['next_evolution_number'] = evolution_number
        break

    self.logger.info(f'>>>>>>>>>>>{pokemon}')

    self.pokemon_info.append(pokemon)

    self.export_data()

  def export_data(self):
    df_pokemon = pandas.DataFrame(data=self.pokemon_info)
    df_pokemon.to_json('data/pokemon_info.json')



