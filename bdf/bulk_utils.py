# coding: utf-8

import os
from bdf.bulk import Bulk


def extend_elements_from_nids(bulk, selected_nids):
    """
    """
    nid_to_eids_map = bulk.get_node_id_to_element_ids_map()
    # get eids attached to selected nids
    extended_eids = [i for nid in selected_nids for i in nid_to_eids_map[nid]]
    # get nids linked to extended eids
    extended_nids = list(set([nid for eid in extended_eids for nid in bulk.elements[eid].nodes]))

    # Loop while length of selected nids is lower than length of extended_nids
    if len(selected_nids) < len(extended_nids):
        extended_eids = extend_elements_from_nids(bulk, extended_nids)

    return list(set(extended_eids))


def main():
    """the interface for bulk_test"""
    # set file name of testing model
    test_path = os.path.join('..', 'models')
    bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

    # create instance of class Bulk
    bulk = Bulk()
    # read testing model
    bulk.read_bulk(bdf_filename)
    #
    part = extend_elements_from_nids(bulk, [473, 472])
    print(part)
    print(len(part))


if __name__ == '__main__':
    main()
