module Teleport where
import Quipper

-- Prepares a Bell state given two qubits in a computational basis state.
prepareEntangledPair :: (Qubit, Qubit) -> Circ (Qubit, Qubit) 
prepareEntangledPair (left, right) = do
    gate_H_at left
    right <- qnot right `controlled` left
    return (left, right)

-- Teleports the state of the 'msg' qubit to the given 'target' qubit 
-- using the 'helper' qubit as a resource.
teleport :: (Qubit, Qubit, Qubit) -> Circ (Qubit)
teleport (msg, helper, target) = do
    (helper, target) <- prepareEntangledPair (helper, target)
    -- The Adjoint of a Bell preparation is a Bell measurement.
    (msg, helper) <- reverse_simple prepareEntangledPair (msg, helper)
    -- We apply a Pauli correction based on the Bell measurement.
    (z, x) <- measure (msg, helper) -- measuring two qubits in computational basis
    target <- gate_X target `controlled` x -- X classically controlled on bit x
    target <- gate_Z target `controlled` z -- Z classically controlled on bit z
    cdiscard (z, x) -- discarding classical bits
    return target

-- Checks that the Teleport operation correctly teleports
-- half of an entangled pair.
teleportTest :: Circ Qubit
teleportTest = do
    with_ancilla $ \reference -> do
        (msg, helper, target) <- qinit (False, False, False)
        (reference, msg) <- prepareEntangledPair (reference, msg)
        target <- teleport (msg, helper, target)
        -- If the teleportation circuit is correct joint state
        -- of `reference` and `target` must be a Bell pair
        (reference, target) <-
            reverse_simple prepareEntangledPair (reference, target)
        -- using with_ancilla asserts that `reference` is in state zero
        return target
