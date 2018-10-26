#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 20:26:33 2018

@author: michel
"""

import random
import matplotlib.pyplot as plt
import numpy as np
import math

def generate_box_of_pills(nb_pill_in_box):
    """
    Generate a box of pills by ramdomly picking pills from a stack of pill-a
    and pill-b. 
    
    Uniform distribution of the random.choice() command guarantee the number
    of pill-a and pill-b are expected to be close.
    
    """
    pills = ['pill-a', "pill-b"]
    box = []
    for i in range(nb_pill_in_box):
        box.append(random.choice(pills))
    return box


def run_experiment(box, goal):
    """
    """
    pill_b_consecutive_counter = 0
    total_nb_pills = len(box)
    for i in range(total_nb_pills):
        pill_taken = box.pop()
        if (pill_taken =='pill-a'):
            pill_b_consecutive_counter = 0
        elif (pill_taken =='pill-b'):
            pill_b_consecutive_counter += 1
            if pill_b_consecutive_counter == goal:
                return i + 1
        else:
            print("Hum, don't know about that pill. Skippint it!")
            
    return None
    

def run_test_campaign(nb_patients, nb_pills_in_box, goal):        
    """
    """
    test_campaign_results = []
    for i in range(nb_patients):
        patient_box = generate_box_of_pills(nb_pills_in_box)    
        days = run_experiment(patient_box, goal)    
        if (days != None):
            test_campaign_results.append(days)

    return test_campaign_results


def mean(data):
    """
    """
    nb_samples = len(data)
    total = 0
    for i in range(0,nb_samples):
        total += data[i]        
    return total / nb_samples


def std(data):
    """
    """    
    m = mean(data)
    nb_samples = len(data)
    accumulator = 0;
    for i in range(0,nb_samples-1):
        accumulator += (data[i] - m)**2
    std_dev = math.sqrt(accumulator / nb_samples)
    return std_dev




"""

    Helper functions below this point used for reflection

"""   

def min_max(campaign_results):
    """
    """
    data = np.array(campaign_results)
    min = data.min()
    max = data.max()
    return (min, max)


def summarize(data, nb_bins):
    """
    """
    summarized_data = []
    for i in range(nb_bins):
        counter = 0
        for j in range(len(data)):
            if data[j]==i:
                counter += 1
        summarized_data.append(counter)
    return summarized_data
 


"""
    Config parameters
    
"""
nb_consecutive_days_for_pill_b_success = 3
nb_pills_in_box = 100
nb_patients = 10000

print("Nb consecutive days for pill_b success:", nb_consecutive_days_for_pill_b_success)
print("Nb pills in the box:", nb_pills_in_box)
print("Nb patients:", nb_patients)



"""
    Test the code for 1 patient

"""
print("="*80)
box = generate_box_of_pills(nb_pills_in_box)
print("box:", box)
recovery_time = run_experiment(box, nb_consecutive_days_for_pill_b_success)
print("recovery time in days: ", recovery_time)


"""
    Run test campaign
"""
results = run_test_campaign(nb_patients, nb_pills_in_box, nb_consecutive_days_for_pill_b_success)
nb_uncurred_people = nb_patients - len(results)
min, max = min_max(results)

hb_mean = mean(results)
hb_std = std(results)

print("="*80)
print("campaign results:",results)
print("campaign results length:", len(results))
print("uncurred people:", nb_uncurred_people)
print("min days:{}, max days:{}".format(min, max))

print("\nNumpy calculations:")
print("mean:", np.array(results).mean())
print("std :", np.array(results).std())

print("\nHomebrew calculations:")
print("mean:", hb_mean)
print("std :", hb_std)


"""
Plot the results
"""
plt.plot(results)
plt.show()

num_bins = nb_pills_in_box
plt.hist(results, num_bins, facecolor='red')
plt.title("Days to recover")
plt.xlabel("Patient number (number)")
plt.ylabel("Days to recover (number)")
plt.show()


summarized_data = summarize(results, num_bins)
print("Summarized data",summarized_data)
plt.hist(np.array(summarized_data), density=True)
plt.title("Summarized data. \n Shows how many patients had similar number of days to recover")
plt.xlabel("Days to recover (number)")
plt.ylabel("Number of patients (number)")
plt.show()
print("summarized data:", summarized_data)


count, bins, _ = plt.hist(results, density=True)
plt.plot(bins, 1 / (hb_std * np.sqrt(2 * np.pi)) * np.exp( - (bins - hb_mean)**2 / (2 * hb_std**2) ),linewidth=2, color='r')
plt.show()


