# -*- coding: utf-8 -*-
# Componentes do site (15/10/2026): chave do formulário em 2 etapas, conversão do Google Ads, WhatsApp flutuante e o formulário.
# Usados por build_site.py e copiados iguais para as páginas de public/. Contrato do formulário com o n8n:
# antere-automacao/docs/contrato_formulario_site.md.

WHATSAPP_NUMERO = "5511955032670"  # atendimento com IA (o mesmo "WhatsApp comercial" da página de contato e da Campanha TEF)
WHATSAPP_MSG = "Olá! Vim pelo site da Antere e quero saber mais sobre as soluções."
WEBHOOK_ETAPA1 = "https://raregoat-n8n.cloudfy.live/webhook/site-proposta-etapa1"
WEBHOOK_ETAPA2 = "https://raregoat-n8n.cloudfy.live/webhook/site-proposta-etapa2"
FORM_ANTIGO = "https://raregoat-n8n.cloudfy.live/form/proposta?ref=site_institucional"
URL_PDVET = "https://portal.pdvet.com.br/cadastro"
ADS_SEND_TO = "AW-18479570694/4-TPCPzV6ZcdEIa-3-tE"

# ---- AS CHAVES -------------------------------------------------------------------------------------------------------
# public/site-config.js (fora de assets/, que tem cache de 1 ano). false = desligada; true = ligada. Ver o README.
SITE_CONFIG_JS = """/* Chave do formulário de proposta em 2 etapas (antere-site, README, seção "Chave do formulário").
   false: os botões "Quero minha proposta" levam ao formulário antigo do n8n (/form/proposta) e a conversão do Google Ads
          dispara no clique do botão.
   true:  os botões levam a /proposta.html (formulário em 2 etapas) e a conversão dispara no envio com sucesso da etapa 1.
   Só ligar depois de os webhooks site-proposta-etapa1/2 estarem publicados e do teste de ponta a ponta. */
window.ANTERE_FORM_NOVO = false;

/* Chave do aviso de cookies (LGPD), README, seção "Aviso de cookies".
   false: a tag do Google Ads carrega em toda visita, como antes, e não aparece aviso.
   true:  aparece a faixa "Aceitar" / "Recusar"; a tag só carrega depois do "Aceitar" e a escolha fica guardada no navegador.
   Só ligar depois da validação da conversão do Google Ads. */
window.ANTERE_COOKIES = false;
"""

SWITCH_SCRIPT = r"""
<script>
/* Chave do formulário (15/10/2026): com window.ANTERE_FORM_NOVO === true (site-config.js), os links de proposta passam a
   levar a /proposta.html com os mesmos parâmetros (ref e UTM). Desligada ou sem site-config.js, nada muda. */
(function(){if(window.ANTERE_FORM_NOVO!==true)return;
var as=document.querySelectorAll('a[href*="/form/proposta"]');
for(var i=0;i<as.length;i++){try{var u=new URL(as[i].href,window.location.href);as[i].href='/proposta.html'+u.search}catch(e){}}
})();
</script>
"""

CONV_SCRIPT = r"""
<script>
/* Google Ads (09/10/2026): conversão no clique de qualquer link para /form/proposta. ATIVA desde 10/10/2026; esvaziar ROTULO desliga (send_to = AW-18479570694/<rótulo>).
   15/10/2026: com a chave do formulário ligada (ANTERE_FORM_NOVO), a conversão passa a ser no envio da etapa 1 e o clique não conta. */
(function(){var ROTULO='4-TPCPzV6ZcdEIa-3-tE';if(!ROTULO)return;
document.addEventListener('click',function(e){if(window.ANTERE_FORM_NOVO===true)return;var a=e.target&&e.target.closest?e.target.closest('a[href*="/form/proposta"]'):null;if(!a||typeof window.gtag!=='function')return;
try{window.gtag('event','conversion',{send_to:'AW-18479570694/'+ROTULO})}catch(x){}},true);
})();
</script>
"""

WA_FLOAT = """
<style>
.wa-float{position:fixed;right:16px;bottom:calc(16px + var(--faixa-cookies,0px) + env(safe-area-inset-bottom,0px));z-index:30;display:inline-flex;align-items:center;gap:.5rem;padding:.7rem 1.05rem .7rem .85rem;border-radius:999px;background:#0F7B40;color:#fff;font:600 .95rem/1.1 'Sora',ui-sans-serif,system-ui,sans-serif;text-decoration:none;box-shadow:0 6px 20px rgba(0,0,0,.25);transition:opacity .15s ease,transform .15s ease}
.wa-float:hover{background:#0B6534}
.wa-float:focus-visible{outline:3px solid #D9822B;outline-offset:2px}
.wa-float svg{width:22px;height:22px;flex:none}
.wa-float.wa-oculto{opacity:0;visibility:hidden;pointer-events:none;transform:translateY(8px)}
@media (max-width:760px){body{padding-bottom:80px}}
@media print{.wa-float{display:none}}
</style>
<a class="wa-float" id="wa-float" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener" data-wa="flutuante" aria-label="Fale com a gente pelo WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.2 20.8l4.5-1.2A8.8 8.8 0 1 0 12 3.2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .5.4l.7 1.6c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5.6 1 1.4 1.8 2.4 2.3.2.1.4.1.5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.3.1.3.3.3.5 0 .5-.2 1.1-.7 1.4-.6.4-1.4.5-2.3.2-1.9-.6-3.6-2-4.6-3.8-.6-1-.8-2.4-.3-3.6z" fill="currentColor"/></svg><span>Fale com a gente</span></a>
""" % (WHATSAPP_NUMERO, __import__('urllib.parse').parse.quote(WHATSAPP_MSG))

