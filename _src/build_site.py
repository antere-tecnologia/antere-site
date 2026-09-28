# -*- coding: utf-8 -*-
import os
FORM = "https://raregoat-n8n.cloudfy.live/form/proposta?ref=site_institucional"
SITE = "https://www.antere.com.br"
CONTATO_WEBHOOK = "https://raregoat-n8n.cloudfy.live/webhook/site-contato"

CSS = r"""
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="assets/icon-192.png"><link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png"><meta name="theme-color" content="#3A34D6">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
:root{
  --indigo:#3A34D6; --indigo-ink:#2B27A8; --indigo-tint:#EDEBFC; --indigo-soft:#C7C6F5;
  --petroleo:#12786B; --petroleo-tint:#E4F5F1; --ambar:#D9822B; --ambar-tint:#FBF0E0;
  --ground:#F7F5F1; --surface:#FFFFFF; --line:#E5E1D8; --ink:#1B1E27; --ink-2:#4A4E5B; --ink-3:#8B8F9C;
  --on-accent:#F7F5F1;
  --font-display:'Sora',ui-sans-serif,system-ui,sans-serif; --font-body:'Source Sans 3',ui-sans-serif,system-ui,sans-serif;
  --radius:14px; --gutter:clamp(16px,4vw,48px);
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --indigo:#7B76F0; --indigo-ink:#A3A0F5; --indigo-tint:#23244A; --indigo-soft:#3C3A7A;
  --petroleo:#3FB39F; --petroleo-tint:#123530; --ambar:#E39A4E; --ambar-tint:#3A2A14;
  --ground:#12131A; --surface:#1C1E2A; --line:#2C2F3E; --ink:#F1EFEA; --ink-2:#C4C6D0; --ink-3:#8B8F9C; --on-accent:#0F1020;
}}
:root[data-theme="dark"]{
  --indigo:#7B76F0; --indigo-ink:#A3A0F5; --indigo-tint:#23244A; --indigo-soft:#3C3A7A;
  --petroleo:#3FB39F; --petroleo-tint:#123530; --ambar:#E39A4E; --ambar-tint:#3A2A14;
  --ground:#12131A; --surface:#1C1E2A; --line:#2C2F3E; --ink:#F1EFEA; --ink-2:#C4C6D0; --ink-3:#8B8F9C; --on-accent:#0F1020;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--font-body);font-size:17px;line-height:1.55}
h1,h2,h3{font-family:var(--font-display);line-height:1.12;letter-spacing:-0.015em;text-wrap:balance;margin:0}
h1{font-size:clamp(2rem,5.2vw,3.4rem);font-weight:700}
h2{font-size:clamp(1.5rem,3.2vw,2.2rem);font-weight:600}
h3{font-size:1.15rem;font-weight:600}
p{margin:0}
a{color:var(--indigo)}
.wrap{max-width:1120px;margin:0 auto;padding-inline:var(--gutter)}
.eyebrow{font-family:var(--font-display);font-size:.78rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--petroleo)}
.lede{font-size:1.15rem;color:var(--ink-2);max-width:60ch}
.btn{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--font-display);font-weight:600;font-size:.98rem;padding:.85rem 1.35rem;border-radius:999px;text-decoration:none;border:2px solid transparent;transition:transform .15s ease,background .15s ease}
.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid var(--ambar);outline-offset:2px}
.btn-primary{background:var(--indigo);color:var(--on-accent)}
.btn-primary:hover{background:var(--indigo-ink);transform:translateY(-1px)}
.btn-ghost{background:transparent;color:var(--indigo);border-color:var(--indigo-soft)}
.btn-ghost:hover{background:var(--indigo-tint)}
/* header */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:color-mix(in srgb,var(--ground) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:68px}
.brand{display:flex;align-items:center;gap:.6rem;text-decoration:none;color:var(--ink)}
.brand img{display:block;height:38px;width:auto}
.brand img.logo-dark,.slogan img.logo-dark{display:none}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]) .brand img.logo-light,:root:not([data-theme="light"]) .slogan img.logo-light{display:none} :root:not([data-theme="light"]) .brand img.logo-dark,:root:not([data-theme="light"]) .slogan img.logo-dark{display:block} }
:root[data-theme="dark"] .brand img.logo-light,:root[data-theme="dark"] .slogan img.logo-light{display:none}
:root[data-theme="dark"] .brand img.logo-dark,:root[data-theme="dark"] .slogan img.logo-dark{display:block}
@media (max-width:480px){ .brand img{height:32px} }
nav.menu{display:flex;gap:1.3rem;align-items:center}
nav.menu a{color:var(--ink-2);text-decoration:none;font-weight:500;font-size:.98rem;padding:.3rem 0;border-bottom:2px solid transparent}
nav.menu a[aria-current="page"]{color:var(--ink);border-bottom-color:var(--indigo)}
nav.menu a:hover{color:var(--ink)}
.top .btn{padding:.6rem 1.05rem;font-size:.9rem}
.menu-toggle{display:none;background:none;border:1px solid var(--line);border-radius:10px;padding:.45rem .6rem;color:var(--ink);font:inherit}
@media (max-width:760px){
  nav.menu{display:none;position:absolute;left:0;right:0;top:100%;background:var(--surface);border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;padding:.5rem var(--gutter) 1rem;gap:.2rem}
  nav.menu.open{display:flex}
  nav.menu a{padding:.7rem 0;border-bottom:1px solid var(--line)}
  .menu-toggle{display:inline-block}
  .top .btn-primary{display:none}
}
/* sections */
section{padding-block:clamp(3rem,7vw,5.5rem)}
.section-head{display:grid;gap:.75rem;max-width:64ch;margin-bottom:2.2rem}
.grid-3{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.25rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1.5rem;display:grid;gap:.6rem;align-content:start}
.card h3{color:var(--ink)}
.card p{color:var(--ink-2)}
.card .k{font-family:var(--font-display);font-size:1.7rem;font-weight:700;color:var(--indigo);font-variant-numeric:tabular-nums}
footer{border-top:1px solid var(--line);padding-block:2.5rem;color:var(--ink-3);font-size:.92rem}
footer .wrap{display:grid;gap:1.2rem}
footer .slogan img{display:block;height:auto;width:min(100%,360px)}
footer .cols{display:flex;flex-wrap:wrap;gap:1.5rem 2.5rem}
footer a{color:var(--ink-2);text-decoration:none}
footer a:hover{text-decoration:underline}
.note{display:flex;gap:.6rem;align-items:flex-start;background:var(--ambar-tint);border-left:4px solid var(--ambar);border-radius:8px;padding:.85rem 1rem;color:var(--ink);font-size:.95rem}
.note b{font-family:var(--font-display);font-weight:600}
.skeleton{border:2px dashed var(--line);border-radius:var(--radius);padding:1.5rem;color:var(--ink-3);display:grid;gap:.6rem}
.skeleton .bar{height:12px;border-radius:6px;background:var(--line);width:78%}
.skeleton .bar.s{width:46%}
@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}
</style>
"""

def nav(active):
    items = [("index.html","Home"),("como-funciona.html","Como funciona"),("solucoes.html","Soluções"),("calculadora.html","Calculadora"),("sobre.html","Sobre"),("contato.html","Contato")]
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h==active else '', t) for h,t in items)
    return f"""
<header class="top"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Antere, página inicial"><img class="logo-light" src="assets/logo-h-light.png" alt="Antere" width="560" height="178"><img class="logo-dark" src="assets/logo-h-dark.png" alt="" aria-hidden="true" width="560" height="178"></a>
  <button class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav class="menu" id="menu" aria-label="Principal">{links}</nav>
  <a class="btn btn-primary" href="{FORM}">Quero minha proposta</a>
</div></header>
"""

