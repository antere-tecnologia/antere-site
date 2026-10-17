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
Google Ads (09/10/2026): tag `gtag.js` com o ID `AW-18479570694` no `<head>` de todas as páginas (as 7 do site, o formulário e as 3 de `legal/`), uma vez por página; no gerador é `GTAG_HEAD` (`_src/componentes.py`). Desde 15/10/2026 a tag é carregada por um script logo depois do `site-config.js`, para obedecer ao aviso de cookies quando ele for ligado; com o aviso desligado, carrega em toda visita, como antes. A conversão no clique dos links para `/form/proposta` está ativa desde 10/10/2026 (`CONV_SCRIPT` no gerador e o mesmo script no fim do `<body>` das 7 páginas), com `var ROTULO='4-TPCPzV6ZcdEIa-3-tE'` (`send_to: 'AW-18479570694/4-TPCPzV6ZcdEIa-3-tE'`), uma conversão por clique. Para trocar o rótulo ou desligar (`ROTULO=''`), alterar no gerador e nas 7 páginas de `public/`.

## Chave do formulário de proposta em 2 etapas (15/10/2026)

O formulário novo (`public/proposta.html`, contrato em `antere-automacao/docs/contrato_formulario_site.md`) está pronto e **desligado**.

- **Onde fica:** `public/site-config.js`, linha `window.ANTERE_FORM_NOVO = false;` (no gerador, `SITE_CONFIG_JS` em `_src/componentes.py`). O arquivo fica fora de `assets/` de propósito: `assets/` tem cache de 1 ano. Ele carrega no `<head>` de todas as páginas (nas de `legal/`, pelo endereço completo `https://www.antere.com.br/site-config.js`, porque elas também abrem em `legal.antere.com.br`).
- **Desligada (`false`, o estado atual):** os 20 botões "Quero minha proposta" levam ao formulário antigo do n8n (`/form/proposta?ref=site_institucional` com as UTM) e a conversão do Google Ads dispara no clique. Quem abrir `/proposta.html` direto é mandado ao formulário antigo; `/proposta.html?previa=1` abre o formulário novo para teste.
- **Ligar:** só depois de a Operação publicar os webhooks `site-proposta-etapa1/2` e do teste de ponta a ponta. Trocar para `window.ANTERE_FORM_NOVO = true;` em `public/site-config.js` e em `SITE_CONFIG_JS` (`_src/componentes.py`), ajustar o primeiro teste de `testes/site.test.js` (que confere a chave desligada), rodar os testes e gravar na `main`. Com a chave ligada, os botões passam a levar a `/proposta.html` com os mesmos `ref` e UTM, o clique deixa de contar conversão e a conversão `AW-18479570694/4-TPCPzV6ZcdEIa-3-tE` passa a disparar no envio com sucesso da etapa 1.
- **Voltar:** trocar de novo para `false` nos dois lugares e gravar na `main`. Não precisa mexer em nenhuma página.
- **Teste da chave:** `testes/site.test.js` confere que, com a chave desligada, nenhum link do site aponta para o formulário novo (no HTML e depois dos scripts) e que, com a chave ligada (simulada), os 20 links vão para `/proposta.html`.

### Formulário: e-mail conferido antes do envio (16/10/2026)

Aprovado pelo Rodrigo para o formulário novo (proposta da Operação: `antere-automacao/docs/proposta_formulario_email_1610.md`). Lado do site pronto em `proposta.html`; o combinado com a Operação está em `propostas/formulario_email_operacao_1610.md`.
- **Sugestão de correção:** erros comuns de digitação no domínio (lista de 10 domínios; distância 1 até 5 letras antes do ponto e 2 acima, com a mesma primeira letra; mais o `.br` sobrando, como `gmail.com.br`; regra do Rodrigo de 16/10, igual à da `lib/` da Operação) mostram "Você quis dizer …?" com "Sim, trocar" e "Não, está certo". Não troca sozinho; o envio espera a resposta.
- **Domínio sem e-mail:** quem confere é o servidor; com `422` `dominio_sem_email`, a tela mostra "Esse endereço não recebe e-mail. Confira o que vem depois do @." e a sugestão do servidor, se houver.
- **Link de lote ou campanha com `lead_id` e `token`:** a página tira os dois da URL, busca nome e e-mail em `GET /webhook/form-proposta-dados` e preenche; o envio leva `lead_id_cadastro`, `token_cadastro` e `email_alterado`. Sem resposta do endpoint, abre vazio, como antes.
- Depende do servidor (regra 1, endpoint e campos novos), que é da Operação. A chave do formulário continua desligada.

### Formulário: ajustes de 17/10/2026 (Rodrigo)

