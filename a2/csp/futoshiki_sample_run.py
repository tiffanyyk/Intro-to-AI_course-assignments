# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:38:19 2020

@author: Tiffany Yau
"""

from futoshiki_csp import *
from propagators import *

def print_sudo_soln(var_array):
    for row in var_array:
	        print([var.get_assigned_value() for var in row])

puzzle1 = [[3,'.',0,'.',0,'<',0],[0,'.',0,'.',0,'.',0],[0,'.',0,'<',0,'.',0],[0,'.',0,'>',0,'.',1]]
puzzle1 = [[0,'>',0,'.',0,'>',0,'>',0], # put this 5x5 in myself 
              [4,'.',0,'.',0,'.',0,'.',2],
              [0,'.',0,'.',4,'.',0,'.',0],
              [0,'.',0,'.',0,'.',0,'<',4],
              [0,'<',0,'<',0,'.',0,'.',0]]

csp,var_array = futoshiki_csp_model_1(puzzle1)
solver = BT(csp)
print("GAC")
solver.bt_search(prop_GAC)
print("Solution")
print_sudo_soln(var_array)
print("===========")

csp,var_array = futoshiki_csp_model_2(puzzle1)
solver = BT(csp)
print("GAC")
solver.bt_search(prop_GAC)
print("Solution")
print_sudo_soln(var_array)
print("===========")