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
        # read bulk file
        self.read_bdf(bulk_filename)
        # get 2D parts with self.part_2d method
        self._get_part_2d()
        # set self.fasteners with method self._get_fasteners
        # set self.junctions with method self._get_junctions

    def _get_part_2d(self):
        """
        Get 2D parts of a finite element model
        """
        # set first 2D part id
        part_id = 11
        #
        bulk_nids = list(self.node_ids)
        # while bulk_nids is not empty, search for attached elements
        while bulk_nids:
            # select starting nid
            selected_nids = [bulk_nids[0]]
            # get extended 2D elements from nid
            elements_2d = extend_2d_elements_from_nids(self, selected_nids)
            # store instance of Part2D
            if elements_2d:
                part_2d = Part2D(part_id, elements_2d)
                self.part_2d[part_id] = part_2d
                # add ids of 2D parts nodes to selected_nids
                selected_nids = selected_nids + part_2d.nodes
            # update bulk_nids
            bulk_nids = [nid for nid in bulk_nids if nid not in selected_nids]
            # increment part_id by 1
            part_id += 1


class Part2D:
    """
    Part2d object
    """
    def __init__(self, part_id, elements):
        """
        Initialize Part2d object

        Parameters
        ----------
        part_id: int
            id number of part object
        elements: dict {element_id_1: element_obj_1, ..., element_id_n: element_obj_n}
            dictionary of all element's objects of the part object
        """
        self.part_id = part_id
        self.elements = elements
        self.nodes = self._get_nodes()

    def _get_nodes(self):
        """
        """
        return list(set([nid for elm in self.elements.values() for nid in elm.nodes]))


def extend_2d_elements_from_nids(bulk, selected_nids):
    """
    """
    # define list of 2D element types
    elm_2d_type = ['CQUAD4', 'CTRIA3']
    # get 2D elements ids linked to each nid of the model
    nid_to_2d_eids_map = {nid: [eid for eid in eids if bulk.elements[eid].type in elm_2d_type]
                          for nid, eids in bulk.get_node_id_to_element_ids_map().items()}
    # get eids attached to selected nids
    extended_eids = [eid for nid in selected_nids for eid in nid_to_2d_eids_map[nid]]
    # get nids linked to extended eids
    extended_nids = list(set([nid for eid in extended_eids for nid in bulk.elements[eid].nodes]))
    # loop while length of selected nids is lower than length of extended_nids
    if len(selected_nids) < len(extended_nids):
        extended_eids = extend_2d_elements_from_nids(bulk, extended_nids)
    # return only 2D elements
    return {eid: bulk.elements[eid] for eid in list(set(extended_eids))}
