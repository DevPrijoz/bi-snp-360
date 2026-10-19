# BI SNP 360° — Governança e Gestão

> **ESTADO: protótipo técnico funcional / piloto de API — NÃO HOMOLOGADO PARA PRODUÇÃO.**
> Toda a base exibida na interface pública é **sintética e fictícia**, sem representação de dados reais do MPOR. Não utilizar para decisões institucionais.

**Versão de desenvolvimento:** v0.3.0 • 19 testes de API, dados e segurança aprovados localmente. A execução em CI deve ser conferida a cada commit.

**Repositório principal (privado):** [DevPrijoz/bi-snp-360](https://github.com/DevPrijoz/bi-snp-360). **Pasta demonstrativa:** `web/`. **Status GitHub Pages:** dependente de habilitação na conta. Veja [DEPLOY_STATUS.md](docs/DEPLOY_STATUS.md). O sistema de inspiração é o [BI Hidrovias da SNHN](https://hzhcdyvz4w-tech.github.io/bi-hidrovias/); não reutiliza os dados ou a estrutura orgânica da SNHN.

## O que está disponível

- Interface responsiva com 12 módulos, filtros globais, detalhamento, semáforo, panorama, gráficos, catálogo inicial de 19 indicadores e relatório imprimível.
- Base de demonstração JSON com 12 registros e 10 fontes **marcadas como fictícias/previstas**.
- Exportação CSV e JSON, importação de CSV **somente local e temporária no navegador** (somente conteúdo sintético/autorizado).
- API FastAPI com persistência para piloto, autenticação **OIDC/JWT obrigatória**, checagem de permissões por unidade, trilha de auditoria, homologação segregada, publicação explícita e encerramento de alertas com providência e evidência.
- Importação CSV de piloto com `dry_run=true` por padrão, limite de tamanho, verificação de duplicados e sem publicação automática.
- Testes automatizados (19 cenários), validador de publicação e workflows de CI; deploy da **demonstração pública somente manual**, nunca automático.
- Contratos preliminares de 6 bases e utilitário isolado de conferência de CSV, que gera manifesto SHA-256 pendente de homologação **sem exportar o conteúdo para o frontend ou repositório**.

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

## Publicação web (bloqueio de conta)

Leia [DEPLOY_STATUS.md](docs/DEPLOY_STATUS.md). O Pages não está ativado porque o `GITHUB_TOKEN` do workflow não pode criar o site (erro de permissão). O endereço não deve ser divulgado como ativo antes do deploy bem-sucedido. O repositório principal deve permanecer privado; alternativa de hospedagem separada requer autorização e conexão da conta do provedor.
