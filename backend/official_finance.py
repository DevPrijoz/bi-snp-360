"""Funções puras de conciliação preliminar para cargas autorizadas, sempre fora da demonstração pública.

NÃO conecta sistemas de governo. NÃO homologa fontes. NUNCA carregar datasets reais em web/.
Recebe matrizes já extraídas localmente; use scripts/analyze_official_workbooks_local.py.
"""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import re

MONETARY_FIELDS = (
    'dot_inicial', 'dot_atualizada', 'destaque_concedido', 'credito_disponivel',
    'credito_indisponivel', 'empenhado', 'liquidado', 'pago_loa',
    'rap_bloqueado', 'rap_inscrito', 'rap_pago', 'rap_a_pagar'
)

class InvalidFinancialSource(ValueError):
    """Planilha com estrutura/valores incompatíveis com contrato preliminar."""


def as_amount(value, *, context='valor') -> Decimal:
    if value is None or value == '':
        return Decimal(0)
    if isinstance(value, bool):
        raise InvalidFinancialSource(f'{context}: valor booleano inválido')
    if isinstance(value, str):
        # No guesswork for local currency formatting: this is not a locale parser.
        raise InvalidFinancialSource(f'{context}: texto em campo monetário, requer validação do layout')
    try:
        amount=Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise InvalidFinancialSource(f'{context}: valor numérico inválido') from None
    if not amount.is_finite():
        raise InvalidFinancialSource(f'{context}: NaN/Infinito não permitido')
    return amount


def extract_execution_rows(matrix: list[list]) -> tuple[list[dict], dict, dict]:
    """Layout da aba LOA+RAP SNP 2026: 4 cabeçalhos, linhas analíticas, 'Total' final.

    Colunas monetárias baseadas em índice 21..32 (0-based). Não mistura estoques de RAP com pagamentos.
    Devolve folhas, linha total e diferença de conciliação exata por campo.
    """
    if len(matrix) < 6 or len(matrix[3]) < 33:
        raise InvalidFinancialSource('Layout insuficiente: esperados pelo menos 33 campos e 4 linhas de cabeçalho')
    if str(matrix[-1][0]).strip().lower() != 'total':
        raise InvalidFinancialSource('Última linha deve ser TOTAL. Não somar total novamente como registro.')
    result=[]
    for idx, row in enumerate(matrix[4:-1], start=5):
        if len(row) < 33:
            raise InvalidFinancialSource(f'Linha {idx}: menos de 33 colunas')
        if not str(row[0] or '').strip():
            raise InvalidFinancialSource(f'Linha {idx}: setor ausente')
        rec={'source_row':idx,'sector':str(row[0]).strip(),
             'action':str(row[7] or '').strip(),'plan':str(row[9] or '').strip(),
             'source':str(row[20] or '').strip()}
        for j,key in enumerate(MONETARY_FIELDS,21):
            rec[key]=as_amount(row[j],context=f'linha {idx}/{key}')
        result.append(rec)
    if not result:
        raise InvalidFinancialSource('Nenhuma linha analítica para processar')
    total={key:as_amount(matrix[-1][j],context=f'total/{key}') for j,key in enumerate(MONETARY_FIELDS,21)}
    differences={key:sum((r[key] for r in result),Decimal(0))-total[key] for key in MONETARY_FIELDS}
    return result,total,differences


def summarize(rows: list[dict], *, by: str | None = None) -> dict:
    """Soma valores numéricos; não acrescenta RAP inscrito à despesa paga."""
    aggregate=defaultdict(lambda:{field:Decimal(0) for field in MONETARY_FIELDS})
    for row in rows:
        key=row.get(by,'all') if by else 'all'
        for field in MONETARY_FIELDS:
            aggregate[key][field]+=row[field]
    return dict(aggregate)


def safe_ratio(num: Decimal, den: Decimal) -> Decimal | None:
    return (num / den) if den else None


def extract_historical_totals(matrix: list[list], start_year=2019, end_year=2026) -> list[dict]:
    """Aceita somente linhas com TOTAL ... AAAA; não agrega detalhamento ou subtotal PAC/DEMAIS."""
    found={}
    for idx,row in enumerate(matrix, start=1):
        if not row or not isinstance(row[0],str):
            continue
        text=row[0].strip().upper()
        matched=re.search(r'^TOTAL\s+.*\b(20\d\d)\b$',text)
        if matched:
            year=int(matched.group(1))
            if not start_year<=year<=end_year:continue
            if year in found:raise InvalidFinancialSource(f'Exercício {year}: mais de uma linha total')
            if len(row)<14:raise InvalidFinancialSource(f'Histórico linha {idx}: menos de 14 colunas')
            found[year]={'year':year,'row':idx,'updated':as_amount(row[3]),
                'committed':as_amount(row[5]),'liquidated':as_amount(row[7]),
                'paid_loa':as_amount(row[8]),'rap_inscribed':as_amount(row[10]),
                'rap_paid':as_amount(row[11]),'total_paid':as_amount(row[13])}
    years=set(range(start_year,end_year+1))
    if set(found)!=years:raise InvalidFinancialSource(f'Exercícios não encontrados: {sorted(years-set(found))}')
    return [found[y] for y in sorted(found)]


def identify_pending(matrix: list[list], group: str) -> list[dict]:
    """Localiza linhas de demanda sem somar cabeçalhos ou subtotais como itens novos."""
    items=[]
    for idx,row in enumerate(matrix,1):
        if len(row)<4:continue
        label=str(row[2] or '').strip()
        if not label or any(word in label.casefold() for word in ['total da ordem bancária','ação / plano orçamentário']):
            continue
        value=row[3]
        if not isinstance(value,(int,float,Decimal)):
            continue
        items.append({'group':group,'source_row':idx,'process':str(row[1] or '').strip(),
                      'description':label,'value':as_amount(value)})
    return items
