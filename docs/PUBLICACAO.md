# BI SNP 360° — Publicação e pendências

## Entrega na conta DevPrijoz
O repositório privado contém:
- `index.html`: apresentação autônoma (HTML offline).
- `web/`: frontend estático organizado em HTML, CSS, JavaScript e JSON **exclusivamente sintético**.
- `.github/workflows/ci.yml`: verificações estáticas automáticas.
- `.github/workflows/pages.yml`: implantação estática preparada para GitHub Pages.

**Atenção:** a URL potencial `https://devprijoz.github.io/bi-snp-360/` só é utilizável após uma implantação Pages bem-sucedida. Não considerar publicada com base apenas no endereço.

## Habilitar Pages
1. Abrir `Settings > Pages` do repositório.
2. Em **Build and deployment > Source**, escolher **GitHub Actions** (caso o plano/visibilidade do repositório permitam Pages).
3. Conferir em `Actions > Publicar demonstracao estatica - GitHub Pages` a execução e o endereço confirmado em **Deployments**.
4. Se o plano não permitir Pages em repositório privado, **não** publicar as bases internas tornando o repositório público. Antes, obter autorização institucional e hospedar só uma cópia **limpa da demo**, separada do backend.

## Escopo da entrega
A demonstração inclui 12 cartões funcionais, detalhes dos registros ilustrativos, catálogo de indicadores, filtros, alertas, fontes e relatórios. Os números e providências do exemplo são fictícios. O uso interno requer inventário SIORG, fonte oficial homologada, acesso OIDC e autorização de TI.

## Segurança
Nenhum segredo, documento do SEI ou informação pessoal deve ser incluído em `web/`. A publicação via Pages transfere **todos** os arquivos de `web/` para um site eventualmente público. A integração corporativa deve usar API protegida em ambiente próprio, **nunca** credenciais de API diretamente no navegador.

## Referências
Proposta executiva BI SNP 360°, de 15/10/2026. Inspiração visual: BI Hidrovias/SNHN.
