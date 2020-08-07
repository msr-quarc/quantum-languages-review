import Teleport
import System.Random
-- The core Quipper module provides functions like print_simple.
import Quipper
-- This module provides simulators for use with Quipper.
import Quipper.Libraries.Simulation -- simulation functions including run_generic

main :: IO ()
main = do

  -- Print out the circuit using the print_simple function.
  print_simple ASCII teleportTest

  -- Show the circuit in the previewer.
  -- We haven't enabled any GUI features for compatibility with the Docker image,
  -- but the following line can be uncommented when running outside the container.
  -- print_simple Preview teleportTest

  -- Show gate counts for the circuit.
  print_simple GateCount teleportTest

  -- Efficiently simulate the circuit using the Clifford simulator.
  run_clifford_generic teleportTest >>= print

  -- Simulate the circuit using the full state-vector simulator.
  random_number_generator <- newStdGen
  print $ run_generic random_number_generator (0.0 :: Double) teleportTest

