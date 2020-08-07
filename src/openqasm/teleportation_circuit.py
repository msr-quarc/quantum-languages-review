from qiskit import *
from qiskit.circuit import *

def prepare_bell_pair(circuit, left, right):
    """
    Adds the gates to the given circuit to prepare a Bell state between the two qubits.
    :type circuit: QuantumCircuit
    :type left:    Qubit
    :type right:   Qubit
    """
    circuit.h(left)
    circuit.cx(left, right)

def adjoint_prepare_bell_pair(circuit, left, right):
    """
    Adds the gates to the given circuit that implement the adjoint of the sequence of 
    gates added by prepare_bell_pair.
    :type circuit: QuantumCircuit
    :type left:    Qubit
    :type right:   Qubit
    """
    # Qiskit supports generating the adjoint for QuantumCircuit instances, but
    # in this case it is more convenient to just implement it as python function.
    circuit.cx(left, right)
    circuit.h(left)

def teleport(circuit, msg, helper, target, corrz, corrx):
    """
    Adds the gates to the given circuit that teleport the state of the 'msg' qubit 
    to the given 'target' qubit using the 'helper' qubit as a resource, and
    using the classical registers corrz and corrx to store the measurement results.
    :type circuit: QuantumCircuit
    :type msg:     Qubit
    :type helper:  Qubit
    :type target:  Qubit
    :type corrz:   ClassicalRegister
    :type corrx:   ClassicalRegister
    """
    prepare_bell_pair(circuit, helper, target)
    adjoint_prepare_bell_pair(circuit, msg, helper)
    # Add the gates to measure the message and the helper qubit in the computational 
    # basis and store the results in the classical registers corrz and corrx.
    circuit.measure(msg, corrz[0])
    circuit.measure(helper, corrx[0])
    # Add the gates to apply a Pauli correction conditional on the stored outcomes 
    # of the single-qubit measurements in computational basis.
    # Note that c_if expects a ClassicalRegister, which is why we need two of them.
    circuit.z(target).c_if(corrz, 1)
    circuit.x(target).c_if(corrx, 1)

def prepare_message(prep):
    """
    Constructs and returns a QuantumCircuit instance that applies the given state 
    preparation routine to a single qubit. 
    :type prep: Callable[[QuantumCircuit, Qubit], None]
    """
    qubits = QuantumRegister(1, "qubits")
    circuit = QuantumCircuit(qubits, name="prep")
    prep(circuit, qubits[0])
    return circuit

def teleportation_experiment(prep):     
    """
    Constructs and returns a QuantumCircuit instance containing a teleportation experiment. 
    If the experiment succeeds, then the last classical bit in the circuit will be 0.
    :type prep: Callable[[QuantumCircuit, Qubit], None]
    """
    # We need to declare all quantum and classical registers that are going to be 
    # used as part of the circuit before we can construct the circuit instance.
    qubits = QuantumRegister(3, "qubits")
    msg, helper, target = map(lambda idx: qubits[idx], range(3))
    # Branching conditional on measurements outcomes requires passing in a classical 
    # register, hence we construct a separate register for the x- and z-correction.
    corrz = ClassicalRegister(1, "corrz")
    corrx = ClassicalRegister(1, "corrx")
    # We also need a classical register to store the measurement outcome that 
    # indicates whether the teleportation succeeded.
    final = ClassicalRegister(1, "final")

    # We construct a separate subcircuit implementing the passed in state preparation 
    # function such that we can easily invert it later. 
    prep = prepare_message(prep)

    # We create a QuantumCircuit instance to which we then add gates.
    circuit = QuantumCircuit(qubits, corrz, corrx, final, name="teleport")
    # We plug the constructed subcircuit for preparing the message to teleport 
    # into the circuit and teleport the message. 
    circuit.append(prep.to_instruction(), [msg])
    teleport(circuit, msg, helper, target, corrz, corrx)
    # We apply the inverse of the message preparation circuit to the target qubit.  
    # If the target qubit is in the intended state, this will map it to $\ket{0}$.
    circuit.append(prep.inverse().to_instruction(), [target])
    # If the message is teleported successfully this measurement should always be 0.
    circuit.measure(target, final[0])
    return circuit

