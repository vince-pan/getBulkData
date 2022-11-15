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
        """
        Read method for the bulk files

        Parameters
        ----------
        bulk_filename: str
            the input bulk file
        """
        self.read_bdf(bulk_filename)
        # set self.part_2d with method self._get_part_2d
        # set self.fasteners with method self._get_fasteners
        # set self.junctions with method self._get_junctions

    def get_parts_2d(self):
        """
        Get 2D parts of a finite element model
        """
        # list of all node ids
        self.bulk_nids = self.node_ids

        # blank part list
        self.part_list = {}

        # blank element ids list
        self.attached_eids = {}

        # blank node list from which search for elements
        self.selected_nids = {}

        # while bulk_nids is not empty, search for attached elements
        while bulk_nids.len() =! 0:
            self.selected_nids = self._set_selected_nids(bulk)
            self.bulk_nids.remove(self.selected_nids)
            self.attached_eid, part_list = self._get_attached_eid_from_nid()