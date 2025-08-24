#include "qft.h"


#define PI 3.14159265358979323846

// QFT
void qft(int n, double complex *state) {
    int dim = 1 << n;  // 2^n
    double complex *out = calloc(dim, sizeof(double complex));

    for (int k = 0; k < dim; k++) {
        for (int j = 0; j < dim; j++) {
            double angle = 2 * PI * j * k / dim;  
            out[k] += state[j] * cexp(I * angle) / sqrt(dim);
        }
    }

    for (int i = 0; i < dim; i++) state[i] = out[i];
    free(out);
}

// inverse QFT
void inverse_qft(int n, double complex *state) {
    int dim = 1 << n;
    double complex *out = calloc(dim, sizeof(double complex));

    for (int k = 0; k < dim; k++) {
        for (int j = 0; j < dim; j++) {
            double angle = -2 * PI * j * k / dim;   
            out[k] += state[j] * cexp(I * angle) / sqrt(dim);
        }
    }

    for (int i = 0; i < dim; i++) state[i] = out[i];
    free(out);
}

int main() {
    int n ; 
    printf("Enter the number of qubits: ");
    scanf("%d",&n);
    int dim = 1 << n;

    
    double complex *state = calloc(dim, sizeof(double complex));
    state[1] = 1.0 + 0.0*I;

    printf("Initial state |001>:\n");
    for (int i = 0; i < dim; i++) {
        printf("  %2d: %.3f + %.3fi\n", i, creal(state[i]), cimag(state[i]));
    }

    // Apply QFT
    qft(n, state);
    printf("\nAfter QFT:\n");
    for (int i = 0; i < dim; i++) {
        printf("  %2d: %.3f + %.3fi\n", i, creal(state[i]), cimag(state[i]));
    }

    // Apply inverse QFT
    inverse_qft(n, state);
    printf("\nAfter inverse QFT (should return to |001>):\n");
    for (int i = 0; i < dim; i++) {
        printf("  %2d: %.3f + %.3fi\n", i, creal(state[i]), cimag(state[i]));
    }

    free(state);
    return 0;
}