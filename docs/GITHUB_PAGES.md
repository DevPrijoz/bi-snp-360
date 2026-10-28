# GitHub Pages — BI SNP 360°

## Estado verificado em 28/10/2026

- Repositório **DevPrijoz/bi-snp-360**: **privado**, branch `main`.
- Existe uma interface HTML/CSS/JS funcional em `web/`, com dados exclusivamente **fictícios**.
- Workflow de deploy: [`.github/workflows/pages.yml`](../.github/workflows/pages.yml), acionado por alteração em `web/` ou no próprio workflow e manualmente.
- Teste e verificador de publicabilidade: **aprovados** na execução do Pages [40744381760](https://github.com/DevPrijoz/bi-snp-360/actions/runs/40744381760).
- Etapa `actions/configure-pages@v5`: **falhou com 404**, porque o serviço Pages não está configurado no repositório.
- O endereço previsto `https://devprijoz.github.io/bi-snp-360/` **não deve ser apresentado como publicado** até o GitHub mostrar deployment com status `success`.

## Habilitação única pelo titular

1. Abrir https://github.com/DevPrijoz/bi-snp-360/settings/pages com o login proprietário.
2. Em **Build and deployment / Source**, escolher **GitHub Actions**, se essa opção estiver disponível.
3. Se a tela informar que Pages não está disponível para o repositório privado, verificar o plano da conta. Conforme a documentação GitHub, Pages em repositório privado exige GitHub Pro, Team ou Enterprise; com GitHub Free, o repositório precisa ser público.
4. **Não tornar este repositório público sem auditoria e remoção de histórico**. Ele contém material interno da diretoria codificado em HTML na pasta `diretoria/`. O conteúdo e o histórico ficam acessíveis se a visibilidade for alterada.
5. Após habilitar, ir a https://github.com/DevPrijoz/bi-snp-360/actions/workflows/pages.yml , clicar em **Run workflow**, branch `main`, e verificar a URL em Settings > Pages.
6. Em aba anônima, verificar `https://devprijoz.github.io/bi-snp-360/` e `.../data/demo_public.json`. Os dados devem conter `"synthetic": true`. Não deve existir `/diretoria/` no Pages.

## Separação obrigatória

| Destino | Arquivos | Acesso |
| --- | --- | --- |
| GitHub Pages (se habilitado) | apenas `web/` | público, dados fictícios |
| Vercel diretoria | `diretoria/` | Vercel Authentication, não remover sem substituição adequada |
| GitHub repositório principal | código e histórico completo | privado |

**GitHub Pages padrão é um serviço estático e público.** Não utilize como acesso restrito por usuário à diretoria.

## Planos alternativos

- Manter o repositório privado com o plano GitHub Pro e usar Pages **somente para a demonstração**.
- Criar um repositório público **separado** contendo exclusivamente a demonstração, preservando o repositório principal privado.
- Continuar na Vercel com proteção de acesso para dados oficiais; ela já está implantada separadamente e não depende do Pages.
