def _set_selected_nids(bulk):
    """
    Select node ids from which search for attached element ids
    """
    if bulk.selected_nids.len() == 0:  # if not bulk.selected_nids:
        bulk.selected_nids = bulk.bulk_nids[0]
    else
        bulk.selected_nids = [bulk.attached_eids[i].node_ids for i in bulk.attached_eids]

def _get_attached_eid_from_nid(bulk):
    """
    Get attached element ids from a node ids list
    """
    len = bulk.attached_eids.len()
    temp = get_eids_from_nid(bulk.selected_nids)

    for i in temp:
        if temp[i] in bulk.attached_eids:
            continue
        else
            bulk.attached_eids.append(temp[i])
    # On vérifie si des éléments ont été ajoutés à attached_eids

    if len == bulk.attached_eids.len():
        cur_part = PART()
        cur_part.elements = bulk.attached_eids
        bulk.part_list.append(cur_part)
    else
        pass
