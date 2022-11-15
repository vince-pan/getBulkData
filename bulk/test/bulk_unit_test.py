import os

from bulk.bulk import Bulk

test_path = os.path.join('..', '..', 'models')
bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

bulk = Bulk()
bulk.read_bulk(bdf_filename)
bulk.get_parts_2d()
