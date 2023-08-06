""" 
Tests for keogram.py and plot_keogram.py.
"""
import unittest
import pathlib
from datetime import datetime

import pandas as pd
import numpy as np

import asilib
from asilib.analysis.keogram import keogram
from asilib.plot.plot_keogram import plot_keogram


class Test_keogram(unittest.TestCase):
    def setUp(self):
        self.asi_array_code = 'REGO'
        self.location_code = 'LUCK'
        return

    def test_steve_keogram(self, create_reference=False):
        """
        Tests that the STEVE keogram pd.DataFrame is identical.
        """
        keo = keogram(
            self.asi_array_code,
            self.location_code,
            ['2017-09-27T08', '2017-09-27T08:10'],
            map_alt=230,
        )
        reference_path = pathlib.Path(
            asilib.config['ASILIB_DIR'], 'tests', 'data', 'test_steve_keogram.csv'
        )

        if create_reference:
            keo.to_csv(reference_path)
        keo_reference = pd.read_csv(reference_path, index_col=0, parse_dates=True)
        keo_reference.columns = map(float, keo_reference.columns)

        # Test that the keogram values are the same.
        assert np.all(keo.to_numpy() == keo_reference.to_numpy())
        # Test that the keogram latitudes are the same.
        assert np.all(np.isclose(keo.columns, keo_reference.columns))
        # Test that the indices (time stamps) are the same.
        assert np.all(keo.index == keo_reference.index)
        return

    def test_keogram_altitude_error(self):
        """
        Checks that keogram() raises an AssertionError if map_alt is not
        in the list of skymap calibration altitudes.
        """
        with self.assertRaises(AssertionError):
            keo = keogram(
                self.asi_array_code,
                self.location_code,
                ['2017-09-27T08', '2017-09-27T08:10'],
                map_alt=200,
            )
        return

    def test_keogram_no_images(self):
        """
        Checks that keogram() raises a ValueError if it tries to make a keogram with
        nonexistant data.
        """
        with self.assertRaises(ValueError):
            keo = keogram(
                "THEMIS", "ATHA", (datetime(2017, 9, 15, 2, 0, 0), datetime(2017, 9, 15, 3, 0, 0))
            )
        return


class Test_plot_keogram(unittest.TestCase):
    def setUp(self):
        self.asi_array_code = 'REGO'
        self.location_code = 'LUCK'
        return

    def test_steve_plot_keogram_alt(self):
        """
        Tests that the STEVE keogram plot is made without an error.
        """
        plot_keogram(
            self.asi_array_code,
            self.location_code,
            ['2017-09-27T08', '2017-09-27T08:10'],
            map_alt=230,
        )
        return

    def test_steve_plot_keogram_alt(self):
        """
        Tests that the STEVE keogram plot is made without an altitude (columns are the image indices).
        """
        plot_keogram(self.asi_array_code, self.location_code, ['2017-09-27T08', '2017-09-27T08:10'])
        return


if __name__ == '__main__':
    unittest.main()
