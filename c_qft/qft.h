#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef QFT_H
#define QFT_H

#include <complex.h>

void qft(int n,double complex *state);

void inverse_qft(int n,double complex *state);

#endif