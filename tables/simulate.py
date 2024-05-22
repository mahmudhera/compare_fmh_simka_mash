import random

# given N, the total number of elements in the universe, and n, the number of elements in the set,
# create a random set of n elements from the universe {0, 1, 2, ..., N-1}
def create_random_set(N, n):
    return set(random.sample(range(N), n))

def cosine_similarity(set1, set2):
    return len(set1.intersection(set2)) / (len(set1) * len(set2))**0.5

def cosine_similarity_squared(set1, set2):
    return len(set1.intersection(set2))**2 / (len(set1) * len(set2))

# given N, the total number of elements in the universe, and scale_factor, return a list of N elements,
# each of which is 1 with probability scale_factor and 0 with probability 1 - scale_factor
def simulate_hash_function(N, scale_factor):
    return [1 if random.random() < scale_factor else 0 for _ in range(N)]

# fmh_selections: a list of N bits
# set1: a set of elements from the universe {0, 1, 2, ..., N-1}
# return a new set that contains the elements in set1 that are selected by the filter
def take_fmh_sketch(set1, fmh_selections):
    return {i for i in set1 if fmh_selections[i] == 1}

def main():
    N = 100000
    scale_factor = 0.01
    
    # set random seed
    random.seed(0)

    num_simulations = 5
    num_iterations = 1000
    for _ in range(num_simulations):
        n1 = random.randint(1, N)
        while n1 < 10000:
            n1 = random.randint(1, N)
        n2 = random.randint(1, N)
        while n2 < 10000:
            n2 = random.randint(1, N)

        set1 = create_random_set(N, n1)
        set2 = create_random_set(N, n2)

        num_common = len(set1.intersection(set2))
        m = n1-num_common
        p = n2-num_common
        n = num_common
        f = (1.0/scale_factor - 1.0)**0.5

        print(n1, n2, num_common, m, p)

        num_okay_1 = 0
        num_okay_2 = 0
        num_okay_3 = 0
        for __ in range(num_iterations):
            fmh_selections = simulate_hash_function(N, scale_factor)
            set1_fmh = take_fmh_sketch(set1, fmh_selections)
            set2_fmh = take_fmh_sketch(set2, fmh_selections)
            
            cosine_squared_orig = cosine_similarity_squared(set1, set2)
            cosine_squared_fmh = cosine_similarity_squared(set1_fmh, set2_fmh)
            error = abs(cosine_squared_orig - cosine_squared_fmh)/cosine_squared_orig

            c = 1
            a = c * f * ( p/(n*(p+n)) )**0.5 + c * f * ( m/(n*(m+n)) )**0.5 + c*c*f*f* ( p*m/(n*n*(p+n)*(m+n)) )**0.5
            theoretical_error = a

            #print(error, theoretical_error)
            if error <= theoretical_error:
                num_okay_1 += 1

            c = 2
            a = c * f * ( p/(n*(p+n)) )**0.5 + c * f * ( m/(n*(m+n)) )**0.5 + c*c*f*f* ( p*m/(n*n*(p+n)*(m+n)) )**0.5
            theoretical_error = a

            if error <= theoretical_error:
                num_okay_2 += 1

            c = 3
            a = c * f * ( p/(n*(p+n)) )**0.5 + c * f * ( m/(n*(m+n)) )**0.5 + c*c*f*f* ( p*m/(n*n*(p+n)*(m+n)) )**0.5
            theoretical_error = a

            if error <= theoretical_error:
                num_okay_3 += 1
        
        print("c=1: ", num_okay_1/num_iterations)
        print("c=2: ", num_okay_2/num_iterations)
        print("c=3: ", num_okay_3/num_iterations)


if __name__ == "__main__":
    main()