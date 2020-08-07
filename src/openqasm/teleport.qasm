// All OpenQASM programs begin with a header indicating the language version.
OPENQASM 2.0;
include "qelib1.inc";

// We need to declare all quantum and classical registers that are going to be used.
// We will use qubits[0] as the qubit containing the message ('msg'), qubits[1] as 
// the helper qubit ('helper'), and qubits[2] as the target qubit ('target').
qreg qubits[3];
// Branching conditional on measurements outcomes requires passing in a classical 
// register, hence we construct a separate register for the x- and z-correction.
creg corrz[1];
creg corrx[1];
// We also need a classical register to store the measurement outcome that 
// indicates whether the teleportation succeeded.
creg final[1];

// We prepare the state $\ket{+}$ to teleport.
h qubits[0];

// Prepares a Bell state between the helper and the target qubit.
h qubits[1];
cx qubits[1], qubits[2];

// Perform the inverse operation on the message and helper qubit.
cx qubits[0], qubits[1];
h qubits[0];

// We measure the message and the helper qubit in the computational basis
// and store the results in the classical registers corrz and corrx.
measure qubits[0] -> corrz[0]; //* \label{lst:openqasm:teleport:measure}
measure qubits[1] -> corrx[0];

// We apply a Pauli correction conditional on the stored outcomes of 
// the single-qubit measurements in computational basis.
if (corrz==1) z qubits[2]; //* \label{lst:openqasm:teleport:correction}
if (corrx==1) x qubits[2];

// If the target qubit is indeed in a $\ket{+}$ state, this will map it to $\ket{0}$.
h qubits[2];

// If the message is teleported successfully this measurement should always be 0.
measure qubits[2] -> final[0];