FOOTER = f"""
<footer><div class="wrap">
  <div class="slogan"><img class="logo-light" src="assets/logo-slogan-light.png" alt="Antere. Automação comercial, do caixa ao pagamento." width="720" height="186" loading="lazy"><img class="logo-dark" src="assets/logo-slogan-dark.png" alt="" aria-hidden="true" width="720" height="186" loading="lazy"></div>
  <div class="cols">
    <a href="{FORM}">Solicitar proposta</a>
    <a href="como-funciona.html">Como funciona</a>
    <a href="solucoes.html">Soluções</a>
    <a href="calculadora.html">Calculadora de economia</a>
    <a href="sobre.html">Sobre</a>
    <a href="contato.html">Contato</a>
  </div>
  <div>Antere Tecnologia (F. de Carvalho Spahn Consultoria em Tecnologia da Informação LTDA). Seus dados são usados exclusivamente para elaborar sua proposta comercial, conforme a LGPD.</div>
</div></footer>
<script>
(function(){{var b=document.getElementById('menu-toggle'),m=document.getElementById('menu');if(!b)return;b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}})();
</script>
"""

UTM_SCRIPT = r"""
<script>
/* UTM (28/09/2026): guarda utm_source, utm_medium, utm_campaign e gclid da chegada (sessionStorage, 1ª chegada da sessão) e acrescenta aos links de proposta (/form/proposta), mantendo o ref. */
(function(){var K=['utm_source','utm_medium','utm_campaign','gclid'],S='antere_utm',g=null,q;
try{q=new URLSearchParams(window.location.search)}catch(e){return}
var c={},tem=false;for(var i=0;i<K.length;i++){var v=q.get(K[i]);if(v){c[K[i]]=String(v).slice(0,200);tem=true}}
try{g=JSON.parse(window.sessionStorage.getItem(S)||'null')}catch(e){g=null}
if(!g&&tem){g=c;try{window.sessionStorage.setItem(S,JSON.stringify(g))}catch(e){}}
if(!g)return;
var as=document.querySelectorAll('a[href*="/form/proposta"]');
for(var j=0;j<as.length;j++){try{var u=new URL(as[j].href,window.location.href);for(var k=0;k<K.length;k++){if(g[K[k]]&&!u.searchParams.get(K[k]))u.searchParams.set(K[k],g[K[k]])}as[j].href=u.toString()}catch(e){}}
})();
</script>
"""

def page(title, description, active, body, extra_head="", extra_script="", standalone=True):
    canon = SITE + "/" + ("" if active == "index.html" else active)
    head = (f"<title>{title}</title>\n<meta name=\"description\" content=\"{description}\">\n"
            f"<link rel=\"canonical\" href=\"{canon}\">\n"
            f"<meta property=\"og:type\" content=\"website\"><meta property=\"og:site_name\" content=\"Antere\"><meta property=\"og:locale\" content=\"pt_BR\">\n"
            f"<meta property=\"og:title\" content=\"{title}\"><meta property=\"og:description\" content=\"{description}\"><meta property=\"og:url\" content=\"{canon}\">\n"
            f"<meta property=\"og:image\" content=\"{SITE}/assets/og-image.png\"><meta name=\"twitter:card\" content=\"summary_large_image\">\n"
            + CSS + extra_head)
    content = head + nav(active) + body + FOOTER + UTM_SCRIPT + extra_script
    if standalone:
        return "<!doctype html>\n<html lang=\"pt-BR\" data-theme=\"dark\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + head + "</head>\n<body>\n" + nav(active) + body + FOOTER + UTM_SCRIPT + extra_script + "\n</body>\n</html>\n"
    return content

