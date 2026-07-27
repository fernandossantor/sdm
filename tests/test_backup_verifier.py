import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.verificar_backup import ARQUIVOS_OBRIGATORIOS, verificar


class TestBackupVerifier(unittest.TestCase):
    @staticmethod
    def _criar_conjunto(raiz):
        linhas = []
        for nome in ARQUIVOS_OBRIGATORIOS:
            conteudo = f"conteúdo de {nome}\n".encode()
            (raiz / nome).write_bytes(conteudo)
            linhas.append(f"{hashlib.sha256(conteudo).hexdigest()}  {nome}")
        (raiz / "SHA256SUMS").write_text(
            "\n".join(linhas) + "\n",
            encoding="utf-8",
        )

    def test_aceita_conjunto_completo_e_integro(self):
        with tempfile.TemporaryDirectory() as diretorio:
            raiz = Path(diretorio)
            self._criar_conjunto(raiz)

            resultado = verificar(raiz)

        self.assertTrue(resultado["valido"])
        self.assertEqual(len(resultado["arquivos"]), 4)

    def test_rejeita_checksum_divergente(self):
        with tempfile.TemporaryDirectory() as diretorio:
            raiz = Path(diretorio)
            self._criar_conjunto(raiz)
            (raiz / "data.sql").write_text("alterado", encoding="utf-8")

            resultado = verificar(raiz)

        self.assertFalse(resultado["valido"])
        self.assertIn("Checksum divergente: data.sql.", resultado["erros"])

    def test_rejeita_arquivo_ausente(self):
        with tempfile.TemporaryDirectory() as diretorio:
            raiz = Path(diretorio)
            self._criar_conjunto(raiz)
            (raiz / "roles.sql").unlink()

            resultado = verificar(raiz)

        self.assertFalse(resultado["valido"])
        self.assertIn("roles.sql ausente.", resultado["erros"])


if __name__ == "__main__":
    unittest.main()
