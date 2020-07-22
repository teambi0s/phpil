# phpil

A Fuzzer for the PHP language. The core concept is based on
[Fuzzili](https://github.com/googleprojectzero/fuzzilli). Basically, its a port
of Fuzzili, re-written in python for PHP :).

Currently only code generation is present. A python module for collecting
clang’s sanitizer-coverage is present in [coverage](/coverage).

We did this as a course project for the college, but the course got completed
before we completed the entire fuzzer :). So it currently its a random php
program generator. Might work more on this if we find time later. 

To run simply do 

``` sh
python main.py
```

That will print out a syntactically and semantically correct PHP code sample.


## How it works

It works in a similar manner as Fuzzili. The fuzzing is done on a IR (PHPIL). A
lifter lifts the PhpIL code to the PHP code when all the processing for the
sample is done. The intermediate language (PHPIL) has opcodes which should on a
high level cover most of the PHP functionalities (we did not do it for all the
functionalities yet). Here is a high level overview of the working - 

- [Code Generators](/PhpIL/code_generators.py) - The code generators use the
opcodes to generate blocks of semantically and syntactically correct code. This
code is still in PhpIL. Once a block of code is generated, it is passed on to
the analyzers for further analysis.

- [Analyzers](/PhpIL/analyzer.py) - Currently supports 3 types of analysis -
    - Scope Analyzer - keeps track of the scope of each of the
variables that is currently in use.
    - Context Analyzer - This is used to keep track of the program context. For
example, we don’t want to emit a ‘return‘ instruction when we
are not even within a function. 
    - Type Analyzer - Its used to infer the types of the variables used
in the input program. 

- [lifter](/PhpIL/lifter.py) - Finally we need to convert the PHPIL code to PHP
  code. This job is taken care of by the lifter. 

## Other notes

* Coverage - We can use clang sanitizer coverage to track the code coverage
  dynamically. For this we just need to compile php with the right options.
  [phpcov.c](coverage/phpcov.c) is a python module to track the code coverage in
  python. This is very similar to Fuzzili. We use a shared memory region to
  share the coverage data between the fuzzer and the binary. It has not been
  integrated yet though.

* [program_builder](PhpIL/program_builder.py) - used to keep track of the
  current program that is being built/modified. Basically, its an instance of a
  PhpIL program.

* [settings](PhpIL/settings.py) - Governs the probability of a code generator
  being selected. The higher the value of a code generator, the more likely it
  is to appear in the sample. If zero, it will never appear.

## TODOs

Of course there are many things left. To name a few -
* Mutation
* Coverage
* Sane selection of integers/strings
* Execution and crash tracking
  
## Authors 

* [Vignesh Rao](https://twitter.com/sherl0ck__)
* [Tarunkant Gupta](https://twitter.com/TarunkantG)
* [Saastha Vasan](https://twitter.com/ThinkMalicious)

