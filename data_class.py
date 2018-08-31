# Copyright (c) 2018 Kyle Lopin (Naresuan University) <kylel@nu.ac.th>

"""
Data class to hold data from IoT sensor nodes
"""

# standard libraries
import array
import logging


__author__ = 'Kyle Vitautas Lopin'

class StreamingData(object):
    def __init__(self):
        self.number_nodes = 3
