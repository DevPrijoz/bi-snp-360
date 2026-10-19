# Segurança, acessos e privacidade

## Diretriz inegociável

O repositório GitHub e a interface estática NÃO devem conter informação interna/restrita do SEI, SIAFI, dados pessoais, credenciais, segredos, tokens, caches privados, relatórios protegidos ou arquivos de origem. GitHub Pages **não substitui** autenticação nem RBAC no servidor.

## Estado real da segurança

| Controle | Situação |
|---|---|
| Dados falsos explicitamente identificados | Implementado na demo pública |
| API sem dados internos enquanto IdP ausente | Implementado (503 para acessos internos) |
| Validação de token OIDC RS256, aud, iss, exp, sub, iat | Código implementado; precisa de IdP institucional |
| Checagem de unidade/permissão por objeto | Implementado no piloto, com testes |
| Segregação autor/homologador | Implementado no piloto |
| Transparência redigida e publicação explícita | Implementado no piloto |
| Trilha de alterações | Implementado em banco do piloto; não é log WORM |
| Criptografia/TLS, backup, auditoria centralizada, DLP | Dependem de operação com TI |
| Política de acesso às CGs, retenção e LGPD | Depende de decisão institucional |
| Pentest, hardening e homologação | Pendentes |

## Princípio de menor privilégio

Todas as ações internas exigem `Authorization: Bearer <JWT>` assinado pelo IdP. Claims esperadas (fornecimento e autorização institucional a definir):

```json
{
  "sub": "identidade-corporativa",
  "iss": "https://idp.institucional.exemplo",
  "aud": "snp360-api",
  "exp": 1790000000,
  "iat": 1780000000,
  "unit_codes": ["GAB"],
  "roles": ["equipe_tecnica"],
  "permissions": ["records:read", "records:write"]
}
```

Permissões distintas: `records:read`, `records:read:all`, `records:write`, `records:write:all`, `records:homologate`, `records:publish`, `records:restricted:read`, `records:restricted:write`, `records:restricted:homologate`, `records:restricted:publish`, `data:import`, `audit:read`. A concessão de cada claim depende de mapeamento formal e gestor de identidade; a API **não presume** autorização por cargo/título isolado.

Para que `records:homologate` ou `records:publish` funcionem fora das unidades atribuídas, também deve ser fornecida a permissão adicional `records:homologate:all` ou `records:publish:all`. **Não se deve criar essas claims sem autorização formal.**

## Checklist antes de produção

- [ ] Aprovar arquitetura, homologar rede, ingress HTTPS/HSTS e serviço de identidade.
- [ ] Confirmar SIORG das CGs e quem pode ver/editar/homologar/publicar/exportar.
- [ ] Implementar frontend institucional autenticado, política de sessão e renovação de tokens.
- [ ] Integrar banco institucional, backups cifrados, migrações versionadas e HA.
- [ ] Implementar rate limiting, revisão de payload, varredura de dependências, scans SAST/DAST e testes de penetração.
- [ ] Validar LGPD, classificação, retenção, descarte, minimização, registro de incidente e logs sem PII.
- [ ] Homologar todos os conectores, chaves, regras de reconciliação e campos públicos.
- [ ] Testar publicação para evitar vazamento indireto por agregação, link, exportação ou erro.
- [ ] Aprovar o catálogo, regras de semáforo e plano de continuidade.

Os endereços de evidência nos registros são referências de acesso controlado nos sistemas de origem, nunca documentos públicos automaticamente.
