#!/usr/bin/env python3
from __future__ import division, print_function, absolute_import

import subprocess
from subprocess import DEVNULL
import os
import fileinput

import numpy as np
from numpy import pi

# This assumes that NekCEM and NekCEM-Examples live in the same
# top-level directory; the user should adjust as needed.
NEK = os.path.abspath(os.path.join('..', '..', 'NekCEM', 'bin', 'nek'))

c0 = 299792458.0e6
l0 = 1.0
hbar = 6.582e-16


class ReaState():
    """Change an `.rea` file upon entering and restore it upon exit."""
    def __init__(self, name, params):
        self.rea = name + '.rea'
        self.params = params
        self.old_params = {}
        self.offset = 4

    def __enter__(self):
        for i, line in enumerate(fileinput.input(self.rea, inplace=True)):
            try:
                print('  {}'.format(self.params[i-self.offset+1]))
                self.old_params[i] = line
            except KeyError:
                print(line, end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i, line in enumerate(fileinput.input(self.rea, inplace=True)):
            try:
                print(self.old_params[i], end='')
            except KeyError:
                print(line, end='')


def main():
    lmbdas = np.linspace(1.5, 3.0, 16)
    Ts = []

    for lmbda in lmbdas:
        omega = 1.240/lmbda # eV
        omega = l0*omega/(c0*hbar) # rad
        fintim = 10*2*pi/omega

        params = {}
        params[10] = fintim
        params[60] = lmbda
        with ReaState('tungsten2d', params):
            print("Running lmbda = {}...".format(lmbda))
            subprocess.run([NEK, 'tungsten2d', '4'],
                           stdout=DEVNULL, stderr=DEVNULL)

            with open('tungsten2d.np=4.output') as log:
                for line in log:
                    if 'transmittance' in line:
                        Ts.append(float(line.split()[1]))
        with open('data.txt', 'w') as f:
            f.write('lambda eps_s\n')
            for lmbda, T in zip(lmbdas, Ts):
                f.write('{} {}\n'.format(lmbda, T))


if __name__ == '__main__':
    main()
