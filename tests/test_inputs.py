import unittest

from components.inputs import interpretar_numero_ptbr


class TestEntradasPtBr(unittest.TestCase):

    def test_interpreta_milhar_e_centavos(self):
        self.assertEqual(interpretar_numero_ptbr("1.000,00"), 1000)
        self.assertEqual(interpretar_numero_ptbr("1.000.000,00"), 1000000)
        self.assertEqual(interpretar_numero_ptbr("15.354"), 15354)

    def test_interpreta_moeda_e_formato_decimal_alternativo(self):
        self.assertEqual(interpretar_numero_ptbr("R$ 15.354,89"), 15354.89)
        self.assertEqual(interpretar_numero_ptbr("1000.00"), 1000)


if __name__ == "__main__":
    unittest.main()
