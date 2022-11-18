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
        # read bdf file
        self.read_bdf(bulk_filename)
        # set self.part_2d with method
        self._get_part_2d()
        # set self.fasteners with method self._get_fasteners
        # set self.junctions with method self._get_junctions

    def _get_part_2d(self):
        """
        Get 2D parts of a finite element model
        """
        # list of all node ids
        _bulk_nids = list(self.node_ids)

        # blank element ids list
        _attached_eids = []

        # selected nids to search for attached elements
        _selected_nids = []

        # search for part 2d
        self._search_for_part_2d(_bulk_nids, _attached_eids, _selected_nids)

    def _search_for_part_2d(self, bulk_nids, attached_eids, selected_nids):
        """
        Search for part 2d
        :param self:
        :param bulk_nids:
        :param attached_eids:
        :param selected_nids:
        """
        # create a dict map with nodes and their attached elements
        nid_to_eids_map = self.get_node_id_to_element_ids_map()

        # entire model elements
        elements = self.elements

        # part id
        pid = 0

        length_old = len(attached_eids)

        # while bulk_nids is not empty, search for attached elements
        while bulk_nids:
            while length_old < len(attached_eids) or len(attached_eids) == 0:
                selected_nids = _set_selected_nids(bulk_nids, selected_nids, attached_eids, elements)
                bulk_nids = _remove_selected_nids_from_bulk_nids(bulk_nids, selected_nids)
                length_old = len(attached_eids)
                attached_eids = _get_attached_eid_from_nid(selected_nids, attached_eids, nid_to_eids_map)
            pid += 1
            # Part2D creation
            cur_part = Part2D(pid)
            # add attached element ids to part
            cur_part.elements = attached_eids
            # add current part to part_2d list
            self.part_2d[pid] = cur_part.elements
            selected_nids = []
            attached_eids = []


def _set_selected_nids(bulk_nids, selected_nids, attached_eids, elements):
    """
    Select node ids from which search for attached element id
    :param bulk_nids:
    :param selected_nids:
    :param attached_eids:
    :param elements:
    :return:
    """
    # if selected_nids is empty
    if not selected_nids:
        selected_nids.append(bulk_nids[0])
    else:
        selected_nids = []
        for i in range(len(attached_eids)):
            for j in range(len(elements[attached_eids[i]].node_ids)):
                if elements[attached_eids[i]].node_ids[j] not in selected_nids:
                    selected_nids.append(elements[attached_eids[i]].node_ids[j])
    return selected_nids


def _remove_selected_nids_from_bulk_nids(bulk_nids, selected_nids):
    """
    Remove nodes in bulk_ids from selected_nids
    :param bulk_nids:
    :param selected_nids:
    :return:
    """
    set_bulk_nids = set(bulk_nids)
    set_selected_nids = set(selected_nids)
    bulk_nids = list(set_bulk_nids.difference(set_selected_nids))
    return bulk_nids


def _get_attached_eid_from_nid(selected_nids, attached_eids, nid_to_eids_map):
    """
    Get attached element ids from a node ids list
    :param selected_nids:
    :param attached_eids:
    :param nid_to_eids_map:
    :return:
    """
    for i in range(len(selected_nids)):  # note : improve code by replacing for loop by concatenate function
        for j in range(len(nid_to_eids_map[selected_nids[i]])):
            if nid_to_eids_map[selected_nids[i]][j] not in attached_eids:
                attached_eids.append(nid_to_eids_map[selected_nids[i]][j])
    return attached_eids


class Part2D:
    """
    Part2d object
    """
    def __init__(self, part_id):
        """
        Initialize Part2d object
        :param part_id:
        """
        self.part_id = part_id
        self.elements = {}