# ---------------- HOME ----------------
HOME_CSS = r"""
<style>
.hero{padding-block:clamp(2.5rem,6vw,5rem) clamp(2rem,5vw,4rem)}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(2rem,5vw,4.5rem);align-items:center}
.hero-copy{display:grid;gap:1.3rem}
.hero-copy h1 em{font-style:normal;color:var(--indigo)}
.hero-ctas{display:flex;flex-wrap:wrap;gap:.75rem;align-items:center}
.hero-meta{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;color:var(--ink-3);font-size:.92rem}
.hero-meta span::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--petroleo);margin-right:.5rem;vertical-align:middle}
@media (max-width:860px){.hero .wrap{grid-template-columns:1fr}}
/* demo */
.demo{background:var(--indigo);border-radius:22px;padding:1.4rem;color:var(--on-accent);display:grid;gap:1rem;position:relative;overflow:hidden}
.demo .steps{display:flex;gap:.4rem}
.demo .steps span{flex:1;height:5px;border-radius:3px;background:rgba(255,255,255,.28);position:relative;overflow:hidden}
.demo .steps span i{position:absolute;inset:0;background:var(--on-accent);transform:scaleX(0);transform-origin:left}
.demo .steps span.done i{transform:scaleX(1)}
.demo .steps span.active i{animation:fill 3.6s linear forwards}
@keyframes fill{to{transform:scaleX(1)}}
.demo .label{display:flex;justify-content:space-between;align-items:baseline;font-family:var(--font-display);font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;opacity:.85}
.demo .label b{font-size:1rem;letter-spacing:0;text-transform:none;opacity:1}
.stage{display:grid}
.panel{grid-area:1/1;background:var(--surface);color:var(--ink);border-radius:16px;padding:1.2rem;display:grid;gap:.7rem;align-content:start;opacity:0;transform:translateY(10px);transition:opacity .45s ease,transform .45s ease;pointer-events:none}
.panel.show{opacity:1;transform:none}
.panel h3{font-size:1rem}
.field{display:grid;gap:.25rem;font-size:.85rem;color:var(--ink-3)}
.field div{border:1px solid var(--line);border-radius:8px;padding:.45rem .6rem;color:var(--ink);background:var(--ground);min-height:2.1rem;font-variant-numeric:tabular-nums}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}
.pdf{border:1px solid var(--line);border-radius:10px;padding:.9rem;display:grid;gap:.4rem;background:var(--ground)}
.pdf .t{font-family:var(--font-display);font-weight:600}
.pdf .l{display:flex;justify-content:space-between;font-size:.92rem;color:var(--ink-2);font-variant-numeric:tabular-nums}
.pdf .l b{color:var(--ink)}
.ok{display:flex;align-items:center;gap:.7rem;padding:.7rem .8rem;border-radius:10px;background:var(--petroleo-tint);color:var(--petroleo);font-weight:600}
.ok i{width:22px;height:22px;border-radius:50%;background:var(--petroleo);display:inline-grid;place-items:center;color:#fff;font-style:normal;font-size:.8rem}
.chip{display:inline-block;padding:.2rem .6rem;border-radius:999px;background:var(--indigo-tint);color:var(--indigo);font-size:.8rem;font-family:var(--font-display);font-weight:600}
.demo .caption{font-size:.9rem;opacity:.9}
/* journey */
.journey{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;counter-reset:j}
.journey .j{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1.4rem;display:grid;gap:.5rem;position:relative}
.journey .j::before{counter-increment:j;content:counter(j);font-family:var(--font-display);font-weight:700;color:var(--indigo);font-size:.9rem;background:var(--indigo-tint);width:28px;height:28px;border-radius:50%;display:grid;place-items:center}
.journey .j p{color:var(--ink-2)}
.journey .j .t{font-size:.85rem;color:var(--petroleo);font-weight:600}
@media (max-width:760px){.journey{grid-template-columns:1fr}}
/* solutions strip */
.strip{background:var(--surface);border-block:1px solid var(--line)}
.strip .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:2.5rem;align-items:center}
.strip ul{margin:0;padding:0;list-style:none;display:grid;gap:.6rem}
.strip li{display:flex;gap:.7rem;align-items:flex-start;color:var(--ink-2)}
.strip li::before{content:"";flex:none;width:9px;height:9px;border-radius:50%;background:var(--petroleo);margin-top:.55rem}
.fast{border:1px solid var(--indigo-soft);background:var(--indigo-tint);border-radius:var(--radius);padding:1.4rem;display:grid;gap:.6rem}
.fast .k{font-family:var(--font-display);font-size:2rem;font-weight:700;color:var(--indigo);font-variant-numeric:tabular-nums}
@media (max-width:860px){.strip .wrap{grid-template-columns:1fr}}
/* topics (atuação integrada) */
.topics{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}
.topics a.card{text-decoration:none;color:inherit;transition:border-color .2s,transform .2s}
.topics a.card:hover{border-color:var(--indigo-soft);transform:translateY(-2px)}
.topics .card .go{color:var(--indigo);font-weight:600;font-size:.92rem}
@media (max-width:760px){.topics{grid-template-columns:1fr}}
/* feature (solução em destaque) */
.feature{background:#1B1E27;color:#F1EFEA}
.feature .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(2rem,5vw,4rem);align-items:center}
.feature .eyebrow{color:#A3A0F5;display:block;margin-bottom:.6rem}
.feature h2{color:#F1EFEA;margin-bottom:.9rem}
.feature p{color:#C4C6D0}
.feature ul{margin:1.2rem 0 0;padding:0;list-style:none;display:grid;gap:.6rem}
.feature li{display:flex;gap:.7rem;align-items:flex-start;font-weight:600;color:#F1EFEA}
.feature li::before{content:"";flex:none;width:9px;height:9px;border-radius:50%;background:var(--petroleo);margin-top:.55rem}
.feature .eco{background:var(--ground);color:var(--ink);border-radius:22px;padding:1.8rem;display:grid;gap:.9rem}
.feature .eco h3{font-size:1.5rem;font-family:var(--font-display)}
.feature .eco .pills{display:flex;flex-wrap:wrap;gap:.5rem}
.feature .eco .pills span{padding:.35rem .75rem;border-radius:999px;border:1px solid var(--line);background:var(--surface);font-size:.88rem;font-weight:600;color:var(--ink-2)}
:root[data-theme="dark"] .feature{background:#1C1E2A;border-block:1px solid var(--line)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .feature{background:#1C1E2A;border-block:1px solid var(--line)}}
@media (max-width:860px){.feature .wrap{grid-template-columns:1fr}}
/* portfolio */
.portfolio{display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem}
.portfolio a.card{text-decoration:none;color:inherit;transition:border-color .2s,transform .2s}
.portfolio a.card:hover{border-color:var(--indigo-soft);transform:translateY(-2px)}
.portfolio .card .eyebrow{color:var(--indigo)}
.portfolio .card.hl{border-color:var(--indigo);box-shadow:0 0 0 1px var(--indigo)}
.callout{margin-top:1.25rem;border:1px solid var(--indigo-soft);background:var(--indigo-tint);border-radius:var(--radius);padding:1.2rem 1.4rem;display:grid;gap:.3rem}
.callout b{font-family:var(--font-display);color:var(--indigo)}
@media (max-width:760px){.portfolio{grid-template-columns:1fr}}
/* hero product stack */
.stack{background:var(--indigo);border-radius:22px;padding:1.4rem;color:var(--on-accent);display:grid;gap:.9rem}
:root[data-theme="dark"] .stack{background:#24216A;color:#E8E7FF;border:1px solid #3C3A7A}
.stack .label{font-family:var(--font-display);font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;opacity:.85}
.stack .row{background:var(--surface);color:var(--ink);border-radius:14px;padding:.95rem 1.1rem;display:grid;gap:.5rem}
.stack .row h3{font-size:1rem}
.stack .chips{display:flex;flex-wrap:wrap;gap:.4rem}
.stack .chips span{padding:.22rem .6rem;border-radius:999px;background:var(--indigo-tint);color:var(--indigo);font-size:.8rem;font-family:var(--font-display);font-weight:600}
.stack .row.alt .chips span{background:var(--petroleo-tint);color:var(--petroleo)}
.stack .caption{font-size:.9rem;opacity:.9}
/* product categories */
.cat{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,2.1fr);gap:clamp(1.5rem,4vw,3.5rem);padding-block:2.2rem;border-top:1px solid var(--line)}
.cat:first-of-type{border-top:0;padding-top:0}
.cat-head{display:grid;gap:.6rem;align-content:start;position:sticky;top:90px}
.cat-head .n{font-family:var(--font-display);font-weight:700;color:var(--indigo);font-size:.85rem;letter-spacing:.06em}
.cat-head h3{font-size:1.45rem}
.cat-head p{color:var(--ink-2)}
.prods{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.1rem}
.prod{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1.3rem;display:grid;gap:.6rem;align-content:start}
.prod.hl{border-color:var(--indigo);box-shadow:0 0 0 1px var(--indigo)}
.prod .tag{font-family:var(--font-display);font-size:.75rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--petroleo)}
.prod h4{font-size:1.1rem;font-weight:600;margin:0}
.prod p{color:var(--ink-2);font-size:.97rem}
.prod ul{margin:.2rem 0 0;padding:0;list-style:none;display:grid;gap:.35rem}
.prod li{display:flex;gap:.55rem;align-items:flex-start;font-size:.93rem;color:var(--ink-2)}
.prod li::before{content:"";flex:none;width:7px;height:7px;border-radius:50%;background:var(--petroleo);margin-top:.5rem}
.prod p a{color:var(--indigo);font-weight:600;text-decoration:none}
.prod p a:hover{text-decoration:underline}
@media (max-width:860px){.cat{grid-template-columns:1fr}.cat-head{position:static}}
/* journey compact (rodapé) */
.journey-wrap{background:var(--surface);border-block:1px solid var(--line)}
/* cta band */
.band{background:var(--ink);color:var(--ground);border-radius:22px;padding:clamp(1.8rem,4vw,3rem);display:grid;grid-template-columns:1.2fr auto;gap:1.5rem;align-items:center}
.band h2{color:var(--ground)}
.band p{color:var(--ink-3)}
@media (max-width:760px){.band{grid-template-columns:1fr}}
</style>
"""

