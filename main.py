import numpy as np


def mod_q(x, q):
    """Helper function to compute modulo q correctly for both scalars and arrays."""
    return np.remainder(x, q)


def keygen(n, m, q):
    """
    Generates a public and private key for the LWE encryption scheme.

    Parameters:
      n : int -- dimension of the secret vector
      m : int -- number of LWE samples (rows of A)
      q : int -- modulus

    Returns:
      public_key: (A, b) where A is an (m x n) matrix and b is an m-dimensional vector.
      secret_key: s, the secret n-dimensional vector.
    """
    # Secret key: a random vector in Z_q^n
    s = np.random.randint(0, q, size=n)

    # Public key generation:
    A = np.random.randint(0, q, size=(m, n))

    # Error vector: choose small errors; here, we choose uniformly from {-1, 0, 1}
    e = np.random.choice([-1, 0, 1], size=m)

    # Compute b = A*s + e (mod q)
    b = mod_q(np.dot(A, s) + e, q)

    return (A, b), s


def encrypt(public_key, mu, q):
    """
    Encrypts a single bit message mu using the public key.

    Parameters:
      public_key: tuple (A, b) from keygen.
      mu : int -- message bit (0 or 1)
      q : int -- modulus

    Returns:
      ciphertext: (u, v)
    """
    A, b = public_key
    m = A.shape[0]

    # Choose random binary vector r in {0,1}^m
    r = np.random.randint(0, 2, size=m)

    # Compute u = r^T * A (note: u is a 1 x n vector)
    u = mod_q(np.dot(r, A), q)

    # Compute v = r^T * b + floor(q/2)*mu mod q
    v = mod_q(np.dot(r, b) + (q // 2) * mu, q)

    return (u, v)


def decrypt(ciphertext, s, q):
    """
    Decrypts the ciphertext using the secret key s.

    Parameters:
      ciphertext: tuple (u, v) from encryption.
      s: secret key vector.
      q: modulus.

    Returns:
      Decrypted bit (0 or 1)
    """
    u, v = ciphertext

    # Compute inner product u · s (note: u is 1 x n and s is n-dimensional)
    inner = np.dot(u, s) % q
    v_prime = mod_q(v - inner, q)

    # Decide based on whether v_prime is closer to 0 or to q/2.
    # Here we use q/4 as a threshold for a simple decision.
    # For a robust scheme, the threshold would depend on the error distribution.
    if v_prime < q/4 or v_prime > 3*q/4:
        return 0
    else:
        return 1


def main():
    # Parameters (these are toy parameters for demonstration)
    n = 10   # dimension of the secret vector
    m = 30   # number of LWE samples (rows of A)
    q = 97   # modulus (a small prime)

    # Key generation
    public_key, secret_key = keygen(n, m, q)
    print("Public Key (A, b):")
    print("A =", public_key[0])
    print("b =", public_key[1])
    print("Secret Key s =", secret_key)

    # Encrypt a bit (0 or 1)
    message = np.random.randint(0, 2)
    print("\nOriginal message:", message)

    ciphertext = encrypt(public_key, message, q)
    print("Ciphertext (u, v):")
    print("u =", ciphertext[0])
    print("v =", ciphertext[1])

    # Decrypt the ciphertext
    decrypted_message = decrypt(ciphertext, secret_key, q)
    print("Decrypted message:", decrypted_message)

    if decrypted_message == message:
        print("Decryption successful!")
    else:
        print("Decryption failed.")


if __name__ == "__main__":
    main()
