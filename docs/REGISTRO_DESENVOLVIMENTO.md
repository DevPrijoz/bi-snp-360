# Registro de desenvolvimento e decisões

**2026-10-19 | v0.1.0 | protótipo local**

## Entradas documentais

- PDF recebido: `SNP BI_SNP_360_Proposta_Executiva_Governanca_Gestao_2026.pdf`, 11 páginas, proposta de 15/10/2026.
- Base de referência: repositório público `hzhcdyvz4w-tech/bi-hidrovias`, README e `index.html` (consultados apenas para padrões visuais e organização).
- Destino indicado para todos os projetos SNP 360: conta GitHub `DevPrijoz`. Nome de novo repositório sugerido: `bi-snp-360`.

## Implementações

1. Interface estática responsiva de comando executivo, com navegação por 12 módulos e busca/filtros.
2. 19 fichas preliminares no catálogo de indicadores, com método, unidade de medida, fonte e frequência proposta.
3. 12 registros de exemplo sintéticos, 10 unidades de trabalho e 10 fontes previstas; ressalva explícita em toda visualização.
4. Semáforo visual com 4 estados, detalhe de demanda, exportação CSV, importação local transitória e relatório para impressão.
5. API de piloto com modelo persistente, trilha, validação por outra pessoa, publicação intencional e encerramento mediante providência e evidência.
6. Testes automatizados cobrindo fronteira pública, RBAC por unidade, segregação, importação, auditoria e fechamento.
7. Workflows de CI e deploy público de acionamento manual, sem incorporação de dados institucionais.

## Limitações e riscos declarados

- Repositório remoto novo ainda NÃO criado ou publicado (conexão GitHub atual não disponibiliza `create_repository`).
- Páginas demonstrativas **não utilizam nem representam bases reais**.
- Backend não configurado para IdP corporativo, produção nem dados internos.
- Vínculo atual das CGs não foi homologado, e não foi concedido acesso a APIs oficiais.
- Indicadores orçamentários não calculados até entrega de dados e regras oficiais.
- Controles do piloto não substituem avaliação de segurança, integração do frontend nem homologação por TI.

## Protocolos de continuidade

Cada nova base deve entrar via feature branch com descrição de origem, data de corte, instrumento de autorização, contrato de campos, critérios de qualidade, validação por ponto focal e cenário de rollback. Ao aprovar, atualizar `MODELO_DADOS.md`, `MODULOS.md`, testes, `ROADMAP.md` e este registro.

## 2026-10-19 | v0.2.0 | endurecimento e contratos de entrada

- Criados contratos canônicos **preliminares**, sem fontes oficiais conectadas.
- Ferramenta de conferência inicial de CSV em ambiente local, impedindo duplicação e dados fora do contrato e gerando manifesto técnico não publicável com SHA-256.
- Guardião de publicação que verifica arquivos proibidos, marcador de demonstração e padrões de segredo.
- Workflows CI e deploy manual executam validadores; suíte ampliada para 19 testes.
- Criados `docs/INGESTAO_BASES.md` e `docs/ACEITE_E_PENDENCIAS.md`.
- Criar repositório ainda depende de ação no GitHub: a conexão disponível não dispõe de criação de repositórios.