HOME = f"""
<main>
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <span class="eyebrow">Consultoria de automação comercial</span>
    <h1>Automação comercial, <em>do caixa ao pagamento.</em></h1>
    <p class="lede">TEF, link de pagamento, PIX, adquirência e conta digital integrados ao seu sistema de vendas. Uma operação de pagamentos que acompanha o ritmo do seu negócio, com implantação e suporte de ponta a ponta.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="{FORM}">Quero minha proposta</a>
      <a class="btn btn-ghost" href="calculadora.html">Simule sua economia</a>
    </div>
    <div class="hero-meta"><span>Integração com PDV e ERP</span><span>Multiadquirente</span><span>Acompanhamento técnico</span></div>
  </div>
  <div class="stack" aria-label="Ecossistema Antere: automação comercial, meios de pagamento, banking e adquirência">
    <div class="label">Um ecossistema, três frentes</div>
    <div class="row"><h3>Automação comercial</h3><div class="chips"><span>PDVet (pet shops e clínicas)</span><span>Integração PDV / ERP</span><span>Conciliação</span><span>Implantação</span></div></div>
    <div class="row alt"><h3>Meios de pagamento</h3><div class="chips"><span>TEF PayGo</span><span>Link de pagamento</span><span>Gateway</span><span>PIX</span></div></div>
    <div class="row"><h3>Banking e adquirência</h3><div class="chips"><span>Conta digital C6 Bank</span><span>C6 Pay</span><span>Multiadquirente</span></div></div>
    <p class="caption">Tudo conectado ao seu caixa, sem redigitação e sem planilha paralela.</p>
  </div>
</div></section>

<section id="produtos"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Nossos produtos</span>
    <h2>Três frentes, um ecossistema integrado</h2>
    <p class="lede">Escolha o que a sua operação precisa hoje. Tudo se conecta ao mesmo caixa e cresce junto com o negócio.</p>
  </div>

  <div class="cat" id="automacao-comercial">
    <div class="cat-head"><span class="n">01</span><h3>Automação comercial</h3><p>Sistema de gestão para o balcão, integração com PDV e ERP e conciliação, para a venda nascer integrada ao pagamento.</p></div>
    <div class="prods">
      <div class="prod hl" id="pdvet"><span class="tag">Sistema de gestão · Pet shops, clínicas e varejo</span><h4>PDVet</h4><p>Caixa, agenda e cobrança recorrente em um tablet. Nasceu para pet shops e atende clínicas veterinárias e outros comércios de balcão. Revenda e implantação Antere.</p><ul><li>Venda offline: fecha sem internet e sincroniza sozinha</li><li>Caixa com fechamento cego e auditoria de tudo</li><li>Agenda de serviços por profissional (banho e tosa, consultas), com histórico do cliente e do pet</li><li>Lembretes automáticos e cobrança recorrente (assinaturas e pacotes)</li><li>Estoque por movimento, venda por peso ou unidade</li><li>NFC-e, integração com TEF e várias unidades na mesma conta</li><li>Roda no navegador do tablet, sem instalar; terminais ilimitados</li></ul><p><a href="https://pdvet.com.br/" target="_blank" rel="noopener">Conhecer o PDVet →</a></p></div>
      <div class="prod"><span class="tag">Integração</span><h4>Integração PDV e ERP</h4><p>O pagamento acontece dentro do seu sistema de vendas.</p><ul><li>Captura TEF integrada ao PDV, sem redigitar valores</li><li>Homologação do seu sistema com as adquirentes</li><li>Retaguarda e fechamento de caixa conectados</li></ul></div>
      <div class="prod"><span class="tag">Gestão</span><h4>Conciliação e recebíveis</h4><p>Cada venda já nasce casada com o recebível.</p><ul><li>Conciliação automática de cartão e PIX</li><li>Agenda de recebíveis por adquirente</li><li>Relatórios para financeiro e gestão</li></ul></div>
      <div class="prod"><span class="tag">Consultoria</span><h4>Diagnóstico e implantação</h4><p>Acompanhamento técnico do desenho à operação.</p><ul><li>Diagnóstico da operação e dos canais de venda</li><li>Escolha de adquirentes e bancos que fazem sentido</li><li>Cadastro, instalação, treinamento e suporte contínuo</li></ul></div>
    </div>
  </div>

  <div class="cat" id="meios-de-pagamento">
    <div class="cat-head"><span class="n">02</span><h3>Meios de pagamento</h3><p>Uma jornada de pagamento segura, integrada e preparada para crescer, no balcão e fora dele.</p></div>
    <div class="prods">
      <div class="prod hl" id="tef-paygo"><span class="tag">Presencial</span><h4>TEF PayGo</h4><p>Captura TEF integrada ao PDV para uma operação sem atrito.</p><ul><li>Integrado ao sistema de vendas, sem digitação manual</li><li>Multiadquirente e multibandeira no mesmo terminal</li><li>Débito, crédito, voucher e PIX no TEF</li><li>Terminais e caixas ilimitados</li><li>Conciliação automática das transações</li><li>Suporte e homologação de ponta a ponta</li></ul></div>
      <div class="prod" id="gateway"><span class="tag">Digital</span><h4>Link de pagamento e Gateway</h4><p>Venda fora do balcão com a mesma segurança do caixa.</p><ul><li>Link de pagamento por WhatsApp, e-mail e redes sociais</li><li>Checkout para loja virtual e aplicativos</li><li>Cartão, PIX e boleto com parcelamento</li><li>Antifraude e tokenização</li><li>Integração com ERP e plataformas de cobrança</li><li>Painel de vendas e conciliação unificados</li></ul></div>
    </div>
  </div>

  <div class="cat" id="banking">
    <div class="cat-head"><span class="n">03</span><h3>Banking e adquirência</h3><p>Conta, recebíveis e adquirência conectados, para vender, receber e controlar no mesmo lugar.</p></div>
    <div class="prods">
      <div class="prod" id="c6-bank"><span class="tag">Banking</span><h4>Conta digital C6 Bank</h4><p>Conta empresarial integrada aos recebíveis.</p><ul><li>PIX empresarial e boletos</li><li>Agenda de recebíveis na própria conta</li><li>Crédito e APIs para integração financeira</li></ul></div>
      <div class="prod" id="c6-pay"><span class="tag">Adquirência</span><h4>C6 Pay</h4><p>Experiência completa de pagamento no ponto de venda.</p><ul><li>Cartão, voucher, aproximação, PIX e link</li><li>PINPad integrado ao TEF PayGo</li><li>Recebíveis direto na conta C6 Bank</li></ul></div>
      <div class="prod"><span class="tag">Multiadquirência</span><h4>Demais adquirentes e bancos</h4><p>Integramos os parceiros que a sua operação já usa.</p><ul><li>Roteamento por adquirente no mesmo TEF</li><li>Sem forçar troca de fornecedor</li><li>Comparativo de condições na proposta</li></ul></div>
    </div>
  </div>
</div></section>

<section class="feature"><div class="wrap">
  <div>
    <span class="eyebrow">Produto em destaque</span>
    <h2>TEF PayGo para uma operação de pagamentos sem atrito</h2>
    <p>Da venda registrada no PDV à autorização da adquirente, a Antere apoia uma jornada integrada, segura e fluida, sem digitação manual de valores.</p>
    <ul>
      <li>Integração com o ecossistema comercial: PDV, ERP e retaguarda</li>
      <li>Terminais e caixas ilimitados, multibandeira e multiadquirente</li>
      <li>Acompanhamento técnico de ponta a ponta, da homologação à ativação</li>
    </ul>
  </div>
  <div class="eco">
    <span class="eyebrow">Ecossistema conectado</span>
    <h3>Preparado para integrar.</h3>
    <div class="pills"><span>Windows</span><span>Android</span><span>Linux</span><span>Web / API</span></div>
    <p style="color:var(--ink-2)">Compatível com os principais sistemas de PDV do mercado. Se o seu ainda não estiver homologado, a homologação faz parte da implantação.</p>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">O que muda no seu dia a dia</span>
    <h2>Menos erro de caixa, conciliação em minutos, tudo no mesmo lugar</h2>
  </div>
  <div class="grid-3">
    <div class="card"><span class="k">0</span><h3>redigitação de valor</h3><p>Com TEF integrado ao sistema de vendas, o valor vai direto para a maquininha. Acaba o erro de digitação no fechamento.</p></div>
    <div class="card"><span class="k">min</span><h3>em vez de horas na conciliação</h3><p>Cada venda já nasce casada com o recebível. Você confere, não reconstrói.</p></div>
    <div class="card"><span class="k">1</span><h3>ecossistema para vender e receber</h3><p>PIX, cartão, link de pagamento e conta digital conectados ao mesmo caixa, com um único parceiro acompanhando.</p></div>
  </div>
  <div class="callout" style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between"><div><b>Quanto sua empresa pode economizar?</b><span style="display:block">Compare o que paga hoje em débito, crédito, parcelado e PIX com as condições reais C6 Pay.</span></div><a class="btn btn-primary" href="calculadora.html">Simule sua economia</a></div>
</div></section>

<section class="journey-wrap"><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Como funciona</span>
    <h2>Da primeira conversa ao pagamento ativo no caixa</h2>
    <p class="lede">Três momentos, todos acompanhados pela Antere.</p>
  </div>
  <div class="journey">
    <div class="j"><h3>Diagnóstico</h3><p>Você conta como é a operação: caixas, canais de venda e soluções de interesse. Um formulário curto, sem reunião de descoberta.</p><span class="t">menos de 2 minutos</span></div>
    <div class="j"><h3>Proposta</h3><p>A proposta chega no seu e-mail com as condições para a sua operação, sem esperar retorno de vendedor.</p><span class="t">em instantes</span></div>
    <div class="j"><h3>Ativação</h3><p>Aceite eletrônico, dados de implantação, cadastro nas adquirentes e ativação no seu PDV, com acompanhamento em cada passo.</p><span class="t">até 10 dias úteis</span></div>
  </div>
  <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="como-funciona.html">Ver o passo a passo completo</a></p>
</div></section>

<section><div class="wrap">
  <div class="band">
    <div><h2>Vamos simplificar sua operação de pagamentos?</h2><p>Conte como é o seu negócio e receba uma proposta com as condições ideais para a sua operação.</p></div>
    <a class="btn btn-primary" href="{FORM}">Quero minha proposta</a>
  </div>
</div></section>
</main>
"""

