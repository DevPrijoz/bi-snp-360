# Relatório técnico de qualidade — release 0.2.0

**Data:** 2026-10-19. **Escopo:** código do protótipo e API piloto, sem ambientes institucionais integrados.

## Testes executados

| Verificação | Resultado | Limite |
|---|---|---|
| `pytest -q` | 19 testes aprovados | Não é teste de integração institucional |
| `python scripts/validate_assets.py` | 12 registros fictícios / 10 unidades / 10 fontes propostas | Não atesta fontes oficiais |
| `node --check web/assets/app.js` | Sem erro de sintaxe JavaScript | Não substitui teste de navegadores móveis |
| `python scripts/release_guard.py` | Arquivos rastreados sem achados bloqueadores | Não substitui DLP, classificação nem inspeção humana |
| Navegação via Chromium em documento embutido | Inicialização, módulo orçamento, geração de relatório e download CSV passaram; 0 erros JavaScript | Ambiente de teste isolado, sem hospedagem remota |

## Evidências visuais

- `docs/preview/painel-visao-geral.png` — versão demonstrativa da tela inicial.
- `docs/preview/painel-orcamento.png` — orçamento, com indicadores **não homologados** claramente sinalizados.

## Restrições para a assinatura do aceite

Não há comprovação de disponibilidade, performance, segurança externa, backups, disaster recovery, autenticação de IdP real, testes de autorização institucionais, integração real, homologação de regras contábeis nem aprovação das áreas. Portanto, estes testes qualificam a **entrega do protótipo** e não o uso como fonte gerencial oficial.

## Publicação e rastreabilidade

A conta GitHub de destino está definida: `DevPrijoz`; o repositório separado `bi-snp-360` ainda depende de criação via interface GitHub porque a conexão disponível não possui operação de criação de repositórios. Não misturar este release aos repositórios de projetos anteriores.