WA_SCRIPT = r"""
<script>
/* WhatsApp (15/10/2026): links com data-wa levam ao atendimento com IA com a mensagem padrão e a origem (UTM) da visita;
   o clique em qualquer link do WhatsApp vira o evento whatsapp_click no Google Ads, sem conversão. O botão flutuante some
   quando estaria por cima de um botão de proposta. */
(function(){var NUM='__NUM__',MSG='__MSG__',g=null,q=null;
try{g=JSON.parse(window.sessionStorage.getItem('antere_utm')||'null')}catch(e){g=null}
try{q=new URLSearchParams(window.location.search)}catch(e){q=null}
function v(k){return String((q&&q.get(k))||(g&&g[k])||'').slice(0,100)}
var o=[v('utm_source'),v('utm_medium'),v('utm_campaign')].filter(Boolean).join(' / ');
var href='https://wa.me/'+NUM+'?text='+encodeURIComponent(MSG+(o?'\n\nOrigem: '+o:''));
var ws=document.querySelectorAll('a[data-wa]');for(var i=0;i<ws.length;i++)ws[i].href=href;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href*="wa.me/"]'):null;if(!a||typeof window.gtag!=='function')return;
try{window.gtag('event','whatsapp_click',{local:a.getAttribute('data-wa')||'link',pagina:window.location.pathname,utm_source:v('utm_source'),utm_medium:v('utm_medium'),utm_campaign:v('utm_campaign'),gclid:v('gclid')})}catch(x){}},true);
var f=document.getElementById('wa-float');if(!f)return;
var SEL='a[href*="/form/proposta"],a[href*="proposta.html"]',pend=false;
function confere(){pend=false;f.classList.remove('wa-oculto');var r=f.getBoundingClientRect(),m=10,cobre=false,cs=document.querySelectorAll(SEL);
for(var j=0;j<cs.length&&!cobre;j++){var c=cs[j];if(c===f||!c.offsetParent)continue;var b=c.getBoundingClientRect();
if(b.width&&b.height&&b.left<r.right+m&&b.right>r.left-m&&b.top<r.bottom+m&&b.bottom>r.top-m)cobre=true}
if(cobre)f.classList.add('wa-oculto')}
function agenda(){if(!pend){pend=true;(window.requestAnimationFrame||setTimeout)(confere)}}
window.addEventListener('scroll',agenda,{passive:true});window.addEventListener('resize',agenda);document.addEventListener('click',agenda);agenda();
})();
</script>
""".replace('__NUM__', WHATSAPP_NUMERO).replace('__MSG__', WHATSAPP_MSG)

# <head>: site-config.js e a tag do Google Ads. A tag carrega na hora com ANTERE_COOKIES desligada (como antes de 15/10) e, com
# ela ligada, só depois do "Aceitar" (escolha em localStorage "antere_cookies"). As legais usam o endereço absoluto do site-config.js,
# porque também são servidas em legal.antere.com.br.
ADS_ID = "AW-18479570694"
def gtag_head(config_src="/site-config.js"):
    return """<script src="%s"></script>
<!-- Google Ads (09/10/2026): tag global gtag.js, ID %s. 15/10/2026: carregada por script, para obedecer ao aviso de cookies quando ligado -->
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','%s');
(function(){var feito=false;window.antereCarregarAds=function(){if(feito)return;feito=true;var t=document.createElement('script');t.async=true;t.src='https://www.googletagmanager.com/gtag/js?id=%s';document.head.appendChild(t)};
if(window.ANTERE_COOKIES!==true){window.antereCarregarAds();return}
var c=null;try{c=JSON.parse(window.localStorage.getItem('antere_cookies')||'null')}catch(e){c=null}
if(c&&c.escolha==='aceito')window.antereCarregarAds()})();</script>
""" % (config_src, ADS_ID, ADS_ID, ADS_ID)
GTAG_HEAD = gtag_head()
GTAG_HEAD_LEGAL = gtag_head("https://www.antere.com.br/site-config.js")

