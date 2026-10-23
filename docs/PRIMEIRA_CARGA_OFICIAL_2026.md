# Primeiro ciclo de dados oficiais — SNP 2026

**Status: primeira leitura e consolidação preliminar concluídas; publicação institucional NÃO homologada.**

## Arquivos recebidos em 23/10/2026

1. Série histórica de execução 2019–2026 (abas Resumo, Detalhado, auxiliar e Observação).
2. Dados secundários de autorização/repasse (contém números de processos e referências de autorização).
3. Execução orçamentária LOA+RAP SNP 2026 (linhas de detalhamento e total).
4. Processos pendentes (inclui demandas orçamentárias e financeiras com referências operacionais).

**Nenhum desses arquivos e nenhum indicador real derivado devem ser publicados em** `web/`, Vercel, GitHub ou GitHub Pages sem classificação e autorização explícitas. Os indicadores oficiais estão em relatório e planilha locais separados, para circulação no canal corporativo autorizado.

## Regras técnicas aprovadas apenas para conferência

- Na planilha 2026, usar somente as linhas analíticas, excluindo a linha final `Total` para evitar dupla contagem.
- Doze campos monetários são reconciliados contra a linha total da mesma planilha antes de agregar.
- Separar pagamento LOA, pagamento RAP, valor de RAP inscrito e RAP a pagar.
- Na série histórica, usar somente a linha anual `TOTAL ... 20xx`, sem somar novamente PAC/DEMAIS.
- Pendências são registros de acompanhamento, não pagamentos efetuados ou obrigações vencidas presumidas.
- Classificação provisória é **USO INTERNO**, com revisão obrigatória pelo gestor da informação.

## Achados que impedem publicação automática

- Divergência material de RAP pago entre resumo histórico e aba auxiliar no exercício de 2020.
- Divergência na dotação atualizada do exercício de 2022 entre duas abas históricas.
- Diferença residual de empenhado entre dois arquivos para o exercício de 2026.
- Código de ação divergente entre uma referência secundária e o detalhamento 2026.
- Diferença entre valor autorizado e soma dos componentes LOA+RAP na base secundária.
- Linha de subtotal e linha de demanda sem número de processo nas pendências.
- Fórmulas de divisão por zero em linhas auxiliares do histórico.
- Falta de data de corte declarada na planilha detalhada e falta de classificação explícita para divulgação.

**As diferenças exatas estão documentadas no relatório restrito local.** Não alterar valores da origem por inferência.

## Rotina reproduzível em estação corporativa autorizada

Executar `scripts/analyze_official_workbooks_local.py` apontando os quatro arquivos e uma pasta institucional fora do repositório. Requer `artifact_tool`; a ferramenta não acessa internet, não escreve dados em `web/` e não aplica reconciliação contábil nem homologação.

## Próximas decisões com a área gestora

1. Designar homologador orçamentário e financeiro, confirmar o corte dos dados.
2. Decidir qual aba/extrato tem prevalência em cada divergência e registrar evidência.
3. Validar chaves programa, ação, PO, PTRES, UO, GND e fonte para indicadores.
4. Atualizar as demandas pendentes diretamente nos sistemas de origem.
5. Autorizar formalmente a classificação: dados agregados liberados para divulgação? Dados operacionais devem permanecer restritos?
6. Indicar ambiente institucional autorizado (SharePoint/Teams com permissão por usuário, por exemplo) para circular resultados reais.
7. Depois, implantar ingestão autenticada, banco auditável e revisão de segurança antes de publicação automática.

**Até as decisões acima,** https://bi-snp-360.vercel.app/ permanece exclusivamente sintético, como já advertido na interface.
