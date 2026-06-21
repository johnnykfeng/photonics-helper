from enum import Enum

from pydantic import BaseModel, Field

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

class Wavelength(BaseModel):
    """Model representing an optical wavelength with constrained units."""
    value: float = Field(
        ..., 
        gt=0, 
        description="The numerical value of the wavelength (must be strictly positive)."
    )
    unit: WavelengthUnit = Field(
        default=WavelengthUnit.NANOMETER,
        description="The unit of measurement for the wavelength."
    )

    @property
    def value_si(self) -> float:
        """Return the value of the wavelength in SI units (meters)."""
        unit_factors = {
            "nm": 1e-9,
            "um": 1e-6,
            "fm": 1e-15,
            "pm": 1e-12,
            "mm": 1e-3,
            "m": 1,
            "A": 1e-10,
        }
        return self.value * unit_factors[self.unit]

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

class Frequency(BaseModel):
    """Model representing an optical frequency with constrained units."""
    value: float = Field(
        ...,
        gt=0,
        description="The numerical value of the frequency (must be strictly positive)."
    )
    unit: FrequencyUnit = Field(
        default=FrequencyUnit.GIGAHERTZ,
        description="The unit of measurement for the frequency."
    )

    @property
    def value_si(self) -> float:
        """Return the value of the frequency in SI units (Hz)."""
        unit_factors = {
            "Hz": 1,
            "kHz": 1e3,
            "MHz": 1e6,
            "GHz": 1e9,
            "THz": 1e12,
        }
        return self.value * unit_factors[self.unit.value]
