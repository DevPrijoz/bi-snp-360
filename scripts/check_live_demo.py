"""Verifica se o portal executivo NÃO entrega dados a uma sessão anônima.

A aplicação está protegida por Vercel Authentication (All Deployments).
Este teste usa uma sessão sem cookies e sem segredos de bypass.
"""
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import HTTPError

BASE = "https://bi-snp-360.vercel.app"
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, url):
        return None

client = build_opener(NoRedirect())

def assert_protected(path):
    req = Request(BASE + path, headers={"User-Agent": "BI-SNP-360-Privacy-Check/1.0"})
    try:
        with client.open(req, timeout=25) as response:
            status = response.status
            body = response.read(160000).lower()
            location = response.headers.get("Location", "")
    except HTTPError as exc:
        status = exc.code
        body = exc.read(30000).lower()
        location = exc.headers.get("Location", "")
    if b'id="dat"' in body or b'id="fontes-originais"' in body:
        raise AssertionError(f"Dados do BI foram expostos a acesso anonimo: {path}")
    if status in (401, 403):
        print(f"OK: {path} protegido com HTTP {status}")
        return
    if 300 <= status < 400 and "vercel" in location.lower():
        print(f"OK: {path} redirecionado para autenticacao")
        return
    if status == 200 and b"vercel" in body and (
        b"authentication" in body or b"sign in" in body or b"login" in body or b"entrar" in body
    ):
        print(f"OK: {path} mostra login, nao dados")
        return
    raise AssertionError(f"Acesso anonimo inesperado: {path}, HTTP {status}")

if __name__ == "__main__":
    assert_protected("/")
    assert_protected("/controle_fontes.json")