COOKIE_SCRIPT = r"""
<style>
.cookie-faixa{position:fixed;left:0;right:0;bottom:0;z-index:40;background:#1C1E2A;color:#F1EFEA;border-top:1px solid #2C2F3E;box-shadow:0 -6px 20px rgba(0,0,0,.25);padding:1rem 16px calc(1rem + env(safe-area-inset-bottom,0px));font:400 .95rem/1.45 'Source Sans 3',ui-sans-serif,system-ui,sans-serif}
.cookie-faixa .cf-in{max-width:1120px;margin:0 auto;display:flex;flex-wrap:wrap;gap:.75rem 1.25rem;align-items:center;justify-content:space-between}
.cookie-faixa p{margin:0;flex:1 1 320px}
.cookie-faixa a{color:#A3A0F5}
.cookie-faixa .cf-bt{display:flex;gap:.6rem;flex:0 0 auto}
.cookie-faixa button{font:600 .95rem/1 'Sora',ui-sans-serif,system-ui,sans-serif;min-height:44px;padding:.65rem 1.2rem;border-radius:999px;border:2px solid #7B76F0;background:#7B76F0;color:#0F1020;cursor:pointer}
.cookie-faixa button:focus-visible{outline:3px solid #D9822B;outline-offset:2px}
@media (max-width:520px){.cookie-faixa .cf-bt{flex:1 1 100%}.cookie-faixa button{flex:1}}
body.cookies-aberto{padding-bottom:calc(var(--faixa-cookies,0px) + 16px)}
@media print{.cookie-faixa{display:none}}
</style>
<script>
/* Aviso de cookies (15/10/2026), atrás da chave ANTERE_COOKIES (site-config.js). Desligada: não faz nada.
   Ligada: sem escolha guardada, mostra a faixa; "Aceitar" carrega a tag do Google Ads (antereCarregarAds, no <head>) e "Recusar" não;
   a escolha fica em localStorage "antere_cookies". O link "Preferências de cookies" no rodapé reabre a faixa. */
(function(){if(window.ANTERE_COOKIES!==true)return;var K='antere_cookies',f=null;
function le(){try{return JSON.parse(window.localStorage.getItem(K)||'null')}catch(e){return null}}
function grava(v){try{window.localStorage.setItem(K,JSON.stringify({escolha:v,em:new Date().toISOString()}))}catch(e){}}
function altura(){document.documentElement.style.setProperty('--faixa-cookies',(f&&!f.hidden?f.offsetHeight:0)+'px')}
function fecha(){if(f)f.hidden=true;document.body.classList.remove('cookies-aberto');altura()}
function abre(){if(!f){f=document.createElement('div');f.className='cookie-faixa';f.id='cookie-faixa';f.setAttribute('role','region');f.setAttribute('aria-label','Aviso de cookies');
 f.innerHTML='<div class="cf-in"><p>Usamos cookies e a tag do Google Ads só para medir o resultado dos nossos anúncios. Você escolhe se aceita. Saiba mais na <a href="https://legal.antere.com.br/privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</p><div class="cf-bt"><button type="button" id="cookie-recusar">Recusar</button><button type="button" id="cookie-aceitar">Aceitar</button></div></div>';
 document.body.appendChild(f);
 f.querySelector('#cookie-aceitar').addEventListener('click',function(){grava('aceito');fecha();if(window.antereCarregarAds)window.antereCarregarAds()});
 f.querySelector('#cookie-recusar').addEventListener('click',function(){grava('recusado');fecha()});
 window.addEventListener('resize',altura)}
 f.hidden=false;document.body.classList.add('cookies-aberto');altura()}
var cols=document.querySelector('footer .cols');if(cols){var a=document.createElement('a');a.href='#';a.id='cookie-preferencias';a.textContent='Preferências de cookies';a.addEventListener('click',function(e){e.preventDefault();abre()});cols.appendChild(a)}
if(!le())abre();
})();
</script>
"""

