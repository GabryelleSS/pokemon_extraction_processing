import pandas

class PokemonAnalysis():
  def average_by_type_attack(self):
    df_pokemon = pandas.read_json('./data/pokemon_info.json') 
    data = pandas.DataFrame(data=tuple(df_pokemon.damage_taken))

    with open('./data/mapperReduce/input/damage_taken.txt', mode='a+') as damage_file:
      for column, row in data.items():
        for value in row:
          damage_file.write(f'{column} {value}\n')

    with open('./data/mapperReduce/input/pokemon_type.txt', mode='a+') as pokemon_type:
      for _, type_name in df_pokemon.type.items():
        pokemon_type.write(f'{type_name} 1\n')

PokemonAnalysis().average_by_type_attack()