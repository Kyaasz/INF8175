from copy import deepcopy
from schedule import Schedule
import random
import math 

## Takes a solution and returns a dictionnary of all the valid neighbors solutions that upgrade the solution associated to their costs (= maximum number of different time slots)

def dic_neighbors_sol(schedule, solution):
    dic = dict()
    sample_keys = random.sample(list(solution.keys()), round(len(solution)*0.7))
    time_slots_number = max(solution.values())
    for key in sample_keys: 
        valk = solution[key]
        range_change = 1
        for val in range(valk-range_change, valk):
            new_sol = solution.copy()
            if val != new_sol[key]:
            ## checking there is no conflictual node
                conflictual_nodes = schedule.get_node_conflicts(key)
                neighbors_ok = True
                for n in conflictual_nodes: 
                    neighbors_ok = neighbors_ok and (new_sol[n] != val)
                if neighbors_ok: 
                    ## new pairing key value and possible modifications
                    new_sol[key] = val
                    keys_associated_valk = [key for key, value in new_sol.items() if value == valk]
                    if len(keys_associated_valk) == 0: 
                        keys_associated_valkp = [key for key, value in new_sol.items() if value > valk]
                        for k in keys_associated_valkp: 
                            new_sol[k] -=1
                    ## updating new solutions
                    new_time_slots_number = max(new_sol.values())
                    dic[tuple(new_sol.items())] = new_time_slots_number            
    return dic


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

    ## simulated annealing temperature
    T0 = 1 
    alpha = 0.8
    T = T0
    max_iter = 10000

    ## tracking of the best solution
    best_sol = solution
    best_value = max(solution.values())

    
    ## local search algorithm

    for r in range(max_iter): 
        print(f"iteration {r}")
        ## gathering all the neighbors solutions
        dic_sols = dic_neighbors_sol(schedule, solution)
        if len(dic_sols) == 0: 
            return best_sol
        else:
            ## selection of a new solution
            selected_sol = random.choice(list(dic_sols.items())) 
            delta = selected_sol[1] - best_value
            if delta <= 0: 
                solution = dict(selected_sol[0])
            elif random.random() < math.exp(-delta/T): 
                solution = dict(selected_sol[0])

            ## possible update of best solution 
            sol_value = max(solution.values())
            if sol_value < best_value: 
                best_sol = solution 
                best_value = sol_value
            
            ## update of the temperature
            T = alpha*T

    return best_sol