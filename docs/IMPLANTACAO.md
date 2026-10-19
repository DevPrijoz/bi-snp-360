# Implantação e operação

## Escopo de deploy disponível AGORA

**Demonstração pública**: publicar somente a pasta `web/`. O workflow `.github/workflows/public-demo.yml` é **manual**, requer GitHub Pages habilitado e protege contra deploy acidental ao verificar `synthetic=true`. Não colocar arquivo institucional real sob `web/`.

**API piloto**: executar localmente com venv ou `docker compose up --build`, com SQLite exclusivo de desenvolvimento. `docker-compose.yml` publica a porta apenas em `127.0.0.1`. Para acessar dados, exige configuração OIDC; credenciais de produção não devem ser armazenadas em arquivos do repositório.

## Modelo de implantação institucional FUTURA (não implementada)

- Infraestrutura aprovada por TI/MPOR, preferencialmente ambientes separados dev/homologação/prod.
- Gateway HTTPS com certificados corporativos, TLS, proteção contra abuso e políticas de acesso.
- IdP OIDC institucional configurado com JWT RS256 assinado, `iss`, `aud`, chaves JWKS e claims autorizadas.
- Banco PostgreSQL/serviço gerenciado com criptografia, backup, retenção, migrações e segregação de privilégios.
- Segurança de rede para conectores oficiais e custódia de credenciais em cofre institucional, sem acesso de navegador público às fontes.
- Logs, métricas, trilhas, alertas operacionais, incidente, versionamento de data cutoff e revisão de publicação.
- Frontend autenticado implementado e testado separadamente (atualmente protótipo estático, deliberadamente não integrado à API).

## Recebimento de novas bases

1. Nomear responsável técnico e gestor da fonte.
2. Receber autorização formal, base amostral sanitizada e dicionário.
3. Definir identificador único, janela temporal, qualidade e classificação da informação.
4. Criar adaptador de ingestão por fonte em branch de feature.
5. Executar validação/testes em ambiente isolado.
6. Homologar amostras, indicadores, regras de semáforo e perfil de acesso.
7. Executar publicação no ambiente institucional autorizado.

## Operação e incidentes

- Antes de cada publicação registrar versão, commit, fonte, corte, responsável, testes, parecer técnico e autorização.
- Falhas de ingestão devem bloquear atualização sem modificar o último snapshot homologado.
- Revogação de permissão deve ocorrer no IdP e refletir nos tokens e sessões; estudar expiração máxima com segurança.
- Nunca resolver divergência alterando um dado oficial de origem dentro do BI; a correção deve acontecer no sistema proprietário.
- Alertas só encerram depois da providência executada, evidência anexada e validação por responsável autorizado.

## Compromissos institucionais

Não há prazo de entrada em produção garantido. As etapas dependem das decisões e autorizações sugeridas no PDF: pontos focais, organograma, bases, permissão e homologação de indicadores.
