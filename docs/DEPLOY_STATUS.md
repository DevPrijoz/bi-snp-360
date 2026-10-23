# Hospedagem BI SNP 360° — estado atual em 23/10/2026

## Produção

- **Endereço:** https://bi-snp-360.vercel.app/
- **Destino:** portal executivo de acesso restrito, com dados fornecidos pelo responsável.
- **Vercel:** projeto `bi-snp-360`, `framework=null`, diretório raiz `diretoria`, branch `main`.
- **Proteção obrigatória:** `ssoProtection.deploymentType=all` (Vercel Authentication, All Deployments); nunca desligar nem criar bypass para a diretoria.
- **GitHub:** repositório `DevPrijoz/bi-snp-360` privado. `diretoria/index.html` contém o painel e os seis documentos em base64, para download após login.
- **Teste anônimo:** deve redirecionar para a autenticação, nunca responder com `<script id="dat"` ou `<script id="fontes-originais"`.
- **Limite:** os usuários autorizados da diretoria ainda não foram designados. O plano Hobby pode limitar o acesso externo; acesso real individual exige conta e permissão na Vercel.

## Dados e homologação

Quatro XLSX originais foram embutidos **sem alteração de bytes**, com hash SHA-256. O painel executa uma leitura gerencial preliminar e preserva as divergências identificadas; não substitui a homologação de fontes. A série histórica tem corte informado 09/10/2026; o corte do detalhamento e responsáveis serão cadastrados em versões posteriores.

## Demonstração anterior

`web/` contém o código de protótipo sintético e continua submetido a `scripts/release_guard.py`. Essa pasta deixou de ser a raiz de hospedagem Vercel; dados oficiais não devem ser misturados ali. O backend é piloto local, não API produtiva.

## Controle de acesso

Para incluir diretor:
1. Solicitar que o destinatário tenha conta Vercel e acesse o link de produção autenticado.
2. Aprovar **individualmente** o acesso na área de Deployment Protection / Requests do projeto, respeitando o limite da conta.
3. Revogar acesso quando não for mais necessário.
4. Não usar Shareable Link (link de bypass), senhas em JavaScript, links públicos ou exceções de proteção.

**Validação técnica:** execução `READY` na Vercel com domínio principal, e monitoramento de acesso anônimo pelo workflow de privacidade. Não substitui inspeção manual autenticada no navegador da diretoria.
