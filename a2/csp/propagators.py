#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    ### Step 1: Get the list of constraints affected by the newest variable assignment ###
    if not newVar: # prop_FC called with no variables instantiated yet, so we need to decide what processing to do
        # look for unary constraints of the csp (scope contains only one var)
        # forward check these constraints
        constraints = csp.get_all_cons() # list of all constraints in csp
    else: # check only constraints containing newVar=var
        constraints = csp.get_cons_with_var(newVar) # constraints involving the newly instantiated variable
    ### Step 2: Find out which of the constraints from step 1 have only one uninstantiated variable left ###
    output_lst = [] # to track variable / value pairs that are pruned
    for constraint in constraints: # for each constraint to be considered: 
        if constraint.get_n_unasgn() == 1: # if there's only 1 uninst. var left in its scope
            unasgn_var = constraint.get_unasgn_vars() # find the unassigned variable; should be a list of one
            unasgn_var = unasgn_var[0]
            dom_unasgn_var = unasgn_var.cur_domain()
            for d in dom_unasgn_var: # for each possible domain value, see if it will lead to DWO
                unasgn_var.assign(d)
                assigned_vals = [var.get_assigned_value() for var in constraint.get_scope()] # format input to check function
                if not constraint.check(assigned_vals): # false, not satisfy
                    unasgn_var.prune_value(d) # remove from current domain
                    output_lst.append((unasgn_var,d))
                    if unasgn_var.cur_domain_size == 0: # if there's no remaining potentially valid values left in domain
                        unasgn_var.unassign() # undo assignment of d to variable
                        return (False, output_lst) # return stuff for DWO
                unasgn_var.unassign() # unassign the variable for next loop iteration
    return (True, output_lst)

# define queue class to be used for GAC queue
class Queue:
  def __init__(self):
      self.queue = list()
  def enqueue(self,data):
      self.queue.insert(0,data)
      return True
  def dequeue(self): # first in, first out
      if len(self.queue)>0:
          return self.queue.pop()
  def size(self):
      return len(self.queue)
  def print_queue(self):
      return self.queue

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    constraints = Queue()
    output_lst = [] # track var / val pairs of pruned things
    if not newVar: # start GAC
        # initialize the GAC queue with all constraints of the csp
        constr = csp.get_all_cons()
        for c in constr:
            constraints.enqueue(c)
    else:
        constr = csp.get_cons_with_var(newVar) # for each constraint whose scope contains newVar, put c in queue
        for c in constr:
            constraints.enqueue(c)
        vardom = newVar.cur_domain() 
        for d in vardom:
            if d != newVar.get_assigned_value():
                newVar.prune_value(d)
                output_lst.append((newVar,d)) # track in output list the pruned stuff
#    print("done 1",constraints.size())
    while constraints.size() > 0: # GAC_enforce from lecture notes
        constraint = constraints.dequeue()
        variables = constraint.get_scope() # vars involved in the constraint
        for var in variables: # check if each variable has support for all values in domain
            for d in var.cur_domain():
                # find an assignment A for all other vars in scope(C) such that C(A U V=d) is True
                # use has_support function
                pruned = False
                if not constraint.has_support(var,d): # if no support
                    var.prune_value(d) # remove from domain of var
                    output_lst.append((var,d))
                    pruned = True
                if var.cur_domain_size() == 0:  # if there's no remaining potential vals, DWO
                    constraints = Queue() # empty GAC queue
                    return (False, output_lst) # DWO
                elif (pruned): # add all constraints affected by the pruning into queue
                    cons_to_add = csp.get_cons_with_var(var)
                    for c in cons_to_add:
                        constraints.enqueue(c)
#        print(constraints.size())
    return (True, output_lst) # returns this if not DWO

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    # need to return the variable with the fewest legal values (smallest curDom)
    unasgn_vars = csp.get_all_unasgn_vars()
    cur_dom_sz = []
    for var in unasgn_vars: # find the domain size of all remaining unassigned variables
        cur_dom_sz.append(var.cur_domain_size())
    mrv_idx = cur_dom_sz.index(min(cur_dom_sz)) # choose the variable with the smallest remaining dom size
    return unasgn_vars[mrv_idx]
    
    

	