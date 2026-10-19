# Arquitetura técnica e decisões

**Data-base:** 19/10/2026. **Versão:** 0.2.0. **Classificação:** documentação do protótipo, sem informações internas. **Destinatário proposto:** SNP / MPOR.

## Objetivo

Construir um portal de decisão e acompanhamento das competências portuárias da Secretaria Nacional de Portos, com consolidação de ações, recursos, responsabilidades e medidas corretivas. Quatro perspectivas: **direção, gestão, coordenação e controle**.

## Separação obrigatória dos contextos

```text
   DEMONSTRAÇÃO PÚBLICA (sem dados reais)
   GitHub Pages / servidor de arquivos estáticos
                 |
     web/index.html + assets/ + demo_public.json
     dados com marcação synthetic=true
                 X  SEM CONEXÃO DIRETA
                 |
   AMBIENTE INSTITUCIONAL (DEPENDE DE APROVAÇÃO)
   Rede/infraestrutura homologada da TI-MPOR
       |
   Gateway TLS + SSO OIDC institucional
       |
   Portal autenticado [a construir / homologar]
       | HTTPS com token validado no servidor
   API FastAPI + controle de permissões por unidade e registro
       |              |                  |
  PostgreSQL     Trilha auditoria     Serviço ingestão (a ampliar)
       ^                                   ^
       |                                   |
   Catálogo mestre, fonte, cutoff, versionamento, reconciliação
       ^
       |
   SEI / SIOP / SIAFI / Transferegov / Obrasgov / ANTAQ /
   Infra S.A. / autoridades portuárias / PNCP / TCU-CGU
          (conectores ainda NÃO implementados)
```

O painel público da SNHN inspirou navegação e organização visual; para a SNP o **domínio de negócio, unidades e modelos são próprios**. O sistema não agrega matérias atribuídas à SNHN salvo autorização e justificativa expressas.

## Camadas previstas

1. **Origem:** fontes oficiais/institucionais sob responsabilidade de seus gestores; sistema de origem continua autoridade do dado.
2. **Aquisição:** API oficial ou extração formalmente autorizada; cada carga terá hash, data/hora, versão, operador e instrumento de autorização.
3. **Staging:** armazenamento isolado, criptografia, retenção e reconciliação sem alterações no dado bruto.
4. **Tratamento:** validação de schema, data, unidade, moeda, chaves, relações verificáveis, duplicidade e qualidade.
5. **Catálogo mestre:** identificadores canônicos de unidades, processos, instrumentos, empreendimentos, projetos e fontes; nenhuma conciliação por semelhança nominal sem homologação.
6. **Serviço de regras:** semáforo com limiares homologados, qualidade, atualização, agregações versionadas e auditoria.
7. **API:** JWT OIDC validado pelo backend, regras de unidade/perfil/registro, DTO público minimizado; sem segredos no JS.
8. **Apresentação:** visões executivas com drill-down até o registro autorizado, data de corte, origem e trilha.

## Especificação do escopo nesta versão

| Componente | Estado | Observação |
|---|---|---|
| Layout, módulos, filtros, gráficos e relatório | Implementado | Demonstração exclusivamente fictícia. |
| Registro de solicitações/providências na API | Implementado em piloto | Sem frontend interno autenticado. |
| Homologação e publicação | Implementado em piloto | Depende de claims do IdP e papéis aprovados. |
| Encerramento auditado | Implementado em piloto | Requer evidência e homologação separada. |
| Importador CSV API | Implementado em piloto | Campos fixos, sem mapeamento de datasets reais. |
| Contratos e conferência de CSV autorizado | Implementado em piloto | Validação isolada, sem conciliação, importação produtiva ou publicação. |
| Bases oficiais SIOP, SIAFI, SEI e demais | **Não integrado** | Acesso/recortes e conectores dependem de autorização. |
| Infraestrutura institucional | **Não disponibilizada** | Homologação de TI pendente. |
| SSO corporativo em operação | **Não habilitado** | API espera parâmetros OIDC reais. |
| Migrações/backup/log centralizado/monitoramento | **Pendentes** | Pré-requisitos para produção. |

## Decisões arquiteturais (ADRs)

**ADR-001 — Não publicar dado sensível:** dados internos jamais residirão em páginas públicas ou repositórios públicos. Uma senha local no navegador não configura proteção. *Decisão: fronteira completa entre demonstração e ambiente institucional.*

**ADR-002 — Sem números oficiais fictícios:** bases de exemplo exigem identificação expressa `synthetic=true`, banner constante e fontes/validações pendentes. Nenhum indicador será representado como oficial até homologação.

**ADR-003 — Identificadores estáveis:** dados cruzados apenas com chaves e regras explícitas, fonte, corte, vigência e vínculo validado. Sem associação por nome semelhante.

**ADR-004 — Cor não encerra alerta:** procedimento de encerramento separado de situação/semáforo, exigindo evidência documental, justificativa, aprovador e log.

**ADR-005 — Sem autenticação de fachada:** backend não aceita senha no JS nem contas demonstrativas; JWT RS256 assinado por IdP externo. Em falta de parâmetros a API interna indisponibiliza acessos.

**ADR-006 — Banco do piloto isolado:** SQLite local apenas para desenvolvimento/testes; para produção migrar a PostgreSQL ou serviço homologado, com migrações, backup e alta disponibilidade definidos pela TI.

## Riscos conhecidos

- Vinculação das CGs do PDF não homologada no SIORG; exibição da interface com ressalva.
- Não há data real, acessos concedidos nem amostras oficiais autorizadas.
- Catálogo de 19 indicadores preliminares não substitui dicionário oficial.
- Não está pronto para produção: integração frontal autenticada, pentest, política de retenção, trilhas imutáveis e validação de publicação aguardam aprovação.
- Claims `unit_codes` e `permissions` só têm força quando o IdP institucional os emite sob governança aprovada. Não expor ou usar tokens em GitHub.

## Marco legal e metodológico

Proposta executiva BI SNP 360°, 15/10/2026, p. 3–10. Referências indicadas: Decretos 11.354/2023, 11.979/2024, 12.663/2025, 9.203/2017, SIORG e Portaria MPOR 110/2025. A aplicabilidade atual precisa ser revisada pelo jurídico e gestores, pois o documento é conceitual.

**ADR-007 — Porta de publicação:** CI e deployment manual executam verificação de arquivos proibidos e exigem snapshot demonstrativo. Este controle automático não substitui classificação da informação e revisão humana.
