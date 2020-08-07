from qiskit import *
import argparse # used to process command line arguments
from teleportation_circuit import * # custom teleportation implementation in Qiskit

def run_experiment(circuit):
    """
    Executes the given QuantumCircuit on the qasm_simulator and returns the histogram. 
    :type circuit: QuantumCircuit
    """
    # Qiskit Aer allows to simulate circuits using one of several different backends.
    backend = BasicAer.get_backend('qasm_simulator')

    # We can send the constructed circuit to an Aer backend to get an object 
    # that represents the asynchronous execution of our circuit.
    # We repeat the simulation 100 times, and return the histogram.
    job = execute(circuit, backend, shots=100)

    # The result of a job tells us whether the job completed successfully, 
    # and all measurement results obtained during the job.
    result = job.result()
    return result.get_counts(circuit)


if __name__ == "__main__":
    # We do some minimal command line parsing to allow giving a qasm file as input.
    parser = argparse.ArgumentParser()
    parser.add_argument("--qasm", dest="qasm")
    args = parser.parse_args()

    if args.qasm: 
        # Qiskit Terra allows to load an OpenQASM file and compile it to a circuit.
        print("Loading circuit from file " + args.qasm + ".")
        circuit = QuantumCircuit.from_qasm_file(args.qasm)
    else: 
        # Alternatively, we can also construct the circuit in Qiskit.
        print("Running the circuit returned by teleportation_experiment.")
        # We choose to teleport a $\ket{+}$ state, 
        # but any function for the preparation routine could be passed in here. 
        circuit = teleportation_experiment(lambda prep, q: prep.h(q))

    data = run_experiment(circuit)

    # We check whether the teleportation succeeded for all shots, 
    # i.e. we check if the final measurement was always 0.
    is_correct = lambda key: key.startswith('0')
    success = all(map(is_correct, data.keys()))

    if success: print("\nTeleportation succeeded!")
    else: print("\nTeleportation failed.")

    # We additionally print the histogram of the measured values for all shots. 
    # and emit the executed circuit. A matrix representation cannot be printed
    # since the circuit is not unitary. 
    print("\nFull histogram:")
    print(data)
