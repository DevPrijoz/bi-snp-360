import pytest
from decimal import Decimal
from backend.official_finance import (
    as_amount,extract_execution_rows,extract_historical_totals,InvalidFinancialSource,
    summarize,safe_ratio,identify_pending,MONETARY_FIELDS,
)

def fixture(detail=2):
    h=[[None]*33 for _ in range(4)]; rows=[]
    for i in range(detail):
        r=[None]*33;r[0]='DGMP' if i%2==0 else 'DNOP';r[7]='218T' if i%2==0 else '00V4'
        r[9]='0001';r[20]='1000';r[22]=100; r[26]=25+i;r[28]=10+i; r[30]=50+i;r[31]=15+i;r[32]=35
        rows.append(r)
    total=[None]*33;total[0]='Total'
    for j in range(21,33):total[j]=sum((row[j] or 0) for row in rows)
    return h+rows+[total]

def test_exact_reconciliation():
    rows,total,diff=extract_execution_rows(fixture());assert len(rows)==2
    assert all(x==0 for x in diff.values());assert total['dot_atualizada']==200

def test_reject_double_counting_total():
    x=fixture();x[-1][0]='subtotal'
    with pytest.raises(InvalidFinancialSource):extract_execution_rows(x)

def test_detect_one_cent_difference():
    x=fixture();x[-1][26]+=0.01
    assert extract_execution_rows(x)[2]['empenhado']==Decimal('-0.01')

def test_invalid_text_is_not_guessed():
    x=fixture();x[4][22]='1.234,56'
    with pytest.raises(InvalidFinancialSource):extract_execution_rows(x)

@pytest.mark.parametrize('n',[float('inf'),float('nan'),True,'#DIV/0!'])
def test_invalid_money_rejected(n):
    with pytest.raises(InvalidFinancialSource):as_amount(n)

def test_missing_money_is_not_a_payment():
    assert as_amount(None)==0
    assert safe_ratio(Decimal(1),Decimal(0)) is None

def test_sector_rollup_separated():
    rows,total,_=extract_execution_rows(fixture(3));sets=summarize(rows,by='sector')
    assert sets['DGMP']['dot_atualizada']==200
    assert sets['DNOP']['dot_atualizada']==100
    assert sets['DGMP']['pago_loa']==22
    assert sets['DGMP']['rap_pago']==32

def test_historical_uses_only_annual_total():
    rows=[]
    for year in range(2019,2027):
        rec=[None]*14;rec[0]=f'TOTAL DEMAIS + PAC {year}';rec[3]=100
        rec[5]=80;rec[7]=20;rec[8]=15;rec[10]=60;rec[11]=10;rec[13]=25
        rows.extend([rec,[f'PAC {year}']+[100]*13])
    years=extract_historical_totals(rows)
    assert len(years)==8 and years[0]['year']==2019 and years[-1]['year']==2026
    assert sum(x['total_paid'] for x in years)==200

def test_duplicate_annual_total_fails():
    rows=[]
    for year in range(2019,2027):
        r=[None]*14;r[0]=f'TOTAL DEMAIS {year}';rows.append(r)
    rows.append(rows[-1])
    with pytest.raises(InvalidFinancialSource):extract_historical_totals(rows)

def test_pending_subtotal_excluded():
    rows=[[None]*8 for _ in range(4)]
    rows[0][2]='Ação / Plano Orçamentário / Descrição'; rows[1][2]='Reforma';rows[1][3]=250
    rows[2][2]='Total da Ordem Bancária';rows[2][3]=250
    rows[3][2]='Energia Solar';rows[3][3]=90
    out=identify_pending(rows,'Ordenador')
    assert len(out)==2 and sum(v['value'] for v in out)==340
