import unittest
from dnplab import dnpdata
from numpy.testing import assert_array_equal
import dnplab.dnpImport as wrapper
import dnplab.dnpNMR as nmr
import dnplab.dnpMath as Math
import dnplab as dnp
import numpy as np
import os
import copy
import matplotlib.pyplot as plt


class dnpNMR_tester(unittest.TestCase):
    def setUp(self):
        path = os.path.join(".", "data", "topspin", "304")
        self.data = wrapper.load(path, data_type="topspin")
        self.ws = dnp.create_workspace()
        self.ws["raw"] = self.data
        self.ws.copy("raw", "proc")

        path = os.path.join(".", "data", "topspin", "5")
        data = wrapper.load(path, data_type="topspin")
        self.ws_off = dnp.create_workspace()
        self.ws_off.add("raw", data)
        self.ws_off.copy("raw", "proc")

    def test_basic_nmr_processing(self):

        shape_data = np.shape(self.ws)
        n_pts = np.shape(self.ws["proc"])
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 1].real), 5.447918664876271, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 1].real), -4.128415225672084, places=4
        )

        nmr.remove_offset(self.ws)
        self.assertAlmostEqual(shape_data, np.shape(self.ws))
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 1].real), 5.445267326190019, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 1].real), -4.131066564358336, places=4
        )

        self.ws.copy("proc", "temp")
        nmr.left_shift(self.ws, shift_points=100)
        shifted_n_pts = np.shape(self.ws["proc"])
        self.assertEqual(shifted_n_pts[0], n_pts[0] - 100)
        self.ws.copy("temp", "proc")

        wf = Math.hamming_window(len(self.ws["proc"].values))
        self.assertEqual(max(wf), 1.0)
        self.assertAlmostEqual(min(wf), 0.07671999999999995, places=4)

        wf = Math.hann_window(len(self.ws["proc"].values))
        self.assertEqual(max(wf), 1.0)
        self.assertEqual(min(wf), 0.0)

        wf = Math.lorentz_gauss_window(self.ws["proc"], dim="t2", exp_lw=5, gauss_lw=10)
        self.assertAlmostEqual(max(wf), 1.1895922020471337, places=4)

        self.ws.copy("proc", "temp")
        nmr.window(self.ws, type="hamming", inverse=True)
        self.assertAlmostEqual(
            max(self.ws["proc"].values[0]),
            2.5727782192869477 - 4.397983406867447j,
            places=4,
        )
        self.ws.copy("temp", "proc")

        wf = Math.sin2_window(len(self.ws["proc"]))
        self.assertEqual(max(wf), 1.0)

        wf = Math.traf_window(self.ws["proc"], dim="t2", traf_lw = 1.)

        wf = Math.exponential_window(self.ws["proc"], "t2", 5)
        self.assertAlmostEqual(min(wf), 0.00035733315645396175, places=4)

        self.ws.copy("proc", "temp")
        nmr.window(self.ws, type="gaussian", linewidth=[2, 10])
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 1].real),
            5.456135803263017,
            places=4,
        )
        self.ws.copy("temp", "proc")

        self.ws.pop("temp")

        nmr.window(self.ws, type="exponential", linewidth=5)
        self.assertEqual(shape_data, np.shape(self.ws))
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 1].real), 5.390978190372195, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 1].real), -3.9647928998767163, places=4
        )

        nmr.fourier_transform(self.ws, zero_fill_factor=2)
        self.assertEqual(shape_data, np.shape(self.ws))
        self.assertEqual(len(self.ws["proc"].values[:, 4].real), 15844)
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 4].real), 61.3994271072369, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 4].real), -76.53300374124703, places=4
        )

        self.ws.copy("proc", "temp")
        nmr.autophase(
            self.ws,
            method="search",
            order="first",
            pivot=len(self.ws["proc"].values[:, 7]) / 2,
            delta=np.pi / 2,
            reference_slice=None,
            force_positive=False,
        )
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 3].real), 227.24572247945258, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 3].real), -157.25762551416526, places=4
        )
        phs0 = self.ws["proc"].attrs["phase0"]
        phs1 = self.ws["proc"].attrs["phase1"]
        self.assertEqual(len(phs1), len(self.ws["proc"].values))
        self.ws.copy("proc", "keep")
        self.ws.copy("temp", "proc")

        nmr.autophase(
            self.ws,
            method="arctan",
            order="zero",
            reference_slice=1,
            force_positive=True,
        )
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 7].real), 411.71339056159314, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 7].real), 0.13285193948862864, places=4
        )
        self.ws.copy("temp", "proc")

        nmr.autophase(
            self.ws,
            method="manual",
            order="first",
            pivot=len(self.ws["proc"].values[:, 7]) / 2,
            delta=np.pi / 2,
            phase=phs1 * (45 * np.pi / 180),
        )
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 3].real), 227.24572247945258, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 3].real), -157.25762551416526, places=4
        )
        self.ws.copy("temp", "proc")

        nmr.autophase(
            self.ws,
            method="manual",
            order="zero",
            phase=phs0 * (45 * np.pi / 180),
        )
        self.assertAlmostEqual(
            max(self.ws["proc"].values[:, 3].real), 238.27990936049952, places=4
        )
        self.assertAlmostEqual(
            min(self.ws["proc"].values[:, 3].real), -66.28951430959444, places=4
        )

    def test_calc_enhancement(self):

        nmr.remove_offset(self.ws)
        nmr.window(self.ws, linewidth=15)
        nmr.fourier_transform(self.ws, zero_fill_factor=2)
        nmr.autophase(self.ws, method="arctan")
        ws = copy.deepcopy(self.ws)
        dnp.dnpTools.integrate(self.ws, integrate_center=0, integrate_width="full")
        nmr.calculate_enhancement(self.ws)

        self.assertAlmostEqual(self.ws["enhancements"].values[0], 1.0, places=6)
        self.assertAlmostEqual(
            self.ws["enhancements"].values[-1], -1.3474199443567987, places=6
        )

        nmr.remove_offset(self.ws_off)
        nmr.window(self.ws_off, linewidth=15)
        nmr.fourier_transform(self.ws_off, zero_fill_factor=2)
        nmr.autophase(self.ws_off, method="arctan")

        nmr.calculate_enhancement(
            self.ws_off,
            off_spectrum=self.ws_off["proc"],
            on_spectra=ws["proc"],
            integrate_center="max",
            integrate_width="full",
            method="amplitude",
            dim="f2",
        )

        self.assertAlmostEqual(
            self.ws_off["enhancements"].values[0], -0.8783961394424274, places=6
        )
        self.assertAlmostEqual(
            self.ws_off["enhancements"].values[-1], 0.9658179866930302, places=6
        )


class dnpNMR_tester_sim(unittest.TestCase):
    def setUp(self):
        p1 = np.array([0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0])
        p2 = np.array([0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0, 0, 0])
        p3 = np.array([0, 0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0])
        self.data = dnpdata(
            np.array([p1, p2, p3]).T,
            [np.arange(0, len(p1)), np.arange(0, 3)],
            ["x", "t2"],
        )
        self.ws = dnp.create_workspace()
        self.ws["raw"] = self.data
        self.ws.copy("raw", "proc")

    def test_align(self):
        nmr.align(self.ws, dim="x")
        assert_array_equal(
            self.ws["proc"].values,
            np.array(
                [
                    [0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0],
                    [0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0],
                    [0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0],
                ]
            ).T,
        )
