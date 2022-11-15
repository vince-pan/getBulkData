from pyNastran.bdf.bdf import _get
def _set_selected_nids(bulk):
    """
    Select node ids from which search for attached element ids
    """
    #if selected_nids is empty
    if not bulk._selected_nids:
        bulk._selected_nids.append(bulk._bulk_nids[0])
    else:
        [bulk._selected_nids.append(bulk._attached_eids[i].node_ids) for i in bulk._attached_eids]

def _get_attached_eid_from_nid(bulk):
    """
    Get attached element ids from a node ids list
    """
    length = len(bulk._attached_eids)
    temp = get_eids_from_nid(bulk._selected_nids)
    for i in range (len(temp)):
        if temp[i] in bulk._attached_eids:
            continue
        else:
            #put the element in attached_eids if not already in
            bulk._attached_eids.append(temp[i])

    #Verify if elements has been added in attached_eids list
    if length == bulk._attached_eids.len():
        cur_part = PART()
        cur_part.elements = bulk._attached_eids
        bulk._part_list.append(cur_part)
    else:
        pass

def _remove_selected_nids_from_bulk_nids(bulk):
    """
    remove nodes in _selected_nids from _bulk_ids
    """
    for i in range (len(bulk._selected_nids)):
        bulk._bulk_nids.remove(bulk._selected_nids[i])