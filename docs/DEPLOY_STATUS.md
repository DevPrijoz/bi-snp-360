# Situação de implantação — 19/10/2026

## Demonstração publicada na Vercel

- Projeto: `bi-snp-360` no espaço de trabalho Vercel associado à conta do desenvolvedor.
- URL de produção: **https://bi-snp-360.vercel.app/**
- Implantação: `dpl_5cyTHNFWCfx8eERTYcqAaTDWK7pe`, versão do commit `d1bd5d0b1c5506e0533f5f631bec3ec3753527ad`, `readyState=READY` e alias sem erro.
- Git: `DevPrijoz/bi-snp-360` (privado), branch `main`.
- Configuração Vercel: `framework=null` (site estático), `rootDirectory=web`, sem comandos de instalação/build. O backend **não** participa do site publicado.
- A proteção por autenticação Vercel mantém-se nas **pré-visualizações**; versão de produção demonstrativa sem essa exigência.
- O deploy e a resolução do domínio foram confirmados pela API Vercel; as ferramentas disponíveis não conseguiram realizar uma requisição HTTP de navegação ao domínio. **O teste de abertura no navegador, links, filtros e responsividade ainda deve ser executado.**

## Causa e resolução da falha inicial

A importação do repositório inteiro para a Vercel detectou erroneamente FastAPI, produzindo o erro `FASTAPI_ENTRYPOINT_NOT_FOUND`. O módulo `backend/main.py` **existe**, mas é parte da API interna piloto e não deve ser publicado pela Vercel no mesmo projeto da demonstração.

**Resolução:** alterar o projeto Vercel para `framework=null`, `rootDirectory=web` e realizar um novo deployment de produção do `main`. A API da Vercel retornou `READY` com alias `bi-snp-360.vercel.app`.

## Qualidade e riscos

- GitHub Actions: **26 testes aprovados**, verificador de publicação sintética e verificação JavaScript, execução https://github.com/DevPrijoz/bi-snp-360/actions/runs/39301139844.
- Base publicada: JSON **apenas ilustrativo/sintético**. Não disponibilizar na Vercel dados do SEI, SIAFI, SIOP interno, documentos restritos, credenciais ou informações pessoais.
- A disponibilidade do site demonstrativo não significa implantação institucional, autenticação OIDC, banco de produção ou integração das fontes.
- A assinatura/condições de uso da hospedagem devem ser avaliadas antes de usar esta plataforma como serviço oficial do MPOR.

## GitHub Pages (não requerido agora)

As tentativas anteriores de habilitar Pages automaticamente no repositório privado falharam com HTTP 403 (`Resource not accessible by integration`). A demonstração passou a utilizar Vercel; não fazer mudanças de visibilidade no repositório para contornar o erro.

## Testes finais de aceite da demonstração

1. Abrir https://bi-snp-360.vercel.app/ em navegador não autenticado e confirmar carregamento da página.
2. Verificar a rota `/data/demo_public.json` e os arquivos `/assets/styles.css` e `/assets/app.js`.
3. Confirmar 12 módulos, filtros, detalhes, exportação e relatório.
4. Conferir responsividade em 375px e 1440px sem overflow horizontal.
5. Confirmar presença do aviso de **dados fictícios** e ausência de dados institucionais reais.
