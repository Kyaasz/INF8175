from copy import deepcopy
from schedule import Schedule
import random
import math 
import time


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
    max_slots_list = max(solution.values())
    new_slots_list = list(range(1,max_slots_list+1))
    new_slots_list.remove(current_slot)
    random.shuffle(new_slots_list)
    for slot in new_slots_list: 
        candidate_sol = generate_sol(solution, key, slot)
        try: 
            schedule.verify_solution(candidate_sol)
            candidate_sol = update_sol(candidate_sol, current_slot)
            candidate_score = evaluate_sol(candidate_sol)
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
    start_time = time.time()
    time_limit = 285
    # naive and first solution
    solution = dict()
    time_slot_idx = 1
    for c in schedule.course_list:

        assignation = time_slot_idx
        solution[c] = assignation
        time_slot_idx += 1

    nb_courses = len(solution)
    print("HERE :", nb_courses)
    current_score = evaluate_sol(solution)
    best_sol = solution 
    best_score = current_score

    ## Local search algorithm
    
    keys_not_placed = list(solution.keys())

    T0 = 1
    alpha = 0.99
    T = T0
    max_iter = 50000
    iter = 0
    flags = -1
    nb_wo_progress = 0
    while flags < 0: 
        selected_key = random.choice(keys_not_placed)
        selected_sol, selected_score = generate_neighbor(schedule, solution, selected_key, current_score)
        
        if selected_score == 0: 
            keys_not_placed.remove(selected_key) ## the course cannot be placed in a better slot
            if not keys_not_placed:
                flags = 1
        else: 
            delta = selected_score - current_score
            if delta <= 0:
                solution = selected_sol
                current_score = selected_score
            elif random.random() < math.exp(-delta/T): 
                solution = selected_sol
                current_score = selected_score
        if current_score < best_score: 
            best_score = current_score
            best_sol = solution
            nb_wo_progress = 0
        else: 
            nb_wo_progress +=1
        
        T = alpha*T
        iter +=1
        if iter >= max_iter: 
            flags = 0
        if time.time() - start_time >= time_limit:
            flags = 2
        if nb_wo_progress > 2000: 
            flags = 3

    if flags == 0: 
        print("Nombre maximum d'itérations atteint")
    elif flags == 1: 
        print("Plus aucune clé ne peut être déplacée")
    elif flags == 3:
        print("Pas de progrès depuis 2000 itérations")
    else: 
        print("Limite de temps atteinte")
    return best_sol

    
