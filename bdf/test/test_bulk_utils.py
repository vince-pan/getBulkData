import unittest
import os

from bdf.bulk import Bulk
from bdf.bulk_utils import extend_2d_elements_from_nids


class TestExtendElements(unittest.TestCase):
    def setUp(self):
        test_path = os.path.join('../..', 'models')
        bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)

        self.selected_nids = [562]
        self.part = extend_2d_elements_from_nids(self.bulk, self.selected_nids)

    def test_is_output_dictionary(self):
        self.assertIsInstance(self.part, dict)

    def test_number_of_elements(self):
        self.assertEqual(len(self.part), 75)

    def test_elements_types(self):
        elm_types = list(set([elm_obj.type for elm_obj in self.part.values()]))
        for elm_type in elm_types:
            with self.subTest(elm_type=elm_type):
                self.assertIn(elm_type, ['CQUAD4', 'CTRIA3'])
