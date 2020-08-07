# Quipper 0.9 Docker container

## Running this sample

To build and run this sample, execute the following commands:

```cmd
docker build -t quipper . 
docker run -it quipper
./run_teleportation
```

## Building and running other Quipper code

Note that the teleportation example is already built as part of the Docker container setup. In general, to build and run other Quipper programs, run 
```cmd
./build.sh my_program.hs
```
from within the container. If my_program.hs contains a main function, this will produce the corresponding my_program file that can then be run with the command 
```cmd
./my_program
```

## Useful reference and documentation

* [Project home page](https://www.mathstat.dal.ca/~selinger/quipper/)
* [Quipper: A Scalable Quantum Programming Language](https://arxiv.org/pdf/1304.3390.pdf)
  [doi:10.1145/2491956.2462177](https://doi.org/10.1145/2491956.2462177)
* [Quipper reference](https://www.mathstat.dal.ca/~selinger/quipper/doc/)
