import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


ESTADO_INICIAL = (1, 2, 3, 4, 5, 6, 7, 0, 8)
ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class TestFuncoesBase(unittest.TestCase):
    def test_manhattan_retorna_um_para_um_movimento(self):
        self.assertEqual(main.manhattan(ESTADO_INICIAL, ESTADO_OBJETIVO), 1)

    def test_obter_sucessores_do_vazio_no_canto_inferior(self):
        sucessores = main.obter_sucessores(ESTADO_INICIAL)

        self.assertEqual(len(sucessores), 3)
        estados = {estado for _, estado in sucessores}
        self.assertIn((1, 2, 3, 4, 5, 6, 7, 8, 0), estados)
        self.assertIn((1, 2, 3, 4, 0, 6, 7, 5, 8), estados)
        self.assertIn((1, 2, 3, 4, 5, 6, 0, 7, 8), estados)

    def test_problema_tem_solucao_detecta_paridade(self):
        estado_sem_solucao = (1, 2, 3, 4, 5, 6, 8, 7, 0)

        self.assertTrue(main.problema_tem_solucao(ESTADO_INICIAL, ESTADO_OBJETIVO))
        self.assertFalse(main.problema_tem_solucao(estado_sem_solucao, ESTADO_OBJETIVO))

    def test_reconstruir_caminho_retorna_sequencia_completa(self):
        no_final, _ = main.busca_largura(ESTADO_INICIAL, ESTADO_OBJETIVO)
        caminho = main.reconstruir_caminho(no_final)

        self.assertEqual([no.estado for no in caminho], [ESTADO_INICIAL, ESTADO_OBJETIVO])
        self.assertEqual([no.acao for no in caminho], [None, "Direita"])


class TestBuscas(unittest.TestCase):
    def assert_solucao_de_um_passo(self, funcao_busca):
        solucao, expandidos = funcao_busca(ESTADO_INICIAL, ESTADO_OBJETIVO)

        self.assertIsNotNone(solucao)
        self.assertEqual(solucao.estado, ESTADO_OBJETIVO)
        self.assertEqual(solucao.custo, 1)
        self.assertEqual(solucao.profundidade, 1)
        self.assertGreaterEqual(expandidos, 1)

        caminho = main.reconstruir_caminho(solucao)
        self.assertEqual([no.estado for no in caminho], [ESTADO_INICIAL, ESTADO_OBJETIVO])

    def test_busca_largura(self):
        self.assert_solucao_de_um_passo(main.busca_largura)

    def test_busca_profundidade(self):
        solucao, expandidos = main.busca_profundidade(ESTADO_INICIAL, ESTADO_OBJETIVO)

        self.assertIsNotNone(solucao)
        self.assertEqual(solucao.estado, ESTADO_OBJETIVO)
        self.assertLessEqual(solucao.profundidade, 30)
        self.assertGreaterEqual(expandidos, 1)

        caminho = main.reconstruir_caminho(solucao)
        self.assertEqual(caminho[0].estado, ESTADO_INICIAL)
        self.assertEqual(caminho[-1].estado, ESTADO_OBJETIVO)

    def test_busca_custo_uniforme(self):
        self.assert_solucao_de_um_passo(main.busca_custo_uniforme)

    def test_busca_gulosa(self):
        self.assert_solucao_de_um_passo(main.busca_gulosa)

    def test_busca_a_estrela(self):
        self.assert_solucao_de_um_passo(main.busca_a_estrela)

    def test_busca_ida_estrela(self):
        self.assert_solucao_de_um_passo(main.busca_ida_estrela)


class TestEntradaInterativa(unittest.TestCase):
    def test_ler_estado_rejeita_entrada_invalida_e_depois_aceita(self):
        entradas = [
            "1 2 3",
            "1 2 3 4 5 6 7 8 8",
            "1 2 3 4 5 6 7 8 0",
        ]

        with patch("builtins.input", side_effect=entradas), redirect_stdout(io.StringIO()):
            estado = main.ler_estado("estado inicial")

        self.assertEqual(estado, ESTADO_OBJETIVO)


if __name__ == "__main__":
    unittest.main()