HOME_JS = r"""
"""

# ---------------- COMO FUNCIONA ----------------
COMO = f"""
<style>
.passos{{display:grid;gap:1rem;max-width:760px;counter-reset:p}}
.passo{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:1.3rem 1.4rem;display:grid;grid-template-columns:44px 1fr;gap:1rem;align-items:start}}
.passo .n{{counter-increment:p;font-family:var(--font-display);font-weight:700;color:var(--indigo);background:var(--indigo-tint);width:40px;height:40px;border-radius:50%;display:grid;place-items:center}}
.passo .n::before{{content:counter(p)}}
.passo h3{{margin-bottom:.35rem}}
.passo p{{color:var(--ink-2)}}
.fecho{{margin-top:2.5rem;display:grid;gap:1rem;justify-items:start}}
</style>
<main>
<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Como funciona</span>
    <h1>Da primeira conversa até sua operação rodando com cartão e PIX integrados</h1>
    <p class="lede">Sem burocracia, sem retrabalho, sem você precisar acompanhar cada etapa manualmente.</p>
  </div>
  <div class="passos">
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Você chega até a gente</h3><p>Pelo site, por indicação de um parceiro ou por um contato direto. O primeiro passo é simples: você nos conta um pouco sobre o seu negócio.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Entendemos o seu perfil</h3><p>Analisamos as informações que você compartilhou para já chegar com uma proposta que faz sentido para a realidade da sua empresa, sem processo genérico.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Boas-vindas</h3><p>Você recebe um contato inicial confirmando que estamos com você, com os próximos passos claros.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Sua proposta, personalizada</h3><p>Preparamos uma proposta comercial sob medida, com as condições certas para o seu volume e perfil de negócio. Pronta em minutos, não em dias.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Acompanhamento, sem você precisar cobrar</h3><p>Se surgir qualquer dúvida no caminho, a gente está por perto: lembretes automáticos para você nunca perder o fio da meada, e uma pessoa de verdade disponível sempre que precisar de uma conversa mais próxima.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Conversa e fechamento</h3><p>Quando faz sentido negociar uma condição especial ou tirar uma dúvida mais específica, alguém do nosso time assume a conversa diretamente com você.</p></div></div>
    <div class="passo"><span class="n" aria-hidden="true"></span><div><h3>Ativação</h3><p>Formalizamos tudo de forma eletrônica, coletamos os dados técnicos necessários e cuidamos da ativação junto aos nossos parceiros de pagamento. No final, você só precisa se preocupar em vender.</p></div></div>
  </div>
  <div class="fecho">
    <h2>Pronto para simplificar como sua empresa recebe pagamentos?</h2>
    <div class="hero-ctas"><a class="btn btn-primary" href="{FORM}">Quero minha proposta</a><a class="btn btn-ghost" href="contato.html">Fale com a gente</a></div>
  </div>
</div></section>
</main>
"""

