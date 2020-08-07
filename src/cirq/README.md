# Cirq Docker container

## Running this sample

To build and run this sample, execute the following commands:

```
cd src/cirq
docker build -t cirq .
docker run -it cirq
python teleport.py
```

## Building and running other Cirq code

Cirq is embedded into python and can be run using the python interpreter just like any other python code: 
```cmd
python my_program.py
```

