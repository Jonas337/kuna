"""Table-driven coverage for the SAB 80C517A/83C517A-5 processor spec."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "specs/Ghidra/Processors/8051/data/languages/80c517.pspec"
LDEFS = ROOT / "specs/Ghidra/Processors/8051/data/languages/8051.ldefs"

SFR = {
    'ACC': 0xe0,
    'ADCON0': 0xd8,
    'ADCON1': 0xdc,
    'ADDATH': 0xd9,
    'ADDATL': 0xda,
    'ARCON': 0xef,
    'B': 0xf0,
    'CC4EN': 0xc9,
    'CCEN': 0xc1,
    'CCH1': 0xc3,
    'CCH2': 0xc5,
    'CCH3': 0xc7,
    'CCH4': 0xcf,
    'CCL1': 0xc2,
    'CCL2': 0xc4,
    'CCL3': 0xc6,
    'CCL4': 0xce,
    'CLRMSK': 0xa6,
    'CMEN': 0xf6,
    'CMH0': 0xd3,
    'CMH1': 0xd5,
    'CMH2': 0xd7,
    'CMH3': 0xe3,
    'CMH4': 0xe5,
    'CMH5': 0xe7,
    'CMH6': 0xf3,
    'CMH7': 0xf5,
    'CML0': 0xd2,
    'CML1': 0xd4,
    'CML2': 0xd6,
    'CML3': 0xe2,
    'CML4': 0xe4,
    'CML5': 0xe6,
    'CML6': 0xf2,
    'CML7': 0xf4,
    'CMSEL': 0xf7,
    'COMCLRH': 0xa4,
    'COMCLRL': 0xa3,
    'COMSETH': 0xa2,
    'COMSETL': 0xa1,
    'CRCH': 0xcb,
    'CRCL': 0xca,
    'CTCON': 0xe1,
    'CTRELH': 0xdf,
    'CTRELL': 0xde,
    'DPH': 0x83,
    'DPL': 0x82,
    'DPSEL': 0x92,
    'IEN0': 0xa8,
    'IEN1': 0xb8,
    'IEN2': 0x9a,
    'IP0': 0xa9,
    'IP1': 0xb9,
    'IRCON0': 0xc0,
    'IRCON1': 0xd1,
    'MD0': 0xe9,
    'MD1': 0xea,
    'MD2': 0xeb,
    'MD3': 0xec,
    'MD4': 0xed,
    'MD5': 0xee,
    'P0': 0x80,
    'P1': 0x90,
    'P2': 0xa0,
    'P3': 0xb0,
    'P4': 0xe8,
    'P5': 0xf8,
    'P6': 0xfa,
    'P7': 0xdb,
    'P8': 0xdd,
    'PCON': 0x87,
    'PSW': 0xd0,
    'S0BUF': 0x99,
    'S0CON': 0x98,
    'S0RELH': 0xba,
    'S0RELL': 0xaa,
    'S1BUF': 0x9c,
    'S1CON': 0x9b,
    'S1RELH': 0xbb,
    'S1RELL': 0x9d,
    'SETMSK': 0xa5,
    'SP': 0x81,
    'SYSCON': 0xb1,
    'T2CON': 0xc8,
    'TCON': 0x88,
    'TH0': 0x8c,
    'TH1': 0x8d,
    'TH2': 0xcd,
    'TL0': 0x8a,
    'TL1': 0x8b,
    'TL2': 0xcc,
    'TMOD': 0x89,
    'WDTH': 0x85,
    'WDTL': 0x84,
    'WDTREL': 0x86,
    'XPAGE': 0x91,
}

HEADER_BITS = {
    'AC': 0xd6,
    'ADEX': 0xdd,
    'ADM': 0xdb,
    'BD': 0xdf,
    'BSY': 0xdc,
    'CLK': 0xde,
    'CY': 0xd7,
    'EADC': 0xb8,
    'EAL': 0xaf,
    'ES0': 0xac,
    'ET0': 0xa9,
    'ET1': 0xab,
    'ET2': 0xad,
    'EX0': 0xa8,
    'EX1': 0xaa,
    'EX2': 0xb9,
    'EX3': 0xba,
    'EX4': 0xbb,
    'EX5': 0xbc,
    'EX6': 0xbd,
    'EXEN2': 0xbf,
    'EXF2': 0xc7,
    'F0': 0xd5,
    'F1': 0xd1,
    'I2FR': 0xcd,
    'I3FR': 0xce,
    'IADC': 0xc0,
    'IE0': 0x89,
    'IE1': 0x8b,
    'IEX2': 0xc1,
    'IEX3': 0xc2,
    'IEX4': 0xc3,
    'IEX5': 0xc4,
    'IEX6': 0xc5,
    'INT0': 0xb2,
    'INT1': 0xb3,
    'IT0': 0x88,
    'IT1': 0x8a,
    'MX0': 0xd8,
    'MX1': 0xd9,
    'MX2': 0xda,
    'OV': 0xd2,
    'P': 0xd0,
    'RB80': 0x9a,
    'RD': 0xb7,
    'REN0': 0x9c,
    'RI0': 0x98,
    'RS0': 0xd3,
    'RS1': 0xd4,
    'RXD': 0xb0,
    'SM0': 0x9f,
    'SM1': 0x9e,
    'SM20': 0x9d,
    'SWDT': 0xbe,
    'T0': 0xb4,
    'T1': 0xb5,
    'T2CM': 0xca,
    'T2I0': 0xc8,
    'T2I1': 0xc9,
    'T2PS': 0xcf,
    'T2R0': 0xcb,
    'T2R1': 0xcc,
    'TB80': 0x9b,
    'TF0': 0x8d,
    'TF1': 0x8f,
    'TF2': 0xc6,
    'TI0': 0x99,
    'TR0': 0x8c,
    'TR1': 0x8e,
    'TXD': 0xb1,
    'WDT': 0xae,
    'WR': 0xb6,
}

PORT_BITS = {
    'CCM0': 0xf8,
    'CCM1': 0xf9,
    'CCM2': 0xfa,
    'CCM3': 0xfb,
    'CCM4': 0xfc,
    'CCM5': 0xfd,
    'CCM6': 0xfe,
    'CCM7': 0xff,
    'CLKOUT': 0x96,
    'CM0': 0xe8,
    'CM1': 0xe9,
    'CM2': 0xea,
    'CM3': 0xeb,
    'CM4': 0xec,
    'CM5': 0xed,
    'CM6': 0xee,
    'CM7': 0xef,
    'INT2': 0x94,
    'INT3': 0x90,
    'INT4': 0x91,
    'INT5': 0x92,
    'INT6': 0x93,
    'T2': 0x97,
    'T2EX': 0x95,
}


class Test80C517Spec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = ET.parse(SPEC).getroot()
        cls.sfr = {
            s.get("name"): int(s.get("address").split(":")[1], 16)
            for s in root.findall("./default_symbols/symbol")
            if s.get("address", "").startswith("SFR:")
        }
        cls.bits = {
            s.get("name"): int(s.get("address").split(":")[1], 16)
            for s in root.findall("./default_symbols/symbol")
            if s.get("address", "").startswith("BITS:")
        }

    def test_sfr_map_is_exact(self):
        self.assertEqual(self.sfr, SFR)

    def test_header_bits_are_present(self):
        for name, address in HEADER_BITS.items():
            with self.subTest(name=name):
                self.assertEqual(self.bits.get(name), address)

    def test_port_and_compare_bits_are_present(self):
        for name, address in PORT_BITS.items():
            with self.subTest(name=name):
                self.assertEqual(self.bits.get(name), address)

    def test_no_cip51_names_leak(self):
        for name in ("FIFLG", "FIFLG1", "HIFLG", "SCON", "SBUF"):
            with self.subTest(name=name):
                self.assertNotIn(name, self.sfr)
                self.assertNotIn(name, self.bits)

    def test_ldefs_names_the_family(self):
        root = ET.parse(LDEFS).getroot()
        entries = [e for e in root.findall("language") if e.get("id") == "8051:BE:16:80c517"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.get("processorspec"), "80c517.pspec")
        self.assertEqual(entry.get("slafile"), "8051.sla")
        self.assertIsNone(entry.get("manualindexfile"))
        description = entry.findtext("description")
        self.assertIn("80C517A", description)
        self.assertIn("83C517A-5", description)


if __name__ == "__main__":
    unittest.main()
