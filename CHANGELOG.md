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
