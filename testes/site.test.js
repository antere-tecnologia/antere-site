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
const SEND_TO = 'AW-18479570694/4-TPCPzV6ZcdEIa-3-tE';
const UTM = '?utm_source=google&utm_medium=cpc&utm_campaign=pagamento_integrado';
const PAGINAS = ['index.html', 'calculadora.html', 'como-funciona.html', 'contato.html', 'sobre.html', 'solucoes.html', '404.html'];
const LEGAIS = ['legal/privacidade.html', 'legal/termos.html', 'legal/exclusao-dados.html'];
const CNPJ = '11.222.333/0001-81';
let lib = null;
try { lib = require(path.join(__dirname, '..', '..', 'antere-automacao', 'n8n', 'lib', 'formulario_site.js')); } catch (e) { lib = null; }

let ok = 0, falhas = 0;
async function t(nome, f) {
  try { await f(); ok++; console.log('ok - ' + nome); } catch (e) { falhas++; console.log('FALHOU - ' + nome + '\n', e && e.stack || e); }
}

// Contexto com o site servido de public/ e tudo de fora bloqueado. chave: undefined = site-config.js real; true/false = simulado.
async function contexto(b, { chave, webhooks, viewport } = {}) {
  const ctx = await b.newContext({ viewport: viewport || { width: 1280, height: 900 } });
  const reqs = [];
  await ctx.route('**/*', async (r) => {
    const u = new URL(r.request().url());
    if (u.origin === BASE) {
      if (u.pathname === '/site-config.js' && chave !== undefined) return r.fulfill({ body: 'window.ANTERE_FORM_NOVO = ' + chave + ';', contentType: 'application/javascript' });
      let f = u.pathname.slice(1) || 'index.html';
      const arq = path.join(PUB, f);
      if (!fs.existsSync(arq) || fs.statSync(arq).isDirectory()) return r.fulfill({ status: 404, body: fs.readFileSync(path.join(PUB, '404.html')), contentType: 'text/html' });
      const tipo = f.endsWith('.js') ? 'application/javascript' : f.endsWith('.png') ? 'image/png' : 'text/html';
      return r.fulfill({ body: fs.readFileSync(arq), contentType: tipo });
    }
    if (u.hostname === 'www.googletagmanager.com') return r.fulfill({ body: '', contentType: 'application/javascript' });
    if (u.href.startsWith(E1) || u.href.startsWith(E2)) {
      const corpo = JSON.parse(r.request().postData() || '{}'); reqs.push({ url: u.href, corpo });
      const resp = webhooks ? webhooks(u.href, corpo) : { status: 503, body: { ok: false, erro: 'indisponivel' } };
      return r.fulfill({ status: resp.status, body: JSON.stringify(resp.body), contentType: 'application/json' });
    }
    return r.abort();
  });
  return { ctx, reqs };
}
const eventos = (p, nome) => p.evaluate((n) => (window.dataLayer || []).filter(a => a[0] === 'event' && a[1] === n).map(a => a[2] || {}), nome);
const semNavegar = (p) => p.evaluate(() => document.addEventListener('click', e => { if (e.target.closest('a')) e.preventDefault(); }));
const hrefsProposta = (p) => p.$$eval('a', as => as.map(a => a.href).filter(h => /\/form\/proposta|proposta\.html/.test(h)));

