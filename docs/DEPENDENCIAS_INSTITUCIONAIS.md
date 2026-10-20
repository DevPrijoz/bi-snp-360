# O que precisamos das áreas — roteiro objetivo de habilitação

**Não transmitir documentos restritos, credenciais, números de processos ou bases internas por GitHub, Vercel ou mensagens públicas.** Os itens abaixo devem ser recebidos e aprovados em ambiente corporativo autorizado.

## Prioridade 1 — Orçamento e Finanças

| Insumo | Quem deve fornecer / validar | Para quê | Situação |
|---|---|---|---|
| Unidade responsável por cada fonte e autorização de acesso | Gestor de dados SIOP/SIAFI e coordenação orçamentária | Permitir coleta regular, com classificação, finalidade e retenção | Pendente |
| Layout LOA, execução, RAP e pagamentos | Gestores SIOP/SIAFI (extrações permitidas e dicionário) | Adaptar contratos `contracts/datasets.json` às fontes reais | Pendente |
| Exercícios, UOs, ações, POs, fontes, competências e documentos | Área orçamentária, sob autorização | Criar as chaves de vinculação e a granularidade | Pendente |
| Fórmulas e conciliação de empenhado/liquidado/pago/RAP | Área contábil e gestores de origem | Evitar dupla contagem e documentar estornos/cancelamentos | Pendente |
| Responsável pela homologação e frequência de atualização | Chefia da área gestora | Aprovar versão de dados e datas de corte | Pendente |

## Prioridade 2 — Produtos setoriais

| Insumo | Área proponente | Entrega que viabiliza | Situação |
|---|---|---|---|
| Carteira de empreendimentos e fonte financeira autorizada | DGMP / área de obras | Investimentos e Obras | Pendente |
| Planilha ou cadastro de contratos/outorgas com situação e marcos | DNOP / coordenação competente | Outorgas e Contratos | Pendente |
| Inventário de processos, unidades, fluxos e perfis de acesso ao SEI | Unidade gestora SEI / TI | Processos e Prazos (ambiente interno) | Pendente |
| Fonte pública ANTAQ e método de agregação de movimentação | Área portuária/estatística | Desempenho Setorial | Pendente |

## Prioridade 3 — Plataforma institucional

| Insumo / decisão | Responsável proposto | Situação |
|---|---|---|
| Aprovar arquitetura e ambiente de desenvolvimento/homologação/produção | TI/segurança MPOR | Pendente |
| Definir IdP/OIDC, `issuer`, `audience`, JWKS e mapeamento de permissões, **sem compartilhar segredos** | TI/identidade e governança | Pendente |
| Definir PostgreSQL, migrações, criptografia, backup e testes de restauração | TI/DBA | Pendente |
| Confirmar unidades orgânicas e vínculo atual no SIORG | Gabinete / área de planejamento | Pendente |
| Definir produtores, executores, homologadores e regras de delegação | Chefias e governança | Pendente |
| Aprovar LGPD, política de retenção, exposição pública e avaliações de segurança | Jurídico, encarregado, TI | Pendente |
| Homologar indicadores, semáforos, evidências e relatórios finais | Responsáveis de negócio | Pendente |

## Primeiro aceite possível sem bases reais

A ferramenta de conferência de **quatro contratos orçamentários** pode ser demonstrada com amostras sintéticas, sem aprovação de dados internos. Isso não autoriza operar o ambiente público com informações institucionais. O marco técnico está em [PACOTE_ORCAMENTARIO.md](PACOTE_ORCAMENTARIO.md).
