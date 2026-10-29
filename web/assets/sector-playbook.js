/* BI SNP 360° — suplemento técnico demonstrativo. Nenhum dado institucional é incluído. */
(() => {
  'use strict';
  const TECH = {
    'Direção Estratégica': {
      unit:'Gabinete SNP · referência preliminar', decision:'Quais prioridades exigem deliberação da direção e qual é a próxima providência?',
      questions:['Prioridades sem decisão registrada','Pendências com impacto intersetorial','Encaminhamentos com prazo crítico'],
      checks:['Identificador único da demanda e ato de origem','Responsável, prazo e estado da deliberação','Evidência de decisão e data da última atualização'],
      outputs:['Mapa de prioridades','Fila de decisões','Ata sintética de encaminhamentos'],cadence:'Semanal'
    },
    'Orçamento e Finanças': {
      unit:'SNP / área orçamentária · a confirmar',decision:'Quanto há disponível, quanto foi executado e quais divergências exigem apuração?',
      questions:['Dotação atualizada e saldo disponível','Empenhado, liquidado e pago no exercício','RAP inscrito, pago e cancelado por exercício'],
      checks:['Conciliar LOA e execução por exercício, UO, ação e PO','Separar pagamento LOA de pagamento RAP; evitar duplicidade','Registrar corte, estornos, unidades e totalizações da origem'],
      outputs:['Quadro LOA × execução','Conciliação LOA/RAP','Painel de saldos e divergências'],cadence:'Mensal e por atualização recebida'
    },
    'Investimentos e Obras': {
      unit:'DGMP · referência preliminar',decision:'Quais entregas estão em risco de prazo, custo ou escopo?',
      questions:['Carteira por empreendimento, fase e modalidade','Execução física × financeira','Desvios de prazo, aditivos e próximos marcos'],
      checks:['Chave única de empreendimento, contrato e fonte','Data-base física e financeira comparáveis','Justificativa e evidência para cada desvio'],
      outputs:['Carteira priorizada','Curva físico-financeira','Registro de marcos e riscos'],cadence:'Mensal'
    },
    'Outorgas e Contratos': {
      unit:'DNOP · referência preliminar',decision:'Quais processos e obrigações contratuais requerem acompanhamento?',
      questions:['Projetos por estágio e tipo de outorga','Contratos vigentes e prazos relevantes','Obrigações e marcos a vencer'],
      checks:['Identificador estável do projeto e instrumento','Situação e vigência conforme a fonte oficial','Responsável por obrigação, vencimento e evidência'],
      outputs:['Funil de outorgas','Agenda de obrigações','Visão de contratos por fase'],cadence:'Semanal / mensal'
    },
    'Planejamento Portuário': {
      unit:'CG de Planejamento Portuário · a validar',decision:'Onde estão as revisões prioritárias e as lacunas de capacidade?',
      questions:['Planos e PDZ vigentes','Agenda de revisões e estudos','Demanda projetada × capacidade portuária'],
      checks:['Versão e vigência de cada plano','Base e hipótese da projeção de demanda','Unidade de medida, horizonte e ato de aprovação'],
      outputs:['Mapa de planos','Calendário de revisões','Matriz capacidade × demanda'],cadence:'Trimestral'
    },
    'Governança Portuária': {
      unit:'CG de Governança Portuária · a validar',decision:'Quais compromissos pactuados estão sem comprovação de cumprimento?',
      questions:['Metas aplicáveis e atendidas','Responsabilidades e delegações','Providências de governança em atraso'],
      checks:['Metas com numerador e denominador explícitos','Exclusão fundamentada de itens não aplicáveis','Evidência, período e unidade responsável'],
      outputs:['Scorecard de metas','Mapa de compromissos','Plano de providências'],cadence:'Trimestral'
    },
    'Coordenação Institucional': {
      unit:'Gabinete / coordenações · a confirmar',decision:'Quais demandas dependem de mais de uma unidade e quem deve agir?',
      questions:['Demandas por área e responsável','Dependências entre unidades','Encaminhamentos sem retorno'],
      checks:['Uma unidade proprietária por demanda','Registro de áreas participantes e dependências','Prazo, histórico e evidência do encaminhamento'],
      outputs:['Matriz de responsabilidades','Fila intersetorial','Síntese para reunião de coordenação'],cadence:'Semanal'
    },
    'Processos e Prazos': {
      unit:'Áreas gestoras / SEI · acesso autorizado',decision:'Quais processos apresentam risco de vencimento ou paralisação?',
      questions:['Prazos a vencer e vencidos','Tempo em cada etapa','Providências pendentes e responsáveis'],
      checks:['Identificadores e permissões de consulta','Marco inicial, prazo final e regra de suspensão','Atualização de situação e histórico sem duplicações'],
      outputs:['Mapa de vencimentos','Fila de providências','Indicador de tempo de tramitação'],cadence:'Diária / semanal'
    },
    'Riscos e Controle': {
      unit:'Gabinete / controle · a confirmar',decision:'Quais riscos demandam resposta, evidência ou decisão corretiva?',
      questions:['Riscos por criticidade','Planos de ação abertos','Recomendações com prazo vencido'],
      checks:['Critérios de probabilidade e impacto declarados','Dono do risco e plano de resposta','Evidência de encerramento e revisão de criticidade'],
      outputs:['Matriz probabilidade × impacto','Plano de resposta','Registro de recomendações'],cadence:'Semanal'
    },
    'Desempenho Setorial': {
      unit:'DGMP / bases ANTAQ · a confirmar',decision:'Como evoluem movimentação, produtividade e tendências portuárias?',
      questions:['Movimentação por carga, instalação e período','Comparativos e sazonalidade','Indicadores operacionais de produtividade'],
      checks:['Escopo geográfico e classificação de carga','Unidade física e datas comparáveis','Fonte ANTAQ e revisões de séries anteriores'],
      outputs:['Série temporal','Comparativo portuário','Nota de qualidade metodológica'],cadence:'Mensal'
    },
    'Dados e Inovação': {
      unit:'CG de Inovação e Transformação Digital · a validar',decision:'Quais bases estão confiáveis e prontas para sustentar decisões?',
      questions:['Fontes catalogadas × integradas','Validação e atualização por fonte','Incidentes e pendências de qualidade'],
      checks:['Contrato de dados e responsável definido','Data de atualização, trilha e retenção','Segregação pública × acesso restrito por perfil'],
      outputs:['Catálogo de fontes','Matriz de qualidade','Plano de evolução técnica'],cadence:'Mensal'
    },
    'Relatórios Executivos': {
      unit:'SNP / consolidação transversal',decision:'Qual síntese sustenta decisões sem perder contexto ou rastreabilidade?',
      questions:['Indicadores validados por setor','Decisões propostas e responsáveis','Alertas, fontes e data de corte'],
      checks:['Não misturar exercícios ou escopos incompatíveis','Exibir ressalvas e grau de validação','Identificar versão, responsável e data de emissão'],
      outputs:['Briefing executivo','Ficha de decisão','Caderno de evidências'],cadence:'Por reunião ou atualização'
    }
  };
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const items = (values) => values.map(s => `<li>${esc(s)}</li>`).join('');
  const card = (title, list, cls='') => `<article class="tech-card ${cls}"><h3>${esc(title)}</h3><ul>${items(list)}</ul></article>`;
  function sectorTemplate(name, data){
    return `<section class="tech-section" aria-label="Ficha técnica do setor" data-tech-sector="${esc(name)}">
      <div class="tech-top"><div><div class="tech-eyebrow">MATRIZ TÉCNICA · ${esc(data.cadence)}</div><h2>O que este setor precisa acompanhar</h2><p>${esc(data.decision)}</p></div><button class="btn light" type="button" data-tech-export="${esc(name)}">↓ Ficha técnica CSV</button></div>
      <div class="tech-mini"><span><strong>Unidade proposta</strong>${esc(data.unit)}</span><span><strong>Dados no Pages</strong>Somente exemplos fictícios</span><span><strong>Homologação</strong>Dependente da fonte e do responsável</span></div>
      <div class="tech-cols">${card('Indicadores e perguntas de gestão',data.questions)}${card('Regras mínimas de conferência',data.checks)}${card('Saídas para a chefia',data.outputs,'tech-last')}</div>
      <div class="tech-flow" aria-label="Fluxo de gestão"><span>01 · Fonte</span><span>02 · Validação</span><span>03 · Indicadores</span><span>04 · Decisão</span></div>
      <p class="tech-footnote">Referência metodológica do protótipo. Nomes das unidades e regras de cálculo precisam ser confirmados no uso institucional.</p>
    </section>`;
  }
  function peoplePage(){
    return `<section class="people-panel"><div class="tech-eyebrow">GOVERNANÇA TRANSVERSAL · CADASTROS</div><h1 class="page-title">Pessoas e Equipes</h1>
    <p class="page-sub">Modelo de gestão de lotação, vínculos, designações, PGD e participação em colegiados, sem divulgar registros nominais.</p>
    <div class="tech-warning"><strong>Ambiente público demonstrativo.</strong> Nesta página não há dados reais de pessoas. A relação nominal e os documentos recebidos não são publicados no GitHub Pages.</div>
    <div class="people-kpis"><div><span>Cadastro e lotação</span><strong>—</strong><small>Registro único e vínculo temporal</small></div><div><span>Modalidades PGD</span><strong>—</strong><small>Elegibilidade e período vigentes</small></div><div><span>Designações</span><strong>—</strong><small>Titular, substituto, vacância</small></div><div><span>Colegiados</span><strong>—</strong><small>Composição e mandato</small></div></div>
    <div class="tech-cols">${card('Indicadores a estruturar',['Quantitativo por vínculo e unidade','Distribuição de lotações e cargos','Registros PGD por modalidade e vigência'])}${card('Qualidade e segurança',['Evitar contar a mesma pessoa duas vezes','Distinguir pessoa, posto e designação','Não divulgar CPF, matrícula, contatos ou remuneração'])}${card('Entregas gerenciais',['Quadro sintético de equipes','Mapa de designações e substituições','Agenda de participação em colegiados'])}</div>
    <div class="people-note"><h2>Como as bases se relacionam</h2><p>Cadastro de pessoas → vínculo e lotação → designações → PGD → participação em comissões e colegiados. Cada relação deve usar chaves verificadas, vigência e fonte para evitar junções apenas por semelhança de nomes.</p></div>
    <div class="tech-flow"><span>Cadastro</span><span>Vínculo</span><span>Lotação</span><span>Governança</span></div>
    <button class="btn light" data-view="home" type="button">← Voltar à visão geral</button></section>`;
  }
  function homePerspectives(){
    return `<section class="perspective-board" aria-label="Perspectivas do BI"><div class="tech-eyebrow">QUATRO PERSPECTIVAS DA GESTÃO</div><div class="perspective-grid">
    <div><span>01 / DIREÇÃO</span><strong>Decidir</strong><small>Prioridades, deliberações e metas</small></div>
    <div><span>02 / GESTÃO</span><strong>Executar</strong><small>Recursos, contratos e entregas</small></div>
    <div><span>03 / COORDENAÇÃO</span><strong>Responsabilizar</strong><small>Unidades, prazos e dependências</small></div>
    <div><span>04 / CONTROLE</span><strong>Corrigir</strong><small>Riscos, alertas e evidências</small></div></div></section>`;
  }
  function enhance(){
    const nav = document.getElementById('navigation');
    if(nav && !nav.querySelector('[data-tech-nav]')){
      nav.insertAdjacentHTML('beforeend',`<div class="nav-section"><div class="nav-caption">PESSOAS E ESTRUTURA</div><button type="button" class="nav-link" data-tech-nav="pessoas"><span class="nav-icon">♙</span><span>Pessoas e Equipes</span></button></div>`);
    }
    const content = document.getElementById('content');
    if(!content || content.querySelector('[data-tech-sector], .people-panel'))return;
    const h1=content.querySelector('h1.page-title');
    const title=h1?.textContent?.trim();
    if(title && Object.prototype.hasOwnProperty.call(TECH,title)){
      const warning=content.querySelector('.notice.warning');
      if(warning) warning.insertAdjacentHTML('beforebegin',sectorTemplate(title,TECH[title]));
      else content.insertAdjacentHTML('beforeend',sectorTemplate(title,TECH[title]));
    }else if(title==='Visão geral da Secretaria'&&!content.querySelector('.perspective-board')){
      content.querySelector('.overview-hero')?.insertAdjacentHTML('afterend',homePerspectives());
    }
  }
  function downloadSector(name){
    const d=TECH[name];if(!d)return;
    const csv = [['Campo','Conteúdo'],['Módulo',name],['Unidade proposta',d.unit],['Decisão',d.decision],['Periodicidade',d.cadence],...d.questions.map(s=>['Indicador / pergunta',s]),...d.checks.map(s=>['Validação',s]),...d.outputs.map(s=>['Produto',s])];
    const q=s=>'"'+String(s).replace(/^[\s]*[=+@-]/,m=>"'"+m).replaceAll('"','""')+'"';
    const blob=new Blob(['\ufeff'+csv.map(row=>row.map(q).join(';')).join('\r\n')],{type:'text/csv;charset=utf-8'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='BI_SNP_360_Ficha_Tecnica_'+name.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Za-z0-9]/g,'_')+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
  }
  document.addEventListener('click',ev=>{
    const nav=ev.target.closest('[data-tech-nav]');
    if(nav){ev.preventDefault(); const content=document.getElementById('content');if(!content)return;content.innerHTML=peoplePage();document.getElementById('breadcrumb').textContent='Pessoas e Equipes';document.title='Pessoas e Equipes | BI SNP 360°';document.getElementById('sidebar')?.classList.remove('open');try{history.replaceState({},'',location.pathname+location.search+'#pessoas')}catch{}window.scrollTo(0,0);nav.classList.add('active');return;}
    const button=ev.target.closest('[data-tech-export]'); if(button){ev.preventDefault();downloadSector(button.dataset.techExport);}
  },true);
  let scheduled=false;
  const observer=new MutationObserver(()=>{if(scheduled)return;scheduled=true;queueMicrotask(()=>{scheduled=false;enhance()})});
  const mount=()=>{const root=document.getElementById('content');const nav=document.getElementById('navigation');if(!root||!nav)return;observer.observe(root,{childList:true,subtree:false});observer.observe(nav,{childList:true,subtree:false});enhance();};
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);else mount();
})();
