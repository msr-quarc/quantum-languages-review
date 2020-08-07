#! /bin/bash

ghc -O -rtsopts -with-rtsopts=-K50m -i"/src/quipper-0.9/quipper" -i"/src/quipper-0.9" -fwarn-incomplete-patterns "$@"