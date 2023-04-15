# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:54:38 2022

@author: xiaol
"""

annual_salary=float(input("Enter your annual salary:"))
semi_annual_raise=float(input("Enter the semiannual raise, as a decimal:"))
portion_saved=float(input("Enter the portion of salary to be saved (in decimal form):"))
total_cost=float(input("Enter the cost of your dream home:"))
portion_down_payment = 0.25
current_saving=0
r=0.04
n=0
while current_saving <=portion_down_payment*total_cost:
    current_saving+=current_saving*r/12+annual_salary/12*portion_saved
    n+=1
    if n%6==0:
        annual_salary+=annual_salary*semi_annual_raise
print ("Number of months=",n)