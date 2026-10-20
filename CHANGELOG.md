## v0.5.0 — Preparação do ciclo orçamentário (20/10/2026)

- Novo contrato preliminar para pagamentos LOA/RAP em `contracts/datasets.json`.
- Script de conferência conjunta de LOA/execução/RAP/pagamentos: reporte local apenas de contagens e hashes, sem dados brutos ou publicação.
- Gerador restrito de amostras fictícias e testes de rejeição/atomicidade.
- Matriz de integrações demonstrativa refinada e documentação de solicitação de dados.
- Nenhuma integração real efetuada; fonte, dicionário, infraestrutura e homologação pendentes.

## v0.4.0 — Resiliência e gestão das integrações (demonstração)

- Nova visão navegável **Situação das integrações** com seis fontes prioritárias, responsáveis propostos, pré-requisitos e estados explicitamente pendentes.
- Matriz CSV exportável, sem dados institucionais.
- `/health.json` para verificações de disponibilidade, sem backend.
- `vercel.json` com cabeçalhos protetivos no frontend.
- Validação estrita de datas em importações demonstrativas e proteção adicional contra fórmulas executáveis em CSV exportado.
- Testes automáticos do contrato web e verificação HTTPS agendada no GitHub Actions.
- Nenhuma integração oficial implementada. Entrada em produção institucional permanece bloqueada por autorizações, dados e infraestrutura.

# Histórico de versões

## 0.2.0 — 2026-10-19

- Adicionados 6 contratos preliminares: LOA, execução, RAP, processos, obras e movimentação.
- Implementado validador local de CSV autorizado, com conferência de unicidade, tipos, datas, autorização informada, SHA-256 e manifesto de ingestão pendente.
- Implementado `release_guard.py` para impedir versionamento de arquivos de base proibidos, segredos óbvios e snapshot público sem marcação sintética.
- Ampliada a suíte para 19 testes (incluindo ingestão e segurança de publicação).
- CI e deploy manual de Pages agora executam o guardião de publicação antes dos demais passos.
- Criados manuais de ingestão e matriz de aceite e dependências institucionais.
- Nenhum conector oficial foi ativado e nenhuma base institucional foi importada.

## 0.1.0 — 2026-10-19

- Protótipo visual responsivo de 12 módulos e console executivo SNP.
- 19 indicadores preliminares e 10 fontes previstas, sem dados oficiais.
- 12 registros sintéticos com identificação inequívoca de demonstração.
- Exportação CSV e relatório executivo; importação local apenas para teste.
- API piloto com autenticação OIDC obrigatória, autorização por unidade/classificação, auditoria, homologação, publicação controlada e fechamento com evidência.
- Validação de CSV com prévia, sem substituição automática nem publicação.
- Nove testes de backend, script de validação de dados e verificação JS.
- Documentação de arquitetura, dados, segurança, integração, operações e plano de evolução.

**Limitação:** ainda não há repositório remoto criado, integração real, infraestrutura institucional ou homologação.
