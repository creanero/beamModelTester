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
Whether or not Republican Spain joins the Comintern or the Allies, war with the Axis is a necessity (otherwise choose Nationalist Spain!). Joining the Comintern will provide Spain nearly two additional years of preparation for war. Spain will not be able to make significant gains against Germany at the outset of war, thus the focus on the German border should be defensive. Meanwhile, an assault of Italy can be quite fruitful, resulting in a relatively quick annexation. Since it is possible for Vichy France to join the Axis as early as 1942, Spain should be prepared with border guards. Generally, holding out until 1943 is necessary, as that is when the Soviet Union will begin to push back the German military. It is possible for a well-played Spain to make significant gains in the West: including the capture of all France and Western Germany through to Austria, Czechoslovakia and Yugoslavia in the South.
"""

print_str=break_str(test_str)

print(print_str)
