from copy import deepcopy
from schedule import Schedule
import random
import math 

## Takes a solution and returns a dictionnary of all the valid neighbors solutions that upgrade the solution associated to their costs (= maximum number of different time slots)

def dic_neighbors_sol(schedule, solution, key):
    valk = solution[key]
    new_sol = solution.copy()
    new_val_tab = list(range(1,valk))
    ## new pairing key value and possible modifications
    if valk > 1:
        new_sol[key] = random.choice(new_val_tab)
        try: 
            schedule.verify_solution(new_sol)
            keys_associated_valk = [key for key, value in new_sol.items() if value == valk]
            if len(keys_associated_valk) == 0: 
                keys_associated_valkp = [key for key, value in new_sol.items() if value > valk]
                for k in keys_associated_valkp: 
                    new_sol[k] -=1
            ## updating new solutions
            new_time_slots_number = max(new_sol.values())
            return new_sol, new_time_slots_number
        except AssertionError: 
            return new_sol, 0
    return new_sol, 0

def solve(schedule : Schedule):
    """
    Your solution of the problem    
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    shuffle_number = 100
    shuffle_solutions = dict()
    slot_lists = list(range(1,len(schedule.course_list)+1))

    # naive and first solution
    for ka in range(shuffle_number):
        print("shuffle", ka) 
        random.shuffle(slot_lists)
        solution = dict()
        for s,c in enumerate(schedule.course_list):
            solution[c] = slot_lists[s]

        ## simulated annealing temperature
        T0 = 1 
        alpha = 0.9
        T = T0
        max_iter = 500

        ## tracking of the best solution
        best_sol = solution
        best_value = max(solution.values())

        
        ## local search algorithm
        keys = solution.keys()
        flags = -1 
        iter_k = 0
        while flags < 0: 
            ## choice of a random key 
            reroll = True
            max_reroll = 20
            reroll_k = 0

            while reroll:
                selected_key = random.choice(list(keys)) 
                returned_sol, returned_value = dic_neighbors_sol(schedule, solution, selected_key)
                reroll = reroll and (returned_value == 0) and (reroll_k < max_reroll)
                reroll_k += 1 

            if returned_value == 0:
                flags = 1 
            else:
                ## selection of a new solution
                delta = returned_value - best_value
                if delta <= 0: 
                    solution = returned_sol
                elif random.random() < math.exp(-delta/T): 
                    solution = returned_sol

                ## possible update of best solution 
                sol_value = max(solution.values())
                if sol_value < best_value: 
                    best_sol = solution 
                    best_value = sol_value
                
                ## update of the temperature
                T = alpha*T
            iter_k += 1 
            if iter_k > max_iter: 
                flags = 0
        shuffle_solutions[tuple(best_sol.items())] = best_value

    shuffle_best_sol = dict(min(shuffle_solutions, key=shuffle_solutions.get))

    return shuffle_best_sol