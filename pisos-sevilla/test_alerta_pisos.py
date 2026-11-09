import copy
import unittest

import alerta_pisos as ap

CONFIG = ap.cargar_config()


def anuncio(**kw):
    base = dict(id="1", fuente="t", url="u", precio=850, dormitorios=2,
                barrio="Nervión", lat=37.3847, lon=-5.9720)
    base.update(kw)
    return ap.Anuncio(**base)


class TestFiltros(unittest.TestCase):
    def test_cumple_basico(self):
        a = anuncio()
        self.assertTrue(ap.cumple(a, CONFIG))
        self.assertEqual(a.zona, "Nervión")

    def test_precio_limite(self):
        self.assertTrue(ap.cumple(anuncio(precio=900), CONFIG))
        self.assertFalse(ap.cumple(anuncio(precio=901), CONFIG))

    def test_dormitorios(self):
        self.assertFalse(ap.cumple(anuncio(dormitorios=1), CONFIG))
        self.assertFalse(ap.cumple(anuncio(dormitorios=3), CONFIG))

    def test_zona_por_nombre_sin_tildes(self):
        a = anuncio(barrio="TIRO DE LINEA", lat=None, lon=None)
        self.assertTrue(ap.cumple(a, CONFIG))
        self.assertEqual(a.zona, "Tiro de Línea")

    def test_zona_por_coordenadas(self):
        a = anuncio(barrio="", lat=37.3687, lon=-5.9843)  # junto a Bami
        self.assertTrue(ap.cumple(a, CONFIG))
        self.assertEqual(a.zona, "Bami")

    def test_fuera_de_zona(self):
        a = anuncio(barrio="Triana", lat=37.3830, lon=-6.0050)
        self.assertFalse(ap.cumple(a, CONFIG))

    def test_excluir_bajos(self):
        cfg = copy.deepcopy(CONFIG)
        cfg["criterios"]["excluir_bajos"] = True
        self.assertFalse(ap.cumple(anuncio(planta="bj"), cfg))
        self.assertTrue(ap.cumple(anuncio(planta="3"), cfg))


class TestEstado(unittest.TestCase):
    def test_no_repite_y_avisa_rebaja(self):
        vistos = {}
        self.assertEqual(len(ap.ejecutar(CONFIG, [anuncio()], vistos)), 1)
        self.assertEqual(len(ap.ejecutar(CONFIG, [anuncio()], vistos)), 0)
        rebajado = ap.ejecutar(CONFIG, [anuncio(precio=800)], vistos)
        self.assertEqual(len(rebajado), 1)
        self.assertIn("rebajado", rebajado[0].zona)

    def test_demo(self):
        nuevos = ap.ejecutar(CONFIG, ap.fuente_demo(CONFIG), {})
        self.assertEqual(sorted(a.id for a in nuevos), ["1001", "1005", "1006", "1007"])


if __name__ == "__main__":
    unittest.main()
