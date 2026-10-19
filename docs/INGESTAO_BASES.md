# Ingestão incremental de bases — procedimento técnico v0.2.0

**Status:** ferramenta local de validação inicial concluída, sem integração ou homologação de nenhuma base real. Nenhum CSV institucional deve ser versionado ou enviado ao GitHub.

## 1. Pré-requisitos para cada fonte

1. Registrar responsável pela origem, gestor da informação, autorização de acesso/uso e finalidade do tratamento.
2. Confirmar classificação (**público / interno / restrito**), base legal e políticas de retenção.
3. Receber planilha ou exportação sanitizada, **somente em ambiente institucional aprovado**.
4. Confirmar unidade de medida, corte temporal, dicionário de campos e chave de identificação. Não associar dotações, obras, outorgas e processos por semelhança de nomes.
5. Confrontar o contrato `contracts/datasets.json` com o layout real e aprovar as alterações antes de ingestão. São modelos preliminares, não extratores oficiais.
6. Validar/conciliar e fazer aceite funcional pela área gestora. Publicação externa exige avaliação separada.

## 2. Contratos de entrada preliminares

| ID | Fonte prevista | Granularidade inicial | Situação |
|---|---|---|---|
| `loa` | SIOP | linha de dotação / ação / plano / fonte / exercício | Layout a homologar |
| `execucao` | SIAFI | linha de execução financeiro-orçamentária | Layout a homologar |
| `rap` | SIAFI | linha RAP por exercício de inscrição | Layout a homologar |
| `processos` | SEI | processo com unidade e prazo | Autorização imprescindível |
| `obras` | Obrasgov | empreendimento / avanço | Relacionamentos a definir |
| `movimentacao` | ANTAQ | instalação / competência | Dados públicos a verificar |

O arquivo de contrato não substitui documentação técnica de cada órgão. Valores decimais são aceitos apenas no padrão técnico com `.` como separador e sem milhar; **não** são convertidos por heurística. Datas devem seguir `AAAA-MM-DD`, inclusive datas de corte.

## 3. Ferramenta de conferência isolada

Grave a exportação autorizada fora do repositório ou em `local_data/` (diretório ignorado pelo Git) e execute no ambiente aprovado:

```bash
python scripts/inspect_dataset.py local_data/amostra_autorizada.csv \
  --contract loa \
  --classification interno \
  --cutoff 2026-10-19 \
  --authorization-ref DOCUMENTO-DE-AUTORIZACAO-VALIDO
```

A ferramenta valida o cabeçalho e o contrato, campos requeridos, chave composta, datas e valores, e calcula um **SHA-256** do arquivo. Salva apenas um manifesto em `local_data/manifests/`, com `publishable=false` e `validation_state=pendente_homologacao`. Nenhum dado é enviado por rede, convertido em snapshot público ou escrito em `web/`. Não se presume que a autorização apresentada seja válida; isso cabe ao gestor.

**Limitações atuais:** não identifica conteúdo sensível automaticamente, não é um conector SIOP/SIAFI/SEI, não faz conciliação interfontes, não calcula indicadores oficiais, não implementa a etapa de homologação de um dataset e não salva dados em PostgreSQL.

## 4. Política de qualidade e rollback

- Qualquer erro invalida toda a conferência, sem publicação parcial.
- O último conjunto homologado permanece inalterado até a aprovação de uma nova versão.
- Erros de unidade, somatório, relacionamento ou identificação não são corrigidos por arredondamentos presumidos.
- Quando existirem datasets reais, registrar identificadores de importação, auditoria, versão do contrato, fonte, data de corte, responsáveis, alterações e rollback transacional.
- O hash **não** atesta autenticidade do órgão de origem: ele permite apenas conferir se os mesmos bytes foram usados.

## 5. Próximas entregas com as áreas

Receber recortes de LOA/RAP/Pagamentos (incluindo os extratos do trabalho orçamentário já existentes, somente se autorizados), catálogo de investimentos, outorgas e processos prioritários. Homologar chaves entre SIOP/SIAFI/SEI e unidade responsável, antes de qualquer painel agregado.
