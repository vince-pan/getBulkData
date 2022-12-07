"""
Main Bulk class.  Defines:
  - Bulk
  - Part2D
  - Fastener
  - Junction
"""

import numpy as np

from pyNastran.bdf.bdf import BDF
from utils.coord import Coord, Point


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

        # initialize read statement
        self.read_statement = ""

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
        try:
            # reading a full-run model
            self.read_bdf(bulk_filename)
            self.read_statement = "full-run"
        except RuntimeError:
            try:
                # reading a model-only model
                self.read_bdf(bulk_filename, punch=True)
                self.read_statement = "model-only"
            except RuntimeError:
                # non FEA model
                print('FATAL ERROR: Trying to read an non FEA model')
        except IOError as io_err:
            # bad model include in run file
            print(f'FATAL ERROR: {io_err.args[0]}')

        if self.read_statement:
            # get 2D parts with self.part_2d method
            self._get_part_2d()
            # set self.fasteners with method self._get_fasteners
            self._get_fasteners()
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
                part_2d = Part2D(part_id, elements_2d, self)
                self.part_2d[part_id] = part_2d
                # add ids of 2D parts nodes to selected_nids
                selected_nids = selected_nids + list(part_2d.nodes)
            # update bulk_nids
            bulk_nids = [nid for nid in bulk_nids if nid not in selected_nids]
            # increment part_id by 1
            part_id += 1

    def _get_fasteners(self):
        """
         Get all fasteners of a finite element model
        """
        self.fasteners = {rgd_element.eid: Fastener(rgd_element) for rgd_element in self.rigid_elements.values() if len(rgd_element.Gmi_ref) == 1}


class Part2D:
    """
    Part2d object
    """
    def __init__(self, part_id, elements, bulk):
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
        self.bulk = bulk
        self.nodes = self._get_nodes()

    def _get_nodes(self):
        """
        """
        nids = list(set([nid for elm in self.elements.values() for nid in elm.nodes]))
        return {nid: self.bulk.nodes[nid] for nid in self.bulk.nodes.keys() if nid in nids}


class Fastener:
    """
    Fastener object
    """
    def __init__(self, fastener):
        """
        Initialize Fastener object
        :param fastener: rigid element object
        """
        self.fastener = fastener
        # fastener id
        self.fastener_id = fastener.eid
        # fastener type
        self.fastener_type = fastener.type
        # fastener local coordinate system
        self.coord = self._get_fastener_coord()

    def _get_fastener_coord(self):
        """
        """
        # master node
        origin_point = Point(self.fastener.gn_ref.xyz[0],
                             self.fastener.gn_ref.xyz[1],
                             self.fastener.gn_ref.xyz[2])
        # slave node
        z_axis_point = Point(self.fastener.Gmi_ref[0].xyz[0],
                             self.fastener.Gmi_ref[0].xyz[1],
                             self.fastener.Gmi_ref[0].xyz[2])

        # xz plane point calculated by z axis vector 90° rotation
        xz_plane_point = self._compute_xz_plane_point()
        # fastener coordinate system define by 3 points : oirign, z point and xz plane point
        return Coord(origin_point, z_axis_point, xz_plane_point)

    def _compute_xz_plane_point(self):
        """
        """
        # 90 degrees z local axis vector rotation around y global axis
        x_axis = np.dot(np.array([[0, 0, 1],
                                          [0, 1, 0],
                                          [-1, 0, 0]]),
                                np.array([[self.fastener.Gmi_ref[0].xyz[0] - self.fastener.gn_ref.xyz[0]],
                                          [self.fastener.Gmi_ref[0].xyz[1] - self.fastener.gn_ref.xyz[1]],
                                          [self.fastener.Gmi_ref[0].xyz[2] - self.fastener.gn_ref.xyz[2]]])).flatten()
        # compute xz_plane_point in this way :
        # X_B = X_vector + X_A
        # Y_B = Y_vector + Y_A
        # Z_B = Z_vector + Z_A
        return Point(x_axis[0] + self.fastener.gn_ref.xyz[0],
                     x_axis[1] + self.fastener.gn_ref.xyz[1],
                     x_axis[2] + self.fastener.gn_ref.xyz[2])


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
