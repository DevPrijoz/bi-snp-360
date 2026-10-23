# Portal de dados para a Diretoria — 23/10/2026

## Abrangência e versões

Os arquivos originais fornecidos pelo responsável (histórico 2019–2026, dados secundários, execução LOA+RAP 2026 e processos pendentes) estão embutidos sem alterações no arquivo `diretoria/index.html`, com integridade SHA-256 conferida; também estão acessíveis os derivados de relatório gerencial e conferência. O aplicativo apresenta indicadores **preliminares**; diferenças e data de corte continuam pendentes de homologação.

## Segurança e papéis

O repositório GitHub permanece privado e o domínio Vercel deve ter **Vercel Authentication / All Deployments** (não Standard / Preview). Não compartilhar links de bypass ou exceções de proteção. Solicitações de acesso devem ser aprovadas individualmente pela titularidade da conta. No plano Hobby a Vercel pode limitar usuários externos; verifique a licença necessária para o número de diretores.

## Implantação

Projeto `bi-snp-360`, branch `main`, pasta Vercel root `diretoria`, framework **Other/None**, sem build e com autenticação para toda a produção. A pasta `web/` mantém a demo sintética no GitHub, mas **não** faz parte do novo deploy de produção.

## Atualização

1. Confirmar quem enviou as novas planilhas, fonte oficial, exercício e data de corte.
2. Comparar dados sem alterar arquivos originais e gerar relatório de divergências.
3. Validar documentos e hashes em ambiente local.
4. Atualizar somente `diretoria/` após checagem da proteção do domínio.
5. Confirmar implantação READY e ensaio com usuário autorizado; preservar versões anteriores.

Responsáveis e cortes definitivos serão incorporados quando informados, sempre com histórico.