SOL = f"""
<main>
<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Soluções</span>
    <h1>Produtos por categoria</h1>
    <p class="lede">O que a Antere integra ao seu caixa, organizado em três frentes. Detalhe técnico e condições ficam para a proposta e a implantação.</p>
  </div>

  <div class="cat" id="automacao-comercial">
    <div class="cat-head"><span class="n">01</span><h3>Automação comercial</h3><p>Frente de caixa, retaguarda e gestão operacional conectados ao pagamento.</p></div>
    <div class="prods">
      <div class="prod hl" id="pdvet"><span class="tag">Sistema de gestão · Pet shops, clínicas e varejo</span><h4>PDVet</h4><p>Sistema de venda e gestão para pet shops, clínicas veterinárias, banho e tosa e outros comércios de balcão, revendido e implantado pela Antere.</p><ul><li>Venda offline com sincronização automática</li><li>Caixa com fechamento cego e auditoria com autor e data</li><li>Agenda de serviços por profissional (banho e tosa, consultas), com histórico do cliente e do pet</li><li>Lembretes automáticos com confirmação pelo link</li><li>Cobrança recorrente: assinatura de banho, ração programada, pacotes</li><li>Controle de estoque por movimento; venda por peso ou unidade</li><li>Relatórios, dashboard e permissões por usuário</li><li>NFC-e, integração com TEF e várias unidades na mesma conta</li><li>Sua marca nas telas; roda no navegador, sem instalação; terminais ilimitados</li></ul><p><a href="https://pdvet.com.br/" target="_blank" rel="noopener">Conhecer o PDVet →</a></p></div>
      <div class="prod"><span class="tag">Integração</span><h4>Integração PDV e ERP</h4><ul><li>Captura TEF dentro do sistema de vendas</li><li>Homologação do seu PDV com as adquirentes</li><li>Retaguarda e fechamento de caixa conectados</li><li>Sem redigitação de valores</li></ul></div>
      <div class="prod"><span class="tag">Gestão</span><h4>Conciliação e recebíveis</h4><ul><li>Conciliação automática de cartão e PIX</li><li>Agenda de recebíveis por adquirente</li><li>Relatórios para financeiro e gestão</li></ul></div>
      <div class="prod"><span class="tag">Consultoria</span><h4>Diagnóstico e implantação</h4><ul><li>Diagnóstico da operação e dos canais de venda</li><li>Escolha de adquirentes e bancos</li><li>Cadastro, instalação, treinamento e suporte contínuo</li></ul></div>
    </div>
  </div>

  <div class="cat" id="meios-de-pagamento">
    <div class="cat-head"><span class="n">02</span><h3>Meios de pagamento</h3><p>Pagamento presencial e digital com a mesma segurança e a mesma conciliação.</p></div>
    <div class="prods">
      <div class="prod hl" id="tef-paygo"><span class="tag">Presencial</span><h4>TEF PayGo</h4><ul><li>Integrado ao PDV, sem digitação manual</li><li>Multiadquirente e multibandeira</li><li>Débito, crédito, voucher e PIX no TEF</li><li>Terminais e caixas ilimitados</li><li>Conciliação automática</li><li>Compatível com Windows, Android, Linux e Web/API</li><li>Homologação e suporte de ponta a ponta</li></ul></div>
      <div class="prod" id="gateway"><span class="tag">Digital</span><h4>Link de pagamento e Gateway</h4><ul><li>Link por WhatsApp, e-mail e redes sociais</li><li>Checkout para loja virtual e aplicativos</li><li>Cartão, PIX e boleto com parcelamento</li><li>Antifraude e tokenização</li><li>Integração com ERP e plataformas de cobrança</li><li>Painel de vendas e conciliação unificados</li></ul></div>
    </div>
  </div>

  <div class="cat" id="banking">
    <div class="cat-head"><span class="n">03</span><h3>Banking e adquirência</h3><p>Conta, recebíveis e adquirência no mesmo lugar.</p></div>
    <div class="prods">
      <div class="prod" id="c6-bank"><span class="tag">Banking</span><h4>Conta digital C6 Bank</h4><ul><li>Conta empresarial com PIX e boletos</li><li>Agenda de recebíveis na própria conta</li><li>Crédito e APIs para integração financeira</li></ul></div>
      <div class="prod" id="c6-pay"><span class="tag">Adquirência</span><h4>C6 Pay</h4><ul><li>Cartão, voucher, aproximação, PIX e link</li><li>PINPad integrado ao TEF PayGo</li><li>Recebíveis direto na conta C6 Bank</li></ul></div>
      <div class="prod"><span class="tag">Multiadquirência</span><h4>Demais adquirentes e bancos</h4><ul><li>Roteamento por adquirente no mesmo TEF</li><li>Integração com os parceiros que você já usa</li><li>Comparativo de condições na proposta</li></ul></div>
    </div>
  </div>

  <p style="margin-top:2.5rem"><a class="btn btn-primary" href="{FORM}">Quero minha proposta</a></p>
</div></section>
</main>
"""

SOBRE = f"""
<style>
.prose{{max-width:68ch;display:grid;gap:1.1rem;font-size:1.08rem;color:var(--ink-2)}}
.prose p strong{{color:var(--ink)}}
.prose .destaque{{border-left:4px solid var(--indigo);padding:.6rem 1rem;background:var(--indigo-tint);border-radius:8px;color:var(--ink)}}
</style>
<main>
<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Sobre a Antere</span>
    <h1>Automação comercial, do caixa ao pagamento.</h1>
  </div>
  <div class="prose">
    <p>A Antere nasceu de uma pergunta simples: por que configurar uma máquina de cartão, aceitar PIX e formalizar uma venda ainda exige tanto trabalho manual?</p>
    <p>Somos uma consultoria de automação comercial focada em um problema específico: ajudar negócios a aceitar pagamentos de forma integrada. Cartão e PIX, sem retrabalho, sem planilha, sem depender de alguém lembrar de enviar o próximo e-mail.</p>
    <p>Construímos toda a nossa própria operação em cima da mesma automação que oferecemos aos nossos clientes. Da primeira proposta até a ativação, o processo roda sozinho, liberando tempo para o que realmente importa: entender o negócio de cada cliente e encontrar a melhor condição para ele.</p>
    <p>Hoje, essa automação comercial já atende parceiros como a <a href="https://pdvet.com.br/" target="_blank" rel="noopener">PDVet</a>, e esse é só o começo. Nosso objetivo é maior: digitalizar o varejo, trazendo controle real sobre vendas e recebimentos para cada vez mais negócios, com os mesmos benefícios que já entregamos todos os dias: automação de ponta a ponta, sem fricção, sem trabalho manual repetido.</p>
    <p class="destaque">Se você chegou até aqui procurando simplificar como sua empresa recebe pagamentos, é exatamente aí que entramos.</p>
  </div>
  <div class="grid-3" style="margin-top:2.5rem">
    <div class="card"><span class="eyebrow">Quem assina</span><h3>Fernanda Spahn</h3><p>Consultoria comercial. É quem assina as propostas e acompanha cada cliente até a ativação.</p></div>
  </div>
  <p style="margin-top:2rem"><a class="btn btn-primary" href="{FORM}">Quero minha proposta</a></p>
</div></section>
</main>
"""

CONTATO = f"""
<style>
.form{{display:grid;gap:1rem;max-width:560px}}
.form label{{display:grid;gap:.3rem;font-weight:500}}
.form input,.form textarea{{font:inherit;padding:.7rem .8rem;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}}
.form textarea{{min-height:120px;resize:vertical}}
.form .hp{{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}}
.form.sent{{opacity:.6}}
.contact-grid{{display:grid;grid-template-columns:1.1fr .9fr;gap:2.5rem;align-items:start}}
@media (max-width:860px){{.contact-grid{{grid-template-columns:1fr}}}}
</style>
<main>
<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Contato</span>
    <h1>Dúvidas gerais? Fale com a gente</h1>
    <p class="lede">Este formulário é para perguntas e parcerias. Para pedir uma proposta, use o botão "Quero minha proposta": ela chega em minutos.</p>
  </div>
  <div class="contact-grid">
    <form class="form" id="contact-form" novalidate>
      <label for="c-nome">Nome<input id="c-nome" name="nome" type="text" autocomplete="name" required maxlength="120"></label>
      <label for="c-email">E-mail<input id="c-email" name="email" type="email" autocomplete="email" required maxlength="160"></label>
      <label for="c-tel">Telefone (opcional)<input id="c-tel" name="telefone" type="tel" autocomplete="tel" maxlength="40"></label>
      <label for="c-msg">Mensagem<textarea id="c-msg" name="mensagem" required maxlength="2000"></textarea></label>
      <label class="hp" aria-hidden="true">Site<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
      <p class="lgpd-note" style="font-size:13px;opacity:.8;margin:0 0 8px">Ao enviar, você concorda com a nossa <a href="https://legal.antere.com.br/privacidade.html" target="_blank" rel="noopener">Política de Privacidade</a>.</p><div><button class="btn btn-primary" type="submit" id="c-btn">Enviar mensagem</button></div>
      <p id="c-status" role="status" aria-live="polite" style="color:var(--ink-2)"></p>
    </form>
    <div style="display:grid;gap:1rem">
      <div class="card"><h3>WhatsApp comercial</h3><p><a href="https://wa.me/5511955032670">(11) 95503-2670</a></p></div>
      <div class="card"><h3>E-mail</h3><p><a href="mailto:comercial@antere.com.br">comercial@antere.com.br</a></p></div>
      <div class="note"><b>Resposta manual.</b> Mensagens enviadas por aqui são registradas e respondidas pela equipe, normalmente em até 1 dia útil.</div>
    </div>
  </div>
</div></section>
</main>
<script>
(function(){{
var f=document.getElementById('contact-form'),s=document.getElementById('c-status'),b=document.getElementById('c-btn');
f.addEventListener('submit',function(e){{
  e.preventDefault();
  if(!f.checkValidity()){{s.textContent='Preencha nome, e-mail e mensagem para enviar.';return;}}
  var d={{nome:f.nome.value.trim(),email:f.email.value.trim(),telefone:f.telefone.value.trim(),mensagem:f.mensagem.value.trim(),website:f.website.value}};
  b.disabled=true;s.textContent='Enviando…';
  fetch('{CONTATO_WEBHOOK}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}})
   .then(function(r){{return r.json().catch(function(){{return {{ok:r.ok}};}});}})
   .then(function(j){{
     if(j&&j.ok){{s.textContent='Recebemos sua mensagem. Retornaremos em breve.';f.reset();f.classList.add('sent');}}
     else{{s.textContent='Não foi possível enviar: '+((j&&j.erros)?j.erros.join(', '):'tente novamente em instantes.');b.disabled=false;}}
   }})
   .catch(function(){{s.textContent='Falha de conexão. Tente novamente ou escreva para comercial@antere.com.br.';b.disabled=false;}});
}});
}})();
</script>
"""

