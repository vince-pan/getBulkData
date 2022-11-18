# coding: utf-8
"""the interface for bulk_test"""

import os

from bulk.bulk import Bulk

test_path = os.path.join('..', '..', 'models')
bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

# create instance of class Bulk
bulk = Bulk()
# read testing model
bulk.read_bulk(bdf_filename)
# print model stat
print(bulk.get_bdf_stats())
