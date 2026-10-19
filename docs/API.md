# Referência API (piloto)

**Base:** `http://localhost:8000` no desenvolvimento. Swagger: `/api/docs`. Internos exigem OIDC/JWT válido; não há usuário de demonstração. `GET /healthz` informa disponibilidade do processo, não do banco/IdP.

| Método | Endpoint | Permissão | Ação |
|---|---|---|---|
| GET | `/healthz` | aberta | status da API |
| GET | `/api/v1/public/records` | aberta | somente registros publicados e homologados, DTO minimizado |
| GET | `/api/v1/me` | token válido | claims de identidade |
| GET | `/api/v1/records` | `records:read` | lista autorizada por unidade e classe |
| GET | `/api/v1/records/{id}` | `records:read` | detalhe autorizado |
| POST | `/api/v1/records` | `records:write` | cria registro, sempre pendente e não publicado |
| PATCH | `/api/v1/records/{id}` | `records:write` | atualiza campos controlados e invalida homologação anterior |
| POST | `/api/v1/records/{id}/homologate` | `records:homologate` | valida com evidência e aprovador distinto do autor |
| POST | `/api/v1/records/{id}/publish` | `records:publish` | publica só classe público homologada |
| POST | `/api/v1/records/{id}/closure-request` | `records:write` | exige providência e evidência |
| POST | `/api/v1/records/{id}/closure-approve` | `records:homologate` | homologação de encerramento por pessoa distinta |
| GET | `/api/v1/alerts` | `records:read` | semáforo por validação/criticidade/prazo |
| POST | `/api/v1/import/csv` | `data:import` + unidade | dry run por padrão, commit controlado e chave externa única |
| GET | `/api/v1/audit/{id}` | `records:read` + `audit:read` | trilha do registro autorizado |

### Exemplo de criação (somente laboratório autorizado)

```bash
curl -X POST http://localhost:8000/api/v1/records \
  -H "Authorization: Bearer $TOKEN_VALIDO_DO_IDP" \
  -H 'Content-Type: application/json' \
  -d '{"external_key":"EXEMPLO-001","module":"processos","title":"Acompanhamento de exemplo","object_goal":"Descrição da meta ilustrativa","unit_code":"GAB","information_unit":"GAB","execution_responsible":"Equipe técnica fictícia","status":"pendente","risk":"dados_pendentes","due_date":"2026-12-02","next_action":"Registrar justificativa e documento","source_id":"SEI","source_record_id":"ID-EXEMPLO-001","data_cutoff":"2026-10-19","classification":"interno"}'
```

**Não colar tokens reais em chats, arquivos, prints, issue ou repositórios.**

### Validação de CSV

```bash
curl -X POST http://localhost:8000/api/v1/import/csv \
 -H "Authorization: Bearer $TOKEN_VALIDO_DO_IDP" \
 -F "file=@scripts/exemplo_importacao.csv" \
 -F 'dry_run=true'
```

O backend não gera nem valida o dicionário final de execução orçamentária. Isso depende dos contratos SIOP/SIAFI e documentação posterior.
