"""
This module contains helper functions to analyze Y maza data

@authors: Gergo Turi gt2253@cumc.columbia.edu
"""
import os
import copy
import numpy as np
import pandas as pd

from analysis.dlc_utils import mount_gdrive

def error_counter(data):
	"""
	Calculates the number of incorrect alternations

	Parameters:
	==========
	data : str
	the sequence of arm alternations.

	Return:
	=======
	errors: int
	number of alternation errors
	"""

	entries = list(data)
	# need to get rid of the first entries
	shortened_entries = entries[2:]
	errors = 0
	for i, letter in enumerate(shortened_entries):
	if shortened_entries[i] == (entries[i] or entries[i+1]):
	 errors+= 1
	return errors

def performance(data, errors):
	"""
	Calculates the Y maze performance of a mouse

	Parameters:
	===========
	data : str
	a single sequence of arm alternations.
	errors : int
	number of incorrect choices

	Return:
	=======
	performnce : float
	"""

	total_entries = len(list(data))
	potential_alternations = total_entries-2
	correct_choices = potential_alternations - errors
	performance = correct_choices / potential_alternations
	return performance