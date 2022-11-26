# coding: utf-8
def extend_2d_elements_from_nids(bulk, selected_nids, iter_nb=9999):
    """

    :param bulk:
    :param selected_nids:
    :param iter_nb:
    :return:
    """
    # define 2D element types
    elm_2d_type = ['CQUAD4', 'CTRIA3']
    # get eids linked to each nid of the model
    nid_to_eids_map = bulk.get_node_id_to_element_ids_map()
    # get eids attached to selected nids
    extended_eids = [eid for nid in selected_nids for eid in nid_to_eids_map[nid]]
    # get nids linked to extended eids
    extended_nids = list(set([nid for eid in extended_eids for nid in bulk.elements[eid].nodes]))

    # loop while all 2D elements of a 2D parts has been found
    # or loop while iter_nb > 1
    if iter_nb == 9999:
        # loop while length of selected nids is lower than length of extended_nids
        if len(selected_nids) < len(extended_nids):
            extended_eids = extend_2d_elements_from_nids(bulk, extended_nids)

    else:
        # loop while iter_nb > 1
        if iter_nb > 1:
            extended_eids = extend_2d_elements_from_nids(bulk, extended_nids, iter_nb - 1)

    # return only 2D elements
    return {eid: bulk.elements[eid] for eid in list(set(extended_eids))
            if bulk.elements[eid].type in elm_2d_type}
