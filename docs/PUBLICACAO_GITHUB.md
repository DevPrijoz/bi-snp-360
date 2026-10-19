# Publicação na conta principal DevPrijoz

A URL `https://github.com/DevPrijoz` identifica um **perfil/conta**, não um repositório Git isolado. O repositório `DevPrijoz/DevPrijoz` é especial (README do perfil) e **não deve receber o código do BI SNP 360°**.

**Destino recomendado:** criar repositório separado `bi-snp-360`, na conta `DevPrijoz`, inicialmente **privado**, sem README e sem arquivos iniciais. Posteriormente ele pode hospedar apenas a demo pública se a administração autorizar. Nenhum dado interno institucional poderá ser enviado ao GitHub público.

## Passo para desbloquear publicação

1. Acesse `https://github.com/new` autenticado na conta DevPrijoz.
2. Owner: `DevPrijoz`; Repository name: `bi-snp-360`; Visibility: **Private**; desmarque README, .gitignore e licença iniciais.
3. Clique em **Create repository** e compartilhe a URL `https://github.com/DevPrijoz/bi-snp-360` para publicação via integração conectada.

## Alternativa para importar o Git bundle

O artefato `bi-snp-360.bundle` transporta o commit do projeto local e a branch `main`. Em um computador com Git instalado:

```bash
git clone bi-snp-360.bundle bi-snp-360
cd bi-snp-360
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/DevPrijoz/bi-snp-360.git
git push -u origin main
```

**Não iniciar repo dentro de `DevPrijoz/DevPrijoz` ou outro projeto preexistente sem autorização explícita.**

Após criação do repositório, `CI` valida Python/Node e testes. Deploy manual da demo pública requer habilitar Pages e autorizar a publicação, sem qualquer base interna. Não ativar o deploy se já houver material institucional no mesmo diretório.

## Pré-voo técnico v0.2.0

```bash
python scripts/release_guard.py
python scripts/validate_assets.py
node --check web/assets/app.js
pytest -q
```

No GitHub, manter **repositório privado**, ativar CI, configurar equipe de acesso, regras de revisão e política de proteção de branch com aprovação da TI. Para o protótipo, **não habilitar Pages automaticamente**: mesmo publicado a partir de repositório privado, o site pode ficar acessível publicamente conforme configuração/plano. Deploy requer decisão expressa de publicização dos materiais de demonstração.


## Atualização de outubro/2026

O repositório `DevPrijoz/bi-snp-360` já foi criado e tem `main` privado. Após importar o pacote, considere este documento uma lista histórica. O endereço GitHub Pages depende de habilitação administrativa. Consulte [DEPLOY_STATUS.md](DEPLOY_STATUS.md).
