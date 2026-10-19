"""Verificacoes basicas que impedem publicar dados internos inadvertidamente."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class TestPublicDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'web/data/demo_public.json').read_text(encoding='utf-8'))
    def test_identificacao_de_ambiente(self):
        self.assertIs(self.data['metadata']['synthetic'], True)
        self.assertEqual(self.data['metadata']['environment'], 'DEMONSTRACAO')
    def test_registros_nao_homologados(self):
        self.assertTrue(self.data['records'])
        for row in self.data['records']:
            self.assertEqual(row['validation'], 'pendente')
            self.assertFalse(row.get('evidence_url'))
            self.assertTrue(row['id'].startswith('DEMO-'))
    def test_identificadores_unicos(self):
        ids = [r['id'] for r in self.data['records']]
        self.assertEqual(len(ids), len(set(ids)))
    def test_sem_referencias_a_dados_internos(self):
        for p in ROOT.glob('web/**/*'):
            if p.is_file():
                self.assertNotIn(p.suffix.lower(), {'.xlsx','.xls','.sqlite','.db','.pem','.key','.p12'})
    def test_12_modulos(self):
        js = (ROOT / 'web/assets/app.js').read_text(encoding='utf-8')
        self.assertEqual(js.count("group:'"), 12)
    def test_html_responsivo(self):
        html = (ROOT / 'web/index.html').read_text(encoding='utf-8')
        css = (ROOT / 'web/assets/styles.css').read_text(encoding='utf-8')
        self.assertIn('name="viewport"', html)
        self.assertIn('@media', css)
    def test_sem_credenciais_web(self):
        text = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (ROOT / 'web').rglob('*') if p.is_file())
        self.assertNotIn('-----BEGIN ' + 'PRIVATE KEY-----', text)
        self.assertNotIn('ghp_', text)
if __name__ == '__main__': unittest.main()
