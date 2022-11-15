def _set_selected_nids(bulk):
    """
    Select node ids from which search for attached element ids
    """
    if bulk.selected_nids.len() == 0:  # if not bulk.selected_nids:
        bulk.selected_nids = bulk.bulk_nids[0]
    else
        bulk.selected_nids = [bulk.attached_eids[i].node_ids for i in bulk.attached_eids]

