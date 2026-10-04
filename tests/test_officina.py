"""
tests/test_officina.py
----------------------
La cartella officina (`SNAPBEND_OFFICINA`, MAP.md D60): calibrazioni e
spessori di chi usa snapbend, fuori dal repo.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from snapbend import Calibration, SheetThicknessTable
from snapbend.rules.officina import OFFICINA_ENV, officina_folder, set_officina


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

    def _con_officina(self):
        return mock.patch.dict(os.environ, {OFFICINA_ENV: str(self.folder)})

    def test_senza_variabile_nessuna_officina(self):
        with mock.patch.dict(os.environ, {OFFICINA_ENV: ""}):
            self.assertIsNone(officina_folder())
            self.assertEqual(Calibration.load("default").data["nome"], "default")

    def test_calibrazione_dalla_cartella_officina(self):
        with self._con_officina():
            self.assertEqual(Calibration.load("mia").data["cava_per_spessore"], {"2": 12})

    def test_la_cartella_officina_vince_sugli_esempi_del_repo(self):
        with self._con_officina():
            self.assertEqual(Calibration.load("default").data["cava_per_spessore"], {"2": 99})

    def test_spessori_dalla_cartella_officina(self):
        with self._con_officina():
            self.assertEqual(SheetThicknessTable.load().thicknesses_mm, [2.0, 4.0])

    def test_set_officina_vince_sulla_variabile(self):
        altra = Path(self.tmp.name) / "altra"
        (altra / "calibrations").mkdir(parents=True)
        (altra / "calibrations" / "mia.json").write_text(json.dumps(
            {"nome": "mia", "cava_per_spessore": {"2": 7}}), encoding="utf-8")
        with self._con_officina():
            set_officina(altra)
            try:
                self.assertEqual(Calibration.load("mia").data["cava_per_spessore"], {"2": 7})
            finally:
                set_officina(None)
            self.assertEqual(Calibration.load("mia").data["cava_per_spessore"], {"2": 12})

    def test_cartella_che_non_esiste(self):
        with mock.patch.dict(os.environ, {OFFICINA_ENV: str(self.folder / "manca")}):
            with self.assertRaises(FileNotFoundError):
                Calibration.load("mia")

    def test_calibrazione_che_non_esiste(self):
        with self._con_officina():
            with self.assertRaises(FileNotFoundError):
                Calibration.load("nessuna")


if __name__ == "__main__":
    unittest.main()


class TestZeroConfig(unittest.TestCase):
    """Chi installa snapbend non configura niente (MAP.md D61): i dati inclusi
    stanno dentro il pacchetto, così `pip install` li porta con sé."""

    def test_dati_inclusi_dentro_il_pacchetto(self):
        import snapbend
        from snapbend.rules.read_section import _SHEET_TABLE
        package = Path(snapbend.__file__).resolve().parent
        for path in (Calibration.CALIBRATIONS_FOLDER / "default.json", _SHEET_TABLE):
            self.assertTrue(path.is_file(), path)
            self.assertTrue(path.resolve().is_relative_to(package), path)

    def test_piega_senza_officina(self):
        from snapbend import Bend, BentProfile
        with mock.patch.dict(os.environ, {OFFICINA_ENV: ""}):
            flat = BentProfile(flanges=[50, 80, 50], bends=[Bend(angle=90), Bend(angle=90)],
                               thickness=2, width=300).develop()
            self.assertTrue(flat.entities)
            self.assertTrue(SheetThicknessTable.load().thicknesses_mm)
