# Marco v0.5.0 — Preparação do pacote orçamentário

> **Status: validador local de *layouts preliminares*.** Não há conexão SIOP/SIAFI, extração automática, conciliação financeira, cálculo oficial, banco de dados de produção nem homologação por gestor.

## O que foi implementado

- Quatro contratos de entrada independentes: **LOA**, **execução**, **RAP** e **pagamentos**, em `contracts/datasets.json`.
- Gerador de CSV **100% sintético** restrito a `local_data/` (ignorados pelo Git), para exercícios funcionais.
- Conferência conjunta dos quatro CSVs, com validação por esquema/duplicidade/corte e relatório único de **contagens e hashes**, sem linhas, valores financeiros nem importação.
- Falha bloqueia o relatório inteiro; saídas individuais temporárias são descartadas. O relatório final tem `publishable: false`, `validation_state: pendente_homologacao`, `reconciliation_performed: false`.

## 1. Ensaiar com amostras fictícias (sem acesso à rede)

```bash
python -m scripts.generate_synthetic_budget --cutoff 2026-10-19
python -m scripts.prepare_budget_package \
  --loa local_data/sintetico/loa.csv \
  --execucao local_data/sintetico/execucao.csv \
  --rap local_data/sintetico/rap.csv \
  --pagamentos local_data/sintetico/pagamentos.csv \
  --classification interno \
  --cutoff 2026-10-19 \
  --authorization-ref TESTE-SINTETICO
```

As pastas `local_data/` e `data/` são excluídas da versão Git. Não versionar nem enviar o resultado ao GitHub, Vercel ou ao ChatGPT.

## 2. Fluxo proposto para dados reais

1. **Autorização:** obter aprovação formal do gestor de cada base e da TI; registrar a classificação (público, interno, restrito), finalidade, retenção e operador responsável.
2. **Amostra autorizada:** receber os quatro extratos em ambiente institucional aprovado, com dicionários, datas de corte e identificadores de origem; **não inserir informações sensíveis no portal demonstrativo**.
3. **Ajustar contratos:** mapear nomes de campos e tipos do layout de cada fonte antes de qualquer importação. Identificadores e chave de documento de pagamento são apenas hipóteses técnicas atuais.
4. **Conferência:** executar `inspect_dataset.py` e `prepare_budget_package.py` no ambiente aprovado. Relatório não equivale a conciliação e não confirma autorização.
5. **Conciliação a implementar:** homologar chaves entre SIOP/SIAFI por exercício, UO, ação, PO, empenho e tipo de pagamento; definir tratamento de cancelamentos, estornos, RAP processados/não processados e múltiplos documentos.
6. **Homologação:** validar fórmula, recorte, valores e divergências com a unidade responsável. Somente ambiente interno autenticado poderá mostrar dados reais.

## 3. Dicionário de solicitação por contrato

| Base | Campos mínimos propostos | Necessidade de homologação |
|---|---|---|
| LOA / SIOP | identificador_linha, exercicio, uo, acao, plano_orcamentario, fonte, dotacao_atualizada, data_corte | Fonte e detalhamento por crédito/PO; exclusão de linhas agregadas |
| Execução / SIAFI | identificador_linha, exercicio, uo, acao, plano_orcamentario, empenhado, liquidado, pago, data_corte | Natureza contábil e conceito de execução (acumulado ou movimento) |
| RAP / SIAFI | identificador_linha, exercicio_inscricao, uo, acao, rap_inscrito, rap_pago, rap_cancelado, data_corte | RAP processados e não processados; cancelamentos e saldos |
| Pagamentos / SIAFI | identificador_linha, exercicio, uo, acao, tipo_origem, documento_pagamento, valor_pago, data_pagamento, data_corte | Tipos LOA/RAP, identificador do documento e reversões |

**Importante:** não se deve somar o `pago` da execução ao `valor_pago` do arquivo pagamentos: podem representar a mesma operação em granularidades diferentes. Também é indevido somar os valores de RAP à execução LOA sem regra contábil aprovada. Essa verificação exige conciliação com amostra oficial e aceite do gestor.

## 4. Critérios de aceite para uma integração real

- Documento de autorização, responsável e classificação rastreáveis.
- Chaves/campos, competência e periodicidade validados.
- Tabelas dimensionais e fatos sem duplicidade e sem cruzamento por nomes aproximados.
- Reconciliação entre extratos aprovada, com divergências documentadas.
- Controle de versões, auditoria, rollback e retenção em banco corporativo.
- API autenticada por IdP e permissões por unidade; ambiente de homologação e testes da TI.
- Relatórios com fonte, fórmula, data de corte, operador e estado de validação.

**A primeira fase se encerra apenas quando houver fonte real autorizada, conciliação revisada e homologação.** O que esta release entrega é a ferramenta local para iniciar esse trabalho com segurança.
