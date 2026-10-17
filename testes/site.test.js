// Testes do site (15/10/2026): chave do formulário, conversão do Google Ads, WhatsApp flutuante, formulário em 2 etapas e
// troca do nome na página Sobre. Roda as páginas de public/ no Chromium do Playwright, sem rede: os webhooks do n8n e o
// gtag.js são simulados e nada é enviado.
//
//   NODE_PATH=$(npm root -g) node testes/site.test.js
//
// Se o repositório antere-automacao estiver ao lado (../antere-automacao), os corpos enviados ao n8n também passam pelas
// regras do servidor (n8n/lib/formulario_site.js).
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const PUB = path.join(__dirname, '..', 'public');
const SRC = path.join(__dirname, '..', '_src');
const BASE = 'https://www.antere.com.br';
const E1 = 'https://raregoat-n8n.cloudfy.live/webhook/site-proposta-etapa1';
const E2 = 'https://raregoat-n8n.cloudfy.live/webhook/site-proposta-etapa2';
const DADOS = 'https://raregoat-n8n.cloudfy.live/webhook/form-proposta-dados';
const SEND_TO = 'AW-18479570694/4-TPCPzV6ZcdEIa-3-tE';
const UTM = '?utm_source=google&utm_medium=cpc&utm_campaign=pagamento_integrado';
const PAGINAS = ['index.html', 'calculadora.html', 'como-funciona.html', 'contato.html', 'sobre.html', 'solucoes.html', '404.html'];
const LEGAIS = ['legal/privacidade.html', 'legal/termos.html', 'legal/exclusao-dados.html'];
const CNPJ = '11.222.333/0001-81';
let lib = null;
try { lib = require(path.join(__dirname, '..', '..', 'antere-automacao', 'n8n', 'lib', 'formulario_site.js')); } catch (e) { lib = null; }
// 17/10: os produtos passaram para a etapa 1 (contrato publicado pela Operação às 10h50). Só confere os corpos com a lib que já tiver o
// contrato novo (aceita a etapa 1 com produtos); com a lib antiga, essa conferência fica de fora.
const libNova = !!(lib && lib.validarEtapa1({ nome: 'Ana Lima', whatsapp: '11987654321', email: 'a@b.com.br', cnpj: '11222333000181', caixas: 1, produtos: ['tef', 'c6pay'], consentimento_lgpd: true }).ok);
// 18/10: sem TEF, o site não manda caixas (etapa 1) nem sistema_pdv/lojas (etapa 2). Só confere esses corpos com a lib que já aceitar isso.
const libSemTef = !!(libNova && lib.validarEtapa1({ nome: 'Ana Lima', whatsapp: '11987654321', email: 'a@b.com.br', cnpj: '11222333000181', produtos: ['link'], consentimento_lgpd: true }).ok);
const confereLib = (corpo, produtos) => libNova && ((produtos || corpo.produtos || []).includes('tef') || libSemTef);

let ok = 0, falhas = 0;
async function t(nome, f) {
  try { await f(); ok++; console.log('ok - ' + nome); } catch (e) { falhas++; console.log('FALHOU - ' + nome + '\n', e && e.stack || e); }
}

// Contexto com o site servido de public/ e tudo de fora bloqueado. chave: undefined = site-config.js real; true/false = simulado.
async function contexto(b, { chave, cookies, webhooks, dados, viewport } = {}) {
  const ctx = await b.newContext({ viewport: viewport || { width: 1280, height: 900 } });
  const reqs = [], gtagJs = [];
  await ctx.route('**/*', async (r) => {
    const u = new URL(r.request().url());
    if (u.origin === BASE) {
      if (u.pathname === '/site-config.js' && (chave !== undefined || cookies !== undefined)) return r.fulfill({ body: 'window.ANTERE_FORM_NOVO = ' + (chave === true) + ';\nwindow.ANTERE_COOKIES = ' + (cookies === true) + ';', contentType: 'application/javascript' });
      let f = u.pathname.slice(1) || 'index.html';
      const arq = path.join(PUB, f);
      if (!fs.existsSync(arq) || fs.statSync(arq).isDirectory()) return r.fulfill({ status: 404, body: fs.readFileSync(path.join(PUB, '404.html')), contentType: 'text/html' });
      const tipo = f.endsWith('.js') ? 'application/javascript' : f.endsWith('.png') ? 'image/png' : 'text/html';
      return r.fulfill({ body: fs.readFileSync(arq), contentType: tipo });
    }
    if (u.hostname === 'www.googletagmanager.com') { gtagJs.push(r.request().frame().url()); return r.fulfill({ body: '', contentType: 'application/javascript' }); }
    if (u.href.startsWith(DADOS)) {
      reqs.push({ url: u.href, metodo: r.request().method() });
      const resp = dados ? dados(u.searchParams) : { status: 404, body: { ok: false } };
      return r.fulfill({ status: resp.status, body: JSON.stringify(resp.body), contentType: 'application/json' });
    }
    if (u.href.startsWith(E1) || u.href.startsWith(E2)) {
      const corpo = JSON.parse(r.request().postData() || '{}'); reqs.push({ url: u.href, corpo });
      const resp = webhooks ? webhooks(u.href, corpo) : { status: 503, body: { ok: false, erro: 'indisponivel' } };
      return r.fulfill({ status: resp.status, body: JSON.stringify(resp.body), contentType: 'application/json' });
    }
    return r.abort();
  });
  return { ctx, reqs, gtagJs };
}
const eventos = (p, nome) => p.evaluate((n) => (window.dataLayer || []).filter(a => a[0] === 'event' && a[1] === n).map(a => a[2] || {}), nome);
const semNavegar = (p) => p.evaluate(() => document.addEventListener('click', e => { if (e.target.closest('a')) e.preventDefault(); }));
const hrefsProposta = (p) => p.$$eval('a', as => as.map(a => a.href).filter(h => /\/form\/proposta|proposta\.html/.test(h)));

