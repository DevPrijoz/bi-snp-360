# BI SNP 360° — Marco técnico v0.6.0

**Data:** 23/10/2026. **Escopo:** governança de recebimento e procedimentos operacionais sem credenciais ou dados oficiais.

## Implementado

- Catálogo de 7 trilhas priorizadas em `contracts/governance_workstreams.json`.
- Gerador de 7 minutas de solicitação e matriz CSV, sem dados institucionais.
- Validador de metadados de recebimento com reprovação de campos desconhecidos, classificações inválidas, datas inconsistentes e possíveis segredos.
- O validador nunca altera estado institucional: `automatic_approval=false`, `publishable=false`.
- Interface de demonstração estendida com **7 procedimentos de articulação**, responsáveis propostos e download do plano CSV.
- Testes regressivos, relatório de implantação e guia de solicitações.

## Não implementado ou autorizado

- Contas e acessos SEI, SIOP, SIAFI ou outros sistemas; não se presumem as permissões de terceiros.
- Transferência ou guarda de arquivos oficiais fora de ambiente autorizado.
- Regras definitivas de reconciliação; conector, banco PostgreSQL, SSO/IdP real, homologação e operação do sistema institucional.
- Atribuição real de responsabilidades ou publicação de indicadores reais.

## Verificação de aceitação

- `python scripts/release_guard.py`
- `python scripts/validate_assets.py`
- `node --check web/assets/app.js`
- `pytest -q`
- Fluxo CI do GitHub + verificação de implantação HTTPS da demo no Vercel após commit.

A versão `0.6.0` é **piloto técnico e demonstrativo**, não entrega institucional homologada.
