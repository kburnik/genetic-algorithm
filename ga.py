from fitness import fitness, BITCOUNT
import argparse
import os
import random
import sys

TRACE_ENABLED = True
"""Whether the debug trace is on."""

URANDOM_STRING_LENGTH = 32
"""Size of the entropy string provided from urandom."""


def trace(*text):
  """Outputs a single chunk of text to stderr."""
  if not TRACE_ENABLED:
    return
  data = " ".join([str(chunk) for chunk in text])
  sys.stderr.write(data + "\n")
  sys.stderr.flush()


def decode(member):
  """Displays int as a binary string."""
  return bin(member)[2:].zfill(BITCOUNT)


def crossover(a, b, pos=None):
  """Crosses over two members by cutting at point pos (right to left).
     If pos is None, a random number between 1 and BITCOUNT-1 is used."""
  if pos is None:
    pos = random.randint(1, BITCOUNT - 1)
  mask = (2 ** pos) - 1
  invmask = (2 ** BITCOUNT) - mask - 1
  na = (a & invmask) | (b & mask)
  nb = (b & invmask) | (a & mask)
  return (na, nb)


def mutate(member, num_bits=None):
  """Mutates a member by fliping up to num_bits random bits. if num_bits is None
     a random value from 1 to BITCOUNT is used."""
  if num_bits is None:
    num_bits = random.randint(1, BITCOUNT)
  elif num_bits < 0:
    raise Exception("Number of bits must be non-negative.")
  for pos in random.sample(range(0, BITCOUNT), num_bits):
    member ^= 1 << pos
  return member


class Defaults:
  """Default values for params."""
  CROSSING_PROBABILITY = 0.9
  MUTATION_PROBABILITY = 0.01
  ITERATION_COUNT = 30
  INITIAL_POPULATION = 20
  RANDOM_SEED = None


class Params(object):
  """Parameters of a genetic algorithm."""
  def __init__(self, crossing, mutation, iterations, population, random_seed):
    self.crossing = crossing
    self.mutation = mutation
    self.iterations = iterations
    self.population = population
    self.random_seed = random_seed

class GeneticAlgo(object):
  """Represents a genetic algorithm"""
  def __init__(self, params):
    self.params = params
    self.population = []

  def initialize(self):
    """Initializes the population."""
    seed = self.params.random_seed
    if seed is None:
      seed = hash(os.urandom(URANDOM_STRING_LENGTH))
    random.seed(seed)
    trace("Using random seed", seed)
    for i in range(self.params.population):
      member = random.randint(0, (2 ** BITCOUNT) - 1)
      self.population.append(member)

  def evolve(self):
    """Generator where each iteration is an evolution step."""
    for generation in range(self.params.iterations):
      # 1) Selection.
      selection = self.select(self.population)

      # 2) Crossover.
      for i in range(0, len(selection) - 1, 2):
        if random.random() < self.params.crossing:
          selection[i], selection[i + 1] = \
            crossover(selection[i], selection[i + 1])

      # 3) Mutation.
      for i in range(len(selection)):
        if random.random() < self.params.mutation:
          selection[i] = mutate(selection[i])

      self.population = list(sorted([member for member in selection],
                             reverse=True,
                             key=lambda member: fitness(member)))
      yield generation

  def select(self, population):
    """Sort existing population by fitness descending."""
    return list(sorted([member for member in population],
                       reverse=True,
                       key=lambda member: fitness(member)))

    # TODO(kburnik): This can be optimized.
    while len(selection) < len(population):
      index = random.random()
      for i, x in enumerate(accumulated_fits):
        # The selected individual is the first one whose accumulated normalized
        # value is greater than index.
        if x[1] > index:
          selection.append(x[0])
          break
    return list(sorted(selection, key=lambda m: fitness(m), reverse=True))

  def display(self):
    """Prints the current population"""
    print "%10s %4s %7s" % ("bin", "int", "fitness")
    for member in self.population:
      print "%10s %4s %7.2f" % (decode(member), member, fitness(member))
    fits = [fitness(member) for member in self.population]
    minval = min(fits)
    maxval = max(fits)
    avgval = sum(fits) / len(fits)
    print "min = %.2f, max = %2.f, avg = %.2f" % (minval, maxval, avgval)


if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("-cp", "--crossing", default=Defaults.CROSSING_PROBABILITY,
                  type=float, help="Crossing probability in [0.00, 1.00]")
  ap.add_argument("-mp", "--mutation", default=Defaults.MUTATION_PROBABILITY,
                  type=float, help="Mutation probability in [0.00, 1.00]")
  ap.add_argument("-i", "--iterations", default=Defaults.ITERATION_COUNT,
                  type=int, help="Iteration count (integer)")
  ap.add_argument("-p", "--population", default=Defaults.INITIAL_POPULATION,
                  type=int, help="Initial population (integer)")
  ap.add_argument("-s", "--random_seed", default=Defaults.RANDOM_SEED, type=int,
                   help="Random seed. Omit to use system clock.")
  args_dict = vars(ap.parse_args())
  params = Params(**args_dict)
  ga = GeneticAlgo(params)
  ga.initialize()

  for i in ga.evolve():
    print "Generation", i + 1
    ga.display()
    print ""