CALC = f"""
<style>
.calc-wrap{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(1.5rem,4vw,3rem);align-items:start}}
.calc-form{{display:grid;gap:1.1rem}}
.calc-form .card{{gap:.9rem}}
.calc-form label{{display:grid;gap:.3rem;font-weight:500;font-size:.95rem}}
.calc-form input{{font:inherit;padding:.7rem .8rem;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink);width:100%}}
.calc-form input:focus{{border-color:var(--indigo)}}
.row2{{display:grid;grid-template-columns:1fr 1fr;gap:.8rem}}
.toggle-group{{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}}
.toggle-opt{{border:2px solid var(--line);border-radius:12px;padding:.8rem;background:var(--surface);cursor:pointer;text-align:center;font:inherit;font-family:var(--font-display);font-weight:600;color:var(--ink-2)}}
.toggle-opt .desc{{display:block;font-family:var(--font-body);font-weight:400;font-size:.85rem;color:var(--ink-3);margin-top:.15rem}}
.toggle-opt.active{{border-color:var(--indigo);background:var(--indigo-tint);color:var(--indigo)}}
.tier-note{{font-size:.92rem;color:var(--petroleo);font-weight:600;min-height:1.4em}}
.calc-side{{display:grid;gap:1rem;position:sticky;top:90px}}
.result{{background:var(--indigo);color:var(--on-accent);border-radius:22px;padding:1.5rem;display:grid;gap:1rem}}
.result .row{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.result .label{{font-size:.85rem;opacity:.85}}
.result .value{{font-family:var(--font-display);font-size:1.9rem;font-weight:700;font-variant-numeric:tabular-nums}}
.result .annual .value{{font-size:1.5rem}}
.pix-note{{background:var(--ambar-tint);border-left:4px solid var(--ambar);border-radius:8px;padding:.8rem 1rem;font-size:.95rem;color:var(--ink)}}
.disclaimer{{font-size:.85rem;color:var(--ink-3);line-height:1.5}}
.calc-side .btn{{width:100%;justify-content:center}}
#resultado{{display:none;gap:1rem}}
#resultado.show{{display:grid}}
@media (max-width:860px){{.calc-wrap{{grid-template-columns:1fr}}.calc-side{{position:static}}.row2{{grid-template-columns:1fr}}}}
</style>
<main>
<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow">Calculadora de economia</span>
    <h1>Quanto sua empresa pode economizar?</h1>
    <p class="lede">Compare o que você paga hoje com as condições reais C6 Pay e PIX grátis pela conta C6 Bank. É só uma simulação: nada é enviado.</p>
  </div>
  <div class="calc-wrap">
    <form class="calc-form" id="calc-form" onsubmit="event.preventDefault();calcular();">
      <div class="card">
        <h3>Como você prefere receber suas vendas?</h3>
        <div class="toggle-group" role="radiogroup" aria-label="Modo de recebimento">
          <button type="button" class="toggle-opt active" id="opt-d1" role="radio" aria-checked="true" onclick="setRecebimento('D1')">D+1 com antecipação<span class="desc">recebe rápido</span></button>
          <button type="button" class="toggle-opt" id="opt-d31" role="radio" aria-checked="false" onclick="setRecebimento('D31')">D+31 sem antecipação<span class="desc">taxa menor</span></button>
        </div>
      </div>
      <div class="card">
        <h3>Débito</h3>
        <div class="row2">
          <label for="fatDebito">Faturamento mensal<input type="text" id="fatDebito" placeholder="R$ 8.000" inputmode="numeric" oninput="atualizarFaixa()"></label>
          <label for="taxaDebito">Taxa que você paga hoje<input type="text" id="taxaDebito" placeholder="Ex: 1,9%" inputmode="decimal"></label>
        </div>
      </div>
      <div class="card">
        <h3>Crédito à vista</h3>
        <div class="row2">
          <label for="fatCredito">Faturamento mensal<input type="text" id="fatCredito" placeholder="R$ 10.000" inputmode="numeric" oninput="atualizarFaixa()"></label>
          <label for="taxaCredito">Taxa que você paga hoje<input type="text" id="taxaCredito" placeholder="Ex: 3,5%" inputmode="decimal"></label>
        </div>
      </div>
      <div class="card">
        <h3>Crédito parcelado (até 6x)</h3>
        <div class="row2">
          <label for="fatParcelado">Faturamento mensal<input type="text" id="fatParcelado" placeholder="R$ 4.000" inputmode="numeric" oninput="atualizarFaixa()"></label>
          <label for="taxaParcelado">Taxa que você paga hoje<input type="text" id="taxaParcelado" placeholder="Ex: 4,5%" inputmode="decimal"></label>
        </div>
      </div>
      <div class="card">
        <h3>PIX</h3>
        <div class="row2">
          <label for="fatPix">Faturamento mensal recebido via PIX<input type="text" id="fatPix" placeholder="R$ 8.000" inputmode="numeric"></label>
          <label for="taxaPix">Taxa que você paga hoje (se houver)<input type="text" id="taxaPix" placeholder="Ex: 0,99% ou 0" inputmode="decimal"></label>
        </div>
      </div>
      <div class="tier-note" id="tierNote" aria-live="polite"></div>
      <div><button class="btn btn-primary" type="submit" id="btn-calcular">Calcular minha economia</button></div>
    </form>
    <aside class="calc-side">
      <div id="resultado" aria-live="polite">
        <div class="result">
          <div class="row">
            <div class="stat"><div class="label">Economia mensal estimada</div><div class="value" id="econMensal">R$ 0</div></div>
            <div class="stat annual"><div class="label">Economia anual estimada</div><div class="value" id="econAnual">R$ 0</div></div>
          </div>
        </div>
        <div class="pix-note" id="pixNote" style="display:none"></div>
      </div>
      <a class="btn btn-primary" href="{FORM}">Quero uma proposta personalizada</a>
      <p class="disclaimer">Simulação com base na tabela oficial de taxas C6 Pay vigente (débito, crédito à vista e parcelado até 6x), com a faixa de taxa aplicada automaticamente conforme seu volume mensal em cartão (até R$ 8 mil, de R$ 8 mil a R$ 30 mil, ou acima de R$ 30 mil). Vendas parceladas de 7 a 12x têm taxa ligeiramente diferente da usada nesta simulação, e o adicional por parcela do recebimento D+1 será detalhado na sua proposta personalizada. PIX recebido via conta C6 Bank tem tarifa zero, dentro da política vigente do C6 Bank para PJ.</p>
    </aside>
  </div>
</div></section>
</main>
<script>
function parseNumero(str) {{
  if (!str) return 0;
  let limpo = str.replace(/[R$\\s]/g, '').replace(/\\./g, '').replace(',', '.').replace('%', '');
  const num = parseFloat(limpo);
  return isNaN(num) ? 0 : num;
}}
const TABELA_C6 = {{
  D1: {{ ate_8k: {{ debito: 1.07, credito: 3.20, parcelado: 2.59 }}, "8k_30k": {{ debito: 0.82, credito: 2.95, parcelado: 2.14 }}, acima_30k: {{ debito: 0.82, credito: 2.95, parcelado: 2.14 }} }},
  D31: {{ ate_8k: {{ debito: 1.07, credito: 2.09, parcelado: 2.59 }}, "8k_30k": {{ debito: 0.94, credito: 1.96, parcelado: 2.46 }}, acima_30k: {{ debito: 0.82, credito: 1.84, parcelado: 2.34 }} }}
}};
const NOME_FAIXA = {{ ate_8k: "até R$ 8 mil/mês", "8k_30k": "R$ 8 mil a R$ 30 mil/mês", acima_30k: "acima de R$ 30 mil/mês" }};
let recebimentoAtual = 'D1';
function setRecebimento(modo) {{
  recebimentoAtual = modo;
  document.getElementById('opt-d1').classList.toggle('active', modo === 'D1');
  document.getElementById('opt-d31').classList.toggle('active', modo === 'D31');
  document.getElementById('opt-d1').setAttribute('aria-checked', modo === 'D1');
  document.getElementById('opt-d31').setAttribute('aria-checked', modo === 'D31');
  atualizarFaixa();
}}
function getFaixa(totalCartao) {{
  if (totalCartao <= 8000) return 'ate_8k';
  if (totalCartao <= 30000) return '8k_30k';
  return 'acima_30k';
}}
function atualizarFaixa() {{
  const totalCartao = parseNumero(document.getElementById('fatDebito').value) + parseNumero(document.getElementById('fatCredito').value) + parseNumero(document.getElementById('fatParcelado').value);
  const faixa = getFaixa(totalCartao);
  document.getElementById('tierNote').textContent = totalCartao > 0 ? 'Sua faixa de taxa C6 Pay: ' + NOME_FAIXA[faixa] : '';
}}
function calcular() {{
  const fatDebito = parseNumero(document.getElementById('fatDebito').value);
  const taxaDebitoAtual = parseNumero(document.getElementById('taxaDebito').value);
  const fatCredito = parseNumero(document.getElementById('fatCredito').value);
  const taxaCreditoAtual = parseNumero(document.getElementById('taxaCredito').value);
  const fatParcelado = parseNumero(document.getElementById('fatParcelado').value);
  const taxaParceladoAtual = parseNumero(document.getElementById('taxaParcelado').value);
  const fatPix = parseNumero(document.getElementById('fatPix').value);
  const taxaPixAtual = parseNumero(document.getElementById('taxaPix').value);
  const totalCartao = fatDebito + fatCredito + fatParcelado;
  const faixa = getFaixa(totalCartao);
  const taxasC6 = TABELA_C6[recebimentoAtual][faixa];
  const custoAtual = (fatDebito * taxaDebitoAtual / 100) + (fatCredito * taxaCreditoAtual / 100) + (fatParcelado * taxaParceladoAtual / 100) + (fatPix * taxaPixAtual / 100);
  const custoC6 = (fatDebito * taxasC6.debito / 100) + (fatCredito * taxasC6.credito / 100) + (fatParcelado * taxasC6.parcelado / 100) + (fatPix * 0);
  const economiaMensal = Math.max(0, custoAtual - custoC6);
  const economiaAnual = economiaMensal * 12;
  const fmt = (v) => v.toLocaleString('pt-BR', {{ style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }});
  document.getElementById('econMensal').textContent = fmt(economiaMensal);
  document.getElementById('econAnual').textContent = fmt(economiaAnual);
  const pixNoteEl = document.getElementById('pixNote');
  if (fatPix > 0 && taxaPixAtual > 0) {{
    const economiaPixMensal = fatPix * taxaPixAtual / 100;
    pixNoteEl.textContent = 'Só no PIX, você deixaria de pagar ' + fmt(economiaPixMensal) + '/mês em tarifas, porque com a conta C6 Bank o PIX recebido é isento.';
    pixNoteEl.style.display = 'block';
  }} else {{
    pixNoteEl.style.display = 'none';
  }}
  document.getElementById('resultado').classList.add('show');
  if (window.matchMedia('(max-width:860px)').matches) document.getElementById('resultado').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}
</script>
"""


