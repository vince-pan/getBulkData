# coding: utf-8
"""
Main Bulk class.  Defines:
  - Bulk
  - Part2D
  - Fastener
  - Junction
"""

from pyNastran.bdf.bdf import BDF
from bulk_utils import _set_selected_nids, _get_attached_eid_from_nid

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
        self._bulk_nids = self.node_ids

        # blank part list
        self._part_list = {}

        # blank element ids list
        self._attached_eids = {}

        # blank node list from which search for elements
        self._selected_nids = {}

        # while bulk_nids is not empty, search for attached elements
        while self._bulk_nids.len() =! 0:
            self._selected_nids = _set_selected_nids(bulk)
            self._bulk_nids.remove(self._selected_nids)
            self._attached_eid, part_list = _get_attached_eid_from_nid(bulk)
