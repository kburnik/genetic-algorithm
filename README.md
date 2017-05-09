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

## Sample reproducable run at near global optimum

```sh
python ga.py -s 175792354
```

Sample Output (STDOUT only)

```
Generation 1
       bin  int fitness
0101110111  375  243.00
0101110111  375  243.00
1101100100  868  237.00
1101100100  868  237.00
0101001100  332  214.00
0100001111  271  150.00
1001100001  609  148.50
1001100001  609  148.50
0110110011  435  135.00
0110110011  435  135.00
0110110011  435  135.00
0010000100  132  110.00
0010001001  137  105.83
0010001001  137  105.83
0010001001  137  105.83
0000101001   41   71.00
0010111011  187   64.17
0010111011  187   64.17
0010111000  184   66.67
1011011011  731   60.00
min = 60.00, max = 243, avg = 138.98

Generation 2
       bin  int fitness
0101110111  375  243.00
0101110111  375  243.00
1101100100  868  237.00
1101100100  868  237.00
1101100100  868  237.00
1101100100  868  237.00
1101100100  868  237.00
1101100100  868  237.00
0100001111  271  150.00
0100001111  271  150.00
1001100001  609  148.50
1001100001  609  148.50
0110100100  420  162.00
0010010011  147   97.50
0010011000  152   93.33
0010101001  169   79.17
0010111000  184   66.67
0010111011  187   64.17
0010111011  187   64.17
0010111011  187   64.17
min = 64.17, max = 243, avg = 159.81

...

Generation 30
       bin  int fitness
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101100111  359  268.00
0101111000  376  241.20
0101111000  376  241.20
0101111000  376  241.20
0101111000  376  241.20
min = 241.20, max = 268, avg = 262.64
```