# ---- FORMULÁRIO (proposta.html) -------------------------------------------------------------------------------------
FORM_HEAD = """<meta name="robots" content="noindex">
<style>
.top .btn-primary{display:none}
.pf section{padding-block:clamp(1.5rem,5vw,3.5rem)}
.pf-wrap{max-width:640px}
.pf-passo{display:grid;gap:1.1rem}
.pf-passo h1{font-size:clamp(1.7rem,6vw,2.4rem)}
.pf-destaque{background:var(--indigo-tint);border-left:4px solid var(--indigo);border-radius:10px;padding:.9rem 1rem;font-family:var(--font-display);font-weight:600;color:var(--ink);font-size:1.02rem}
.pf form{display:grid;gap:1.05rem}
.pf .campo{display:grid;gap:.35rem}
.pf label,.pf legend{font-weight:600;color:var(--ink)}
.pf .dica{color:var(--ink-3);font-size:.9rem}
.pf input[type=text],.pf input[type=email],.pf input[type=tel],.pf input[type=number],.pf select{font:inherit;font-size:1.05rem;width:100%;min-height:50px;padding:.7rem .85rem;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
.pf fieldset{border:0;margin:0;padding:0;display:grid;gap:.5rem}
.pf .opcao{display:flex;gap:.7rem;align-items:flex-start;padding:.8rem .9rem;border:1px solid var(--line);border-radius:10px;background:var(--surface);cursor:pointer;font-weight:500}
.pf .opcao input{width:20px;height:20px;margin:.15rem 0 0;flex:none;accent-color:var(--indigo)}
.pf .opcao:has(input:checked){border-color:var(--indigo);background:var(--indigo-tint)}
.pf .consent{font-weight:400;font-size:.95rem;color:var(--ink-2)}
.pf .erro{color:#C0392B;font-size:.92rem;font-weight:600;margin:0}
.pf .erro:empty{display:none}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .pf .erro{color:#FF8A7A}}
:root[data-theme="dark"] .pf .erro{color:#FF8A7A}
.pf [aria-invalid="true"]{border-color:#C0392B!important}
.pf .btn{justify-content:center;min-height:52px;font-size:1.02rem}
.pf .btn-primary[disabled]{opacity:.65;cursor:progress}
.pf .acoes{display:grid;gap:.75rem}
@media (min-width:600px){.pf .acoes{grid-template-columns:auto auto;justify-content:start}}
.pf .aviso{color:var(--ink-2);font-size:.95rem}
.pf .status{color:var(--ink);font-weight:600}
.pf .status:empty{display:none}
.pf .empresa{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1.1rem 1.2rem;display:grid;gap:.5rem}
.pf .empresa dl{display:grid;grid-template-columns:auto 1fr;gap:.25rem .9rem;margin:0}
.pf .empresa dt{color:var(--ink-3)}
.pf .empresa dd{margin:0;font-weight:600;color:var(--ink);overflow-wrap:anywhere}
.pf .empresa .acoes{grid-template-columns:1fr}
@media (min-width:480px){.pf .empresa .acoes{grid-template-columns:1fr 1fr}}
.pf .btn{white-space:normal;text-align:center;line-height:1.2}
.pf .ok-marca{color:var(--petroleo);font-weight:600}
.pf .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.pf [hidden]{display:none!important}
</style>
"""

