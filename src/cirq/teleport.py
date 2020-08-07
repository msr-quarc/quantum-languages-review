from cirq import *
from cirq.ops import *

def prepare_bell_pair(left, right):
    """
    Prepares a Bell state given two qubits in a computational basis state.
    :type left:  LineQubit
    :type right: LineQubit
    """
    yield H(left)
    yield CNOT(left, right)

def teleport(msg, helper, target):
    """
    Teleports the state of the 'msg' qubit to the given 'target' qubit 
    using the 'helper' qubit as a resource.
    :type msg:    LineQubit
    :type helper: LineQubit
    :type target: LineQubit
    """
    yield prepare_bell_pair(helper, target)
    yield inverse(prepare_bell_pair(msg, helper))
    # We apply a Pauli correction in a coherent manner, as Cirq does not
    # support applying operations conditional on a measurements outcome.
    yield CZ(msg, target)
    yield CNOT(helper, target)

def teleportation_experiment(prep):
    """
    Constructs and returns a Circuit instance containing a teleportation experiment. 
    If the experiment succeeds, then the final measurement of the target qubit will be 0.
    :type prep: Gate
    """
    # We will use three qubits on a line.
    msg, helper, target = map(LineQubit, range(3))

    # We create a Circuit instance to which we then add gates.
    circuit = Circuit()
    # We add the gates to prepare the message to teleport using the given 
    # preparation routine and teleport the message.
    circuit.append(prep(msg))
    circuit.append(teleport(msg, helper, target))
    # If the target qubit is in the intended state, this will map it to $\ket{0}$.
    circuit.append(inverse(prep(target)))
    circuit.append(measure(target, key="final"))
    return circuit

def run_experiment(circuit):
    """
    Executes the given Circuit on the simulator and returns the histogram. 
    :type circuit: Circuit
    """
    # We simulate circuits using the local simulator. 
    backend = Simulator()
    # We repeat the simulation 100 times, and return the histogram.
    # The returned histogram contains the result of all measurements in all runs.    
    result = backend.run(circuit, repetitions=100)
    return result.histogram(key="final")


if __name__ == "__main__":
    # We choose to teleport a $\ket{+}$ state, 
    # but any adjointable state preparation routine could be passed in here. 
    circuit = teleportation_experiment(H)
    data = run_experiment(circuit)

    # We check whether the teleportation succeeded for all shots, 
    # i.e. we check if the final measurement was always 0.
    is_correct = lambda key: key == 0
    success = all(map(is_correct, data.keys()))
    
    if success: print("\nTeleportation succeeded!")
    else: print("\nTeleportation failed.")

    # We additionally print the histogram of the measured value for all shots, 
    # emit the executed circuit, and print the matrix representation of the circuit.
    print("\nFull histogram:")
    print(data)
    print("\nCircuit:")
    print(circuit)
    print("\nMatrix representation:")
    print(unitary(circuit))

