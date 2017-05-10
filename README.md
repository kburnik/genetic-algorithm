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

## Evaluation

You can evaluate the performance (convergence) with the following script:

```sh
# 1024 is chosen to be able to fit on the same graph as the fitness function.
for i in $(seq 0 1023); do
  echo $i $(python ga.py 2>/dev/null | \
            grep "max" | \
            tail -n 1 | \
            cut -f 2 -d ',' | \
            sed s"/ max = //");
done > eval.txt
```

And then visualize the results in in excel/google sheets like
[here](https://docs.google.com/spreadsheets/d/1b0Tjra9tDq3530ZUAoBu_7oIPzdg1NLM0HyxdCvkgns/edit#gid=1612904409).

## Sample reproducable run at near global optimum

```sh
python ga.py -s 175792354
```

Sample Output (STDOUT only)

```
Generation 1
       bin  int fitness
1101100101  869  238.50
1101100101  869  238.50
1001110110  630  180.00
1001111001  633  176.00
0100111000  312  174.00
1001011110  606  144.00
1010100001  673  122.67
0001100011   99  120.00
1100001010  778  102.00
0011101111  239   95.75
0000110000   48   78.00
0000101100   44   74.00
0000010001   17   60.00
0000000001    1   60.00
0011010000  208   46.67
0111101011  491   34.20
0111110011  499   19.80
0111111110  510    0.00
1111100110  998    0.00
1111110001 1009    0.00
min = 0.00, max = 238, avg = 98.20

...

Generation 30
       bin  int fitness
0101101001  361  268.20
0101100110  358  266.00
0101110100  372  248.40
0101001110  334  218.00
1101010101  853  214.50
1101111101  893  178.66
1110000000  896  170.66
1010010011  659  141.34
0001111011  123  117.50
0011111010  250  115.00
0000101111   47   77.00
1011111001  761   76.50
0010111100  188   63.33
0011000000  192   60.00
0000001000    8   60.00
1000100011  547   55.50
1000001110  526   24.00
1111100010  994    0.00
1111100110  998    0.00
1111110001 1009    0.00
min = 0.00, max = 268, avg = 117.73
```
