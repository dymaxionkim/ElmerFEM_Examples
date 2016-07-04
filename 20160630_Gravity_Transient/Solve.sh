#!/bin/bash


ElmerGrid 2 2 ./mesh -metis 4
mpirun -np 4 ElmerSolver_mpi

