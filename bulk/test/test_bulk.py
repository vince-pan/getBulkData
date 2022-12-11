# coding: utf-8
from unittest import TestCase
import os
import numpy as np

from bulk.bulk import Bulk


class TestBulk(TestCase):
    def setUp(self):
        test_path = os.path.join('..', '..', 'models', 'FEM-001')
        bdf_filename = os.path.join(test_path, 'FEM-001-full-run.bdf')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)


class TestGetPart2D(TestBulk):
    def test_2d_parts_number(self):
        self.assertEqual(len(self.bulk.part_2d), 6)

    def test_nb_of_elements_in_parts(self):
        elm_nb = {key: len(value.elements) for key, value in self.bulk.part_2d.items()}
        self.assertEqual(elm_nb, {11: 150, 12: 150, 13: 50, 14: 50, 15: 75, 16: 75})

    def test_2d_parts_element_id(self):
        # check_dict = {part_id: element_id}
        check_dict = {11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16}
        for key, part_2d_obj in self.bulk.part_2d.items():
            for k in part_2d_obj.elements.keys():
                self.assertEqual(str(check_dict[key]), str(k)[:2])

    def test_elements_types(self):
        elm_types = list(set([elm.type for part in self.bulk.part_2d.values() for elm in part.elements.values()]))
        for elm_type in elm_types:
            with self.subTest(elm_type=elm_type):
                self.assertIn(elm_type, ['CQUAD4', 'CTRIA3'])


class TestReadBulk(TestCase):
    def test_read_model_only(self):
        test_path = os.path.join('..', '..', 'models', 'FEM-001')
        bdf_filename = os.path.join(test_path, 'FEM-001-model-only.bdf')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)

    def test_read_run_include(self):
        test_path = os.path.join('..', '..', 'models', 'FEM-001')
        bdf_filename = os.path.join(test_path, 'FEM-001-run-include.dat')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)

    def test_read_run_bad_include(self):
        test_path = os.path.join('..', '..', 'models', 'FEM-001')
        bdf_filename = os.path.join(test_path, 'FEM-001-run-bad-include.dat')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)

    def test_read_no_fea_model(self):
        test_path = os.path.join('..', '..', 'models', 'dummy')
        bdf_filename = os.path.join(test_path, 'non-model-file.txt')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)


class TestBulk2(TestCase):
    def setUp(self):
        test_path = os.path.join('..', '..', 'models', 'FEM-002')
        bdf_filename = os.path.join(test_path, 'FEM-002.bdf')
        self.bulk = Bulk()
        self.bulk.read_bulk(bdf_filename)


class TestGetFasteners(TestBulk2):
    def test_fastener_number(self):
        self.assertEqual(len(self.bulk.fasteners), 5)

    def test_vector_normalization(self):
        vectors = [fastener.coord.x_vector for fastener in self.bulk.fasteners.values()]
        for vector in vectors:
            self.assertEqual(np.linalg.norm(vector), 1.0)

    def test_det_matrix(self):
        matrices = [fastener.coord.transformation_matrix for fastener in self.bulk.fasteners.values()]
        for matrix in matrices:
            self.assertEqual(np.linalg.det(matrix), 1)
