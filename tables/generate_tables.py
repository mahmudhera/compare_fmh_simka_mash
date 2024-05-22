from suggest_scale_factor import get_min_scale_factor
from simulate import *

if __name__ == '__main__':
    

    for min_value in [10000, 100000, 1000000, 10000000]:
        print('For min size:', min_value)
        print(f'err_rate |\t 0.91 | 0.93 | 0.95 | 0.97 | 0.99')
        for error_rate in [0.01, 0.03, 0.05, 0.07, 0.09, 0.10]:
            print(f'{error_rate} |\t\t', end='')
            for confidence_rate in [0.91, 0.93, 0.95, 0.97, 0.99]:
                scale_factor = get_min_scale_factor(min_value, min_value, error_rate, confidence_rate)
                print(f'{round(scale_factor,4):.4f}', end='|')
            print('')
    
    

    N = 1000000
    sizes = [100000, 200000, 300000, 400000, 500000]
    #sizes = sizes[:1]
    error = 0.05
    confidence = 0.95

    n1n2_pair_to_hit_rate = {}
    n1n2_pair_to_avg_cosine = {}
    n1n2_pair_to_hit_rate_fixed = {}
    n1n2_pair_to_suggested_scale_factor = {}
    num_simulations = 100
    num_steps_done = 1

    for n1 in sizes:
        for n2 in sizes:
            scale_factor = get_min_scale_factor(n1, n2, error, confidence)
            n1n2_pair_to_suggested_scale_factor[(n1, n2)] = scale_factor

    # print n1 by n2 matrix, with suggested scale factors
    print('************************************')
    print('Suggested scale factor matrix')
    print('************************************')
    print('n1 |\t 100000 \t 200000 \t 300000 \t 400000 \t 500000')
    for n1 in sizes:
        print(f'{n1} |', end='')
        for n2 in sizes:
            print(round(n1n2_pair_to_suggested_scale_factor[(n1,n2)], 4), end='\t')
        print('')
    print('************************************')


    for n1 in sizes:
        for n2 in sizes:
            num_hit = 0
            total_cosine = 0.0
            num_hit_fixed = 0
            scale_factor = get_min_scale_factor(n1, n2, error, confidence)
            for _ in range(num_simulations):
                set1 = create_random_set(N, n1)
                set2 = create_random_set(N, n2)
                cosine_orig = cosine_similarity(set1, set2)
                
                fmh_selections = simulate_hash_function(N, scale_factor)
                set1_fmh = take_fmh_sketch(set1, fmh_selections)
                set2_fmh = take_fmh_sketch(set2, fmh_selections)
                cosine_fmh = cosine_similarity(set1_fmh, set2_fmh)

                range_low, range_high = cosine_orig*(1.0 - error), cosine_orig*(1.0 + error)
                #print (cosine_orig, cosine_fmh, range_low, range_high, range_low <= cosine_fmh <= range_high)

                if range_low <= cosine_fmh <= range_high:
                    num_hit += 1

                fmh_selections_fixed = simulate_hash_function(N, 0.001)
                set1_fmh_fixed = take_fmh_sketch(set1, fmh_selections_fixed)
                set2_fmh_fixed = take_fmh_sketch(set2, fmh_selections_fixed)
                cosine_fmh_fixed = cosine_similarity(set1_fmh_fixed, set2_fmh_fixed)

                if range_low <= cosine_fmh_fixed <= range_high:
                    num_hit_fixed += 1

                total_cosine += cosine_orig

                print(f'Steps completed: {num_steps_done}/2500\r', end='')
                num_steps_done += 1

            hit_rate = num_hit/num_simulations
            avg_cosine = total_cosine/num_simulations
            hit_rate_fixed = num_hit_fixed/num_simulations

            n1n2_pair_to_hit_rate[(n1, n2)] = hit_rate
            n1n2_pair_to_avg_cosine[(n1, n2)] = avg_cosine
            n1n2_pair_to_hit_rate_fixed[(n1, n2)] = hit_rate_fixed

    # print n1 by n2 matrix, with hit rates
    print('************************************')
    print('Hit rate matrix')
    print('************************************')
    print('n1 |\t 100000 \t 200000 \t 300000 \t 400000 \t 500000')
    for n1 in sizes:
        print(f'{n1} |', end='')
        for n2 in sizes:
            print(round(n1n2_pair_to_hit_rate[(n1, n2)], 4), end='\t')
        print('')
    print('************************************')

    # print n1 by n2 matrix, with avg cosine
    print('************************************')
    print('Avg cosine matrix')
    print('************************************')
    print('n1 |\t 100000 \t 200000 \t 300000 \t 400000 \t 500000')
    for n1 in sizes:
        print(f'{n1} |', end='')
        for n2 in sizes:
            print(round(n1n2_pair_to_avg_cosine[(n1, n2)], 4), end='\t')
        print('')
    print('************************************')

    # print n1 by n2 matrix, with hit rates for fixed scale factor
    print('************************************')
    print('Hit rate matrix for fixed scale factor')
    print('************************************')
    print('n1 |\t 100000 \t 200000 \t 300000 \t 400000 \t 500000')
    for n1 in sizes:
        print(f'{n1} |', end='')
        for n2 in sizes:
            print(round(n1n2_pair_to_hit_rate_fixed[(n1, n2)], 4), end='\t')
        print('')