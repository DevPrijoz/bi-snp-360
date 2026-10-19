# BI SNP 360° — Governança e Gestão

**Secretaria Nacional de Portos (SNP) | Ministério de Portos e Aeroportos (MPOR)**

> **Status: protótipo demonstrativo, não homologado para operação institucional.** Não contém dados oficiais e não deve fundamentar decisões administrativas.

## Abrir a demonstração

A primeira interface interativa está em [index.html](./index.html). Faça download do arquivo e abra no navegador, sem depender de uma API.

O repositório é **privado**. Não há publicação pública do GitHub Pages configurada nem autorização de divulgação institucional.

## Escopo executivo

O conceito segue quatro perspectivas: **direção, gestão, coordenação e controle**, conforme a proposta executiva do BI SNP 360° de 15/10/2026.

Os 12 módulos previstos são: Direção Estratégica, Orçamento e Finanças, Investimentos e Obras, Outorgas e Contratos, Planejamento Portuário, Governança Portuária, Coordenação Institucional, Processos e Prazos, Riscos e Controle, Desempenho Setorial, Dados e Inovação e Relatórios Executivos.

## Estado da publicação

| Item | Situação |
| --- | --- |
| Repositório privado | Criado |
| Painel demonstrativo autônomo | Publicado em `index.html` |
| Código completo da API, contratos e testes | **Ainda não importado para este repositório** |
| Integrações com SEI, SIOP, SIAFI ou ANTAQ | Não realizadas |
| Dados oficiais / homologação | Não realizados |
| Portal público de demonstração | Não habilitado |
| Implantação institucional | Pendente de TI, governança e responsáveis de dados |

O pacote técnico local v0.2.0 contém uma API piloto, contratos preliminares, verificações e **19 testes aprovados localmente**. A presença da demonstração neste repositório **não equivale** à publicação integral desse pacote.

## Diretrizes de segurança

- Não versionar arquivos internos, planilhas sensíveis, documentos restritos, dados pessoais ou credenciais.
- O uso interno requer autenticação e autorização verificadas **no servidor**, além de trilhas de auditoria e definição institucional de perfis.
- Indicadores só poderão aparecer como consolidados após identificação da fonte, data de corte, metodologia, responsável e homologação.

## Referências

- Proposta executiva **BI SNP 360° — Governança e Gestão**, 15/10/2026.
- [BI Hidrovias da SNHN (referência visual)](https://hzhcdyvz4w-tech.github.io/bi-hidrovias/).
- [Decreto nº 11.354/2023](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/d11354.htm).

## Próximo marco

Importar para o GitHub os diretórios `web/`, `backend/`, `contracts/`, `scripts/`, `tests/`, `docs/` e os fluxos de CI, preservando o trabalho preparado na versão v0.2.0; executar os testes em CI; e somente depois avaliar demonstração pública e integrações autorizadas.
