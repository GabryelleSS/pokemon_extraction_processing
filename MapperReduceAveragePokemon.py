import pandas
from mrjob.job import MRJob
from mrjob.step import MRStep

pokemon_len = len(pandas.read_json('./data/pokemon_info.json'))

class MapperReduceAveragePokemon(MRJob):
  def steps(self):
    return [
      MRStep(mapper=self.mapper,
            reducer=self.reducer),
      MRStep(mapper=self.mapper_average)
    ]

  def mapper(self, _, line):
    damage_type, damage_value = line.split(' ')
    yield (damage_type, float(damage_value))

  def reducer(self, key, values):
    yield (key, tuple(values))

  def mapper_average(self, key, values):
    yield (key, round(sum(values) / pokemon_len, 1))

if __name__ == '__main__':
  MapperReduceAveragePokemon.run()