# BI SNP 360° — Portal privado da Diretoria

**Acesso:** exige Vercel Authentication configurado para **All Deployments** no projeto `bi-snp-360`. O projeto GitHub de origem permanece privado.

**Conteúdo:** painel gerencial elaborado com as quatro bases fornecidas pelo responsável em 23/10/2026, sem retificá-las. Os seis anexos (quatro XLSX originais, relatório PDF e conferência XLSX) estão empacotados no HTML do portal, com SHA-256 por documento.

**Limites:** a data de corte da série histórica é 09/10/2026; a planilha detalhada LOA+RAP não possui metadado de corte na aba; conciliações e responsáveis aguardam confirmação. Os indicadores NÃO estão homologados.

**Obrigatório antes de divulgar:** confirmar que a Vercel informa `ssoProtection.deploymentType=all`. Nunca adicionar URLs de exceção/bypass nem compartilhar links que dispensam autenticação. A Vercel no plano Hobby pode limitar o número de usuários externos.

**Fluxo de atualização:** usuário fornece as novas planilhas -> conciliação e testes -> conferência das diferenças -> publicação de nova versão privada com todos os cortes e fontes. Nunca alterar arquivos de origem no histórico.
