# Modelo de dados e contrato de ingestão

## Entidades principais

- `Record`: registro canônico de atividade, demanda ou processo. Identificadores `id` (UUID interno), `external_key` (chave estável fornecida pela fonte), `source_id`, `source_record_id`, `module`, `unit_code`, `information_unit`, `classification`.
- Temporalidade: `data_cutoff`, `due_date`, `created_at`, `updated_at`, `validated_at`.
- Responsabilidade: `execution_responsible`, `decision_authority`, `created_by`, `validated_by`, `closure_approved_by`.
- Execução: `title`, `object_goal`, `status`, `risk`, `next_action`, `decision_required`.
- Controle: `validation_state`, `published`, `closure_state`, `closure_action`, `closure_evidence_url`.
- `AuditEvent`: `id`, `record_id`, `actor`, `action`, `details`, `created_at` (não armazena documento/bytes, apenas metadados necessários).

## Contratos e qualidade

- Datas ISO `YYYY-MM-DD`; valores monetários numéricos em BRL e com unidade e regra de arredondamento homologadas (fatos orçamentários ainda pendentes).
- Não completar campos ausentes com zeros que sejam interpretáveis como resultado oficial. Usar **não informado / não validado**.
- Todos os dados de origem devem carregar proveniência e data de corte, com hash da extração (pipeline futura).
- Deduplicação por `external_key`, com chave normalizada e controle de versão. API rejeita carga duplicada: não sobrescreve dados silenciosamente.
- Indicadores exigem `fórmula`, `periodicidade`, `source_id`, `responsável técnico`, `autoridade homologadora` e `grau de confiabilidade`.
- Evidências são links para sistemas autorizados. A API não disponibiliza documentos protegidos nem inclui evidências nas respostas públicas.
- Publicação apenas de registros `classification=publico` e `validation_state=homologado` e `published=true`.

## CSV de piloto

Arquivo de exemplo: `scripts/exemplo_importacao.csv`. Colunas separadas por `;`, UTF-8, uma linha por registro. Colunas principais: `external_key`, `module`, `title`, `object_goal`, `unit_code`, `information_unit`, `execution_responsible`, `status`, `risk`, `due_date`, `next_action`, `source_id`, `source_record_id`, `data_cutoff`, `classification`.

**Fluxo autorizado:** solicitar `POST /api/v1/import/csv` com `dry_run=true`, revisar rejeições, submeter `dry_run=false` por conta autorizada, homologar registros por conta distinta, publicar somente os registros expressamente públicos. Não conectar base real sem acordo institucional.

## Futuras tabelas normalizadas (a modelar com cada unidade)

`unidades`, `fontes`, `coletas`, `cadastro_mestre_projetos`, `processos`, `instrumentos`, `obras`, `medidas_orcamentarias_loa`, `medidas_orcamentarias_rap`, `pagamentos`, `riscos`, `recomendacoes`, `notas_validacao`, `versoes_dicionario`, `permissoes`, `publicacoes`, `evidencias` (metadados), `retencao_politicas`.

A expansão depende de amostras oficiais e da granularidade de cada sistema; **não inferir relacionamentos com base apenas em nomes ou semelhança geográfica**.

## Contratos de datasets v0.2.0

`contracts/datasets.json` contém modelos preliminares para `loa`, `execucao`, `rap`, `processos`, `obras`, `movimentacao`. A validação local não significa ingestão no banco de produção nem homologação de fonte. Manifestos gerados em `local_data/` são ignorados pelo Git e guardam SHA-256, referência de autorização, data de corte e resultado pendente. Consulte `INGESTAO_BASES.md`.
