def div(a, b):
    """
    Returns a/b
    """
    if b != 0:
        return a/b

def add(a, b):
    """
    Returns a + b
    """
    return a+b

def power(a, n):
    """Returns a to the power n"""
    p = 1
    for k in range(1,n+1):
        p = p * a
    
    if n < 0:
        n = -n
        for k in range(1,n+1):
            p = p * a
        p = div(1,p) 

    return p
    # to be implemented

def estPremier(n):
    """
    Cette fonction permet de verifier si le nombre donne est premier ou non premier.
    """
    premier = True
    for i in range(1,n+1):
        if i != 1 and i != n:
            if n % i == 0:
                premier = False
    return premier

def division_euclidienne(devidende, diviseur):
    """
    Faire la division euclidienne.
    """
    q = devidende // diviseur #quotient
    r = devidende % diviseur #reste
    
    return (q,r)
    
    