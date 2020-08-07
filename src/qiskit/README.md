# Qiskit/OpenQASM Docker container

## Running this sample

To build and run this sample, execute the following commands:

```
cd src/qiskit
docker build -t qiskit .
docker run -it qiskit
python run_teleportation.py 
```

## Building and running other Qiskit code

Qiskit is embedded into python and can be run using the python interpreter just like any other python code: 
```cmd
python my_program.py
```
