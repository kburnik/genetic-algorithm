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


def argmax(values):
  """Returns the index of the largest value in a list."""
  return max(enumerate(values), key=lambda x: x[1])[0]


class Defaults:
  """Default values for params."""
  CROSSING_PROBABILITY = 0.9
  MUTATION_PROBABILITY = 0.01
  ITERATION_COUNT = 30
  INITIAL_POPULATION = 20
  RANDOM_SEED = None
  SELECTION_STRATEGY = "fitness-proportional"
  ELITISM = False


class Params(object):
  """Parameters of a genetic algorithm."""
  def __init__(self, crossing, mutation, iterations, population, random_seed,
               selection_strategy, elitism):
    self.crossing = crossing
    self.mutation = mutation
    self.iterations = iterations
    self.population = population
    self.random_seed = random_seed
    self.selection_strategy = selection_strategy
    self.elitism = elitism


class SelectionStrategy(object):
  """Abstract class for a selection strategy."""
  def select_and_crossover(self, population, crossing):
    raise Exception("Method not implemented.")


class FitnessProportionalSelection(SelectionStrategy):
  """Fitness proportionate selection algorithm. Returns the selection
     sorted by fitness descending.
     https://en.wikipedia.org/wiki/Fitness_proportionate_selection"""

  def _select(self, population):
    selection = []
    fits = [fitness(member) for member in population]
    sum_fits = sum(fits)
    normalized_fits = [(member, fitness(member) / sum_fits)
                       for member in population]
    normalized_fits = list(sorted(normalized_fits, key=lambda x: x[1],
                                  reverse=True))
    accumulated = 0
    accumulated_fits = []
    for x in normalized_fits:
      accumulated += x[1]
      accumulated_fits.append((x[0], accumulated))

    used = set()
    # TODO(kburnik): This can be optimized.
    while len(selection) < len(population):
      value = random.random()
      for i, x in enumerate(accumulated_fits):
        value -= x[1]
        if value <= 0:
          if i in used:
            continue
          used.add(i)
          selection.append(x[0])
          break
    return list(sorted(selection, key=lambda m: fitness(m), reverse=True))

  def _crossover(self, a, b):
    """Crosses over two members by cutting at radnom point pos (right to left).
    """
    pos = random.randint(1, BITCOUNT - 1)
    mask = (2 ** pos) - 1
    invmask = (2 ** BITCOUNT) - mask - 1
    na = (a & invmask) | (b & mask)
    nb = (b & invmask) | (a & mask)
    return (na, nb)

  def select_and_crossover(self, population, crossing):
    # 1) Select.
    selection = self._select(population)
    # 2) Crossover.
    for i in range(0, len(selection) - 1, 2):
      if random.random() < crossing:
        selection[i], selection[i + 1] = \
            self._crossover(selection[i], selection[i + 1])
    return selection


class UniformSelection(SelectionStrategy):
  """A Uniform selection strategy, all members of the population are equally
     likely to be chosen for crossover. The crossover is done by keeping same
     bits of parents and randomly choosing a the bit that differs."""

  def _crossover(self, a, b):
    # Create mask of different bits from both parents.
    diffmask = a ^ b
    # Copy the same bits to child.
    child = a & b
    parents = [a, b]
    val = 1
    while diffmask > 0:
      # Check if the bit is set.
      if diffmask % 2 == 1:
        # Choose parent randomly. 50/50 chance.
        parent = parents[random.randint(0, 1)]
        # Copy the set bit from the chosen parent to the child.
        child |= (parent & val)
      diffmask /= 2
      val *= 2
    return child

  def select_and_crossover(self, population, crossing):
    selection = set()
    used_pairs = set()
    while len(selection) < len(population):
      pair = tuple(random.sample(population, 2))
      if pair in used_pairs:
        continue
      used_pairs.add(pair)
      if random.random() < crossing:
        child = self._crossover(*pair)
        selection.add(child)
      else:
        selection.add(pair[0])
        selection.add(pair[1])
    selection = list(selection)
    while len(selection) > len(population):
      selection.pop()
    return selection


class GeneticAlgo(object):
  """Represents a genetic algorithm"""
  def __init__(self, params):
    self.params = params
    self.population = []
    self.elite_member = None
    if params.selection_strategy == "fitness-proportional":
      self.selection_strategy = FitnessProportionalSelection()
    elif params.selection_strategy == "uniform":
      self.selection_strategy = UniformSelection()
    else:
      raise Exception("Invalid strategy %s" % params.selection_strategy)

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
      # 1) Select and 2) Crossover.
      selection = self.selection_strategy.select_and_crossover(
          self.population, self.params.crossing)

      # Find the elite member if elitism is enabled.
      elite_index = -1
      self.elite_member = None
      if self.params.elitism:
        elite_index = argmax([fitness(member) for member in selection])
        self.elite_member = selection[elite_index]

      # 3) Mutation.
      for i in range(len(selection)):
        # If elitism is enabled, don't mutate no matter the odds.
        if i != elite_index and random.random() < self.params.mutation:
          selection[i] = mutate(selection[i])

      self.population = list(sorted(selection,
                                    key=lambda x: fitness(x),
                                    reverse=True))
      yield generation

  def display(self):
    """Prints the current population"""
    print "%10s %4s %7s %6s" % ("bin", "int", "fitness", "elite")
    for member in self.population:
      if self.elite_member == member:
        elite = "ELITE"
      elif self.params.elitism:
        elite = "-"
      else:
        elite = "n/a"
      print "%10s %4s %7.2f %6s" % \
          (decode(member), member, fitness(member), elite)
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
  ap.add_argument("-t", "--selection_strategy",
                  default=Defaults.SELECTION_STRATEGY, type=str,
                  choices=["fitness-proportional", "uniform"],
                  help="The strategy to use for selection and crossover.")
  ap.add_argument("-e", "--elitism", default=Defaults.ELITISM,
                  action="store_true",
                  help="Whether to use elitism (don't mutate best member).")
  args_dict = vars(ap.parse_args())
  params = Params(**args_dict)
  ga = GeneticAlgo(params)
  ga.initialize()

  for i in ga.evolve():
    print "Generation", i + 1
    ga.display()
    print ""
