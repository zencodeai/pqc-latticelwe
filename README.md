# Lattice & LWE based cryptography 

## Introduction

This project is a simple Python example that implements a toy version of an LWE‐based encryption scheme. **Note:** This is a very simplified version meant for educational purposes and should not be used in any production system. Real-world implementations require carefully chosen parameters, robust error distributions (often discrete Gaussians), and extensive security analysis.

## Description

In this example, we work modulo a small integer $`q`$ (the modulus), use small dimensions, and choose the error from a tiny set (e.g. $`\{ -1, 0, 1 \}`$). The scheme works for encrypting a single bit. The idea is as follows:

1. **Key Generation:**  
   - Choose a secret vector $\mathbf{s} \in \mathbb{Z}_q^n$ uniformly at random.
   - Generate a random matrix $\mathbf{A} \in \mathbb{Z}_q^{m \times n}$.
   - Sample a small error vector $\mathbf{e} \in \mathbb{Z}_q^m$.
   - Compute $`\mathbf{b} = ( \mathbf{A}\mathbf{s} + \mathbf{e} ) \mod{q}`$.
   - Public key: $`( \mathbf{A}, \mathbf{b} )`$  
     Private key: $`\mathbf{s}`$

2. **Encryption:**
   - Encryption of bit $`\mu \in \{ 0,1 \}`$
   - Choose a random binary vector $` \mathbf{r} \in \{0,1\}^m`$ (or one with small Hamming weight).
   - Compute<br>
     $`\mathbf{u} = \mathbf{r}^T \mathbf{A} \quad (\text{in } \mathbb{Z}_q^n)`$<br>
     $`v = \mathbf{r}^T \mathbf{b} + \left\lfloor \frac{q}{2} \right\rfloor \mu \quad (\text{in } \mathbb{Z}_q)`$
   - The ciphertext is $`(\mathbf{u}, v)`$.

4. **Decryption:**  
   - Compute $`v' = ( v - \mathbf{u} \cdot \mathbf{s} ) \mod q`$.
   - If $`v'`$ is closer to $`0`$ than to $`\lfloor q/2 \rfloor`$ (in modulo $`q`$ arithmetic), then the decrypted bit is $`0`$; otherwise, it is $`1`$.


## Implementation

- **Key Generation (`keygen`):**  
  - We randomly generate the secret $`\mathbf{s}`$ and matrix $`\mathbf{A} \in \mathbb{Z}_q`$.
  - A small error vector $`\mathbf{e}`$ is sampled from $`\{-1, 0, 1\}`$.
  - The vector $`\mathbf{b}`$ is computed as $`(\mathbf{A}\mathbf{s} + \mathbf{e}) \mod{q}`$.

- **Encryption (`encrypt`):**  
  - A random binary vector $`\mathbf{r}`$ is chosen.
  - The vector $`\mathbf{u} = \mathbf{r}^T \mathbf{A}`$ and scalar $`v = \mathbf{r}^T \mathbf{b} + \lfloor q/2 \rfloor \mu`$ are computed modulo  $`q`$.

- **Decryption (`decrypt`):**  
  - The decryption computes $`v' = (v - \mathbf{u} \cdot \mathbf{s}) \mod{q}`$.
  - By comparing $`v'`$ with the threshold (roughly $`q/4`$ and $`3q/4`$), the original bit is recovered.

Again, this implementation is a simplified toy model. In practice, the parameters (like $`n`$, $`m`$, $`q`$), the error distribution, and the precise decision thresholds must be carefully chosen to ensure both correctness and security.

## Notes:

- Created with the help of ChatGPT o3-mini
