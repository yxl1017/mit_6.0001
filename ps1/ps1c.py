# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:31:02 2023

@author: xiaol
"""

annual_salary=float(input("Enter your annual salary:"))
semi_annual_raise=0.07
total_cost=1000000
portion_down_payment = 0.25
current_saving=0
r=0.04
low=0
high=10000
guess=(low+high)/2
numGuesses=0
while abs(portion_down_payment*total_cost-current_saving)>=100:
    current_saving=0
    portion_saved=guess/10000
    for i in range (36):
        current_saving+=current_saving*r/12+annual_salary/12*portion_saved
        if i%6==0 and i>0:
            annual_salary+=annual_salary*semi_annual_raise
    
    if portion_down_payment*total_cost-current_saving>0:
        low=guess
    else:
        high=guess
    guess=(low+high)/2
    numGuesses+=1   
    if numGuesses > 1000:
        break

if numGuesses>1000:
    print("It is not possible to pay the down payment in three years.")
else:
    rate=guess/10000
    print("steps in bisection search is",numGuesses,"and the best saving rate is",rate)