pages = {
  "index.html": ("Antere", "Consultoria de automação comercial: TEF, link de pagamento, PIX, adquirência e conta digital integrados ao seu sistema de vendas.", "index.html", HOME, HOME_CSS, HOME_JS),
  "como-funciona.html": ("Como funciona · Antere", "Sete passos da primeira conversa até sua operação rodando com cartão e PIX integrados, sem burocracia e sem retrabalho.", "como-funciona.html", COMO, HOME_CSS, ""),
  "solucoes.html": ("Soluções · Antere", "Automação comercial, meios de pagamento (TEF e link), banking e adquirência integrados ao seu caixa.", "solucoes.html", SOL, HOME_CSS, ""),
  "sobre.html": ("Sobre · Antere", "A Antere é uma consultoria de automação comercial: pagamentos integrados, do caixa ao pagamento, sem trabalho manual.", "sobre.html", SOBRE, "", ""),
  "calculadora.html": ("Calculadora de economia · Antere", "Simule quanto sua empresa economiza com as taxas C6 Pay e PIX grátis pela conta C6 Bank, comparando com o que paga hoje.", "calculadora.html", CALC, "", ""),
  "contato.html": ("Contato · Antere", "Fale com a Antere para dúvidas gerais e parcerias.", "contato.html", CONTATO, "", ""),
}
for fn,(t,d,a,b,eh,es) in pages.items():
    open(fn,"w",encoding="utf-8").write(page(t,d,a,b,eh,es, standalone=(fn!="index.html")))
    print(fn, os.path.getsize(fn))

open("sitemap.xml","w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join('  <url><loc>%s/%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (SITE, "" if fn=="index.html" else fn, "1.0" if fn=="index.html" else "0.7") for fn in pages) + '</urlset>\n')
open("robots.txt","w",encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
print("sitemap.xml, robots.txt")
