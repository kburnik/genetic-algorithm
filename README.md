# Genetic algorithm

A simple python implementation of a genetic algorithm.

We start with a population which has individuals of chromosome length of 10
bits. The fitness functions is predefined and you can see it in
[this graph](http://bit.ly/ui-lab5-dobrota-graf).

Fitness proportionate selection algorithm is used for population selection.
No elitism is involved. Crossing over is done as a single point cross over.
Mutation is done by flipping random number of bits up to 9.

You can use command line arguments to control the genetic parameters.

```
python ga.py -h
```

The program will output the random seed used to stderr so you can reproduce each
run.

Problem author is
[Dr.sc. Marko Horvat, dipl. ing.](http://marko-horvat.name/site/).
