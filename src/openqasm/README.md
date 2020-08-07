# Qiskit/OpenQASM Docker container

## Running this sample

To build and run this sample, execute the following commands:

```
cd src/openqasm
docker build -t openqasm .
docker run -it openqasm
python run_teleportation.py 
```

## Building and running other Qiskit code

Qiskit is embedded into python and can be run using the python interpreter just like any other python code: 
```cmd
python my_program.py
```
