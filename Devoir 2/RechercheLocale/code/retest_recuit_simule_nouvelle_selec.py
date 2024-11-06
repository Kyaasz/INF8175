from copy import deepcopy
from schedule import Schedule
import random
import math 


## Generating a new solution from an older one, and a new value to pair to a key

def generate_sol(solution, key, new_slot): 
    new_sol = solution.copy()
    new_sol[key] = new_slot
    return new_sol


## Return first upgrading neighbor, if there is not, return a valid solution (possibly worst than the initial one)

def generate_neighbor(schedule, solution, key, searching_range):
    nb_of_slots = max(solution.values())
    possible_new_val = list( range( max( 1, solution[key] - searching_range ), min( solution[key] + searching_range + 1, nb_of_slots + 2 ) ) ) 
    possible_new_val.remove(solution[key])
    solution_mem = dict()
    for c in possible_new_val:
        candidate_sol = generate_sol(solution, key, c)
        try:
            schedule.verify_solution(candidate_sol)

            keys_associated_valk = [key for key, value in candidate_sol.items() if value == solution[key]]
            if len(keys_associated_valk) == 0: 
                number_of_slots -= 1
                keys_associated_valkp = [key for key, value in candidate_sol.items() if value > solution[key]]
                for k in keys_associated_valkp: 
                    candidate_sol[k] -=1
            
            candidate_value = max(candidate_sol.values())
            if candidate_value < nb_of_slots: 
                return candidate_sol, candidate_value
            else: 
                solution_mem[tuple(candidate_sol.items())] = candidate_value
        except AssertionError: 
            pass
    ## returning a randomly selected possible solution
    nb_candidates = len(solution_mem)
    if  nb_candidates > 0:
        selected_sol, selected_value = random.choice(list(solution_mem.items()))
        return dict(selected_sol), selected_value
    else: 
        return dict(), 0
    
    


def solve(schedule : Schedule):
    """
    Your solution of the problem    
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    
    ## we create a naive first solution

    solution = dict()
    time_slot_idx = 1
    for c in schedule.course_list:
        assignation = time_slot_idx
        solution[c] = assignation
        time_slot_idx += 1

    ## local search algorithm with simulated annealing
    nb_of_courses = len(solution)
    nb_of_slots = nb_of_courses
    searching_range = round(0.2*nb_of_courses)
    
    T0 = 1 
    alpha = 0.99
    T = T0
    flag = -1
    max_iter = 3000
    max_reroll = 30
    iter_k = 0

    best_sol = solution 
    best_value = nb_of_slots

    keys = solution.keys()
    while flag < 0: 
        print(f"iteration {iter_k}")
        reroll = True
        reroll_number = 0
        while reroll:
            selected_key = random.choice(list(keys)) 
            returned_sol, returned_value = generate_neighbor(schedule, solution, selected_key, searching_range)

            reroll_number += 1
            reroll = reroll and (reroll_number<max_reroll) and (returned_value==0)

        if returned_value == 0: 
            print("Nombre de rerolls insuffisant")
            return best_sol
        else: 
            delta = returned_value - nb_of_slots
            if delta <= 0:
                solution = returned_sol
                nb_of_slots = returned_value
            elif random.random() < math.exp(-delta/T): 
                solution = returned_sol
                nb_of_slots = returned_value
            
            if nb_of_slots<best_value: 
                best_sol = solution 
                best_value = nb_of_slots
            ## convergence
            T = alpha*T
            iter_k +=1 
            if iter_k >= max_iter: 
                flag = 0
    print("nombre maximal d'itérations atteint")
    return best_sol