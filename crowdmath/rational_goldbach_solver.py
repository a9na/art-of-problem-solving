from itertools import product
from fractions import Fraction
from time import time
import logging

# Configure logging to provide detailed information about each step of computation
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Problem Summary:
# We aim to identify all positive real numbers `r` such that the semidomain N0[r] (the set of non-negative integer powers of r)
# satisfies an analogue of the Goldbach conjecture. Specifically, we seek values of `r` such that every sufficiently large
# even integer can be represented as a sum of two elements from N0[r].

# Focus on Part (a): Discovering rational values of `r` that satisfy the analogue of the Goldbach conjecture.

def generate_semidomain_elements(r, max_value, max_power=20):
    """
    Generate elements of the semidomain N0[r] up to a specified maximum value.
    
    Parameters:
    - r: The base of the semidomain, representing the value of r.
    - max_value: Upper limit of values for the elements generated.
    - max_power: Maximum power of r to consider, limiting element growth.
    
    Returns:
    - A sorted list of elements within the semidomain N0[r] up to max_value.
    
    Generates values r^k for k = 0, 1, ..., max_power, halting if the element exceeds max_value.
    """
    elements = set()
    for k in range(max_power):
        element = r ** k
        if element > max_value:
            logging.debug(f"Exceeded max_value with r^{k} = {element}")
            break
        elements.add(element)
    logging.info(f"Generated {len(elements)} elements for r = {r}")
    return sorted(elements)

def check_goldbach_analogue(r, max_value):
    """
    Check if N0[r] satisfies the Goldbach analogue for even numbers up to max_value.
    
    Parameters:
    - r: Value of r for the semidomain to verify.
    - max_value: Upper limit of even numbers to test.
    
    Returns:
    - True if every even integer up to max_value is representable as a sum of two elements from N0[r];
      False otherwise.
    
    For each even integer up to max_value, confirms that it can be formed by summing two elements from N0[r].
    """
    elements = generate_semidomain_elements(r, max_value)
    sums = {a + b for a, b in product(elements, repeat=2)}

    # Check representability of even numbers as a sum of two elements
    for even_num in range(4, max_value + 1, 2):
        if even_num not in sums:
            logging.warning(f"Failed to represent even number {even_num} with r = {r}")
            return False
    logging.info(f"r = {r} satisfies the Goldbach analogue up to {max_value}")
    return True

def find_rational_satisfying_goldbach(max_value=1000, max_denominator=10, min_denominator=1):
    """
    Find all rational values q such that N0[q] satisfies the Goldbach analogue up to max_value.
    
    Parameters:
    - max_value: Maximum even number to verify the Goldbach analogue.
    - max_denominator: Upper limit for the denominator of rational numbers considered.
    - min_denominator: Lower limit for the denominator to diversify search.

    Returns:
    - List of rational values of r that satisfy the Goldbach analogue.

    Iterates over rational numbers p/q for given bounds, checking each for the Goldbach analogue.
    """
    start_time = time()
    valid_rationals = []
    total_checked = 0

    for denominator in range(min_denominator, max_denominator + 1):
        for numerator in range(1, denominator + 1):
            r = Fraction(numerator, denominator)
            total_checked += 1
            logging.info(f"Checking r = {r} ({numerator}/{denominator})")

            # Check if r satisfies the Goldbach analogue
            if check_goldbach_analogue(float(r), max_value):
                valid_rationals.append(r)
                logging.info(f"Added r = {r} as satisfying the Goldbach analogue")

    logging.info(f"Total rational numbers checked: {total_checked}")
    logging.info(f"Execution time: {time() - start_time:.2f} seconds")
    return valid_rationals

# Testing Parameters
max_value = 1000  # Upper limit for even numbers in Goldbach analogue testing
max_denominator = 10  # Maximum denominator for rational values of r
min_denominator = 1   # Minimum denominator for rational values of r

# Perform search and output results
satisfying_rationals = find_rational_satisfying_goldbach(max_value, max_denominator, min_denominator)
print("Rational values of r satisfying the Goldbach analogue up to", max_value, ":")
for r in satisfying_rationals:
    print(r)
