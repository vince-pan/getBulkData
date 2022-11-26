# coding: utf-8
from unittest import TestCase
import os

from bdf.bulk import Bulk


class TestBulk(TestCase):
    def setUp(self):
        test_path = os.path.join('..', '..', 'models')
        bdf_filename = os.path.join(test_path, 'FEM-001.bdf')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)


class TestRead(TestBulk):
    def test_2d_parts_number(self):
        self.assertEqual(len(self.bulk.part_2d), 6)

    def test_nb_of_elements_in_parts(self):
        elm_nb = {key: len(value.elements) for key, value in self.bulk.part_2d.items()}
        self.assertEqual(elm_nb, {11: 150, 12: 150, 13: 50, 14: 75, 15: 75, 16: 50})

    def test_2d_parts_element_id(self):
        # check_dict = {part_id: element_id}
        check_dict = {11: 11, 12: 12, 13: 13, 14: 15, 15: 16, 16: 14}
        for key, part_2d_obj in self.bulk.part_2d.items():
            for k in part_2d_obj.elements.keys():
                self.assertEqual(str(check_dict[key]), str(k)[:2])