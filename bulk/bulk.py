# coding: utf-8
"""
Main Bulk class.  Defines:
  - Bulk
  - Part2D
  - Fastener
  - Junction
"""

from pyNastran.bdf.bdf import BDF


class Bulk(BDF):
    """
    NASTRAN BDF Reader/Writer/Editor class with additional data:
        - 2D part list
        - Junction list
    """
    def __init__(self):
        """
        Initialize the Bulk object
        """
        # Initialize BDF class
        super().__init__()

        # store 2D parts
        self.part_2d = {}
        # store fasteners
        self.fasteners = {}
        # store junctions
        self.junctions = {}

    def read_bulk(self, bulk_filename):
        self.read_bdf(bulk_filename)
        # set self_2d with function _get_part_2d
