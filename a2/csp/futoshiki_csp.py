#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''

from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    # returns csp object and var_array (array of variable objects)   
    
    ### Step 1: Assemble Variable objects ###
    num_rows = len(futo_grid)
    num_cols = num_rows # we are told that board is always square
    # assemble domain of all variables, domain[0][0] corresponds with domain of var in top left corner
    var_array = [] # 2D array, where var_array[0][0] is variable object for top left corner
    all_vars = [] # 1D array, represents scope of constraint
    ineq_array = [] # 2D array, with dims: # rows by # cols - 1... each subarray containes ineq for a row
    full_dom = [k for k in range(1,num_rows+1)]
    for i in range(0,num_rows):
        row_variables = []
        row_inequalities = []
        for j in range(0,num_cols):
            if futo_grid[i][2*j]==0:
                var = Variable("V_{}{}".format(i,j),full_dom)
                row_variables.append(var)
            else:
                var = Variable("V_{}{}".format(i,j),[futo_grid[i][2*j]])
                row_variables.append(var)
            # track important info for constraint objects in this loop too
            if j < (num_cols-1):
                row_inequalities.append(futo_grid[i][2*j+1])
            all_vars.append(var) # 1D list of all variables
        var_array.append(row_variables)
        ineq_array.append(row_inequalities)
    
    ### Step 2: Assemble Constraint objects ###
    constraints = [] # track all constraints for this inputted board
    for i in range(0,num_rows):
        for j in range(0,num_cols):
            # check every combination of two values in a row and column, add to sat_tup if okay
            for v in range(j+1,num_cols): 
                
                ## check constraints between vars in same row 
                v1 = var_array[i][j]
                v2 = var_array[i][v]
                if (abs(j-v) == 1): # check if adjacent vars has special constraint
                    c_type = ineq_array[i][j] # string for <, >, or .
                else: # not adjacent, just can't be equal
                    c_type = '.'
                constr = Constraint("C(V_{}{},V_{}{})".format(i,j,i,v),[v1,v2])
                sat_tup = [] # combos of v1 and v2 values that satisfy the constraint
                # use itertools.product to get all combos of v1 and v2 values
                # add the allowed tuples based on the constraint type
                for k in itertools.product(v1.cur_domain(),v2.cur_domain()):
                    if c_type == '.':
                        if k[0] != k[1]: # satisfies the not equal constraint
                            sat_tup.append(k)
                    elif c_type == '<':
                        if k[0] < k[1]:
                            sat_tup.append(k)
                    elif c_type == '>':
                        if k[0] > k[1]:
                            sat_tup.append(k)
                constr.add_satisfying_tuples(sat_tup) # add satisfying tuples to constraint
                constraints.append(constr) # add to list of all constraints
                
                ## check constraints between vars in same col
                v1 = var_array[j][i]
                v2 = var_array[v][i]
                constr = Constraint("C(V_{}{},V_{}{})".format(j,i,v,i),[v1,v2])
                sat_tup = []
                for k in itertools.product(v1.cur_domain(),v2.cur_domain()):
                    if k[0] != k[1]:
                        sat_tup.append(k)
                constr.add_satisfying_tuples(sat_tup)
                constraints.append(constr)
                
    ### Step 3: Make CSP object ###
    csp = CSP("futoshiki_grid",all_vars)
    for constr in constraints:
        csp.add_constraint(constr) # add constraints to csp object
    
    return csp, var_array
    

def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT 
    # returns csp object and var_array (array of variable objects)   
    
    ### Step 1: Assemble Variable objects ###
    num_rows = len(futo_grid)
    num_cols = num_rows # we are told that board is always square
    # assemble domain of all variables, domain[0][0] corresponds with domain of var in top left corner
    var_array = [] # 2D array, where var_array[0][0] is variable object for top left corner
    all_vars = [] # 1D array, represents scope of constraint
    ineq_array = [] # 2D array, with dims: # rows by # cols - 1... each subarray containes ineq for a row
    full_dom = [k for k in range(1,num_rows+1)]
    for i in range(0,num_rows):
        row_variables = []
        row_inequalities = []
        for j in range(0,num_cols):
            if futo_grid[i][2*j]==0:
                var = Variable("V_{}{}".format(i,j),full_dom)
                row_variables.append(var)
            else:
                var = Variable("V_{}{}".format(i,j),[futo_grid[i][2*j]])
                row_variables.append(var)
            # track important info for constraint objects in this loop too
            if j < (num_cols-1):
                row_inequalities.append(futo_grid[i][2*j+1])
            all_vars.append(var) # 1D list of all variables
        var_array.append(row_variables)
        ineq_array.append(row_inequalities)
    
    ### Step 2: Assemble Constraint objects ###
    constraints = []
    for i in range(0,num_rows):
        for j in range(0,num_cols):
            # binary constraints to handle the <, > constraints along rows
            if j < num_cols-1:
                v1 = var_array[i][j]
                v2 = var_array[i][j+1]
                if ineq_array[i][j] == '>':
                    constr = Constraint("C(V_{}{},V_{}{})".format(i,j,i,j+1),[v1,v2])
                    sat_tup = []
                    for k in itertools.product(v1.cur_domain(),v2.cur_domain()):
                        if k[0] > k[1]:
                            sat_tup.append(k)
                    constr.add_satisfying_tuples(sat_tup)
                    constraints.append(constr)
                elif ineq_array[i][j] == '<':
                    constr = Constraint("C(V_{}{},V_{}{})".format(i,j,i,j+1),[v1,v2])
                    sat_tup = []
                    for k in itertools.product(v1.cur_domain(),v2.cur_domain()):
                        if k[0] < k[1]:
                            sat_tup.append(k)
                    constr.add_satisfying_tuples(sat_tup)
                    constraints.append(constr)
        # constraints to ensure all in a row are different
        constr = Constraint("C(row{}_alldiff)".format(i),var_array[i])
        sat_tup = []
        row_domains = [var_array[i][k].cur_domain() for k in range(0,num_cols)]
        for k in itertools.product(*row_domains):
            if len(set(k))==len(k): # if all values are different
                sat_tup.append(k) # add to list of tuples that satisfy all diff constraint
        constr.add_satisfying_tuples(sat_tup)
        constraints.append(constr)
        # constraints to ensure all in a column are different
        constr = Constraint("C(col{}_alldiff)".format(i),[k[i] for k in var_array])
        sat_tup = []
        col_domains = [var_array[k][i].cur_domain() for k in range(0,num_rows)]
        for k in itertools.product(*col_domains):
            if len(set(k))==len(k): # if all values are different
                sat_tup.append(k) # add to list of tuples that satisfy all diff constraint
        constr.add_satisfying_tuples(sat_tup)
        constraints.append(constr)
    
    ### Step 3: Make CSP object ###
    csp = CSP("futoshiki_grid",all_vars)
    for constr in constraints:
        csp.add_constraint(constr) # add constraints to csp object
    
    return csp, var_array
    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
