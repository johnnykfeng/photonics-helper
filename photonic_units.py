import math
from enum import Enum

from pydantic import BaseModel, Field, model_validator

SPEED_OF_LIGHT = 2.998e8  # m/s

class WavelengthUnit(str, Enum):
    """Enumeration of permitted wavelength units in optics (case-insensitive parsing)."""
    NANOMETER = "nm"
    MICROMETER = "um"  # 'μm' is also valid if you prefer unicode
    FEMTOMETER = "fm"
    PICOMETER = "pm"
    MILLIMETER = "mm"
    METER = "m"
    ANGSTROM = "A"     # 'Å' can also be used

    @classmethod
    def _missing_(cls, value):
        """Allow case-insensitive matching for unit strings."""
        if not isinstance(value, str):
            return None
        value_lower = value.lower()
        # Accept both "A" and "a" for Angstrom, and also unicode 'Å' or 'å'
        special_angstroms = {"a", "å", "angstrom"}
        if value_lower in special_angstroms:
            return cls.ANGSTROM
        for member in cls:
            if member.value.lower() == value_lower:
                return member
        return None

_WAVELENGTH_UNIT_FACTORS = {
    WavelengthUnit.NANOMETER: 1e-9,
    WavelengthUnit.MICROMETER: 1e-6,
    WavelengthUnit.FEMTOMETER: 1e-15,
    WavelengthUnit.PICOMETER: 1e-12,
    WavelengthUnit.MILLIMETER: 1e-3,
    WavelengthUnit.METER: 1,
    WavelengthUnit.ANGSTROM: 1e-10,
}

class Wavelength(BaseModel):
    """Model representing an optical wavelength with constrained units."""
    value_si: float = Field(
        ...,
        gt=0,
        description="The wavelength in SI units (meters, must be strictly positive).",
    )
    unit: WavelengthUnit = Field(
        default=WavelengthUnit.NANOMETER,
        description="The unit of measurement for the wavelength.",
    )

    @property
    def value_unit(self) -> float:
        """Return the wavelength expressed in the selected unit."""
        return self.value_si / _WAVELENGTH_UNIT_FACTORS[self.unit]


class FrequencyUnit(str, Enum):
    """Enumeration of permitted frequency units in optics (case-insensitive parsing)."""
    HERTZ = "Hz"
    KILOHERTZ = "kHz"
    MEGAHERTZ = "MHz"
    GIGAHERTZ = "GHz"
    TERAHERTZ = "THz"

    @classmethod
    def _missing_(cls, value):
        """Allow case-insensitive matching for unit strings."""
        if not isinstance(value, str):
            return None
        value_lower = value.lower()
        for member in cls:
            if member.value.lower() == value_lower:
                return member
        return None

_FREQUENCY_UNIT_FACTORS = {
    FrequencyUnit.HERTZ: 1,
    FrequencyUnit.KILOHERTZ: 1e3,
    FrequencyUnit.MEGAHERTZ: 1e6,
    FrequencyUnit.GIGAHERTZ: 1e9,
    FrequencyUnit.TERAHERTZ: 1e12,
}

class Frequency(BaseModel):
    """Model representing an optical frequency with constrained units."""
    value_si: float = Field(
        ...,
        gt=0,
        description="The frequency in SI units (hertz, must be strictly positive).",
    )
    unit: FrequencyUnit = Field(
        default=FrequencyUnit.GIGAHERTZ,
        description="The unit of measurement for the frequency.",
    )

    @property
    def value_unit(self) -> float:
        """Return the frequency expressed in the selected unit."""
        return self.value_si / _FREQUENCY_UNIT_FACTORS[self.unit]


class AngularFrequencyUnit(str, Enum):
    """Enumeration of permitted angular frequency units (case-insensitive parsing)."""
    RAD_PER_SEC = "rad/s"
    KILO_RAD_PER_SEC = "krad/s"
    MEGA_RAD_PER_SEC = "Mrad/s"
    GIGA_RAD_PER_SEC = "Grad/s"
    TERA_RAD_PER_SEC = "Trad/s"

    @classmethod
    def _missing_(cls, value):
        """Allow case-insensitive matching for unit strings."""
        if not isinstance(value, str):
            return None
        value_lower = value.lower()
        for member in cls:
            if member.value.lower() == value_lower:
                return member
        return None

_ANGULAR_FREQUENCY_UNIT_FACTORS = {
    AngularFrequencyUnit.RAD_PER_SEC: 1,
    AngularFrequencyUnit.KILO_RAD_PER_SEC: 1e3,
    AngularFrequencyUnit.MEGA_RAD_PER_SEC: 1e6,
    AngularFrequencyUnit.GIGA_RAD_PER_SEC: 1e9,
    AngularFrequencyUnit.TERA_RAD_PER_SEC: 1e12,
}