(async () => {
  const b = await chromium.launch();

  // ---------------- chave desligada (o estado publicado) ----------------
  await t('site-config.js publicado com a chave desligada', async () => {
    const s = fs.readFileSync(path.join(PUB, 'site-config.js'), 'utf8');
    assert.match(s, /^window\.ANTERE_FORM_NOVO = false;$/m);
  });
  await t('nenhum HTML de public/ tem link para o formulário novo', async () => {
    for (const f of [...PAGINAS, ...LEGAIS, 'proposta.html']) {
      const h = fs.readFileSync(path.join(PUB, f), 'utf8');
      assert.ok(!/<a\b[^>]*href="[^"]*proposta\.html/.test(h), f);
    }
  });
  await t('chave desligada: nenhum botão aponta para o formulário novo; 20 links seguem em /form/proposta com UTM e ref; 1 conversão por clique', async () => {
    const { ctx } = await contexto(b); let total = 0;
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
  await t('chave desligada: /proposta.html leva ao formulário antigo, com as UTM', async () => {
    const { ctx } = await contexto(b); const p = await ctx.newPage(); let destino = null;
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
  const etapa1Ok = (empresa, procura) => (url, c) => url === E1
    ? (procura === 'pdvet' ? { status: 200, body: { ok: true, lead_id: 'a'.repeat(24), pedido_token: '', proximo: 'pdvet', url: 'https://portal.pdvet.com.br/cadastro', empresa } }
      : { status: 200, body: { ok: true, lead_id: 'a'.repeat(24), pedido_token: 'b'.repeat(32), proximo: 'etapa2', empresa } })
    : { status: 200, body: { ok: true, status: 'proposta_enviada', email: c.lead_id ? 'maria@empresa.com.br' : '', escalonar: c.faixa_link === 'acima_10000' } };
  async function preencheE1(p, procura) {
    await p.fill('#f-nome', 'Maria da Silva'); await p.type('#f-whatsapp', '11987654321'); await p.fill('#f-email', 'maria@empresa.com.br');
    await p.type('#f-cnpj', CNPJ.replace(/\D/g, '')); await p.fill('#f-caixas', '3');
    await p.check('input[name=procura][value=' + procura + ']'); await p.check('#f-lgpd');
  }
  const EMP = { cnpj_confirmado: true, razao_social: 'EMPRESA EXEMPLO LTDA', cidade: 'São Paulo', uf: 'SP' };

  await t('formulário: validação na tela antes de enviar (vazio e CNPJ com dígito errado)', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP, 'c6pay') }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1');
    await p.click('#b1');
    for (const c of ['nome', 'whatsapp', 'email', 'cnpj', 'caixas', 'procura', 'consentimento_lgpd']) assert.ok((await p.textContent('#e-' + c)).length > 0, c);
    await preencheE1(p, 'c6pay'); await p.fill('#f-cnpj', ''); await p.type('#f-cnpj', '11222333000182'); await p.click('#b1');
    assert.match(await p.textContent('#e-cnpj'), /não batem/);
    assert.strictEqual(await p.inputValue('#f-whatsapp'), '(11) 98765-4321');
    assert.strictEqual(reqs.length, 0);
    await ctx.close();
  });

  await t('formulário C6 Pay: etapa 1 → conversão → etapa 2 (empresa consultada, campos condicionais) → tela final', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok(EMP, 'c6pay'), viewport: { width: 390, height: 844 } }); const p = await ctx.newPage();
    await p.goto(BASE + '/?utm_source=google&utm_medium=cpc&utm_campaign=pagamento_integrado&gclid=XYZ');
    await p.goto(BASE + '/proposta.html?previa=1&ref=site_institucional');
    assert.strictEqual(await p.locator('#wa-float').count(), 0, 'botão flutuante dentro do formulário');
    assert.match(await p.textContent('.pf-destaque'), /crédito a partir de 1,84%, débito a partir de 0,82% e Pix grátis e ilimitado/);
    await preencheE1(p, 'c6pay'); await p.click('#b1');
    await p.waitForSelector('#pf-e2:not([hidden])');
    const c1 = reqs[0].corpo;
    assert.deepStrictEqual([c1.nome, c1.whatsapp, c1.email, c1.cnpj, c1.caixas, c1.procura, c1.consentimento_lgpd, c1.website], ['Maria da Silva', '(11) 98765-4321', 'maria@empresa.com.br', '11222333000181', 3, 'c6pay', true, '']);
    assert.deepStrictEqual([c1.utm_source, c1.utm_medium, c1.utm_campaign, c1.gclid, c1.ref], ['google', 'cpc', 'pagamento_integrado', 'XYZ', 'site_institucional']);
    if (lib) assert.ok(lib.validarEtapa1(c1).ok, JSON.stringify(lib.validarEtapa1(c1)));
    const conv = await eventos(p, 'conversion'); assert.strictEqual(conv.length, 1); assert.strictEqual(conv[0].send_to, SEND_TO);
    assert.strictEqual(await p.textContent('#v-razao'), 'EMPRESA EXEMPLO LTDA'); assert.strictEqual(await p.textContent('#v-cnpj'), CNPJ); assert.strictEqual(await p.textContent('#v-cidade'), 'São Paulo/SP');
    assert.ok(await p.isHidden('#c-razao'));
    await p.click('#b-correto'); assert.ok(await p.isVisible('#m-correto'));
    assert.ok(await p.isHidden('#c-faixa') && await p.isHidden('#c-vendas') && await p.isHidden('#c-receb'));
    await p.check('input[name=produtos][value=link]');
    assert.ok(await p.isVisible('#c-faixa') && await p.isHidden('#c-vendas') && await p.isHidden('#c-receb'), 'só link');
    await p.uncheck('input[name=produtos][value=link]'); await p.check('input[name=produtos][value=tef]');
    assert.ok(await p.isHidden('#c-faixa') && await p.isVisible('#c-vendas') && await p.isVisible('#c-receb'), 'só TEF');
    assert.strictEqual(await p.locator('#f-faixa option[value]:not([value=""])').count(), 8);
    await p.check('input[name=produtos][value=link]');
    await p.fill('#f-sistema', 'PDVet'); await p.fill('#f-lojas', '2'); await p.selectOption('#f-faixa', '201_600');
    await p.check('input[name=vendas_cartao][value="8_30mil"]'); await p.check('input[name=recebimento][value=d1]'); await p.check('input[name=conta_pj_c6][value=sim]');
    assert.match(await p.textContent('#pf-e2'), /Se você parar aqui, tudo bem: nossa equipe comercial entra em contato para completar\./);
    assert.ok(!/me ligue/i.test(await p.textContent('main')));
    await p.click('#b2'); await p.waitForSelector('#pf-fim:not([hidden])');
    const c2 = reqs[1].corpo;
    assert.deepStrictEqual(c2, { lead_id: 'a'.repeat(24), pedido_token: 'b'.repeat(32), razao_social: 'EMPRESA EXEMPLO LTDA', sistema_pdv: 'PDVet', lojas: 2, produtos: ['tef', 'link'], conta_pj_c6: 'sim', website: '', faixa_link: '201_600', vendas_cartao: '8_30mil', recebimento: 'd1' });
    if (lib) assert.ok(lib.validarEtapa2(c2, { lead_id: c2.lead_id, pedido_token: c2.pedido_token, procura: 'c6pay' }).ok);
    assert.strictEqual(await p.textContent('#pf-fim h1'), 'Sua proposta foi enviada.');
    assert.strictEqual(await p.textContent('#v-email'), 'maria@empresa.com.br');
    assert.match(await p.textContent('#t-fim'), /Spam e Promoções/);
    assert.strictEqual(await p.textContent('#pf-fim a[data-wa]'), 'Tirar dúvidas no WhatsApp');
    for (const sel of ['#pf-e1 a[data-wa]', '#pf-fim a[data-wa]']) assert.strictEqual(new URL(await p.getAttribute(sel, 'href')).searchParams.get('text'), 'Olá! Vim pelo site da Antere e quero saber mais sobre as soluções.\n\nOrigem: google / cpc / pagamento_integrado', sel);
    assert.strictEqual((await eventos(p, 'conversion')).length, 1, 'a etapa 2 não conta outra conversão');
    await ctx.close();
  });

  await t('formulário: CNPJ não consultado pede a razão social digitada; "Corrigir" abre o campo', async () => {
    const { ctx, reqs } = await contexto(b, { webhooks: etapa1Ok({ cnpj_confirmado: false, razao_social: '', cidade: '', uf: '' }, 'c6pay') }); const p = await ctx.newPage();
    await p.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p, 'c6pay'); await p.click('#b1'); await p.waitForSelector('#pf-e2:not([hidden])');
    assert.ok(await p.isHidden('#bloco-empresa')); assert.ok(await p.isVisible('#f-razao'));
    await p.fill('#f-sistema', 'Nenhum'); await p.fill('#f-lojas', '1'); await p.check('input[name=produtos][value=link]'); await p.selectOption('#f-faixa', 'acima_10000'); await p.check('input[name=conta_pj_c6][value=nao]');
    await p.click('#b2'); assert.strictEqual(await p.textContent('#e-razao_social'), 'Informe a razão social.'); assert.strictEqual(reqs.length, 1);
    await p.fill('#f-razao', 'Minha Empresa Ltda'); await p.click('#b2'); await p.waitForSelector('#pf-fim:not([hidden])');
    assert.strictEqual(reqs[1].corpo.razao_social, 'Minha Empresa Ltda'); assert.ok(!('vendas_cartao' in reqs[1].corpo)); assert.ok(await p.isVisible('#t-escalonar'));
    await ctx.close();
    const x = await contexto(b, { webhooks: etapa1Ok(EMP, 'c6pay') }); const p2 = await x.ctx.newPage();
    await p2.goto(BASE + '/proposta.html?previa=1'); await preencheE1(p2, 'c6pay'); await p2.click('#b1'); await p2.waitForSelector('#pf-e2:not([hidden])');
    await p2.click('#b-corrigir'); assert.ok(await p2.isVisible('#f-razao')); await p2.fill('#f-razao', 'Nome Corrigido SA');
    await p2.fill('#f-sistema', 'Linx'); await p2.fill('#f-lojas', '1'); await p2.check('input[name=produtos][value=tef]'); await p2.check('input[name=vendas_cartao][value=ate_8mil]'); await p2.check('input[name=recebimento][value=d31]'); await p2.check('input[name=conta_pj_c6][value=sim]');
    await p2.click('#b2'); await p2.waitForSelector('#pf-fim:not([hidden])'); assert.strictEqual(x.reqs[1].corpo.razao_social, 'Nome Corrigido SA'); assert.ok(!('faixa_link' in x.reqs[1].corpo));
    await x.ctx.close();
  });

  await t('formulário PDVet: tela "Seu contato está registrado" com o botão para o portal da PDVet; 1 conversão', async () => {
    const { ctx } = await contexto(b, { webhooks: etapa1Ok(EMP, 'pdvet') }); const p = await ctx.newPage();
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
          const cobre = [...document.querySelectorAll('a[href*="/form/proposta"]')].some(c => { if (!c.offsetParent) return false; const b = c.getBoundingClientRect(); return b.width && b.left < fr.right && b.right > fr.left && b.top < fr.bottom && b.bottom > fr.top; });
          return { vis, cobre };
        });
        checagens++; if (r.cobre) { ocultou++; assert.ok(!r.vis, pg + ' y=' + y); }
      }
      await p.close();
    }
    assert.ok(checagens > 100 && ocultou > 0, checagens + ' ' + ocultou);
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
  console.log(`${ok} testes ok, ${falhas} falharam` + (lib ? ' (com as regras do n8n)' : ' (sem o antere-automacao ao lado: regras do n8n não conferidas)'));
  process.exitCode = falhas ? 1 : 0;
})();
