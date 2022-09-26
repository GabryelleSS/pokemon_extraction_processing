from mrjob.job import MRJob
from mrjob.step import MRStep

class MapperReduceAmountPokemon(MRJob):
  def steps(self):
    return [
      MRStep(mapper=self.mapper,
            reducer=self.reducer),
      MRStep(mapper=self.mapper_amount)
    ]

  def mapper(self, _, line):
    pokemon_type, amount = line.split(' ')
    yield (pokemon_type, float(amount))

  def reducer(self, key, values):
    yield (key, tuple(values))

  def mapper_amount(self, key, values):
    yield (key, int(sum(values)))

if __name__ == '__main__':
  MapperReduceAmountPokemon.run()