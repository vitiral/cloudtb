# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 21:17:46 2013

@author: user
"""

import pdb
import sys, os
import rope
from pprint import pprint as pp

import rope.base.project
from rope.base import libutils

myproject = rope.base.project.Project(os.getcwd()) 
myresource = libutils.path_to_resource(myproject, 'textools.py')

from rope.refactor.extract import ExtractVariable
# extractor = ExtractVariable(myproject, resource, start, end)
# Where `start` and `end` are the offsets of the region to extract in
# resource. 
# class SimilarFinder(object) in refactor.similarfinder.py looks useful

from rope import refactor

 

# useful functions:
# rope.base.analyze_modules