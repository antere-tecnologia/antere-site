# Site institucional Antere

Publicado no Netlify (projeto `antere-site`) a partir da pasta `public/`.

- `public/`: tudo que vai ao ar — páginas (`index.html`, `como-funciona.html`, `solucoes.html`, `sobre.html`, `contato.html`, `calculadora.html`, `404.html`), o formulário `proposta.html` (fora do menu e do sitemap), a chave `site-config.js`, `assets/`, `legal/`, `robots.txt`, `sitemap.xml`, `_headers` e `_redirects`.
- `public/legal/`: Política de Privacidade, Termos de Uso e Exclusão de Dados. Continuam acessíveis em `legal.antere.com.br` pelas regras de `_redirects` (o domínio precisa estar adicionado ao projeto no Netlify).
- `_src/`: gerador das páginas (`build_site.py`), componentes comuns (`componentes.py`: chave, conversão, WhatsApp e o formulário) e logos originais. Não é publicado. Rode `python3 build_site.py` numa cópia de `_src/` e copie os arquivos gerados para `public/`.
  - Atenção: o gerador ainda difere de `public/` em detalhes (linhas em branco, a posição da regra `:root[data-theme="dark"] .stack{...}` e o invólucro do `index.html`). A cor do tema foi alinhada em 15/10/2026. Antes de copiar páginas regeradas por cima de `public/`, compare com `diff` e mantenha o que está publicado.
- `testes/site.test.js`: testes das páginas no Chromium, sem rede (webhooks e gtag simulados). Rodar com `NODE_PATH=$(npm root -g) node testes/site.test.js` (precisa do Playwright). Com o repositório `antere-automacao` ao lado, os corpos enviados ao n8n passam também pelas regras do servidor.
- `netlify.toml`: `publish = "public"`, sem comando de build.

Formulário de contato envia POST para `https://raregoat-n8n.cloudfy.live/webhook/site-contato`.
CTA de proposta aponta para `https://raregoat-n8n.cloudfy.live/form/proposta?ref=site_institucional`.
UTM (28/09/2026): um script em todas as páginas guarda `utm_source`, `utm_medium`, `utm_campaign` e `gclid` da chegada (sessionStorage) e acrescenta esses parâmetros aos links de proposta, mantendo o `ref`. Testes e fonte do script: `antere-automacao/n8n/ferramentas/site_utm/utm_inline.js` e `n8n/testes/site_utm.test.js`.
Google Ads (09/10/2026): tag `gtag.js` com o ID `AW-18479570694` no `<head>` de todas as páginas (as 7 do site e as 3 de `legal/`), uma vez por página; no gerador é `GTAG_HEAD`. A conversão no clique dos links para `/form/proposta` está ativa desde 10/10/2026 (`CONV_SCRIPT` no gerador e o mesmo script no fim do `<body>` das 7 páginas), com `var ROTULO='4-TPCPzV6ZcdEIa-3-tE'` (`send_to: 'AW-18479570694/4-TPCPzV6ZcdEIa-3-tE'`), uma conversão por clique. Para trocar o rótulo ou desligar (`ROTULO=''`), alterar no gerador e nas 7 páginas de `public/`.

## Chave do formulário de proposta em 2 etapas (15/10/2026)

O formulário novo (`public/proposta.html`, contrato em `antere-automacao/docs/contrato_formulario_site.md`) está pronto e **desligado**.

- **Onde fica:** `public/site-config.js`, linha `window.ANTERE_FORM_NOVO = false;` (no gerador, `SITE_CONFIG_JS` em `_src/componentes.py`). O arquivo fica fora de `assets/` de propósito: `assets/` tem cache de 1 ano.
- **Desligada (`false`, o estado atual):** os 20 botões "Quero minha proposta" levam ao formulário antigo do n8n (`/form/proposta?ref=site_institucional` com as UTM) e a conversão do Google Ads dispara no clique. Quem abrir `/proposta.html` direto é mandado ao formulário antigo; `/proposta.html?previa=1` abre o formulário novo para teste.
- **Ligar:** só depois de a Operação publicar os webhooks `site-proposta-etapa1/2` e do teste de ponta a ponta. Trocar para `window.ANTERE_FORM_NOVO = true;` em `public/site-config.js` e em `SITE_CONFIG_JS` (`_src/componentes.py`), ajustar o primeiro teste de `testes/site.test.js` (que confere a chave desligada), rodar os testes e gravar na `main`. Com a chave ligada, os botões passam a levar a `/proposta.html` com os mesmos `ref` e UTM, o clique deixa de contar conversão e a conversão `AW-18479570694/4-TPCPzV6ZcdEIa-3-tE` passa a disparar no envio com sucesso da etapa 1.
- **Voltar:** trocar de novo para `false` nos dois lugares e gravar na `main`. Não precisa mexer em nenhuma página.
- **Teste da chave:** `testes/site.test.js` confere que, com a chave desligada, nenhum link do site aponta para o formulário novo (no HTML e depois dos scripts) e que, com a chave ligada (simulada), os 20 links vão para `/proposta.html`.

## WhatsApp (15/10/2026)

Botão flutuante "Fale com a gente" no canto inferior direito de todas as páginas, inclusive as de `legal/`, menos no formulário. Leva ao número do atendimento com IA (`WHATSAPP_NUMERO` em `_src/componentes.py`, hoje 5511955032670) com a mensagem "Olá! Vim pelo site e quero saber sobre o C6 Pay." e, quando a visita veio com UTM, a linha "Origem: fonte / meio / campanha". O botão some quando estaria por cima de um botão de proposta (celular). O clique em qualquer link do WhatsApp vira o evento `whatsapp_click` do Google Ads, sem conversão.

## Sobre (15/10/2026)

O bloco "Quem assina" virou "Quem acompanha você" / "Equipe comercial Antere". O nome da pessoa saiu do site. A razão social da empresa (F. de Carvalho Spahn Consultoria em Tecnologia da Informação LTDA) continua no rodapé e nas páginas legais, porque identifica o controlador dos dados.
