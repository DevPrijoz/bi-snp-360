# BI SNP 360° — Separação segura de desenvolvimento e apresentação

## Situação verificada em 29/10/2026

O repositório **DevPrijoz/bi-snp-360** foi identificado como **público** e contém `diretoria/index.html` com conteúdo e documentos incorporados de circulação restrita. O acesso protegido da Vercel **não protege o código de um repositório GitHub público** nem o histórico.

**Ação prioritária do proprietário:** em https://github.com/DevPrijoz/bi-snp-360/settings, configurar a visibilidade do repositório principal como **Private**. Não tornar a visibilidade pública novamente sem revisão de todos os commits. Torná-lo privado agora não elimina exposições ou cópias anteriores. Se houve informações sigilosas/credenciais, tratar também a revogação e eventual saneamento do histórico.

## Arquitetura final recomendada

| Origem | Endereço | Acesso | Conteúdo |
| --- | --- | --- | --- |
| Repositório mestre | `DevPrijoz/bi-snp-360` | **Privado** | código-fonte completo, `backend/`, controles e materiais autorizados da diretoria |
| Repositório de demonstração | `DevPrijoz/bi-snp-360-web` | **Público** | **somente** os arquivos da pasta `web/` deste projeto, com histórico Git **novo** |
| Pages da demonstração | `devprijoz.github.io/bi-snp-360-web/` | Público | interface e JSON inteiramente sintético |
| Portal da diretoria | `bi-snp-360.vercel.app` | Autenticação | recursos reais autorizados, sem compartilhamento irrestrito |

## Processo correto de migração

1. **Tornar `DevPrijoz/bi-snp-360` privado.** É uma operação administrativa não disponibilizada pelo conector GitHub atual; somente um administrador da conta consegue executá-la no site.
2. Criar o repositório **público e vazio** `DevPrijoz/bi-snp-360-web`: https://github.com/new . Não utilizar template ou fork do projeto principal.
3. Gerar o ZIP limpo: `python scripts/export_safe_public.py` a partir do projeto mestre (ou usar o ZIP da entrega v0.9.0). Confirmar que não contém `diretoria/` ou `backend/`.
4. Criar um histórico Git **novo** para os arquivos do ZIP. **Não** executar `git push --mirror` nem `git clone --bare` do projeto mestre para o repositório público.
5. Configurar o GitHub Pages do novo repositório em **Settings > Pages**; escolher **Deploy from a branch**, branch `main`, pasta `/(root)` após enviar os arquivos limpos para a raiz. O endereço esperado será `https://devprijoz.github.io/bi-snp-360-web/`.
6. Validar em navegador anônimo `/`, `/data/demo_public.json`, gráficos e filtros; rejeitar qualquer publicação de dados reais.
7. Manter os atualizadores de dados reais apenas no repositório mestre/ambiente protegido. Novas versões públicas sempre passam pelo exportador com lista de extensões e apenas o JSON demonstrativo.

## O que já existe na v0.9.0

Os 12 módulos conceituais, suas fichas gerenciais técnicas, matriz de indicadores, alertas e relatórios, além da página conceitual de Pessoas e Equipes. Não há números de pessoal ou orçamento oficial na exportação pública.

**Observação:** o Pages que hoje existe em `https://devprijoz.github.io/bi-snp-360/` é resultado do repositório principal ainda público. Quando o principal tornar-se privado, esse Pages pode parar no plano Free. O novo Pages público será o substituto.
