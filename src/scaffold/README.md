# ScaffCC Docker container

## Running this sample

To build and run this sample, execute the following commands:

```cmd
docker build -t scaffcc .
docker run -ti scaffcc
cd /src
make
cat teleport.qasm
cat teleport.resources
```

Regression tests in `/root/ScaffCC/scripts/regression_test.sh`
pass without problem.

## Building and running other Scaffold code

Note that the teleportation example is already built as part of the Docker container setup. In general, to get the OpenQASM code for a Scaffold program, run 
```cmd
scaffold.sh -b my_program.scaffold
```
from within the container. This will produce the corresponding my_program.qasm file. To get the resources estimation (a my_program.resources file), run 
```cmd
scaffold.sh my_program.scaffold
```

## Useful reference and documentation

[Scaffold manual](http://www.dtic.mil/dtic/tr/fulltext/u2/a571279.pdf) is 
a bit outdated and uses `qreg` instead of `qbit`.

## Knwon issues 

So far running `scaffold.sh -f teleport.scaffold` produces wrong QASM output.