- **Tema escuro em tudo:** etapa 1, etapa 2, tela da PDVet, tela final, erros, "Você quis dizer…?" e carregando. Inclui os controles nativos (`color-scheme: dark`: opções, caixas, a lista de faixas e as setas dos números), o preenchimento automático do navegador e os links e botões de contorno em roxo claro (`--indigo-ink`). O teste "tema escuro em todas as telas e estados" confere fundo, contraste ≥ 4,5 e controles, com o aparelho em modo claro e em modo escuro.
- **Bloco da empresa:** "✓ Dados corretos" (preenchido) e "Corrigir" (contorno), pequenos (36 px), lado a lado, sem quebrar linha.
- **Conta PJ C6:** a pergunta saiu da etapa 2. Enquanto o contrato do n8n exigir `conta_pj_c6`, o site manda `"nao"` (`CONTA_PJ_ENVIO` em `_src/componentes.py`). Quando a Operação tirar a exigência, trocar para `""` (o campo deixa de ir) e ajustar o teste. Combinado em `propostas/formulario_email_operacao_1610.md`.

## WhatsApp (15/10/2026)

Botão flutuante "Fale com a gente" no canto inferior direito de todas as páginas, inclusive as de `legal/`, menos no formulário. Leva ao número do atendimento com IA (`WHATSAPP_NUMERO` em `_src/componentes.py`, hoje 5511955032670) com a mensagem "Olá! Vim pelo site da Antere e quero saber mais sobre as soluções." e, quando a visita veio com UTM, a linha "Origem: fonte / meio / campanha". O botão some quando estaria por cima de um botão de proposta (celular). O clique em qualquer link do WhatsApp vira o evento `whatsapp_click` do Google Ads, sem conversão.

## Sobre (15/10/2026)

O bloco "Quem assina" virou "Quem acompanha você" / "Equipe comercial Antere". O nome da pessoa saiu do site. A razão social da empresa (F. de Carvalho Spahn Consultoria em Tecnologia da Informação LTDA) continua no rodapé e nas páginas legais, porque identifica o controlador dos dados.

## Aviso de cookies (LGPD) (15/10/2026)

Pronto e **desligado**. Será ligado depois da validação da conversão do Google Ads.

- **Onde fica:** `public/site-config.js`, linha `window.ANTERE_COOKIES = false;` (no gerador, `SITE_CONFIG_JS` em `_src/componentes.py`). O carregador da tag está em `GTAG_HEAD`/`GTAG_HEAD_LEGAL` e a faixa em `COOKIE_SCRIPT`, ambos em `_src/componentes.py` e copiados iguais para as 11 páginas de `public/`.
- **Desligado (`false`, o estado atual):** nada muda para o visitante. A tag do Google Ads carrega em toda visita, não aparece faixa, não aparece link de preferências e nada é guardado no navegador.
- **Ligado (`true`):** na primeira visita aparece uma faixa no rodapé: "Usamos cookies e a tag do Google Ads só para medir o resultado dos nossos anúncios. Você escolhe se aceita. Saiba mais na Política de Privacidade.", com os botões "Recusar" e "Aceitar".
  - A tag do Google Ads só carrega depois do "Aceitar" (na hora e nas visitas seguintes). Com "Recusar", ou sem escolha, ela não carrega; os eventos ficam só na fila local (`dataLayer`) e não são enviados.
  - A escolha fica no navegador (`localStorage`, chave `antere_cookies`, com a data). Vale por domínio: `www.antere.com.br` e `legal.antere.com.br` guardam cada um a sua.
  - O rodapé ganha o link "Preferências de cookies", que reabre a faixa para mudar a escolha. As páginas de `legal/` não têm esse rodapé; lá a faixa aparece até a primeira escolha.
  - Enquanto a faixa está aberta, o botão do WhatsApp sobe para ficar acima dela.
- **Ligar:** trocar para `window.ANTERE_COOKIES = true;` em `public/site-config.js` e em `SITE_CONFIG_JS` (`_src/componentes.py`); no `testes/site.test.js`, trocar o teste "cookies: site-config.js publicado com a chave do aviso desligada" para conferir `true` e o teste "cookies desligado" para usar `cookies: false` simulado; rodar os testes e gravar na `main`. Atenção: com o aviso ligado, só entram no Google Ads as conversões de quem aceitou.
- **Voltar:** trocar de novo para `false` nos dois lugares e gravar na `main`.
- **Testes:** `testes/site.test.js` confere que, desligado, nada muda (a tag carrega uma vez em cada uma das 11 páginas sem clique, sem faixa, sem link, sem nada guardado, WhatsApp na posição de sempre) e, ligado (simulado), a faixa, o link da política, a tag só depois do aceite, o "Recusar" guardado e o "Preferências de cookies".

### Proposta: Consent Mode v2 do Google (16/10/2026, não publicada)

