from copy import deepcopy
from schedule import Schedule
import random
import math 


## Generating a new solution from an older one, and a new value to pair to a key

def generate_sol(solution, key, new_slot): 
    new_sol = solution.copy()
    new_sol[key] = new_slot
    return new_sol


def evaluate_sol(solution): 
    return ( sum( list(solution.values()) ) )
    

def update_sol(solution, precedent_slot): 
    if precedent_slot not in solution.values():
        for k,v in solution.items(): 
            if v > precedent_slot:
                solution[k] = v-1
    return solution

def generate_neighbor(schedule, solution, key, current_score): 
    current_slot = solution[key]
    new_slots_list = list(range(1,current_slot))
    new_slots_list.reverse()
    if new_slots_list: 
        for slot in new_slots_list: 
            candidate_sol = generate_sol(solution, key, slot)
            try: 
                schedule.verify_solution(candidate_sol)
                candidate_sol = update_sol(candidate_sol, current_slot)
                candidate_score = evaluate_sol(candidate_sol)
                if candidate_score < current_score:
                    return candidate_sol, candidate_score
            except AssertionError: 
                pass
        
    ## we didn't found a better solution
    return dict(), 0



def solve(schedule : Schedule):
    """
    Your solution of the problem    
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot. 
    """
    
    # naive and first solution
    solution = dict()
    time_slot_idx = 1
    for c in schedule.course_list:

        assignation = time_slot_idx
        solution[c] = assignation
        time_slot_idx += 1

    current_score = evaluate_sol(solution)
    ## Local search algorithm

    keys_not_placed = list(solution.keys())

    max_iter = 30000
    iter = 0
    flags = -1
    while flags < 0: 
        selected_key = random.choice(keys_not_placed)
        selected_sol, selected_score = generate_neighbor(schedule, solution, selected_key, current_score)
        
        iter +=1
        if iter >= max_iter: 
            flags = 0

        if selected_score == 0: 
            keys_not_placed.remove(selected_key) ## the course cannot be placed in a better slot
            if not keys_not_placed:
                flags = 1
        else: 
            solution = selected_sol
            current_score = selected_score
        
    if flags == 0: 
        print("nombre maximum d'itérations atteint")
    else: 
        print("Toutes les clés ont été placées")

    return solution

    
