#!/bin/bash

rm -R case01
rm -R case02
rm -R case03
rm -R case04

mkdir case01
mkdir case02
mkdir case03
mkdir case04

ElmerSolver case01.sif > case01.log &
ElmerSolver case02.sif > case02.log &
ElmerSolver case03.sif > case03.log &
ElmerSolver case04.sif > case04.log &

exit 0