FORM_BODY = r"""
<main class="pf">
<section><div class="wrap pf-wrap">

<div class="pf-passo" id="pf-e1">
  <span class="eyebrow">Etapa 1 de 2</span>
  <h1 tabindex="-1">Quero minha proposta</h1>
  <p class="pf-destaque">C6 Pay: crédito a partir de 1,84% recebendo em 31 dias, débito a partir de 0,82% e Pix grátis e ilimitado.</p>
  <form id="f1" novalidate>
    <div class="campo"><label for="f-nome">Nome completo</label><input id="f-nome" name="nome" type="text" autocomplete="name" maxlength="80" required><p class="erro" id="e-nome"></p></div>
    <div class="campo"><label for="f-whatsapp">WhatsApp</label><input id="f-whatsapp" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="(11) 91234-5678" maxlength="16" required><p class="erro" id="e-whatsapp"></p></div>
    <div class="campo"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" maxlength="120" required><span class="dica">A proposta chega neste e-mail.</span><p class="erro" id="e-email"></p></div>
    <div class="campo"><label for="f-cnpj">CNPJ</label><input id="f-cnpj" name="cnpj" type="text" inputmode="numeric" autocomplete="off" placeholder="00.000.000/0000-00" maxlength="18" required><p class="erro" id="e-cnpj"></p></div>
    <div class="campo"><label for="f-caixas">Nº de caixas</label><input id="f-caixas" name="caixas" type="number" inputmode="numeric" min="1" max="999" step="1" required><span class="dica">Quantos pontos de venda (caixas) a empresa tem.</span><p class="erro" id="e-caixas"></p></div>
    <fieldset class="campo" id="g-procura"><legend>O que você procura?</legend>
      <label class="opcao"><input type="radio" name="procura" value="c6pay" required> C6 Pay: crédito a partir de 1,84% recebendo em 31 dias, débito a partir de 0,82% e Pix grátis</label>
      <label class="opcao"><input type="radio" name="procura" value="pdvet"> Sistema PDV (PDVet)</label>
      <p class="erro" id="e-procura"></p></fieldset>
    <div class="campo"><label class="opcao consent"><input type="checkbox" id="f-lgpd" name="consentimento_lgpd" required> <span>Concordo com o uso dos meus dados para elaboração da proposta, conforme a LGPD e a <a href="https://legal.antere.com.br/privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</span></label><p class="erro" id="e-consentimento_lgpd"></p></div>
    <label class="hp" aria-hidden="true">Site<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
    <p class="status" id="s1" role="status" aria-live="polite"></p>
    <div class="acoes"><button class="btn btn-primary" type="submit" id="b1">Continuar</button></div>
  </form>
  <p><a class="btn btn-ghost" data-wa="formulario_etapa1" href="https://wa.me/__NUM__" target="_blank" rel="noopener">Falar no WhatsApp</a></p>
</div>

<div class="pf-passo" id="pf-pdvet" hidden>
  <span class="eyebrow">Sistema PDV (PDVet)</span>
  <h1 tabindex="-1">Seu contato está registrado.</h1>
  <p class="lede">Para conhecer e contratar o sistema PDV, continue no formulário da PDVet.</p>
  <div class="acoes"><a class="btn btn-primary" id="l-pdvet" href="__PDVET__" rel="noopener">Continuar no site da PDVet</a></div>
</div>

<div class="pf-passo" id="pf-e2" hidden>
  <span class="eyebrow">Etapa 2 de 2 · C6 Pay</span>
  <h1 tabindex="-1">Falta pouco para sua proposta</h1>
  <form id="f2" novalidate>
    <div class="empresa" id="bloco-empresa">
      <strong>Sua empresa (consultada pelo CNPJ)</strong>
      <dl><dt>Razão social</dt><dd id="v-razao"></dd><dt>CNPJ</dt><dd id="v-cnpj"></dd><dt>Cidade/UF</dt><dd id="v-cidade"></dd></dl>
      <div class="acoes" id="acoes-empresa"><button class="btn btn-ghost" type="button" id="b-correto">Os dados estão corretos</button><button class="btn btn-ghost" type="button" id="b-corrigir">Corrigir</button></div>
      <p class="ok-marca" id="m-correto" hidden>Dados confirmados.</p>
    </div>
    <div class="campo" id="c-razao" hidden><label for="f-razao">Razão social</label><input id="f-razao" name="razao_social" type="text" autocomplete="organization" maxlength="120"><span class="dica" id="d-razao"></span><p class="erro" id="e-razao_social"></p></div>
    <div class="campo"><label for="f-sistema">Sistema PDV</label><input id="f-sistema" name="sistema_pdv" type="text" maxlength="80" required><span class="dica">O sistema de caixa que você usa hoje. Se não usa nenhum, escreva "nenhum".</span><p class="erro" id="e-sistema_pdv"></p></div>
    <div class="campo"><label for="f-lojas">Nº de lojas</label><input id="f-lojas" name="lojas" type="number" inputmode="numeric" min="1" max="999" step="1" required><p class="erro" id="e-lojas"></p></div>
    <fieldset class="campo" id="g-produtos"><legend>Produtos</legend>
      <label class="opcao"><input type="checkbox" name="produtos" value="tef"> TEF integrado ao caixa</label>
      <label class="opcao"><input type="checkbox" name="produtos" value="link"> Link de pagamento / pagamento online</label>
      <p class="erro" id="e-produtos"></p></fieldset>
    <div class="campo" id="c-faixa" hidden><label for="f-faixa">Vendas por mês no link de pagamento</label>
      <select id="f-faixa" name="faixa_link"><option value="">Escolha a faixa</option><option value="ate_200">Até 200</option><option value="201_600">201 a 600</option><option value="601_1000">601 a 1.000</option><option value="1001_1500">1.001 a 1.500</option><option value="1501_3000">1.501 a 3.000</option><option value="3001_6000">3.001 a 6.000</option><option value="6001_10000">6.001 a 10.000</option><option value="acima_10000">Acima de 10.000</option></select>
      <p class="erro" id="e-faixa_link"></p></div>
    <fieldset class="campo" id="c-vendas" hidden><legend>Vendas no cartão por mês</legend>
      <label class="opcao"><input type="radio" name="vendas_cartao" value="ate_8mil"> Até R$ 8 mil</label>
      <label class="opcao"><input type="radio" name="vendas_cartao" value="8_30mil"> R$ 8 mil a R$ 30 mil</label>
      <label class="opcao"><input type="radio" name="vendas_cartao" value="acima_30mil"> Acima de R$ 30 mil</label>
      <p class="erro" id="e-vendas_cartao"></p></fieldset>
    <fieldset class="campo" id="c-receb" hidden><legend>Recebimento</legend>
      <label class="opcao"><input type="radio" name="recebimento" value="d1"> D+1 com antecipação</label>
      <label class="opcao"><input type="radio" name="recebimento" value="d31"> D+31 sem antecipação</label>
      <p class="erro" id="e-recebimento"></p></fieldset>
    <fieldset class="campo" id="g-conta"><legend>Tem ou vai abrir conta PJ no C6 Bank?</legend><span class="dica">Com a conta PJ C6, a taxa de implantação (R$ 200) é isenta.</span>
      <label class="opcao"><input type="radio" name="conta_pj_c6" value="sim"> Sim</label>
      <label class="opcao"><input type="radio" name="conta_pj_c6" value="nao"> Não</label>
      <p class="erro" id="e-conta_pj_c6"></p></fieldset>
    <label class="hp" aria-hidden="true">Site<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
    <p class="status" id="s2" role="status" aria-live="polite"></p>
    <div class="acoes"><button class="btn btn-primary" type="submit" id="b2">Receber minha proposta</button></div>
    <p class="aviso">Se você parar aqui, tudo bem: nossa equipe comercial entra em contato para completar.</p>
  </form>
</div>

<div class="pf-passo" id="pf-fim" hidden>
  <span class="eyebrow">Pronto</span>
  <h1 tabindex="-1">Sua proposta foi enviada.</h1>
  <p class="lede" id="t-fim">Enviamos para <strong id="v-email"></strong>. Se não encontrar na caixa de entrada, procure também nas pastas Spam e Promoções.</p>
  <p class="aviso" id="t-escalonar" hidden>Pelo volume informado, um consultor vai falar com você para ajustar a proposta.</p>
  <div class="acoes"><a class="btn btn-primary" data-wa="formulario_fim" href="https://wa.me/__NUM__" target="_blank" rel="noopener">Tirar dúvidas no WhatsApp</a></div>
</div>

</div></section>
</main>
""".replace('__NUM__', WHATSAPP_NUMERO).replace('__PDVET__', URL_PDVET)

