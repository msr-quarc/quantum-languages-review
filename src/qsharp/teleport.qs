namespace Microsoft.Quantum.Samples {

    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;

    /// # Summary
    /// Prepares a Bell state given two qubits in a computational basis state.
    operation PrepareBellPair(left : Qubit, right : Qubit) : Unit is Adj + Ctl { //*\label{lst:qsharp:teleport:bell}*//
        H(left);
        CNOT(left, right);
    }

    /// # Summary
    /// Teleports the state of the 'msg' qubit to the given 'target' qubit,
    /// by temporarily using a 'helper' qubit as a resource.
    operation Teleport(msg : Qubit, target : Qubit) : Unit {
        // Q# supports local allocations of qubits. 
        using (helper = Qubit()) {
            PrepareBellPair(helper, target);
            Adjoint PrepareBellPair(msg, helper); //*\label{lst:qsharp:teleport:bell-adj-invokation}*//
            // We apply a Pauli correction conditional on the outcomes of 
            // single-qubit measurements in computational basis.
            (M(msg)  == One ? Z | I)(target);
            (M(helper) == One ? X | I)(target);
        }
    }

    /// # Summary
    /// Executes a teleportation experiment. 
    /// If it succeeds, then the returned measurement result is Zero. 
    operation TeleportationExperiment(prep : (Qubit => Unit is Adj + Ctl)) : Result {
        // We allocate new qubits for the duration of the block. 
        using ((msg, target) = (Qubit(), Qubit())){
            // We prepare the message to teleport using the given 
            // preparation routine and teleport the message.
            prep(msg);
            Teleport(msg, target);
            // If the target qubit is in the intended state, this will map it to $\ket{0}$.
            Adjoint prep(target);
            return M(target);
        }
    }

    /// # Summary
    /// Unit test to check that various states are teleported correctly.
    // The Test attribute defines the target on which the test will be executed.  
    // "QuantumSimulator" indicates that the test will be executed on the full 
    // state simulator.
    @Test("QuantumSimulator")
    operation TeleportTest() : Unit {
        // We want to execute the teleportation experiment for various messages.
        let messages = [H, X, T];
        for(rep in 1 .. 100) {
            // We run the teleporation experiment for each message.
            let results = ForEach(TeleportationExperiment, messages);
            // We check that each run returned Zero using unit testing tools.
            // 'Fact' will fail and print the give string if success is false.
            let success = All(IsResultZero, results);
            Fact(success, "Teleportation failed.");
        }
    }
}
