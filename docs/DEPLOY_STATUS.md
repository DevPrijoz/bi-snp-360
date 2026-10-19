# Hospedagem web — estado verificado (19/10/2026)

## GitHub principal
- Repositório: `DevPrijoz/bi-snp-360` (privado, `main`).
- Frontend seguro para **demonstração sintética**: pasta `web/`.
- Fluxo de validação: `.github/workflows/ci.yml` (executa análise de segurança, teste de ativos, testes Python e verificação JS).
- Fluxo de publicação: `.github/workflows/pages.yml` (somente por acionamento manual, não usa dados institucionais).

## Por que o GitHub Pages falhou
O Actions tentou usar `actions/configure-pages@v5` antes de o site existir. A tentativa de criação do Pages a partir do `GITHUB_TOKEN` resultou em `Resource not accessible by integration` (HTTP 403). A criação inicial de um site Pages precisa de credenciais/privilégios de administração; habilitar `pages: write` no workflow **não substitui** o procedimento de administração da conta. A repetição do workflow com `enablement: true` não resolve.

## Única decisão/configuração pendente para URL GitHub Pages
Um proprietário deve entrar em `Settings > Pages` e definir `Build and deployment > Source: GitHub Actions` (se permitido pela assinatura e visibilidade do repo). Depois disso, executar em Actions o fluxo de publicação da demo. O endereço `https://devprijoz.github.io/bi-snp-360/` é **um formato previsto, NÃO um site confirmado** até que o fluxo retorne sucesso e o link funcione.

### Se a conta for GitHub Free
Para Pages com conta pessoal gratuita, o repositório precisa ser público. **Não tornar público** o repositório principal, que poderá conter lógica e documentos técnicos internos. Opções seguras: manter o projeto principal privado e utilizar hospedagem separada para a pasta `web/` (por exemplo Vercel após conectar uma conta, configurando `Root Directory = web` e sem publicar backend ou pastas confidenciais) ou avaliar plano GitHub Pro para Pages em repositório privado. Atenção: Pages originado de repositório privado pessoal não é, por si só, um mecanismo para proteger informações confidenciais; somente a demo pode ser publicada na internet.

## O que não deve ser confundido com a demo
A API FastAPI em `backend/` é um piloto, não um serviço de produção. Sem as credenciais/estrutura autorizadas de IdP e bancos, não deve receber dados reais. Frontend interno e integrações requerem homologação separada.

## v0.4.0 — Prontidão da demonstração

Inclui rota estática `health.json`, manifesto Vercel de cabeçalhos HTTP e testes de disponibilidade em `.github/workflows/live-smoke.yml`. Nova página da matriz das seis integrações previstas com **zero fontes conectadas**. Confirmação do novo deploy/CI no GitHub após publicação deste commit.
