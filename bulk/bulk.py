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
        _bulk_nids = list(self.node_ids)

        # blank element ids list
        _attached_eids = []

        # selected nids to search for attached elements
        _selected_nids = []

        # while bulk_nids is not empty, search for attached elements
        while _bulk_nids:
            _selected_nids = _set_selected_nids()
            _bulk_nids = _remove_selected_nids_from_bulk_nids(self)
            _attached_nids = _get_attached_eid_from_nid(self)


def _set_selected_nids(bulk_nids, selected_nids, attached_eids):
    """
    Select node ids from which search for attached element ids
    """
    # if selected_nids is empty
    if not selected_nids:
        selected_nids.append(bulk_nids[0])
    else:
        [selected_nids.append(attached_eids[i].node_ids) for i in attached_eids]
    return selected_nids


def _get_attached_eid_from_nid(selected_nids, attached_eids):
    """
    Get attached element ids from a node ids list
    """
    temp = get_eids_from_nid(selected_nids)
    for i in range(len(temp)):
        if temp[i] in attached_eids:
            # ignore
            continue
        else:
            # put the element in attached_eids if not already in
            attached_eids.append(temp[i])
    return attached_eids


def _remove_selected_nids_from_bulk_nids(bulk_nids, selected_nids):
    """
    remove nodes in _selected_nids from _bulk_ids
    """
    for i in range(len(selected_nids)):
        bulk_nids.remove(selected_nids[i])
    return bulk_nids


class Part2D:
    """
    Part2d object
    """
    def __init__(self):
        """
        Initialize Part2d object
        """
        self.id = None
        self.elements = {}
