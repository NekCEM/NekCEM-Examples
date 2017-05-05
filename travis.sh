#!/bin/bash

EXAMPLESDIR=$PWD
NEKDIR=~/NekCEM

cd ~
git clone --depth 50 https://github.com/NekCEM/NekCEM
cd $EXAMPLESDIR
~/NekCEM/bin/runtests --build-only --np 2
