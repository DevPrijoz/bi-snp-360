# BI SNP 360° — Governança e Gestão

> **ESTADO: protótipo técnico funcional / piloto de API — NÃO HOMOLOGADO PARA PRODUÇÃO.**
> Toda a base exibida na interface pública é **sintética e fictícia**, sem representação de dados reais do MPOR. Não utilizar para decisões institucionais.

**Versão de desenvolvimento:** v0.6.0 (governança e recebimento) • sistema institucional ainda não homologado.

**Repositório principal (privado):** [DevPrijoz/bi-snp-360](https://github.com/DevPrijoz/bi-snp-360). **Pasta demonstrativa:** `web/`. **Demonstração em produção:** https://bi-snp-360.vercel.app/ (acesso pode depender da política de rede do Ministério). Veja [DEPLOY_STATUS.md](docs/DEPLOY_STATUS.md). O sistema de inspiração é o [BI Hidrovias da SNHN](https://hzhcdyvz4w-tech.github.io/bi-hidrovias/); não reutiliza os dados ou a estrutura orgânica da SNHN.


## Marco v0.7.0 — Primeiras planilhas oficiais, controle de publicação

Recebidos quatro arquivos institucionais (série histórica, execução detalhada LOA+RAP, autorizações secundárias e pendências). O projeto implementa funções puras de reconciliação e extração local; **nenhum conteúdo oficial é incluído no repositório ou na Vercel**. O painel público permanece demonstrativo. Consulte [Primeira Carga Oficial](docs/PRIMEIRA_CARGA_OFICIAL_2026.md).

## Marco v0.6.0 — Kit de solicitações e aceite

- Matriz de **7 solicitações** (orçamento, conciliação, SIORG, TI, obras, outorgas, SEI/ANTAQ) com responsabilidades propostas, dependências e evidências.
- Gerador de rascunhos individuais para instrução de demandas internas: `python -m scripts.governance_kit kit`.
- Verificador isolado de metadados de recebimento: `python -m scripts.governance_kit conferir arquivo.json`; nunca homologa nem publica informação automaticamente.
- Nova seção de encaminhamentos no painel demonstrativo, com exportação CSV e zero aprovações oficiais.
- Procedimento completo em [GUIA_SOLICITACOES_E_ACEITE.md](docs/GUIA_SOLICITACOES_E_ACEITE.md).

## Marco v0.5.0 — Preparação orçamentária para ingestão

- Incluído o contrato preliminar **pagamentos**, independente de LOA, execução e RAP; campos e chaves ainda sujeitos à homologação SIAFI.
- Preparado um pacote local para validar os **quatro arquivos em conjunto**, rejeitando arquivos incompatíveis sem publicar linhas, valores ou dados institucionais.
- Gerador de exemplos 100% sintéticos em `local_data/` para ensaios, com testes de falha e conferência.
- Plano público de integrações detalhado no painel, deixando explícito o que está pendente; **zero integrações oficiais**.
- Passo a passo: [docs/PACOTE_ORCAMENTARIO.md](docs/PACOTE_ORCAMENTARIO.md).

## Atualização v0.4.0 — Verificações e matriz de integrações

- **Visão Situação das integrações**: plano de recebimento dos conjuntos de dados prioritários, responsáveis propostos, campos exigidos e exportação de matriz CSV; todos permanecem **pendentes**, sem qualquer vínculo oficial.
- **Verificação de saúde estática**: `/health.json` (retorna `synthetic: true`, `official_integrations: 0`, `institutional_backend: false`).
- **Segurança e qualidade da apresentação**: cabeçalhos de proteção Vercel, validação de datas e mitigação de fórmulas de planilha nos CSVs exportados.
- **Testes automatizados**: 25 testes locais e teste visual Chromium em desktop (1440 px) e celular (375 px), sem erros de JS ou rolagem horizontal; verificação HTTPS agendada e após alterações no GitHub Actions.
- **URL pública da demonstração**: https://bi-snp-360.vercel.app/ — não é ambiente corporativo de dados reais.

**Bloqueadores de produção institucional:** acesso autorizado às fontes, classificação da informação, dicionários e chaves oficiais, homologação por unidades/gestores, IdP/SSO, backend e banco corporativo, gestão de backups, monitoramento, testes de segurança e aceite de TI/MPOR. Nenhum deles fica automaticamente resolvido por implantar o frontend estático.

## O que está disponível

- Interface responsiva com 12 módulos, filtros globais, detalhamento, semáforo, panorama, gráficos, catálogo inicial de 19 indicadores e relatório imprimível.
- Base de demonstração JSON com 12 registros e 10 fontes **marcadas como fictícias/previstas**.
- Exportação CSV e JSON, importação de CSV **somente local e temporária no navegador** (somente conteúdo sintético/autorizado).
- API FastAPI com persistência para piloto, autenticação **OIDC/JWT obrigatória**, checagem de permissões por unidade, trilha de auditoria, homologação segregada, publicação explícita e encerramento de alertas com providência e evidência.
- Importação CSV de piloto com `dry_run=true` por padrão, limite de tamanho, verificação de duplicados e sem publicação automática.
- Testes automatizados, validador de publicação e workflows de CI; a **demonstração pública é implantada automaticamente na Vercel** a partir da branch `main`.
- Contratos preliminares de 7 bases e utilitário isolado de conferência de CSV, que gera manifesto SHA-256 pendente de homologação **sem exportar o conteúdo para o frontend ou repositório**.

**Importante:** A interface demonstrativa **não está ligada à API interna**. Essa separação é intencional: a interface é somente um demonstrador estático para apresentação. O uso institucional precisará de um frontend autenticado, integração segura com o backend, IdP homologado, migrações, observabilidade, segurança e aprovação da TI/gestores.

## Inicialização da interface (não exige instalação)

```bash
cd bi-snp-360
python -m http.server 8080 --directory web
# abrir http://localhost:8080
```

A aplicação usa a base `web/data/demo_public.json`. Se um arquivo não for explicitamente marcado como `synthetic=true` e `environment=DEMONSTRACAO`, seu carregamento será recusado.

## Inicialização da API (piloto LOCAL, sem dados reais)

```bash
cd bi-snp-360
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements-dev.txt
mkdir -p data
# configure somente parâmetros de teste sem credenciais institucionais reais
export SNP_AUTO_CREATE_SCHEMA=1
uvicorn backend.main:app --reload
# documentação de endpoints: http://localhost:8000/api/docs
```

Todas as rotas internas exigem assinatura RS256 e claims de um provedor OIDC configurado (`OIDC_ISSUER`, `OIDC_AUDIENCE`, `OIDC_JWKS_URL`). Na ausência dessas configurações, retornam **HTTP 503**, sem modo de login falso em produção. O endpoint público de transparência só retorna dados classificados `publico`, homologados **e** publicados. Sem dados reais autorizados, retorna `[]`.

### Testes e verificações

```bash
python scripts/validate_assets.py
python scripts/release_guard.py
node --check web/assets/app.js
pytest -q
```

## Organização

```text
bi-snp-360/
├── web/
│   ├── index.html            # painel demonstrativo público
│   ├── assets/              # CSS, JavaScript, ícone
│   └── data/demo_public.json # amostra explicitamente fictícia
├── backend/
│   ├── main.py               # rotas e fluxos de homologação
│   ├── models.py             # persistência e auditoria
│   └── security.py           # identidade externa + autorização granular
├── docs/
│   ├── ARQUITETURA.md
│   ├── MODULOS.md
│   ├── MODELO_DADOS.md
│   ├── SEGURANCA.md
│   ├── IMPLANTACAO.md
│   ├── API.md
│   ├── ROADMAP.md
│   └── REGISTRO_DESENVOLVIMENTO.md
├── contracts/              # contratos preliminares de bases LOA, RAP etc.
├── scripts/                # CSV sintético, conferência de bases e validação da publicação
├── tests/                  # fluxos de segurança e qualidade
├── .github/workflows/      # CI e deploy manual público
├── Dockerfile               # container de API de piloto
└── docker-compose.yml       # somente desenvolvimento LOCAL
```

## Situação dos módulos

**Implementado no protótipo:** interface, navegação, filtros, listagem/descrição de registros, alerta demonstrativo, catálogo preliminar, relatório e exportações; API com CRUD limitado e fluxos de controle.

**Dependente das áreas:** bases oficiais, modelos de integração, dicionário homologado de indicadores, organograma SIORG, responsáveis, credenciais e rede, privacidade, estratégia de produção, aceitação funcional.

**Nunca versionar:** SEI, SIAFI, planilhas internas não públicas, dados pessoais, segredos, chaves, anexos institucionais protegidos, dumps de banco e logs sensíveis.

Consulte os documentos de arquitetura, segurança, operação e plano de trabalho em `docs/`.

**Referência funcional:** *BI SNP 360° — Governança e Gestão*, proposta executiva da SNP/MPOR, de **15/10/2026**, 11 páginas. O documento descreve uma **proposta conceitual**, não autorização institucional, sistema homologado ou integração concedida.

## Próximo ciclo de ingestão

O arquivo `contracts/datasets.json` oferece layouts **propostos** para LOA, execução, RAP, processos, obras e movimentação portuária. O script `scripts/inspect_dataset.py` valida uma extração autorizada **localmente**, registra hash e gera manifesto com situação `pendente_homologacao`, sem carregar informação institucional no GitHub. Leia [INGESTAO_BASES.md](docs/INGESTAO_BASES.md) e [ACEITE_E_PENDENCIAS.md](docs/ACEITE_E_PENDENCIAS.md).

## Publicação web (demonstração ativa na Vercel)

A demonstração sintética é publicada em **https://bi-snp-360.vercel.app/** e o repositório principal permanece privado. A rede corporativa do MPOR pode bloquear o domínio; isso deve ser tratado com a TI, sem contornar políticas. Leia [DEPLOY_STATUS.md](docs/DEPLOY_STATUS.md).
