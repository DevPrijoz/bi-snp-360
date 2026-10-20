# Implantação v0.5.0 — demonstração versus operação institucional

- **Demonstração web:** https://bi-snp-360.vercel.app/ (Vercel; publicação automática da pasta `web/` a partir de `DevPrijoz/bi-snp-360`, branch `main`).
- **CI:** `.github/workflows/ci.yml`; monitor HTTPS `.github/workflows/live-smoke.yml`.
- **Segurança:** JSON sintético, nenhum registro real, nenhuma fonte oficial conectada; API piloto em `backend/` não é implantada na Vercel.
- **Rede MPOR:** o usuário confirmou que o site abre com dados móveis, mas a rede do Ministério apresenta timeout. A causa precisa ser confirmada com a equipe de TI; **não** contornar políticas corporativas. Registro: [issue #5](https://github.com/DevPrijoz/bi-snp-360/issues/5).
- **GitHub Pages:** tentativas falharam por privilégios da integração, mas não é necessário para a demonstração hospedada na Vercel.

## O que a hospedagem comprova

A entrega web depende dos testes de CI e de requisições HTTP externas. **Vercel `READY` não equivale a homologação funcional institucional.** O validador remoto testa HTML, CSS/JS e `health.json`/JSON sintético.

## O que NÃO está implantado

- API interna FastAPI e banco PostgreSQL de produção.
- SSO/IdP real, permissões corporativas e auditoria operacional.
- Integrações oficiais SIOP/SIAFI/SEI/Obrasgov/ANTAQ.
- Extração, apuração e publicação de dados institucionais.

## Próximo marco

Contratos LOA, execução, RAP e pagamentos + conferência conjunta local sem dados reais: [PACOTE_ORCAMENTARIO.md](PACOTE_ORCAMENTARIO.md). Uma integração real depende do órgão gestor da fonte, autorização, dicionário, infraestrutura segura e homologação.
