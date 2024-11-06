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
    if searching_range == 0: 
        possible_new_val = list( range( 1, solution[key] ) ) 
    else: 
        possible_new_val = list( range( solution[key] - searching_range, solution[key] ) ) 
    solution_mem = dict()
    
    if len(possible_new_val)>0:
        c = random.choice(possible_new_val)
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
            if candidate_value <= nb_of_slots: 
                return candidate_sol, candidate_value
            else: 
                return dict(), 0
        except AssertionError: 
            return dict(), 0

        ## returning a randomly selected possible solution
        nb_candidates = len(solution_mem)
        if  nb_candidates > 0:
            selected_sol, selected_value = random.choice(list(solution_mem.items()))
            return dict(selected_sol), selected_value
        else: 
            return dict(), 0
    else: 
        return dict(), 0
    
    


def solve(schedule : Schedule):
    """
    Your solution of the problem    
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    
    nb_restarts = 100
    shuffle_solutions = dict()
    slot_lists = list(range( 1, len(schedule.course_list)+1 ))
    best_value = len(slot_lists)
    if best_value < 100: 
        searching_range = 0
    else:
        searching_range = round(0.1*best_value)
    for res in range(nb_restarts):
        print("restart ", res)

        ## we create a naive first solution
        random.shuffle(slot_lists)

        solution = dict()
        for s, c in enumerate(schedule.course_list):
            solution[c] = slot_lists[s]

        ## local search algorithm

        flag = -1
        max_iter = 1000
        max_reroll = 5
        iter_k = 0
 
        keys = solution.keys()

        while flag < 0: 
            reroll = True
            reroll_number = 0
            while reroll:
                selected_key = random.choice(list(keys)) 
                returned_sol, returned_value = generate_neighbor(schedule, solution, selected_key, searching_range)

                reroll_number += 1
                reroll = reroll and (reroll_number<max_reroll) and (returned_value==0)

            if returned_value == 0: 
                print("Nombre de rerolls insuffisant")
                flag = 1

            else: 
                # by construction, here a neighbor solution cannot downgrade the solution
                solution = returned_sol
                best_value = returned_value
                
                ## convergence
                iter_k +=1 
                if iter_k >= max_iter: 
                    flag = 0

        shuffle_solutions[tuple(solution.items())] = best_value
        
    return dict(min(shuffle_solutions, key=shuffle_solutions.get))
