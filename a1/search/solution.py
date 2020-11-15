#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    # The state input to this function is an instance of sokobanState
    # heur is the sum of all manhattan distances, initialize to 0
    heur = 0
    
    for box_pos in state.boxes:
    
        # man_dist tracks manhattan distance to closest storage location
        # reinitialize it to be the largest possible distance 
        man_dist = float("inf")
        
        for stor_pos in state.storage:
            temp_dist = abs(stor_pos[0]-box_pos[0])+abs(stor_pos[1]-box_pos[1])
            if temp_dist < man_dist:
                man_dist = temp_dist
        
        heur = heur + man_dist #add this man_dist to heuristic
        
    return heur


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def stuck(state,box):
    # HELPER FUNCTION for heur_alternate(state)
    # Determines whether box is stuck in a corner / unable to move to storage
    # INPUT: state of the board, box to be checked (not in storage loc)
    
    # check if at corner of board
    if box[0]==0 or box[0]==state.width:
        if box[1]==0 or box[1]==state.height:
            return True #stuck
        
    # check if cornered by obstacles
    obst_surr = [0,0,0,0]
    if ((box[0],box[1]+1) in state.obstacles) or (box[1]+1 >= state.height): #north
        obst_surr[0] = 1
    if ((box[0]+1,box[1]) in state.obstacles) or (box[0]+1 >= state.width): #east
        obst_surr[1] = 1
    if ((box[0],box[1]-1) in state.obstacles) or (box[1]-1 < 0): #south
        obst_surr[2] = 1
    if ((box[0]-1,box[1]) in state.obstacles) or (box[0]-1 < 0): # west
        obst_surr[3] = 1
    # check if two or more ADJACENT sides are stuck
    if sum(obst_surr) >= 3:
        return True
    # if only 2 obst, check if sides adjacent:
    elif (sum(obst_surr) == 2) and (obst_surr[0]+obst_surr[2] == 1): # sum of idx 0 and 2 = 1 if obst are adjacent
        return True
    
    # stuck if at an edge without storage location along it
    if box[0]==0 or box[0]==state.width or box[1]==0 or box[1]==state.height: # if at an edge
        if not any(stor[0]==box[0] for stor in state.storage): # none of the storage is along its row
            if not any(stor[1]==box[1] for stor in state.storage): # none of storage is along its col
                return True #stuck / will never move to storage
    
    return False

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    heur = 0
    stor_locs = [i for i in state.storage] # copy storage to variable stor_locs
    for box_pos in state.boxes:
    
        ##### Part 1: Check if anything is making that box STUCK #####
        ##### If not, add up manhattan distances of all boxes to closest storage #####
        # check four sides of each box to see if two or more sides have obstacle beside it
        obst_surr = [0,0,0,0] # [north, east, south, west], 1 if there is an obstacle

        # if there is one box that is stuck (man_dist = "inf"), so the whole state has heur = "inf"
        # stop checking boxes at that point and just exit box loop, setting heur to "inf" and return heur
        # if stuck, it is okay if stuck position is a storage location
        if box_pos not in state.storage: # check for obstacles and board edge
            if ((box_pos[0],box_pos[1]+1) in state.obstacles) or (box_pos[1]+1 >= state.height): #north
                obst_surr[0] = 1
            if ((box_pos[0]+1,box_pos[1]) in state.obstacles) or (box_pos[0]+1 >= state.width): #east
                obst_surr[1] = 1
            if ((box_pos[0],box_pos[1]-1) in state.obstacles) or (box_pos[1]-1 < 0): #south
                obst_surr[2] = 1
            if ((box_pos[0]-1,box_pos[1]) in state.obstacles) or (box_pos[0]-1 < 0): # west
                obst_surr[3] = 1
            
            # check if two or more ADJACENT sides are stuck
            sum_obst_surr = sum(obst_surr)
            if sum_obst_surr >= 3:
                heur = float("inf")
                return heur
            # if only 2 obst, check if sides adjacent:
            elif (sum_obst_surr == 2) and (obst_surr[0]+obst_surr[2] == 1): # sum of idx 0 and 2 = 1 if obst are adjacent
                heur = float("inf")
                return heur 
            elif sum_obst_surr == 1: # otherwise, wall on one side, check if box on adjacent side with wall beside that box too
                for i in range(0,len(obst_surr)):
                    if obst_surr[i] == 1:
                        if (i==0): # obst at north, check left/right
                            if ((box_pos[0]-1,box_pos[1]) in state.boxes) and (((box_pos[0]-1,box_pos[1]+1) in state.boxes) or ((box_pos[0]-1,box_pos[1]+1) in state.obstacles) or (box_pos[0]-1<0) or (box_pos[1]+1>=state.height)): # check left for box and top left for wall
                                heur = float("inf")
                                return heur
                            if ((box_pos[0]+1,box_pos[1]) in state.boxes) and (((box_pos[0]+1,box_pos[1]+1) in state.boxes) or ((box_pos[0]+1,box_pos[1]+1) in state.obstacles) or (box_pos[0]+1>=state.width) or (box_pos[1]+1>=state.height)): # check right for box and top right for wall
                                heur = float("inf")
                                return heur
                        elif (i==2): # obst at south, check left/right
                            if ((box_pos[0]-1,box_pos[1]) in state.boxes) and (((box_pos[0]-1,box_pos[1]-1) in state.boxes) or ((box_pos[0]-1,box_pos[1]-1) in state.obstacles) or (box_pos[0]-1<0) or (box_pos[1]-1<0)): # check left for box and bottom left for wall
                                heur = float("inf")
                                return heur
                            if ((box_pos[0]+1,box_pos[1]) in state.boxes) and (((box_pos[0]+1,box_pos[1]-1) in state.boxes) or ((box_pos[0]+1,box_pos[1]-1) in state.obstacles) or (box_pos[0]+1>=state.width) or (box_pos[1]-1<0)): # check right for box and bottom right for wall
                                heur = float("inf")
                                return heur
                        elif (i==1): # obst at east, check top/bottom
                            if ((box_pos[0],box_pos[1]+1) in state.boxes) and (((box_pos[0]+1,box_pos[1]+1) in state.boxes) or ((box_pos[0]+1,box_pos[1]+1) in state.obstacles) or (box_pos[0]+1>=state.width) or (box_pos[1]+1>=state.height)): # check top for box and top right for wall
                                heur = float("inf")
                                return heur
                            if ((box_pos[0],box_pos[1]-1) in state.boxes) and (((box_pos[0]+1,box_pos[1]-1) in state.boxes) or ((box_pos[0]+1,box_pos[1]-1) in state.obstacles) or (box_pos[0]+1>=state.width) or (box_pos[1]-1<0)): # check bottom for box and bottom right for wall
                                heur = float("inf")
                                return heur
                        elif (i==3): # obst at west, check top/bottom
                            if ((box_pos[0],box_pos[1]+1) in state.boxes) and (((box_pos[0]-1,box_pos[1]+1) in state.boxes) or ((box_pos[0]-1,box_pos[1]+1) in state.obstacles) or (box_pos[0]-1<0) or (box_pos[1]+1>=state.height)): # check top for box and top left for wall
                                heur = float("inf")
                                return heur
                            if ((box_pos[0],box_pos[1]-1) in state.boxes) and (((box_pos[0]-1,box_pos[1]-1) in state.boxes) or ((box_pos[0]-1,box_pos[1]-1) in state.obstacles) or (box_pos[0]-1<0) or (box_pos[1]-1<0)): # check bottom for box and bottom left for wall
                                heur = float("inf")
                                return heur
                        # above, checked diagonal for wall, obstacle, or box        

        ##### Part 3: Do edge / obstacle check #####
        # impossible to solve if box is at edge and no storage along that edge
        if box_pos not in state.storage:
            # first check x edge
            if box_pos[0]==0 or box_pos[0]==state.width-1: # if box along x edge
                if not any(stor[0]==box_pos[0] for stor in state.storage): # if no storage along that edge
                    heur = float("inf")
                    return heur
                else: # if there is a storage along that edge
                    for obst in state.obstacles: # check if there is obstacle in the way of that storage
                        if obst[0]==box_pos[0]: # if this obst is along the same edge
                            for stor in state.storage: # check if there is storage between box and obst
                                # if there is storage between, then break out of loop, heur != inf
                                if stor[0]==box_pos[0]: # if along same edge
                                    if box_pos[1]<stor[1]<obst[1] or obst[1]<stor[1]<box_pos[1]:
                                        blocked = False
                                        break # found a valid storage, stop checking storage
                                    else:
                                        blocked = True
                            if (blocked):
                                heur = float("inf")
                                return heur # breaks out of checking obstacles in way of storage
            # check y edge
            if box_pos[1]==0 or box_pos[1]==state.height-1: # if at an edge
                if not any(stor[1]==box_pos[1] for stor in state.storage): # none of the storage is along its row
                    heur = float("inf")
                    return heur
                else: # if there is a storage along that edge
                    for obst in state.obstacles: # check if there is obstacle in the way of that storage
                        if obst[1]==box_pos[1]: # if this obst is along the same edge
                            for stor in state.storage: # check if there is storage between box and obst
                                # if there is storage between, then break out of loop, heur != inf
                                if stor[1]==box_pos[1]: # if along same edge
                                    if box_pos[0]<stor[0]<obst[0] or obst[0]<stor[0]<box_pos[0]:
                                        blocked = False
                                        break # found a valid storage, stop checking storage
                                    else:
                                        blocked = True
                            if (blocked):
                                heur = float("inf")
                                return heur 
        
    for box_pos in state.boxes: # if heur is supposed to be inf, code would not reach this part... at this point we need to calc heur
        # if nothing has caused the function to return heur = inf so far, add manhattan distance to storage
        man_dist = float("inf")
        for stor_pos in stor_locs:
            temp_dist = abs(stor_pos[0]-box_pos[0])+abs(stor_pos[1]-box_pos[1])
            if temp_dist < man_dist:
                man_dist = temp_dist
                stor_loc = stor_pos
        stor_locs.remove(stor_loc) # remove this storage location to avoid overlaps
        heur = heur + man_dist #add this man_dist to heuristic
        
        ##### Part 2: Add closest robot's distance (-1) to heur ##### score is 4/20 better without this!!!
        rob_man_dist = float("inf")
        for rob_pos in state.robots:
            # find closest robot to the box
            temp_dist = abs(rob_pos[0]-box_pos[0])+abs(rob_pos[1]-box_pos[1]) -1 # minus one b/c robot can move box if beside
            if temp_dist < rob_man_dist:
                rob_man_dist = temp_dist
        heur = heur + rob_man_dist

    return heur


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval # f = g + epsilon * h

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    
    # variables for timimg
    start = os.times()[0]
    limit = start + timebound
    
    # initialize some vars for the search
    best_res_found = False
    costbound = (float("inf"),float("inf"),float("inf")) # (g_bound, h_bound, f_bound)
    
    # call the provided search engine with bfs and cycle checking
    wastar_search = SearchEngine('custom', 'full') 
    wastar_search.init_search(initial_state, sokoban_goal_state, heur_fn=heur_fn, fval_function=lambda sN: fval_function(sN, weight)) # initialize

    while (os.times()[0] < limit): # keep looping until time runs out
        res_found = wastar_search.search(limit-os.times()[0],costbound)
        if res_found: # keep going to find a better one
            best_res_found = res_found
            costbound = (res_found.gval-1, float("inf"),res_found.gval-1) #float("inf"))
            weight = weight / 2.0 
            wastar_search.init_search(initial_state, sokoban_goal_state, heur_fn=heur_fn, fval_function=lambda sN: fval_function(sN, weight)) # initialize
        else:
            return best_res_found
        
    return best_res_found


def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    
    # variables for timimg
    start = os.times()[0]
    limit = start + timebound
    
    # initialize some vars for the search
    best_res_found = False
    costbound = (float("inf"),float("inf"),float("inf")) # (g_bound, h_bound, f_bound)
    
    # call the provided search engine with bfs and cycle checking
    gbfs_search = SearchEngine('best_first', 'full') 
    gbfs_search.init_search(initial_state, sokoban_goal_state, heur_fn=heur_fn) # initialize
    
    while (os.times()[0] < limit): # keep looping until time runs out
        res_found = gbfs_search.search(limit-os.times()[0],costbound) 
        if res_found: # keep going to find a better one
            best_res_found = res_found # save it if a better one is found
            costbound = (res_found.gval-1, float("inf"), res_found.gval-1) # bound it to find a better solution than previous
            # keeping the bound on f = g + h should be fine because heuristic for this search is admissible
        else: # if no better one is found, just return the last one found (last best)
            return best_res_found
    
    return best_res_found