FORM_JS = r"""
<script>
/* Formulário de proposta em 2 etapas (15/10/2026). Contrato: antere-automacao/docs/contrato_formulario_site.md.
   Com a chave desligada (site-config.js), a página manda o visitante ao formulário antigo; ?previa=1 abre mesmo assim (teste). */
(function(){
var E1='__E1__',E2='__E2__',ANTIGO='__ANTIGO__',PDVET='__PDVET__',SEND_TO='__SENDTO__',K='antere_form_site';
var q;try{q=new URLSearchParams(window.location.search)}catch(e){q=new URLSearchParams('')}
var ORIG=['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','ref'];
if(window.ANTERE_FORM_NOVO!==true&&q.get('previa')!=='1'){var u0=new URL(ANTIGO);ORIG.forEach(function(k){var v=q.get(k);if(v&&k!=='ref')u0.searchParams.set(k,v)});window.location.replace(u0.toString());return}
var g=null;try{g=JSON.parse(window.sessionStorage.getItem('antere_utm')||'null')}catch(e){g=null}
function origem(){var o={};ORIG.forEach(function(k){var v=q.get(k)||(g&&g[k])||'';o[k]=String(v).slice(0,200)});if(!o.ref)o.ref='site_institucional';return o}
var $=function(id){return document.getElementById(id)};
var st={};try{st=JSON.parse(window.sessionStorage.getItem(K)||'{}')||{}}catch(e){st={}}
function salva(){try{window.sessionStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function mostra(id){['pf-e1','pf-pdvet','pf-e2','pf-fim'].forEach(function(x){$(x).hidden=(x!==id)});window.scrollTo(0,0);var h=$(id).querySelector('h1');if(h)h.focus({preventScroll:true})}
var MSG={nome:{obrigatorio:'Informe seu nome completo.',invalido:'Informe seu nome completo.'},whatsapp:{obrigatorio:'Informe seu WhatsApp com DDD.',invalido:'Confira o WhatsApp: use o DDD e o número.'},
 email:{obrigatorio:'Informe seu e-mail.',invalido:'Confira o e-mail.'},cnpj:{obrigatorio:'Informe o CNPJ.',invalido:'Confira o CNPJ: os números não batem.'},
 caixas:{obrigatorio:'Informe o número de caixas.',invalido:'Use um número de 1 a 999.'},procura:{obrigatorio:'Escolha o que você procura.',invalido:'Escolha o que você procura.'},
 consentimento_lgpd:{obrigatorio:'Para continuar, marque a concordância com o uso dos dados.',invalido:'Para continuar, marque a concordância com o uso dos dados.'},
 razao_social:{obrigatorio:'Informe a razão social.',invalido:'Confira a razão social.'},sistema_pdv:{obrigatorio:'Informe o sistema PDV (ou "nenhum").',invalido:'Confira o sistema PDV.'},
 lojas:{obrigatorio:'Informe o número de lojas.',invalido:'Use um número de 1 a 999.'},produtos:{obrigatorio:'Escolha pelo menos um produto.',invalido:'Escolha pelo menos um produto.'},
 faixa_link:{obrigatorio:'Escolha a faixa de vendas por mês.',invalido:'Escolha a faixa de vendas por mês.'},vendas_cartao:{obrigatorio:'Escolha quanto vende no cartão.',invalido:'Escolha quanto vende no cartão.'},
 recebimento:{obrigatorio:'Escolha o recebimento.',invalido:'Escolha o recebimento.'},conta_pj_c6:{obrigatorio:'Responda sobre a conta PJ C6.',invalido:'Responda sobre a conta PJ C6.'}};
var ALVO={nome:'f-nome',whatsapp:'f-whatsapp',email:'f-email',cnpj:'f-cnpj',caixas:'f-caixas',procura:'g-procura',consentimento_lgpd:'f-lgpd',razao_social:'f-razao',sistema_pdv:'f-sistema',lojas:'f-lojas',produtos:'g-produtos',faixa_link:'f-faixa',vendas_cartao:'c-vendas',recebimento:'c-receb',conta_pj_c6:'g-conta'};
function limpaErros(f){var es=f.querySelectorAll('.erro');for(var i=0;i<es.length;i++)es[i].textContent='';var iv=f.querySelectorAll('[aria-invalid]');for(var j=0;j<iv.length;j++)iv[j].removeAttribute('aria-invalid')}
function marca(lista){var primeiro=null;(lista||[]).forEach(function(x){var e=$('e-'+x.campo);if(!e)return;e.textContent=(MSG[x.campo]||{})[x.erro]||'Confira este campo.';var a=$(ALVO[x.campo]);if(a){a.setAttribute('aria-invalid','true');a.setAttribute('aria-describedby','e-'+x.campo);if(!primeiro)primeiro=a}});
 if(primeiro){var foco=primeiro.matches('input,select')?primeiro:primeiro.querySelector('input');(foco||primeiro).focus();primeiro.scrollIntoView({block:'center'})}}
function dig(v){return String(v||'').replace(/\D/g,'')}
function cnpjOk(v){var d=dig(v);if(d.length!==14||/^(\d)\1{13}$/.test(d))return false;function dv(b){var w=b.length===12?[5,4,3,2,9,8,7,6,5,4,3,2]:[6,5,4,3,2,9,8,7,6,5,4,3,2],s=0;for(var i=0;i<b.length;i++)s+=+b[i]*w[i];var r=s%11;return r<2?0:11-r}return dv(d.slice(0,12))===+d[12]&&dv(d.slice(0,13))===+d[13]}
function zapOk(v){var d=dig(v).replace(/^55(?=\d{10,11}$)/,'');return /^[1-9]\d(9\d{8}|[2-8]\d{7})$/.test(d)}
function mCnpj(v){var d=dig(v).slice(0,14),r=d.slice(0,2);if(d.length>2)r+='.'+d.slice(2,5);if(d.length>5)r+='.'+d.slice(5,8);if(d.length>8)r+='/'+d.slice(8,12);if(d.length>12)r+='-'+d.slice(12);return r}
function mZap(v){var d=dig(v);if(d.length>11&&d.indexOf('55')===0)d=d.slice(2);d=d.slice(0,11);if(!d)return'';if(d.length<3)return'('+d;var n=d.slice(2),c=n.length>8?5:4;return'('+d.slice(0,2)+') '+n.slice(0,c)+(n.length>c?'-'+n.slice(c):'')}
function int(v){var s=String(v||'').trim();return /^\d{1,3}$/.test(s)?+s:NaN}
$('f-cnpj').addEventListener('input',function(){this.value=mCnpj(this.value)});
$('f-whatsapp').addEventListener('input',function(){this.value=mZap(this.value)});
function radio(f,n){var r=f.querySelector('input[name="'+n+'"]:checked');return r?r.value:''}
function envia(url,corpo){var c=window.AbortController?new AbortController():null,t=c?setTimeout(function(){c.abort()},30000):0;
 return fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(corpo),signal:c?c.signal:undefined})
  .then(function(r){clearTimeout(t);return r.json().catch(function(){return{}}).then(function(j){return{status:r.status,j:j||{}}})},function(e){clearTimeout(t);throw e})}
var FALHA='Não foi possível enviar agora. Tente de novo em instantes ou fale com a gente no WhatsApp.';
function conversao(){if(typeof window.gtag==='function'){try{window.gtag('event','conversion',{send_to:SEND_TO})}catch(e){}}}

// ---------- etapa 1
var f1=$('f1'),b1=$('b1'),s1=$('s1');
f1.addEventListener('submit',function(e){e.preventDefault();limpaErros(f1);s1.textContent='';
 var c={nome:f1.nome.value.trim(),whatsapp:f1.whatsapp.value.trim(),email:f1.email.value.trim(),cnpj:dig(f1.cnpj.value),caixas:f1.caixas.value.trim(),procura:radio(f1,'procura'),consentimento_lgpd:$('f-lgpd').checked,website:f1.website.value};
 var er=[];
 if(c.nome.length<2||!/[A-Za-zÀ-ÿ]/.test(c.nome))er.push({campo:'nome',erro:c.nome?'invalido':'obrigatorio'});
 if(!zapOk(c.whatsapp))er.push({campo:'whatsapp',erro:c.whatsapp?'invalido':'obrigatorio'});
 if(!/^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$/.test(c.email))er.push({campo:'email',erro:c.email?'invalido':'obrigatorio'});
 if(!cnpjOk(c.cnpj))er.push({campo:'cnpj',erro:c.cnpj?'invalido':'obrigatorio'});
 var cx=int(c.caixas);if(!(cx>=1&&cx<=999))er.push({campo:'caixas',erro:c.caixas?'invalido':'obrigatorio'});
 if(!c.procura)er.push({campo:'procura',erro:'obrigatorio'});
 if(!c.consentimento_lgpd)er.push({campo:'consentimento_lgpd',erro:'obrigatorio'});
 if(er.length){marca(er);return}
 c.caixas=cx;var o=origem();for(var k in o)c[k]=o[k];
 b1.disabled=true;s1.textContent='Enviando e consultando o CNPJ…';
 envia(E1,c).then(function(x){var j=x.j;b1.disabled=false;s1.textContent='';
  if(x.status===200&&j.ok){
   if(j.proximo==='pdvet'){conversao();$('l-pdvet').href=(j.url&&/^https:\/\//.test(j.url))?j.url:PDVET;mostra('pf-pdvet');return}
   if(j.proximo==='etapa2'&&j.lead_id&&j.pedido_token){conversao();st.lead_id=j.lead_id;st.pedido_token=j.pedido_token;st.email=c.email;st.cnpj=c.cnpj;st.empresa=j.empresa||{};salva();preparaE2();mostra('pf-e2');return}
   mostra('pf-fim');$('t-fim').textContent='Recebemos seus dados. Nossa equipe comercial entra em contato.';return}
  if(x.status===422&&j.erros){marca(j.erros);return}
  s1.textContent=j.mensagem||FALHA}).catch(function(){b1.disabled=false;s1.textContent=FALHA})});

// ---------- etapa 2
var f2=$('f2'),b2=$('b2'),s2=$('s2');
function preparaE2(){var em=st.empresa||{},conf=em.cnpj_confirmado===true&&em.razao_social;
 $('v-cnpj').textContent=mCnpj(st.cnpj||'');
 if(conf){$('bloco-empresa').hidden=false;$('v-razao').textContent=em.razao_social;$('v-cidade').textContent=[em.cidade,em.uf].filter(Boolean).join('/')||'—';$('c-razao').hidden=true;$('f-razao').value=em.razao_social;st.razaoConfirmada=false}
 else{$('bloco-empresa').hidden=true;$('c-razao').hidden=false;$('f-razao').value='';$('d-razao').textContent='Não conseguimos consultar o CNPJ agora. Digite a razão social da empresa.'}}
$('b-correto').addEventListener('click',function(){$('acoes-empresa').hidden=true;$('m-correto').hidden=false;$('c-razao').hidden=true;$('f-razao').value=(st.empresa||{}).razao_social||''});
$('b-corrigir').addEventListener('click',function(){$('acoes-empresa').hidden=true;$('m-correto').hidden=true;$('c-razao').hidden=false;$('d-razao').textContent='Digite a razão social correta.';$('f-razao').focus()});
function produtos(){var r=[],cs=f2.querySelectorAll('input[name="produtos"]:checked');for(var i=0;i<cs.length;i++)r.push(cs[i].value);return r}
function condicionais(){var p=produtos();$('c-faixa').hidden=p.indexOf('link')<0;$('c-vendas').hidden=p.indexOf('tef')<0;$('c-receb').hidden=p.indexOf('tef')<0}
f2.addEventListener('change',function(e){if(e.target&&e.target.name==='produtos')condicionais()});
f2.addEventListener('submit',function(e){e.preventDefault();limpaErros(f2);s2.textContent='';
 var p=produtos(),c={lead_id:st.lead_id,pedido_token:st.pedido_token,razao_social:$('f-razao').value.trim(),sistema_pdv:f2.sistema_pdv.value.trim(),lojas:f2.lojas.value.trim(),produtos:p,conta_pj_c6:radio(f2,'conta_pj_c6'),website:f2.website.value};
 if(p.indexOf('link')>=0)c.faixa_link=$('f-faixa').value;
 if(p.indexOf('tef')>=0){c.vendas_cartao=radio(f2,'vendas_cartao');c.recebimento=radio(f2,'recebimento')}
 var er=[];
 if(c.razao_social.length<2){er.push({campo:'razao_social',erro:'obrigatorio'});$('c-razao').hidden=false}
 if(!c.sistema_pdv)er.push({campo:'sistema_pdv',erro:'obrigatorio'});
 var lj=int(c.lojas);if(!(lj>=1&&lj<=999))er.push({campo:'lojas',erro:c.lojas?'invalido':'obrigatorio'});
 if(!p.length)er.push({campo:'produtos',erro:'obrigatorio'});
 if(p.indexOf('link')>=0&&!c.faixa_link)er.push({campo:'faixa_link',erro:'obrigatorio'});
 if(p.indexOf('tef')>=0&&!c.vendas_cartao)er.push({campo:'vendas_cartao',erro:'obrigatorio'});
 if(p.indexOf('tef')>=0&&!c.recebimento)er.push({campo:'recebimento',erro:'obrigatorio'});
 if(!c.conta_pj_c6)er.push({campo:'conta_pj_c6',erro:'obrigatorio'});
 if(er.length){marca(er);return}
 c.lojas=lj;b2.disabled=true;s2.textContent='Enviando…';
 envia(E2,c).then(function(x){var j=x.j;b2.disabled=false;s2.textContent='';
  if((x.status===200&&j.ok)||j.erro==='ja_enviado'){$('v-email').textContent=j.email||st.email||'';$('t-escalonar').hidden=!j.escalonar;st={};salva();mostra('pf-fim');return}
  if(x.status===422&&j.erros){marca(j.erros);return}
  if(j.erro==='pedido_nao_encontrado'){st={};salva();s2.textContent='Não encontramos seu pedido. Preencha a etapa 1 de novo.';setTimeout(function(){mostra('pf-e1')},2500);return}
  s2.textContent=j.mensagem||FALHA}).catch(function(){b2.disabled=false;s2.textContent=FALHA})});

if(st.lead_id&&st.pedido_token){preparaE2();mostra('pf-e2')}
})();
</script>
""".replace('__E1__', WEBHOOK_ETAPA1).replace('__E2__', WEBHOOK_ETAPA2).replace('__ANTIGO__', FORM_ANTIGO).replace('__PDVET__', URL_PDVET).replace('__SENDTO__', ADS_SEND_TO)