Proposta para quando o aviso de cookies for ligado: em vez de bloquear a tag inteira de quem recusa, usar o modo de consentimento do Google (Consent Mode v2, "modo avançado"). Está pronta em `propostas/consent-mode-v2.patch` (gerador, as 11 páginas de `public/`, `site-config.js` e testes), testada e **não aplicada**: o site no ar continua com a forma descrita acima.

**Como funciona com a proposta (só com `ANTERE_COOKIES = true`; desligado, nada muda e nenhum comando de consentimento é enviado):**
- A tag do Google Ads carrega em toda visita. Antes do `config`, o site envia `gtag('consent', 'default', …)` com `ad_storage`, `ad_user_data` e `ad_personalization` em `denied` (ou `granted` para quem já aceitou antes) e liga `ads_data_redaction`.
- "Aceitar" envia `gtag('consent', 'update', …)` com os três em `granted`; "Recusar" (ou mudar de ideia em "Preferências de cookies") envia os três em `denied`. A escolha continua em `localStorage` (`antere_cookies`).
- O texto da faixa muda para: "Usamos cookies do Google Ads para medir o resultado dos nossos anúncios. Sem o seu aceite, nenhum cookie de anúncio é gravado e o Google recebe só sinais sem identificação. Saiba mais na Política de Privacidade."

**Diferença entre as duas formas:**

| | Forma atual (bloqueio da tag) | Consent Mode v2 (proposta) |
|---|---|---|
| Quem aceita | tag carrega, cookies e conversões normais | igual |
| Quem recusa ou ignora a faixa | a tag não carrega; nada vai ao Google | a tag carrega sem gravar cookies de anúncio; envia ao Google sinais sem cookies (o estado do consentimento e dados técnicos do acesso, sem identificador de anúncio) |
| Conversões de quem recusa | perdidas, sem estimativa | não contadas uma a uma, mas o Google estima por modelagem e soma às conversões da conta |
| Equivale, no vocabulário do Google, a | modo básico | modo avançado |

**Impacto esperado na contagem de conversões:**
- **Forma atual:** a contagem passa a ser só das conversões de quem aceitou. Ela cai na proporção de quem recusa ou não responde à faixa, e os lances automáticos do Google Ads recebem menos sinal.
- **Consent Mode v2:** as conversões de quem aceitou continuam iguais (observadas). Para quem recusou, o Google Ads acrescenta conversões **modeladas** (estimadas), que aparecem somadas na coluna de conversões, sem detalhe por clique. O total tende a ficar mais perto do real.
- **Ressalva de volume:** a modelagem só entra quando a conta tem volume suficiente. Pela documentação do Google, a referência é da ordem de 700 cliques em anúncios em 7 dias por país e domínio; conferir na conta (Metas → Conversões → diagnóstico do modo de consentimento). Abaixo disso, a contagem fica parecida com a da forma atual, só com as conversões de quem aceitou.
- O Google divulga uma recuperação média, por modelagem, de boa parte das conversões perdidas por recusa (na casa de dois terços), mas isso é média do Google, não garantia para esta conta.
- Em qualquer das duas formas, a conversão que hoje conta no clique de todo visitante vai cair em relação aos números de hoje assim que o aviso for ligado.

**Pontos para decidir antes de aplicar:**
- **LGPD:** no modo avançado, a tag fala com o Google mesmo sem aceite (sem cookies e sem identificador de anúncio). A Política de Privacidade precisa dizer isso. Sugestão de texto para a linha do Google Ads (seção 5): "Nosso site usa a tag do Google Ads para medir o desempenho dos nossos anúncios. Os cookies de anúncios só são gravados se você aceitar no aviso de cookies; sem o aceite, a tag envia ao Google apenas sinais sem cookies e sem identificador de anúncio, usados para estimar resultados de forma agregada. Você pode mudar sua escolha a qualquer momento em "Preferências de cookies", no rodapé do site." Vale a validação do Rodrigo (e, se houver, do jurídico).
- **`url_passthrough`** (levar o `gclid` pelos links internos quando os cookies são negados) **não** está na proposta: ele acrescenta parâmetros aos links do site. Pode ser avaliado depois, se a modelagem não entrar por falta de volume.

**Para aplicar (no dia de ligar o aviso):** `git apply propostas/consent-mode-v2.patch`, conferir com `git diff`, trocar `ANTERE_COOKIES` para `true` (ver "Ligar" acima), atualizar a Política de Privacidade, rodar `NODE_PATH=$(npm root -g) node testes/site.test.js` e gravar na `main`. Se o patch não aplicar porque as páginas mudaram, refazer a partir de `_src/componentes.py` (funções `gtag_head` e `COOKIE_SCRIPT`), que concentram a mudança.
