import unittest

from pydantic import ValidationError

from photonic_units import Frequency, FrequencyUnit, Wavelength, WavelengthUnit


class TestWavelength(unittest.TestCase):
    def test_explicit_unit_case_insensitive(self):
        wl = Wavelength(value=532.0, unit="nM")
        self.assertEqual(wl.value, 532.0)
        self.assertEqual(wl.unit, WavelengthUnit.NANOMETER)
        self.assertAlmostEqual(wl.value_si, 532.0e-9)

    def test_default_unit_is_nanometer(self):
        wl = Wavelength(value=532.0)
        self.assertEqual(wl.unit, WavelengthUnit.NANOMETER)
        self.assertAlmostEqual(wl.value_si, 532.0e-9)

    def test_micrometer_conversion(self):
        wl = Wavelength(value=532.0, unit="um")
        self.assertEqual(wl.unit, WavelengthUnit.MICROMETER)
        self.assertAlmostEqual(wl.value_si, 532.0e-6)

    def test_invalid_unit_raises(self):
        with self.assertRaises(ValidationError):
            Wavelength(value=532.0, unit="NotAUnit")

    def test_non_positive_value_raises(self):
        with self.assertRaises(ValidationError):
            Wavelength(value=0)


class TestFrequency(unittest.TestCase):
    def test_explicit_unit_enum(self):
        freq = Frequency(value=193.1, unit=FrequencyUnit.TERAHERTZ)
        self.assertEqual(freq.value, 193.1)
        self.assertEqual(freq.unit, FrequencyUnit.TERAHERTZ)
        self.assertAlmostEqual(freq.value_si, 193.1e12)

    def test_explicit_unit_case_insensitive(self):
        freq = Frequency(value=193.1, unit="khz")
        self.assertEqual(freq.unit, FrequencyUnit.KILOHERTZ)
        self.assertAlmostEqual(freq.value_si, 193.1e3)

    def test_default_unit_is_gigahertz(self):
        freq = Frequency(value=193.1)
        self.assertEqual(freq.unit, FrequencyUnit.GIGAHERTZ)
        self.assertAlmostEqual(freq.value_si, 193.1e9)

    def test_invalid_unit_raises(self):
        with self.assertRaises(ValidationError):
            Frequency(value=193.1, unit="NotAUnit")

    def test_non_positive_value_raises(self):
        with self.assertRaises(ValidationError):
            Frequency(value=0, unit=FrequencyUnit.GIGAHERTZ)


if __name__ == "__main__":
    unittest.main()
