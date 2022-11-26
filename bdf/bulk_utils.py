# coding: utf-8
def extend_2d_elements_from_nids(bulk, selected_nids):
    """
    """
    # get 2D elements ids linked to each nid of the model
    nid_to_2d_eids_map = get_node_id_to_2d_element_ids_map(bulk)
    # get eids attached to selected nids
    extended_eids = [eid for nid in selected_nids for eid in nid_to_2d_eids_map[nid]]
    # get nids linked to extended eids
    extended_nids = list(set([nid for eid in extended_eids for nid in bulk.elements[eid].nodes]))

    # loop while length of selected nids is lower than length of extended_nids
    if len(selected_nids) < len(extended_nids):
        extended_eids = extend_2d_elements_from_nids(bulk, extended_nids)

    # return only 2D elements
    return {eid: bulk.elements[eid] for eid in list(set(extended_eids))}


def get_node_id_to_2d_element_ids_map(bdf):
    """

    """
    elm_2d_type = ['CQUAD4', 'CTRIA3']
    nid_to_2d_elm_map = {}
    for nid, eids in bdf.get_node_id_to_element_ids_map().items():
        nid_to_2d_elm_map[nid] = [eid for eid in eids if bdf.elements[eid].type in elm_2d_type]
    return nid_to_2d_elm_map
