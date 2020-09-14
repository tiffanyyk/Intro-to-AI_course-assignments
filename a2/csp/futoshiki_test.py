# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:51:11 2020

@author: Tiffany Yau
"""

from cspbase import *
from propagators import *
from futoshiki_csp import *
import traceback

def test_futoshiki_FC(futo_grid):
    did_fail = False
    score = 0
    try:
        csp,var_array = futoshiki_csp_model_1(futo_grid)
        curr_vars = csp.get_all_vars()
        curr_vars[0].assign(1)
        flag,pruned = prop_FC(csp,newVar=curr_vars[0])
        details = "Completed without error"
    except Exception:
        details = "One or more runtime errors occurred while testing simple FC: %r" % traceback.format_exc()

    csp.print_soln()
    return score,details

#### Futogrid Test Cases ####
futo_grid1 = [[0,'>',0,'.',0,'>',0,'>',0],
              [4,'.',0,'.',0,'.',0,'.',2],
              [0,'.',0,'.',4,'.',0,'.',0],
              [0,'.',0,'.',0,'.',0,'<',4],
              [0,'<',0,'<',0,'.',0,'.',0]]

print("Testing futoshiki with binary constraints...")
print(test_futoshiki_FC(futo_grid1))
#print("Testing futoshiki with n-ary constraints...")
#csp,var_array = futoshiki_csp_model_2(futo_grid1)