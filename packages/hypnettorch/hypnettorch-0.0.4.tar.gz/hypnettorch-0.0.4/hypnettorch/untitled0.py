#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:00:36 2021

@author: christian
"""
from hypnettorch.data.special.regression1d_data import ToyRegression

n = 100
data = ToyRegression(train_inter=[-3.5, 3.5], num_train=n,
                     map_function=lambda x : x**3, std=3,
                     test_inter=[-4, 4], num_test=10, perturb_test_val=True)
data.plot_dataset()

data = ToyRegression(train_inter=[-3.5, 3.5], num_train=n,
                     map_function=lambda x : x**3, std=lambda x: x**2,
                     test_inter=[-4, 4], num_test=100, perturb_test_val=True)
data.plot_dataset()

