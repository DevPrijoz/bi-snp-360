# BI SNP 360° — Procedimentos de implantação e solicitação das fontes

> **Modelo de trabalho para instrução no SEI/MPOR.** Não é solicitação protocolada, autorização concedida nem documento oficial expedido. Versão v0.6.0, 23/10/2026.

## Fluxo prático com responsáveis

1. **Gabinete/coordenação patrocinadora:** apresentar objetivo, limites e classificação pretendida do BI SNP 360°; designar gestor do projeto, ponto focal em cada área e autoridade que homologará dados. Registrar a demanda e o escopo no procedimento interno adequado.
2. **Área Orçamentária:** abrir demanda formal para amostras *sanitizadas* de SIOP/LOA, execução, RAP e pagamentos e solicitar os quatro dicionários. Informar exercício, UO, ação, PO, fonte, granularidade, origem, data de corte e método de exportação. Classificar cada conjunto antes de disponibilizar. O responsável pela autorização é o proprietário da informação, não o desenvolvedor do BI.
3. **Orçamento + Contabilidade:** homologar fórmulas e conciliação: dotação, empenhado, liquidado, pago, RAP processado/não processado, estornos/cancelamentos e pagos LOA/RAP. **Não** somar pagamentos oriundos de fato já contado em execução. Proibir vínculos por nome semelhante sem chave canônica validada.
4. **Gabinete e chefias:** confirmar unidades vigentes pelo SIORG e atos internos, identificar produtor, gestor, responsável por qualidade, homologador e aprovador de divulgação externa. Elaborar matriz RACI e substitutos.
5. **TI/MPOR e segurança:** aprovar hospedagem e domínios, dev/homologação/produção, IdP/SSO OIDC, RBAC, banco PostgreSQL, TLS, logs, criptografia, segredo em cofre, backup, monitoramento, gestão de incidentes, privacidade e retenção. O site estático Vercel não é ambiente autorizado para dados internos.
6. **DGMP e DNOP:** solicitar separadamente catálogo de investimentos/obras e outorgas/contratos com IDs estáveis, marcos, obrigações, situação, prazo e classificação; homologar metodologia por área.
7. **SEI/MPOR e ANTAQ:** só tratar processos SEI mediante permissão específica e filtros por unidade. Para ANTAQ, partir do catálogo **público** e validar granularidade e metodologia antes de refletir dados na apresentação.

## Entregáveis indispensáveis por fonte

| Entregável | Para quê | Onde guardar |
|---|---|---|
| Autorização formal com finalidade e classificação | Define legitimidade, escopo e responsáveis | SEI/ambiente institucional |
| Dicionário de dados (colunas, tipos, chave e exemplos sintéticos) | Contrato de entrada | Ambiente interno; versão sanitizada pode ser referenciada no Git |
| Arquivo de amostra sanitizada e data de corte | Testes de qualidade sem exposição indevida | Staging institucional aprovado |
| Fórmula, cortes, filtros, limites e responsáveis | Validação de indicador | Catálogo de indicadores aprovado |
| Atas/pareceres de conciliação e homologação | Evidência de aceite | Sistema institucional de registros |
| Decisão de infraestrutura e tratamento | Segurança, continuidade e auditoria | TI/MPOR |

**Não enviar arquivos reais por este chat, à Vercel, ao GitHub ou à demonstração pública.** Dê preferência a exemplos inteiramente sintéticos quando for necessário discutir layouts aqui.

## Como executar o que já está preparado

A pasta `contracts/governance_workstreams.json` contém **sete solicitações** (P01–P07), com prioridades, responsáveis propostos, evidências e critérios de aceite. Gere um kit editável de arquivos Markdown e CSV de acompanhamento, **localmente**:

```bash
python -m scripts.governance_kit kit --output-dir local_data/governanca
```

Cada solicitação gerada é apenas um **rascunho**, sujeito à adaptação e revisão por autoridade competente. O script não dispara e-mails nem cria processos SEI. Os resultados no repositório ficam em `local_data/`, que está no `.gitignore`.

Caso um gestor já tenha compartilhado **somente referências não sensíveis** de recebimento, preencha uma cópia local de `contracts/exemplo_handover_ficticio.json` e execute:

```bash
python -m scripts.governance_kit conferir local_data/metadados_recebimento.json
```

O relatório informa apenas pendências para **revisão humana**. Mesmo quando todas as referências são preenchidas, `automatic_approval=false` e `publishable=false`. Uma marcação declaratória de aprovação não substitui assinatura, ato, trilha de auditoria ou verificação pelo gestor.

## Caminhos oficiais de consulta (não significam integração)

- **SIOP / dados abertos:** [documentação pública de acesso orçamentário](https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos). Aderência a SNP e período precisa ser conferida.
- **SIAFI / Tesouro Gerencial:** [orientações de habilitação](https://www.gov.br/tesouronacional/pt-br/siafi/como-acessar/ambientes-e-instrucoes-de-acesso) e [opções de extração](https://www.gov.br/tesouronacional/pt-br/siafi/atendimento/perguntas-frequentes). Perfis e dados internos requerem autorização.
- **Obrasgov:** [portal da API de dados abertos](https://api-publica.obrasgov.gestao.gov.br/). O portal novo substitui gradualmente o endpoint legado; validar documentação vigente antes de criar conector.
- **ANTAQ:** [catálogo de dados abertos](https://www.gov.br/antaq/pt-br/acesso-a-informacao/dados-abertos). Validar unidade, competência, metodologia e fonte com a área técnica.
- **Transferegov:** [comunicado oficial sobre nova API](https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-no-23-2026-do-portal-do-transferegov.br); ainda não há integração no projeto.

## O que caracteriza aceite técnico ou institucional

**Conferência técnica preliminar:** recebimento de amostras autorizadas, schema, chaves, cutoffs, duplicidades, contagens, hashes e divergências documentadas em staging isolado.

**Homologação de dados:** memória de cálculo e conciliações conferidas, gestor designado, trilha/versão/aceite formal. Sem isso, não chamar indicador de oficial.

**Homologação institucional:** autenticação SSO, controle por unidade, segurança/privacidade, backups, testes de carga, observabilidade, operação, SLA e aprovação de TI/gestores.

**Publicação:** somente após todas as etapas necessárias e classificação; nunca atualizar o painel público por simples cópia de arquivo interno.

## Próximas tarefas técnicas quando houver fontes

1. Criar adaptadores de ingestão versionados por fonte, usando APIs/arquivos autorizados.
2. Implementar staging PostgreSQL e migrações; dados de origem imutáveis e histórico de lotes.
3. Implementar conciliação auditável LOA × execução × RAP × pagamentos **após aprovação das chaves e fórmulas**.
4. Conectar UI institucional autenticada à API e isolar acesso por unidade.
5. Ampliar para investimentos, outorgas e processos, com revisão de qualidade.
