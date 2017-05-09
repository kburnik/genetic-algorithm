BITCOUNT = 10
"""Number of bits for a species member (cromosome length)."""

def fitness(member):
  """Computes the fitness of a species member.
     http://bit.ly/ui-lab5-dobrota-graf"""
  if member < 0 or member >= 1024:
    return -1
  elif member >= 0 and member < 30:
    return 60.0
  elif member >= 30 and member < 90:
    return member + 30.0
  elif member >= 90 and member < 120:
    return 120.0
  elif member >= 120 and member < 210:
    return -0.83333 * member + 220
  elif member >= 210 and member < 270:
    return 1.75 * member - 322.5
  elif member >= 270 and member < 300:
    return 150.0
  elif member >= 300 and member < 360:
    return 2.0 * member - 450
  elif member >= 360 and member < 510:
    return -1.8 * member + 918
  elif member >= 510 and member < 630:
    return 1.5 * member - 765
  elif member >= 630 and member < 720:
    return -1.33333 * member + 1020
  elif member >= 720 and member < 750:
    return 60.0
  elif member >= 750 and member < 870:
    return 1.5 * member - 1065
  elif member >= 870 and member < 960:
    return -2.66667 * member + 2560
  else:
    return 0

if __name__ == "__main__":
  for i in range(0, 1024):
    print i, fitness(i)
