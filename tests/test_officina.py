"""
tests/test_officina.py
----------------------
La cartella officina (`set_officina`, MAP.md D60, D62): calibrazioni e
spessori di chi usa snapbend, fuori dal pacchetto. Facoltativa: senza,
snapbend funziona con i dati inclusi (D61).
"""

import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

import snapbend
from snapbend import Bend, BentProfile, Calibration, SheetThicknessTable
from snapbend.rules.officina import officina_folder, set_officina
from snapbend.rules.read_section import _SHEET_TABLE


@contextmanager
def officina(path):
    set_officina(path)
    try:
        yield
    finally:
        set_officina(None)


class TestCartellaOfficina(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        (self.folder / "calibrations").mkdir()
        (self.folder / "calibrations" / "mia.json").write_text(json.dumps(
            {"nome": "mia", "cava_per_spessore": {"2": 12}}), encoding="utf-8")
        (self.folder / "calibrations" / "default.json").write_text(json.dumps(
            {"nome": "default", "cava_per_spessore": {"2": 99}}), encoding="utf-8")
        (self.folder / "sheet_thicknesses.json").write_text(json.dumps(
            {"thicknesses_mm": [2, 4], "tolerance_mm": 0.1}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_senza_officina(self):
        self.assertIsNone(officina_folder())
        self.assertEqual(Calibration.load("default").data["nome"], "default")

    def test_calibrazione_dalla_cartella_officina(self):
        with officina(self.folder):
            self.assertEqual(Calibration.load("mia").data["cava_per_spessore"], {"2": 12})

    def test_la_cartella_officina_vince_sulle_incluse(self):
        with officina(self.folder):
            self.assertEqual(Calibration.load("default").data["cava_per_spessore"], {"2": 99})

    def test_spessori_dalla_cartella_officina(self):
        with officina(self.folder):
            self.assertEqual(SheetThicknessTable.load().thicknesses_mm, [2.0, 4.0])

    def test_cartella_che_non_esiste(self):
        with officina(self.folder / "manca"):
            with self.assertRaises(FileNotFoundError):
                Calibration.load("mia")

    def test_calibrazione_che_non_esiste(self):
        with officina(self.folder):
            with self.assertRaises(FileNotFoundError):
                Calibration.load("nessuna")


class TestZeroConfig(unittest.TestCase):
    """Chi installa snapbend non configura niente (MAP.md D61): i dati inclusi
    stanno dentro il pacchetto, così `pip install` li porta con sé."""

    def test_dati_inclusi_dentro_il_pacchetto(self):
        package = Path(snapbend.__file__).resolve().parent
        for path in (Calibration.CALIBRATIONS_FOLDER / "default.json",
                     Calibration.CALIBRATIONS_FOLDER / "inside_sum.json", _SHEET_TABLE):
            self.assertTrue(path.is_file(), path)
            self.assertTrue(path.resolve().is_relative_to(package), path)

    def test_piega_senza_officina(self):
        flat = BentProfile(flanges=[50, 80, 50], bends=[Bend(angle=90), Bend(angle=90)],
                           thickness=2, width=300).develop()
        self.assertTrue(flat.entities)
        self.assertTrue(SheetThicknessTable.load().thicknesses_mm)


if __name__ == "__main__":
    unittest.main()