(async () => {
  const b = await chromium.launch();

  // ---------------- chave desligada (o estado publicado) ----------------
  await t('site-config.js publicado com a chave do formulário desligada (17/10/2026, 17h50: pedido não encontrado na etapa 2)', async () => {
    const s = fs.readFileSync(path.join(PUB, 'site-config.js'), 'utf8');
    assert.match(s, /^window\.ANTERE_FORM_NOVO = false;/m);
  });
  await t('o HTML de public/ não tem link fixo para o formulário novo (sem JavaScript, os botões caem no formulário antigo; quem troca é a chave)', async () => {
    for (const f of [...PAGINAS, ...LEGAIS, 'proposta.html']) {
      const h = fs.readFileSync(path.join(PUB, f), 'utf8');
      assert.ok(!/<a\b[^>]*href="[^"]*proposta\.html/.test(h), f);
    }
  });
  await t('chave desligada (o site-config.js publicado): nenhum botão aponta para o formulário novo; 20 links seguem em /form/proposta com UTM e ref; 1 conversão por clique', async () => {
    const { ctx } = await contexto(b, { chave: false }); let total = 0;
    for (const pg of PAGINAS) {
      const p = await ctx.newPage(); await p.goto(BASE + '/' + pg + UTM); await semNavegar(p);
      assert.strictEqual(await p.evaluate(() => window.ANTERE_FORM_NOVO), false, pg);
      const hs = await hrefsProposta(p);
      assert.ok(hs.length >= 2, pg);
      for (const h of hs) {
        assert.ok(!/proposta\.html/.test(h), pg + ' ' + h);
        const u = new URL(h); assert.strictEqual(u.origin + u.pathname, 'https://raregoat-n8n.cloudfy.live/form/proposta', h);
        assert.strictEqual(u.searchParams.get('ref'), 'site_institucional'); assert.strictEqual(u.searchParams.get('utm_campaign'), 'pagamento_integrado');
      }
      const ls = p.locator('a[href*="/form/proposta"]:visible'), n = await ls.count();
      for (let i = 0; i < n; i++) { const a0 = (await eventos(p, 'conversion')).length; await ls.nth(i).click(); assert.strictEqual((await eventos(p, 'conversion')).length - a0, 1, pg + ' link ' + i); }
      assert.ok((await eventos(p, 'conversion')).every(e => e.send_to === SEND_TO));
      total += hs.length; await p.close();
    }
    assert.strictEqual(total, 20);
    await ctx.close();
  });
  await t('chave desligada (simulada): /proposta.html leva ao formulário antigo, com as UTM', async () => {
    const { ctx } = await contexto(b, { chave: false }); const p = await ctx.newPage(); let destino = null;
    await p.route('https://raregoat-n8n.cloudfy.live/form/proposta**', r => { destino = r.request().url(); r.abort(); });
    await p.goto(BASE + '/proposta.html' + UTM).catch(() => {}); await p.waitForTimeout(300);
    assert.ok(destino, 'não redirecionou');
    const u = new URL(destino); assert.strictEqual(u.searchParams.get('ref'), 'site_institucional'); assert.strictEqual(u.searchParams.get('utm_source'), 'google');
    await ctx.close();
  });

  // ---------------- chave ligada (simulada) ----------------
  await t('chave ligada (simulada): os 20 links vão para /proposta.html com UTM e ref, e o clique não conta conversão', async () => {
    const { ctx } = await contexto(b, { chave: true }); let total = 0;
    for (const pg of PAGINAS) {
      const p = await ctx.newPage(); await p.goto(BASE + '/' + pg + UTM); await semNavegar(p);
      const hs = await hrefsProposta(p);
      for (const h of hs) { const u = new URL(h); assert.strictEqual(u.pathname, '/proposta.html', h); assert.strictEqual(u.searchParams.get('ref'), 'site_institucional'); assert.strictEqual(u.searchParams.get('utm_medium'), 'cpc'); }
      const ls = p.locator('a[href*="proposta.html"]:visible'), n = await ls.count();
      for (let i = 0; i < n; i++) await ls.nth(i).click();
      assert.strictEqual((await eventos(p, 'conversion')).length, 0, pg);
      total += hs.length; await p.close();
    }
    assert.strictEqual(total, 20);
    await ctx.close();
  });

  // ---------------- formulário (?previa=1, webhooks simulados) ----------------
  const soPdvet = (c) => Array.isArray(c.produtos) && c.produtos.length === 1 && c.produtos[0] === 'pdvet';
  const ordem = ['tef', 'c6pay', 'link', 'pdvet'], adicional = (c) => !soPdvet(c) && (c.produtos || []).includes('pdvet') ? { interesse_adicional: ['pdvet'], url_pdvet: 'https://portal.pdvet.com.br/cadastro' } : {};
  const etapa1Ok = (empresa) => (url, c) => url === E1
    ? (soPdvet(c) ? { status: 200, body: { ok: true, lead_id: 'a'.repeat(24), pedido_token: '', proximo: 'pdvet', url: 'https://portal.pdvet.com.br/cadastro', empresa } }
      : { status: 200, body: { ok: true, lead_id: 'a'.repeat(24), pedido_token: 'b'.repeat(32), proximo: 'etapa2', produtos: ordem.filter(x => (c.produtos || []).includes(x)), empresa, ...adicional(c) } })
    : { status: 200, body: { ok: true, status: 'proposta_enviada', email: c.lead_id ? 'maria@empresa.com.br' : '', escalonar: c.faixa_link === 'acima_10000' } };
  // produtos: lista de tef, c6pay, link e pdvet ('c6pay' sozinho = ['c6pay'])
  async function preencheE1(p, produtos) {
    await p.fill('#f-nome', 'Maria da Silva'); await p.type('#f-whatsapp', '11987654321'); await p.fill('#f-email', 'maria@empresa.com.br');
    await p.type('#f-cnpj', CNPJ.replace(/\D/g, ''));
    for (const v of [].concat(produtos)) await p.check('input[name=produtos][value=' + v + ']');
    if (await p.isVisible('#f-caixas')) await p.fill('#f-caixas', '3');
    await p.check('#f-lgpd');
  }
  const EMP = { cnpj_confirmado: true, razao_social: 'EMPRESA EXEMPLO LTDA', cidade: 'São Paulo', uf: 'SP' };

  await t('formulário: validação na tela antes de enviar (vazio e CNPJ com dígito errado)', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1');
    await p.click('#b1');
    for (const c of ['nome', 'whatsapp', 'email', 'cnpj', 'produtos', 'consentimento_lgpd']) assert.ok((await p.textContent('#e-' + c)).length > 0, c);
    await preencheE1(p, 'c6pay'); await p.fill('#f-cnpj', ''); await p.type('#f-cnpj', '11222333000182'); await p.click('#b1');
    assert.match(await p.textContent('#e-cnpj'), /não batem/);
    assert.strictEqual(await p.inputValue('#f-whatsapp'), '(11) 98765-4321');
    assert.strictEqual(reqs.length, 0);
    await ctx.close();
  });

  await t('formulário: os 4 produtos na etapa 1 → conversão → etapa 2 só com os campos dos produtos escolhidos → tela final', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP), viewport: { width: 390, height: 844 } }); const p = await ctx.newPage();
    await p.goto(BASE + '/?utm_source=google&utm_medium=cpc&utm_campaign=pagamento_integrado&gclid=XYZ');
    await p.goto(BASE + '/proposta.html?previa=1&ref=site_institucional');
    assert.strictEqual(await p.locator('#wa-float').count(), 0, 'botão flutuante dentro do formulário');
    assert.strictEqual(await p.textContent('.pf-destaque'), 'C6 Pay: crédito a partir de 1,84% recebendo em 31 dias, débito a partir de 0,82% e Pix grátis e ilimitado.');
    assert.deepStrictEqual(await p.$$eval('#g-produtos label', ls => ls.map(l => [l.querySelector('input').type, l.querySelector('input').value, l.textContent.trim()])), [
      ['checkbox', 'tef', 'TEF integrado ao caixa'],
      ['checkbox', 'c6pay', 'C6 Pay: crédito a partir de 1,84% recebendo em 31 dias, débito a partir de 0,82% e Pix grátis'],
      ['checkbox', 'link', 'Link de pagamento / pagamento online'],
      ['checkbox', 'pdvet', 'Sistema PDV (PDVet)']]);
    await preencheE1(p, ['tef', 'c6pay', 'link', 'pdvet']); await p.click('#b1');
    await p.waitForSelector('#pf-e2:not([hidden])');
    const c1 = reqs[0].corpo;
    assert.deepStrictEqual([c1.nome, c1.whatsapp, c1.email, c1.cnpj, c1.caixas, c1.produtos, c1.consentimento_lgpd, c1.website], ['Maria da Silva', '(11) 98765-4321', 'maria@empresa.com.br', '11222333000181', 3, ['tef', 'c6pay', 'link', 'pdvet'], true, '']);
    assert.ok(!('procura' in c1), 'procura deixou de ser mandado (contrato de 17/10)');
    assert.deepStrictEqual([c1.utm_source, c1.utm_medium, c1.utm_campaign, c1.gclid, c1.ref], ['google', 'cpc', 'pagamento_integrado', 'XYZ', 'site_institucional']);
    if (confereLib(c1)) assert.ok(lib.validarEtapa1(c1).ok, JSON.stringify(lib.validarEtapa1(c1)));
    const conv = await eventos(p, 'conversion'); assert.strictEqual(conv.length, 1); assert.strictEqual(conv[0].send_to, SEND_TO);
    assert.strictEqual(await p.textContent('#pf-e2 .eyebrow'), 'Etapa 2 de 2');
    assert.strictEqual(await p.textContent('#v-razao'), 'EMPRESA EXEMPLO LTDA'); assert.strictEqual(await p.textContent('#v-cnpj'), CNPJ); assert.strictEqual(await p.textContent('#v-cidade'), 'São Paulo/SP');
    assert.ok(await p.isHidden('#c-razao'));
    // 17/10: "✓ Dados corretos" (preenchido) e "Corrigir" (contorno), pequenos e lado a lado no celular; sem a pergunta da conta PJ
    const bc = await p.locator('#b-correto').boundingBox(), bk = await p.locator('#b-corrigir').boundingBox();
    assert.strictEqual(await p.textContent('#b-correto'), '✓ Dados corretos'); assert.strictEqual(await p.textContent('#b-corrigir'), 'Corrigir');
    assert.ok(/btn-primary/.test(await p.getAttribute('#b-correto', 'class')) && /btn-ghost/.test(await p.getAttribute('#b-corrigir', 'class')));
    assert.ok(Math.abs(bc.y - bk.y) < 1 && bk.x > bc.x + bc.width - 1, 'lado a lado'); for (const x of [bc, bk]) assert.ok(x.height >= 34 && x.height <= 38, 'altura ' + x.height);
    assert.ok(await p.evaluate(() => [...document.querySelectorAll('#acoes-empresa .btn')].every(b => b.scrollWidth <= b.clientWidth + 1 && b.getBoundingClientRect().height < 40)), 'quebrou linha');
    assert.strictEqual(await p.locator('input[name=conta_pj_c6]').count(), 0); assert.ok(!/conta PJ|isenta/i.test(await p.textContent('#pf-e2')));
    assert.strictEqual(await p.locator('#pf-e2 input[name=produtos]').count(), 0, 'a etapa 2 não pergunta mais os produtos');
    await p.click('#b-correto'); assert.ok(await p.isVisible('#m-correto'));
    assert.ok(await p.isVisible('#f-sistema') && await p.isVisible('#f-lojas') && await p.isVisible('#c-c6') && await p.isVisible('#c-link'));
    assert.strictEqual(await p.locator('#f-faixa option[value]:not([value=""])').count(), 8);
    await p.click('#b2');
    for (const c of ['sistema_pdv', 'lojas', 'vendas_cartao', 'recebimento', 'faixa_link']) assert.ok((await p.textContent('#e-' + c)).length > 0, c);
    assert.strictEqual(reqs.length, 1);
    await p.fill('#f-sistema', 'PDVet'); await p.fill('#f-lojas', '2'); await p.selectOption('#f-faixa', '201_600');
    await p.check('input[name=vendas_cartao][value="8_30mil"]'); await p.check('input[name=recebimento][value=d1]');
    assert.match(await p.textContent('#pf-e2'), /Se você parar aqui, tudo bem: nossa equipe comercial entra em contato para completar\./);
    assert.ok(!/me ligue/i.test(await p.textContent('main')));
    await p.click('#b2'); await p.waitForSelector('#pf-fim:not([hidden])');
    const c2 = reqs[1].corpo;
    assert.deepStrictEqual(c2, { lead_id: 'a'.repeat(24), pedido_token: 'b'.repeat(32), razao_social: 'EMPRESA EXEMPLO LTDA', sistema_pdv: 'PDVet', website: '', lojas: 2, vendas_cartao: '8_30mil', recebimento: 'd1', faixa_link: '201_600' });
    assert.ok(!('conta_pj_c6' in c2), 'conta_pj_c6 saiu do contrato em 17/10');
    if (libNova) assert.ok(lib.validarEtapa2(c2, { lead_id: c2.lead_id, pedido_token: c2.pedido_token, procura: 'proposta', produtos: 'tef,c6pay,link,pdvet' }).ok, JSON.stringify(lib.validarEtapa2(c2, { lead_id: c2.lead_id, pedido_token: c2.pedido_token, procura: 'proposta', produtos: 'tef,c6pay,link,pdvet' })));
    assert.strictEqual(await p.textContent('#pf-fim h1'), 'Sua proposta foi enviada.');
    assert.ok(await p.isVisible('#pdvet-adicional'), 'PDVet junto: oferta do portal na tela final'); assert.strictEqual(await p.getAttribute('#l-pdvet-adicional', 'href'), 'https://portal.pdvet.com.br/cadastro');
    assert.strictEqual(await p.textContent('#v-email'), 'maria@empresa.com.br');
    assert.match(await p.textContent('#t-fim'), /Spam e Promoções/);
    assert.strictEqual(await p.textContent('#pf-fim a[data-wa]'), 'Tirar dúvidas no WhatsApp');
    for (const sel of ['#pf-e1 a[data-wa]', '#pf-fim a[data-wa]']) assert.strictEqual(new URL(await p.getAttribute(sel, 'href')).searchParams.get('text'), 'Olá! Vim pelo site da Antere e quero saber mais sobre as soluções.\n\nOrigem: google / cpc / pagamento_integrado', sel);
    assert.strictEqual((await eventos(p, 'conversion')).length, 1, 'a etapa 2 não conta outra conversão');
    await ctx.close();
  });

  await t('formulário: pelo menos um produto; só PDVet vai ao cadastro da PDVet; PDVet com outro produto vai à etapa 2; a etapa 2 mostra só os campos de cada produto', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, []); await p.click('#b1');
    assert.strictEqual(await p.textContent('#e-produtos'), 'Escolha pelo menos uma opção.'); assert.strictEqual(reqs.length, 0);
    await ctx.close();
    // [marcados na tela, produtos enviados, grupos da etapa 2]; marcar C6 Pay marca também o TEF (18/10)
    const casos = [
      [['pdvet'], ['pdvet'], null],
      [['link', 'pdvet'], ['link', 'pdvet'], { tef: false, c6: false, link: true }],
      [['c6pay'], ['tef', 'c6pay'], { tef: true, c6: true, link: false }],
      [['tef'], ['tef'], { tef: true, c6: false, link: false }],
      [['tef', 'pdvet'], ['tef', 'pdvet'], { tef: true, c6: false, link: false }],
      [['link'], ['link'], { tef: false, c6: false, link: true }],
    ];
    for (const [marcados, prods, grupos] of casos) {
      const x = await contexto(b, { webhooks: etapa1Ok(EMP) }); const q = await x.ctx.newPage();
      await q.goto(BASE + '/proposta.html?previa=1'); await preencheE1(q, marcados); await q.click('#b1');
      if (!grupos) { await q.waitForSelector('#pf-pdvet:not([hidden])'); assert.strictEqual(await q.getAttribute('#l-pdvet', 'href'), 'https://portal.pdvet.com.br/cadastro'); }
      else {
        await q.waitForSelector('#pf-e2:not([hidden])');
        assert.deepStrictEqual({ tef: await q.isVisible('#c-tef'), c6: await q.isVisible('#c-c6'), link: await q.isVisible('#c-link') }, grupos, prods.join('+'));
        if (grupos.tef) { await q.fill('#f-sistema', 'Linx'); await q.fill('#f-lojas', '1'); }
        if (grupos.c6) { await q.check('input[name=vendas_cartao][value=ate_8mil]'); await q.check('input[name=recebimento][value=d31]'); }
        if (grupos.link) await q.selectOption('#f-faixa', 'ate_200');
        await q.click('#b2'); await q.waitForSelector('#pf-fim:not([hidden])');
        const c2 = x.reqs[1].corpo, campos = Object.keys(c2).sort();
        const esperados = ['lead_id', 'pedido_token', 'razao_social', 'website'].concat(grupos.tef ? ['lojas', 'sistema_pdv'] : [], grupos.c6 ? ['recebimento', 'vendas_cartao'] : [], grupos.link ? ['faixa_link'] : []).sort();
        assert.deepStrictEqual(campos, esperados, prods.join('+'));
        if (confereLib(c2, prods)) assert.ok(lib.validarEtapa2(c2, { lead_id: c2.lead_id, pedido_token: c2.pedido_token, procura: 'proposta', produtos: prods.join(',') }).ok, prods.join('+'));
        await q.waitForTimeout(50); assert.strictEqual(await q.isVisible('#pdvet-adicional'), prods.includes('pdvet'), 'oferta do PDVet: ' + prods.join('+'));
      }
      assert.deepStrictEqual(x.reqs[0].corpo.produtos, prods); assert.ok(!('procura' in x.reqs[0].corpo));
      assert.strictEqual('caixas' in x.reqs[0].corpo, prods.includes('tef'), 'caixas só com TEF: ' + prods.join('+'));
      if (confereLib(x.reqs[0].corpo)) assert.ok(lib.validarEtapa1(x.reqs[0].corpo).ok, prods.join('+'));
      assert.strictEqual((await eventos(q, 'conversion')).length, 1, 'conversão no envio da etapa 1: ' + prods.join('+'));
      await x.ctx.close();
    }
  });

  await t('formulário: C6 Pay só com TEF (marcar C6 Pay marca o TEF e mostra o aviso; desmarcar o TEF desmarca o C6 Pay); Nº de caixas só com TEF', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1');
    const marcado = (v) => p.isChecked('input[name=produtos][value=' + v + ']');
    assert.ok(await p.isHidden('#c-caixas') && await p.isHidden('#n-c6tef'));
    await p.check('input[name=produtos][value=c6pay]');
    assert.ok(await marcado('tef') && await marcado('c6pay'), 'marcar C6 Pay marca o TEF');
    assert.ok(await p.isVisible('#n-c6tef')); assert.strictEqual(await p.textContent('#n-c6tef'), 'O C6 Pay é oferecido junto com o TEF integrado ao caixa.');
    assert.ok(await p.isVisible('#c-caixas'), 'Nº de caixas aparece com TEF');
    await p.uncheck('input[name=produtos][value=tef]');
    assert.ok(!(await marcado('tef')) && !(await marcado('c6pay')), 'desmarcar o TEF desmarca o C6 Pay');
    assert.ok(await p.isHidden('#n-c6tef') && await p.isHidden('#c-caixas'));
    await p.check('input[name=produtos][value=tef]'); assert.ok(!(await marcado('c6pay')), 'TEF sozinho não marca o C6 Pay'); assert.ok(await p.isVisible('#c-caixas') && await p.isHidden('#n-c6tef'));
    await p.fill('#f-nome', 'Maria da Silva'); await p.type('#f-whatsapp', '11987654321'); await p.fill('#f-email', 'maria@empresa.com.br'); await p.type('#f-cnpj', '11222333000181'); await p.check('#f-lgpd');
    await p.click('#b1'); assert.strictEqual(await p.textContent('#e-caixas'), 'Informe o número de caixas.'); assert.strictEqual(reqs.length, 0, 'com TEF, caixas é obrigatório');
    await p.uncheck('input[name=produtos][value=tef]'); await p.check('input[name=produtos][value=link]'); await p.click('#b1'); await p.waitForSelector('#pf-e2:not([hidden])');
    assert.ok(!('caixas' in reqs[0].corpo), 'sem TEF, caixas não vai');
    assert.ok(await p.isHidden('#c-tef') && await p.isHidden('#f-sistema') && await p.isHidden('#f-lojas'), 'sem TEF, sem sistema PDV e lojas');
    await ctx.close();
  });

  await t('formulário: erro c6pay_sem_tef do n8n (etapa 1 e etapa 2) mostra "O C6 Pay é oferecido junto com o TEF…"', async () => {
    const r422 = { status: 422, body: { ok: false, erro: 'validacao', erros: [{ campo: 'produtos', erro: 'c6pay_sem_tef' }] } };
    const x = await contexto(b, { webhooks: () => r422 }); const p = await x.ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, ['tef', 'c6pay']); await p.click('#b1');
    await p.waitForFunction(() => document.getElementById('e-produtos').textContent.length > 0);
    assert.strictEqual(await p.textContent('#e-produtos'), 'O C6 Pay é oferecido junto com o TEF integrado ao caixa. Marque também "TEF integrado ao caixa".');
    assert.strictEqual(await p.getAttribute('#g-produtos', 'aria-invalid'), 'true'); assert.strictEqual((await eventos(p, 'conversion')).length, 0);
    await x.ctx.close();
    const y = await contexto(b, { webhooks: (url, c) => url === E1 ? etapa1Ok(EMP)(url, c) : r422 }); const q = await y.ctx.newPage();
    await q.goto(BASE + '/proposta.html?previa=1'); await preencheE1(q, ['tef', 'c6pay']); await q.click('#b1'); await q.waitForSelector('#pf-e2:not([hidden])');
    await q.fill('#f-sistema', 'Linx'); await q.fill('#f-lojas', '1'); await q.check('input[name=vendas_cartao][value=ate_8mil]'); await q.check('input[name=recebimento][value=d31]');
    await q.click('#b2'); await q.waitForFunction(() => /C6 Pay/.test(document.getElementById('s2').textContent));
    assert.strictEqual(await q.textContent('#s2'), 'O C6 Pay é oferecido junto com o TEF integrado ao caixa. Marque também "TEF integrado ao caixa". Volte à etapa 1 para ajustar.');
    await y.ctx.close();
  });

  await t('formulário: CNPJ não consultado pede a razão social digitada; "Corrigir" abre o campo', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok({ cnpj_confirmado: false, razao_social: '', cidade: '', uf: '' }) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, ['link']); await p.click('#b1'); await p.waitForSelector('#pf-e2:not([hidden])');
    assert.ok(await p.isHidden('#bloco-empresa')); assert.ok(await p.isVisible('#f-razao'));
    assert.ok(await p.isHidden('#c-tef')); await p.selectOption('#f-faixa', 'acima_10000');
    await p.click('#b2'); assert.strictEqual(await p.textContent('#e-razao_social'), 'Informe a razão social.'); assert.strictEqual(reqs.length, 1);
    await p.fill('#f-razao', 'Minha Empresa Ltda'); await p.click('#b2'); await p.waitForSelector('#pf-fim:not([hidden])');
    assert.strictEqual(reqs[1].corpo.razao_social, 'Minha Empresa Ltda'); assert.ok(!('conta_pj_c6' in reqs[1].corpo)); assert.ok(!('vendas_cartao' in reqs[1].corpo)); assert.ok(await p.isVisible('#t-escalonar'));
    await ctx.close();
    const x = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p2 = await x.ctx.newPage();
    await p2.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p2, ['tef', 'c6pay']); await p2.click('#b1'); await p2.waitForSelector('#pf-e2:not([hidden])');
    await p2.click('#b-corrigir'); assert.ok(await p2.isVisible('#f-razao')); await p2.fill('#f-razao', 'Nome Corrigido SA');
    await p2.fill('#f-sistema', 'Linx'); await p2.fill('#f-lojas', '1'); await p2.check('input[name=vendas_cartao][value=ate_8mil]'); await p2.check('input[name=recebimento][value=d31]');
    await p2.click('#b2'); await p2.waitForSelector('#pf-fim:not([hidden])'); assert.strictEqual(x.reqs[1].corpo.razao_social, 'Nome Corrigido SA'); assert.ok(!('faixa_link' in x.reqs[1].corpo));
    await x.ctx.close();
  });

  await t('formulário PDVet: tela "Seu contato está registrado" com o botão para o portal da PDVet; 1 conversão', async () => {
    const { ctx } = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, 'pdvet'); await p.click('#b1'); await p.waitForSelector('#pf-pdvet:not([hidden])');
    assert.strictEqual(await p.textContent('#pf-pdvet h1'), 'Seu contato está registrado.');
    assert.match(await p.textContent('#pf-pdvet'), /Para conhecer e contratar o sistema PDV, continue no formulário da PDVet\./);
    assert.strictEqual(await p.textContent('#l-pdvet'), 'Continuar no site da PDVet'); assert.strictEqual(await p.getAttribute('#l-pdvet', 'href'), 'https://portal.pdvet.com.br/cadastro');
    assert.strictEqual((await eventos(p, 'conversion')).length, 1);
    await ctx.close();
  });

  await t('formulário: 422 marca os campos de erros[]; 503 mostra a mensagem; nenhum erro conta conversão', async () => {
    let modo = 422;
    const { ctx } = await contexto(b, { webhooks: () => modo === 422 ? { status: 422, body: { ok: false, erro: 'validacao', erros: [{ campo: 'email', erro: 'invalido' }, { campo: 'cnpj', erro: 'invalido' }] } } : { status: 503, body: { ok: false, erro: 'indisponivel', mensagem: 'Sistema em manutenção. Tente de novo em alguns minutos.' } } });
    const p = await ctx.newPage(); await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, 'c6pay'); await p.click('#b1');
    await p.waitForFunction(() => document.getElementById('e-email').textContent.length > 0);
    assert.strictEqual(await p.getAttribute('#f-email', 'aria-invalid'), 'true'); assert.strictEqual(await p.getAttribute('#f-cnpj', 'aria-invalid'), 'true');
    modo = 503; await p.click('#b1'); await p.waitForFunction(() => document.getElementById('s1').textContent.includes('manutenção'));
    assert.strictEqual((await eventos(p, 'conversion')).length, 0); assert.ok(await p.isVisible('#pf-e1'));
    await ctx.close();
  });

  await t('formulário: tema escuro em todas as telas e estados (sem fundo claro, contraste ≥ 4,5, controles nativos escuros), com o aparelho em modo claro ou escuro', async () => {
    // o ponteiro sai da tela antes de medir: o estado de "passar o mouse" de um botão não é o tema da página
    const auditar = async (p, nome) => { await p.mouse.move(0, 0); await p.waitForTimeout(250); return medir(p, nome); };
    const medir = (p, nome) => p.evaluate((nome) => {
      const rgb = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(parseFloat); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
      const lum = (c) => { const f = (x) => { x /= 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
      const fundo = (el) => { const pilha = []; for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c && c.a > 0) pilha.push(c); if (c && c.a >= 1) break; }
        let r = pilha.length && pilha[pilha.length - 1].a >= 1 ? pilha.pop() : { r: 18, g: 19, b: 26 }; while (pilha.length) { const c = pilha.pop(); r = { r: c.r * c.a + r.r * (1 - c.a), g: c.g * c.a + r.g * (1 - c.a), b: c.b * c.a + r.b * (1 - c.a) }; } return r; };
      const prob = [];
      for (const el of document.querySelectorAll('main *')) {
        const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        if (!r.width || !r.height || cs.visibility === 'hidden' || el.closest('[hidden]') || el.closest('.hp')) continue;
        const bg = fundo(el), Lb = lum(bg);
        if (Lb > 0.25) prob.push(nome + ': fundo claro em ' + el.tagName + '#' + el.id);
        if (['INPUT', 'SELECT'].includes(el.tagName) && !/dark/.test(cs.colorScheme)) prob.push(nome + ': controle claro ' + el.tagName + '#' + el.id);
        const texto = ([...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || ['INPUT', 'SELECT'].includes(el.tagName)) && !['radio', 'checkbox'].includes(el.type);
        if (texto) { const c = rgb(cs.color), t = { r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a) }; const L = lum(t), cr = (Math.max(L, Lb) + .05) / (Math.min(L, Lb) + .05);
          if (cr < 4.5) prob.push(nome + ': contraste ' + cr.toFixed(2) + ' em ' + el.tagName + '#' + el.id + ' "' + (el.innerText || '').slice(0, 30) + '"'); }
      }
      return prob;
    }, nome);
    const probs = [];
    for (const colorScheme of ['light', 'dark']) {
      let modo = 'etapa2';
      const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, colorScheme });
      await ctx.route('**/*', async (r) => {
        const u = new URL(r.request().url());
        if (u.origin === BASE) { const f = u.pathname.slice(1) || 'index.html'; return r.fulfill({ body: fs.readFileSync(path.join(PUB, f)), contentType: f.endsWith('.js') ? 'application/javascript' : 'text/html' }); }
        if (u.href.startsWith(E1) || u.href.startsWith(E2)) { await new Promise(z => setTimeout(z, 300)); const c = JSON.parse(r.request().postData() || '{}');
          const resp = u.href.startsWith(E1) && modo === '422' ? { status: 422, body: { ok: false, erro: 'validacao', erros: [{ campo: 'email', erro: 'dominio_sem_email', sugestao: 'empresa.com.br' }] } } : etapa1Ok(EMP)(u.href.startsWith(E1) ? E1 : E2, c);
          return r.fulfill({ status: resp.status, body: JSON.stringify(resp.body), contentType: 'application/json' }); }
        return r.abort();
      });
      const p = await ctx.newPage(); const nome = (n) => colorScheme + '/' + n;
      const abre = async () => { await p.goto(BASE + '/proposta.html?previa=1'); await p.evaluate(() => sessionStorage.clear()); await p.goto(BASE + '/proposta.html?previa=1'); };
      await abre(); probs.push(...await auditar(p, nome('etapa 1')));
      await p.click('#b1'); probs.push(...await auditar(p, nome('erros da etapa 1')));
      await abre(); await p.fill('#f-email', 'maria@gmial.com'); await p.locator('#f-email').blur(); probs.push(...await auditar(p, nome('você quis dizer')));
      await abre(); modo = '422'; await preencheE1(p, 'c6pay'); await p.click('#b1'); await p.waitForTimeout(80); probs.push(...await auditar(p, nome('carregando etapa 1')));
      await p.waitForFunction(() => document.getElementById('e-email').textContent.length > 0); probs.push(...await auditar(p, nome('422')));
      await abre(); modo = 'pdvet'; await preencheE1(p, 'pdvet'); await p.click('#b1'); await p.waitForSelector('#pf-pdvet:not([hidden])'); probs.push(...await auditar(p, nome('PDVet')));
      await abre(); modo = 'etapa2'; await preencheE1(p, ['tef', 'c6pay', 'link']); await p.click('#b1'); await p.waitForSelector('#pf-e2:not([hidden])');
      probs.push(...await auditar(p, nome('etapa 2')));
      await p.click('#b2'); probs.push(...await auditar(p, nome('erros da etapa 2'))); await p.click('#b-corrigir'); probs.push(...await auditar(p, nome('corrigir')));
      await p.fill('#f-sistema', 'PDVet'); await p.fill('#f-lojas', '2'); await p.selectOption('#f-faixa', '201_600'); await p.check('input[name=vendas_cartao][value="8_30mil"]'); await p.check('input[name=recebimento][value=d1]');
      await p.click('#b2'); await p.waitForTimeout(80); probs.push(...await auditar(p, nome('carregando etapa 2')));
      await p.waitForSelector('#pf-fim:not([hidden])'); probs.push(...await auditar(p, nome('tela final')));
      await ctx.close();
    }
    assert.deepStrictEqual(probs, []);
  });

  // ---------------- e-mail (proposta_formulario_email_1610) ----------------
  const LID = 'c'.repeat(24), TK = 'd'.repeat(32);
  await t('e-mail: "Você quis dizer …?" para erros comuns (gmial.com, hotmial.com, gmail.com.br…); sem pergunta para olive.com e domínio de empresa (regra de 16/10: 1 letra até 5, 2 acima, mesma 1ª letra)', async () => {
    const { ctx } = await contexto(b); const p = await ctx.newPage(); await p.goto(BASE + '/proposta.html?previa=1');
    const casos = { 'maria@gmial.com': 'maria@gmail.com', 'maria@gmail.con': 'maria@gmail.com', 'ana@hotmial.com': 'ana@hotmail.com', 'ana@outlok.com': 'ana@outlook.com', 'jo@gmail.com.br': 'jo@gmail.com', 'jo@yaho.com.br': 'jo@yahoo.com.br', 'jo@gmal.com': 'jo@gmail.com', 'jo@gmai.com': 'jo@gmail.com', 'jo@hotmal.com': 'jo@hotmail.com', 'a@yhaoo.com': 'a@yahoo.com', 'jo@outllok.com': 'jo@outlook.com' };
    for (const [de, para] of Object.entries(casos)) { await p.fill('#f-email', de); await p.locator('#f-email').blur(); assert.ok(await p.isVisible('#sug-email'), de); assert.strictEqual(await p.textContent('#sug-texto'), para, de); }
    for (const ok of ['maria@gmail.com', 'compras@empresaexemplo.com.br', 'jo@yahoo.com.br', 'x@terra.com.br', 'jo@uol.com', 'contato@olive.com', 'a@blive.com', 'a@gmaxyz.com']) { await p.fill('#f-email', ok); await p.locator('#f-email').blur(); assert.ok(await p.isHidden('#sug-email'), ok); }
    await ctx.close();
  });
  await t('e-mail: a sugestão não troca sozinha; envio com erro comum espera a resposta; "Sim, trocar" e "Não, está certo" seguem', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, 'pdvet'); await p.fill('#f-email', 'maria@gmial.com');
    await p.click('#b1'); assert.ok(await p.isVisible('#sug-email')); assert.strictEqual(reqs.length, 0, 'enviou sem a resposta do lead');
    assert.strictEqual(await p.inputValue('#f-email'), 'maria@gmial.com', 'trocou sozinho');
    await p.click('#sug-sim'); assert.strictEqual(await p.inputValue('#f-email'), 'maria@gmail.com');
    await p.click('#b1'); await p.waitForSelector('#pf-pdvet:not([hidden])'); assert.strictEqual(reqs[0].corpo.email, 'maria@gmail.com');
    assert.ok(!('email_alterado' in reqs[0].corpo) && !('lead_id_cadastro' in reqs[0].corpo), 'campos de cadastro sem link de lote');
    await ctx.close();
    const x = await contexto(b, { webhooks: etapa1Ok(EMP) }); const p2 = await x.ctx.newPage();
    await p2.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p2, 'pdvet'); await p2.fill('#f-email', 'jo@gmial.com');
    await p2.click('#b1'); await p2.click('#sug-nao'); await p2.click('#b1'); await p2.waitForSelector('#pf-pdvet:not([hidden])');
    assert.strictEqual(x.reqs[0].corpo.email, 'jo@gmial.com');
    await x.ctx.close();
  });
  await t('e-mail: 422 dominio_sem_email mostra "Esse endereço não recebe e-mail…" e a sugestão do servidor', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: () => ({ status: 422, body: { ok: false, erro: 'validacao', erros: [{ campo: 'email', erro: 'dominio_sem_email', sugestao: 'empresa.com.br' }] } }) });
    const p = await ctx.newPage(); await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, 'c6pay'); await p.fill('#f-email', 'compras@empesa.com.br'); await p.click('#b1');
    await p.waitForFunction(() => document.getElementById('e-email').textContent.length > 0);
    assert.strictEqual(await p.textContent('#e-email'), 'Esse endereço não recebe e-mail. Confira o que vem depois do @.');
    assert.strictEqual(await p.getAttribute('#f-email', 'aria-invalid'), 'true');
    assert.strictEqual(await p.textContent('#sug-texto'), 'compras@empresa.com.br'); assert.strictEqual(reqs.length, 1);
    assert.strictEqual((await eventos(p, 'conversion')).length, 0);
    await ctx.close();
  });
  await t('e-mail: link com lead_id e token abre com nome e e-mail cadastrados, limpa a URL e manda email_alterado', async () => {
    const dados = (sp) => sp.get('lead_id') === LID && sp.get('token') === TK ? { status: 200, body: { email: 'contato@empresa.com.br', nome_contato: 'Carla Souza', empresa: 'EMPRESA EXEMPLO LTDA' } } : { status: 404, body: { ok: false } };
    for (const [novo, alterado] of [[null, false], ['carla@gmail.com', true]]) {
      const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP), dados }); const p = await ctx.newPage();
      await p.goto(BASE + '/proposta.html?previa=1&utm_source=lote&lead_id=' + LID + '&token=' + TK);
      await p.waitForFunction(() => document.getElementById('f-email').value !== '');
      assert.strictEqual(await p.inputValue('#f-email'), 'contato@empresa.com.br'); assert.strictEqual(await p.inputValue('#f-nome'), 'Carla Souza');
      const u = new URL(p.url()); assert.ok(!u.searchParams.has('lead_id') && !u.searchParams.has('token'), p.url()); assert.strictEqual(u.searchParams.get('utm_source'), 'lote');
      assert.strictEqual(reqs[0].metodo, 'GET');
      await p.type('#f-whatsapp', '11987654321'); await p.type('#f-cnpj', '11222333000181'); await p.check('input[name=produtos][value=pdvet]'); await p.check('#f-lgpd');
      if (novo) await p.fill('#f-email', novo);
      await p.click('#b1'); await p.waitForSelector('#pf-pdvet:not([hidden])');
      const c = reqs[1].corpo;
      assert.deepStrictEqual([c.lead_id_cadastro, c.token_cadastro, c.email_alterado, c.email, c.utm_source], [LID, TK, alterado, novo || 'contato@empresa.com.br', 'lote']);
      if (confereLib(c)) assert.ok(lib.validarEtapa1(c).ok);
      await ctx.close();
    }
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP), dados }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1&lead_id=' + LID + '&token=' + 'e'.repeat(32)); await p.waitForTimeout(300);
    assert.strictEqual(await p.inputValue('#f-email'), ''); await preencheE1(p, 'pdvet'); await p.click('#b1'); await p.waitForSelector('#pf-pdvet:not([hidden])');
    assert.ok(!('lead_id_cadastro' in reqs[1].corpo), 'token inválido não manda os campos de cadastro');
    await ctx.close();
  });

  // ---------------- WhatsApp ----------------
  await t('WhatsApp flutuante em todas as páginas e nas legais, com a mensagem e a origem; clique vira evento whatsapp_click, sem conversão', async () => {
    const { ctx } = await contexto(b);
    for (const pg of [...PAGINAS, ...LEGAIS]) {
      const p = await ctx.newPage(); await p.goto(BASE + '/' + pg + UTM); await semNavegar(p);
      const f = p.locator('#wa-float'); assert.strictEqual(await f.count(), 1, pg);
      assert.strictEqual((await f.textContent()).trim(), 'Fale com a gente');
      const u = new URL(await f.getAttribute('href'));
      assert.strictEqual(u.origin + u.pathname, 'https://wa.me/5511955032670');
      assert.strictEqual(u.searchParams.get('text'), 'Olá! Vim pelo site da Antere e quero saber mais sobre as soluções.\n\nOrigem: google / cpc / pagamento_integrado', pg);
      await f.click();
      const ev = await eventos(p, 'whatsapp_click'); assert.strictEqual(ev.length, 1, pg); assert.strictEqual(ev[0].local, 'flutuante'); assert.strictEqual(ev[0].utm_campaign, 'pagamento_integrado');
      assert.strictEqual((await eventos(p, 'conversion')).length, 0, pg);
      await p.close();
    }
    const p = await ctx.newPage(); await p.goto(BASE + '/sobre.html');
    assert.strictEqual(new URL(await p.getAttribute('#wa-float', 'href')).searchParams.get('text'), 'Olá! Vim pelo site da Antere e quero saber mais sobre as soluções.');
    await ctx.close();
  });

  await t('celular (390×844): o botão flutuante nunca fica visível por cima de um "Quero minha proposta"', async () => {
    const { ctx } = await contexto(b, { viewport: { width: 390, height: 844 } }); let checagens = 0, ocultou = 0;
    for (const pg of PAGINAS) {
      const p = await ctx.newPage(); await p.goto(BASE + '/' + pg);
      const altura = await p.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y <= altura; y += 60) {
        await p.evaluate((yy) => window.scrollTo(0, yy), y); await p.waitForTimeout(30);
        const r = await p.evaluate(() => {
          const f = document.getElementById('wa-float'), fr = f.getBoundingClientRect(), vis = getComputedStyle(f).visibility !== 'hidden';
          const cobre = [...document.querySelectorAll('a[href*="/form/proposta"], a[href*="proposta.html"]')].some(c => { if (!c.offsetParent) return false; const b = c.getBoundingClientRect(); return b.width && b.left < fr.right && b.right > fr.left && b.top < fr.bottom && b.bottom > fr.top; });
          return { vis, cobre };
        });
        checagens++; if (r.cobre) { ocultou++; assert.ok(!r.vis, pg + ' y=' + y); }
      }
      await p.close();
    }
    assert.ok(checagens > 100 && ocultou > 0, checagens + ' ' + ocultou);
    await ctx.close();
  });

  // ---------------- aviso de cookies (chave ANTERE_COOKIES) ----------------
  await t('cookies: site-config.js publicado com a chave do aviso desligada', async () => {
    assert.match(fs.readFileSync(path.join(PUB, 'site-config.js'), 'utf8'), /^window\.ANTERE_COOKIES = false;$/m);
  });
  await t('cookies desligado: nada muda (tag carrega em toda página sem clique, sem faixa, sem link de preferências, nada guardado)', async () => {
    const { ctx, gtagJs } = await contexto(b, { viewport: { width: 390, height: 844 } });
    for (const pg of [...PAGINAS, ...LEGAIS, 'proposta.html?previa=1']) {
      const p = await ctx.newPage(); const antes = gtagJs.length;
      await p.goto(BASE + '/' + pg); await p.waitForTimeout(100);
      assert.strictEqual(await p.evaluate(() => window.ANTERE_COOKIES), false, pg);
      assert.strictEqual(gtagJs.length - antes, 1, 'gtag.js em ' + pg);
      assert.ok(await p.evaluate(() => window.dataLayer.some(a => a[0] === 'config' && a[1] === 'AW-18479570694')), pg);
      assert.strictEqual(await p.locator('#cookie-faixa, #cookie-preferencias').count(), 0, pg);
      assert.strictEqual(await p.evaluate(() => window.localStorage.getItem('antere_cookies')), null, pg);
      assert.strictEqual(await p.evaluate(() => document.body.classList.contains('cookies-aberto')), false, pg);
      if (await p.locator('#wa-float').count()) assert.strictEqual(await p.evaluate(() => getComputedStyle(document.getElementById('wa-float')).bottom), '16px', pg);
      await p.close();
    }
    await ctx.close();
  });
  await t('cookies ligado (simulado): faixa com Aceitar/Recusar e link da política; sem aceite a tag não carrega; Recusar fica guardado', async () => {
    const { ctx, gtagJs } = await contexto(b, { cookies: true, viewport: { width: 390, height: 844 } });
    const p = await ctx.newPage(); await p.goto(BASE + '/'); await p.waitForTimeout(100);
    assert.ok(await p.isVisible('#cookie-faixa'));
    assert.strictEqual(await p.getAttribute('#cookie-faixa a', 'href'), 'https://legal.antere.com.br/privacidade.html');
    assert.strictEqual(await p.textContent('#cookie-aceitar'), 'Aceitar'); assert.strictEqual(await p.textContent('#cookie-recusar'), 'Recusar');
    assert.strictEqual(gtagJs.length, 0, 'a tag carregou antes do aceite');
    const fb = await p.evaluate(() => document.getElementById('wa-float').getBoundingClientRect().bottom), cf = await p.evaluate(() => document.getElementById('cookie-faixa').getBoundingClientRect().top);
    assert.ok(fb <= cf, 'WhatsApp por baixo da faixa');
    await p.click('#cookie-recusar');
    assert.ok(await p.isHidden('#cookie-faixa')); assert.strictEqual(JSON.parse(await p.evaluate(() => localStorage.getItem('antere_cookies'))).escolha, 'recusado');
    for (const pg of ['sobre.html', 'proposta.html?previa=1', 'legal/termos.html']) { await p.goto(BASE + '/' + pg); await p.waitForTimeout(100); assert.strictEqual(await p.locator('#cookie-faixa').count(), 0, pg); }
    assert.strictEqual(gtagJs.length, 0, 'a tag carregou depois do Recusar');
    await ctx.close();
  });
  await t('cookies ligado (simulado): Aceitar carrega a tag na hora e nas próximas páginas; "Preferências de cookies" reabre a faixa', async () => {
    const { ctx, gtagJs } = await contexto(b, { cookies: true });
    const p = await ctx.newPage(); await p.goto(BASE + '/calculadora.html'); await p.waitForTimeout(100);
    assert.strictEqual(gtagJs.length, 0); await p.click('#cookie-aceitar'); await p.waitForTimeout(100);
    assert.strictEqual(gtagJs.length, 1); assert.ok(await p.isHidden('#cookie-faixa'));
    await p.goto(BASE + '/contato.html'); await p.waitForTimeout(100);
    assert.strictEqual(gtagJs.length, 2); assert.strictEqual(await p.locator('#cookie-faixa').count(), 0);
    await p.click('#cookie-preferencias'); assert.ok(await p.isVisible('#cookie-faixa'));
    await p.click('#cookie-recusar'); assert.strictEqual(JSON.parse(await p.evaluate(() => localStorage.getItem('antere_cookies'))).escolha, 'recusado');
    await p.goto(BASE + '/index.html'); await p.waitForTimeout(100); assert.strictEqual(gtagJs.length, 2, 'depois de recusar, a tag não carrega mais');
    await ctx.close();
  });

  // ---------------- nome ----------------
  await t('Sobre: "Quem acompanha você" / Equipe comercial Antere; nenhum "Fernanda" em public/ nem no gerador', async () => {
    const h = fs.readFileSync(path.join(PUB, 'sobre.html'), 'utf8');
    assert.ok(h.includes('<span class="eyebrow">Quem acompanha você</span><h3>Equipe comercial Antere</h3><p>Assina as propostas e acompanha cada cliente, da proposta até a ativação.</p>'));
    const todos = [...PAGINAS, ...LEGAIS, 'proposta.html', 'sitemap.xml', 'robots.txt'].map(f => path.join(PUB, f)).concat(fs.readdirSync(SRC).filter(f => f.endsWith('.py')).map(f => path.join(SRC, f)));
    for (const f of todos) assert.ok(!/fernanda/i.test(fs.readFileSync(f, 'utf8')), f);
  });

  await b.close();
  console.log(`${ok} testes ok, ${falhas} falharam` + (libNova ? ' (com as regras do n8n)' : lib ? ' (a lib do n8n ao lado ainda tem o contrato antigo: corpos do formulário não conferidos por ela)' : ' (sem o antere-automacao ao lado: regras do n8n não conferidas)'));
  process.exitCode = falhas ? 1 : 0;
})();
