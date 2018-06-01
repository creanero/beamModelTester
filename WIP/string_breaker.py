# -*- coding: utf-8 -*-
"""
Created on Fri Jun 01 15:59:21 2018

@author: User
"""
def break_str(test_str,length_limit=80):
    out_str=test_str
    test_len_c=len(test_str)
    if test_len_c > length_limit:
        test_list=test_str.split()
        test_len_w=len(test_list)
        break_point = test_len_w/2
        first_half = " ".join(test_list[0:break_point])
        first_half = break_str(first_half)
        
        second_half = " ".join(test_list[break_point:test_len_w])
        second_half = break_str(second_half)
        
        out_str="\n".join([first_half,second_half])
    return(out_str)
        
test_str="""
Now sits the wind fair, and we will aboard.
My Lord of Cambridge, and my kind Lord of Masham,
And you, my gentle knight, give me your thoughts:
Think you not that the powers we bear with us
Will cut their passage through the force of France,
Doing the execution and the act
For which we have in head assembled them?
"""

print_str=break_str(test_str)

print(print_str)