class AngularFrequency(BaseModel):
    """Model representing an angular frequency with constrained units."""
    value_si: float = Field(
        ...,
        gt=0,
        description="The angular frequency in SI units (rad/s, must be strictly positive).",
    )
    unit: AngularFrequencyUnit = Field(
        default=AngularFrequencyUnit.RAD_PER_SEC,
        description="The unit of measurement for the angular frequency.",
    )

    @property
    def value_unit(self) -> float:
        """Return the angular frequency expressed in the selected unit."""
        return self.value_si / _ANGULAR_FREQUENCY_UNIT_FACTORS[self.unit]


class PhotonicUnit(BaseModel):
    """Photonic quantity with synchronized wavelength, frequency, and angular frequency.

    Initialize with exactly one of ``wavelength``, ``frequency``, or ``angular_frequency``;
    the other two representations are derived automatically.
    """
    wavelength: Wavelength
    frequency: Frequency
    angular_frequency: AngularFrequency

    @model_validator(mode="before")
    @classmethod
    def _derive_all_quantities(cls, data):
        if isinstance(data, PhotonicUnit):
            return {
                "wavelength": data.wavelength,
                "frequency": data.frequency,
                "angular_frequency": data.angular_frequency,
            }

        if not isinstance(data, dict):
            raise TypeError("PhotonicUnit must be initialized with keyword arguments")

        wavelength = data.get("wavelength")
        frequency = data.get("frequency")
        angular_frequency = data.get("angular_frequency")
        provided = sum(value is not None for value in (wavelength, frequency, angular_frequency))
        if provided != 1:
            raise ValueError(
                "Exactly one of wavelength, frequency, or angular_frequency must be provided"
            )

        if wavelength is not None:
            if not isinstance(wavelength, Wavelength):
                wavelength = Wavelength(value_si=wavelength)
            wl_si = wavelength.value_si
            freq_hz = SPEED_OF_LIGHT / wl_si
            omega_rad_s = 2 * math.pi * freq_hz
            return {
                "wavelength": wavelength,
                "frequency": Frequency(value_si=freq_hz, unit=FrequencyUnit.GIGAHERTZ),
                "angular_frequency": AngularFrequency(
                    value_si=omega_rad_s,
                    unit=AngularFrequencyUnit.TERA_RAD_PER_SEC,
                ),
            }

        if frequency is not None:
            if not isinstance(frequency, Frequency):
                frequency = Frequency(value_si=frequency)
            freq_hz = frequency.value_si
            wl_si = SPEED_OF_LIGHT / freq_hz
            omega_rad_s = 2 * math.pi * freq_hz
            return {
                "wavelength": Wavelength(value_si=wl_si),
                "frequency": frequency,
                "angular_frequency": AngularFrequency(
                    value_si=omega_rad_s,
                    unit=AngularFrequencyUnit.TERA_RAD_PER_SEC,
                ),
            }

        if not isinstance(angular_frequency, AngularFrequency):
            angular_frequency = AngularFrequency(value_si=angular_frequency)
        omega_rad_s = angular_frequency.value_si
        wl_si = 2 * math.pi * SPEED_OF_LIGHT / omega_rad_s
        freq_hz = omega_rad_s / (2 * math.pi)
        return {
            "wavelength": Wavelength(value_si=wl_si),
            "frequency": Frequency(value_si=freq_hz, unit=FrequencyUnit.GIGAHERTZ),
            "angular_frequency": angular_frequency,
        }


FREQUENCY_UNIT_MAP = {
    "Hz": FrequencyUnit.HERTZ,
    "kHz": FrequencyUnit.KILOHERTZ,
    "MHz": FrequencyUnit.MEGAHERTZ,
    "GHz": FrequencyUnit.GIGAHERTZ,
    "THz": FrequencyUnit.TERAHERTZ,
}

FREQUENCY_UNIT_FACTOR_MAP = {
    "Hz": 1,
    "kHz": 1e3,
    "MHz": 1e6,
    "GHz": 1e9,
    "THz": 1e12,
}

WAVELENGTH_UNIT_MAP = {
    "fm": WavelengthUnit.FEMTOMETER,
    "pm": WavelengthUnit.PICOMETER,
    "nm": WavelengthUnit.NANOMETER,
    "um": WavelengthUnit.MICROMETER,
    "mm": WavelengthUnit.MILLIMETER,
    "m": WavelengthUnit.METER,
}

WAVELENGTH_UNIT_FACTOR_MAP = {
    "fm": 1e-15,
    "pm": 1e-12,
    "nm": 1e-9,
    "um": 1e-6,
    "mm": 1e-3,
    "m": 1,
}

if __name__ == "__main__":
    # pu = PhotonicUnit(wavelength=Wavelength(value_si=532.0e-9, unit="nm"))
    pu = PhotonicUnit(wavelength=1550e-9)

    print(pu.wavelength.value_si)
    print(pu.frequency.value_si)
    print(pu.angular_frequency.value_si)
    
    print(pu.wavelength.value_unit, pu.wavelength.unit.value)
    print(pu.frequency.value_unit, pu.frequency.unit.value)
    print(pu.angular_frequency.value_unit, pu.angular_frequency.unit.value)
