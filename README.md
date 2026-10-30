# Site institucional Antere

Publicado no Netlify (projeto `antere-site`) a partir da pasta `public/`.

- `public/`: tudo que vai ao ar — páginas (`index.html`, `como-funciona.html`, `solucoes.html`, `sobre.html`, `contato.html`, `calculadora.html`, `404.html`), o formulário `proposta.html` (fora do menu e do sitemap), a chave `site-config.js`, `assets/`, `legal/`, `robots.txt`, `sitemap.xml`, `_headers` e `_redirects`.
- `public/legal/`: Política de Privacidade, Termos de Uso e Exclusão de Dados. Continuam acessíveis em `legal.antere.com.br` pelas regras de `_redirects` (o domínio precisa estar adicionado ao projeto no Netlify).
- `_src/`: gerador das páginas (`build_site.py`), componentes comuns (`componentes.py`: chave, conversão, WhatsApp e o formulário) e logos originais. Não é publicado. Rode `python3 build_site.py` numa cópia de `_src/` e copie os arquivos gerados para `public/`.
  - Atenção: o gerador ainda difere de `public/` em detalhes (linhas em branco, a posição da regra `:root[data-theme="dark"] .stack{...}` e o invólucro do `index.html`). A cor do tema foi alinhada em 15/10/2026. Antes de copiar páginas regeradas por cima de `public/`, compare com `diff` e mantenha o que está publicado.
- `testes/site.test.js`: testes das páginas no Chromium, sem rede (webhooks e gtag simulados). Rodar com `NODE_PATH=$(npm root -g) node testes/site.test.js` (precisa do Playwright). Com o repositório `antere-automacao` ao lado, os corpos enviados ao n8n passam também pelas regras do servidor.
- `netlify.toml`: `publish = "public"`, sem comando de build.

Formulário de contato envia POST para `https://raregoat-n8n.cloudfy.live/webhook/site-contato`.
CTA de proposta: no HTML aponta para `https://raregoat-n8n.cloudfy.live/form/proposta?ref=site_institucional`; com a chave do formulário ligada (desde 17/10/2026), o script troca para `/proposta.html` com o mesmo `ref` e as UTM.
UTM (28/09/2026): um script em todas as páginas guarda `utm_source`, `utm_medium`, `utm_campaign` e `gclid` da chegada (sessionStorage) e acrescenta esses parâmetros aos links de proposta, mantendo o `ref`. Testes e fonte do script: `antere-automacao/n8n/ferramentas/site_utm/utm_inline.js` e `n8n/testes/site_utm.test.js`.
Google Ads (09/10/2026): tag `gtag.js` com o ID `AW-18479570694` no `<head>` de todas as páginas (as 7 do site, o formulário e as 3 de `legal/`), uma vez por página; no gerador é `GTAG_HEAD` (`_src/componentes.py`). Desde 15/10/2026 a tag é carregada por um script logo depois do `site-config.js`; desde 17/10/2026, com o aviso de cookies ligado, ela carrega em toda visita com o Consent Mode v2 (anúncios negados até o "Aceitar"; ver "Aviso de cookies"). A conversão no clique dos links para `/form/proposta` está ativa desde 10/10/2026 (`CONV_SCRIPT` no gerador e o mesmo script no fim do `<body>` das 7 páginas), com `var ROTULO='4-TPCPzV6ZcdEIa-3-tE'` (`send_to: 'AW-18479570694/4-TPCPzV6ZcdEIa-3-tE'`), uma conversão por clique. Para trocar o rótulo ou desligar (`ROTULO=''`), alterar no gerador e nas 7 páginas de `public/`. Desde 17/10/2026, com a chave do formulário ligada, a conversão do clique fica parada e a conversão passa a disparar no envio com sucesso da etapa 1 do formulário novo.

## Chave do formulário de proposta em 2 etapas (15/10/2026)

O formulário novo (`public/proposta.html`, contrato em `antere-automacao/docs/contrato_formulario_site.md`) foi ligado em 17/10/2026, depois do teste de ponta a ponta do Rodrigo com `?previa=1`, desligado no mesmo dia às 17h50 (a etapa 2 respondeu "pedido não encontrado" no teste no ar com link + PDVet; análise em `propostas/formulario_email_operacao_1610.md`) e **religado em 17/10/2026, à noite**, depois das correções da Operação e do teste final do Rodrigo (proposta no modelo novo). Detalhes: (proposta gerada às 03h19 de 17/10, com origem e UTM corretas; n8n: Formulario_Site_Proposta 03852d6f, que aceita a etapa 2 sem `conta_pj_c6`; merge na `main` do `antere-automacao` em c349255).

- **Onde fica:** `public/site-config.js`, linha `window.ANTERE_FORM_NOVO = true;` (estado atual) (no gerador, `SITE_CONFIG_JS` em `_src/componentes.py`). O arquivo fica fora de `assets/` de propósito: `assets/` tem cache de 1 ano. Ele carrega no `<head>` de todas as páginas (nas de `legal/`, pelo endereço completo `https://www.antere.com.br/site-config.js`, porque elas também abrem em `legal.antere.com.br`).
- **Ligada (`true`, o estado atual):** os 20 botões "Quero minha proposta" levam a `/proposta.html` com os mesmos `ref` e UTM (a troca é feita por script; sem JavaScript, o link do HTML ainda leva ao formulário antigo). O clique não conta conversão; a conversão `AW-18479570694/4-TPCPzV6ZcdEIa-3-tE` dispara no envio com sucesso da etapa 1.
- **Desligada (`false`):** os 20 botões "Quero minha proposta" levam ao formulário antigo do n8n (`/form/proposta?ref=site_institucional` com as UTM) e a conversão do Google Ads dispara no clique. Quem abrir `/proposta.html` direto é mandado ao formulário antigo; `/proposta.html?previa=1` abre o formulário novo para teste.
- **Ligada em 17/10/2026:** `window.ANTERE_FORM_NOVO = true;` em `public/site-config.js` e em `SITE_CONFIG_JS` (`_src/componentes.py`); testes ajustados.
- **Voltar (se o formulário novo der problema):** trocar para `false` nos dois lugares, trocar o primeiro teste de `testes/site.test.js` para conferir `false`, rodar os testes e gravar na `main`. Não precisa mexer em nenhuma página. Os botões voltam ao formulário antigo do n8n, que continua no ar, e a conversão volta para o clique.
- **Teste da chave:** `testes/site.test.js` confere que o `site-config.js` publicado está com a chave ligada e que, com ela, os 20 links vão para `/proposta.html` com UTM e `ref` e o clique não conta conversão. O caminho de volta continua testado com a chave desligada simulada (20 links em `/form/proposta`, 1 conversão por clique, `/proposta.html` leva ao formulário antigo).

### Formulário: e-mail conferido antes do envio (16/10/2026)

Aprovado pelo Rodrigo para o formulário novo (proposta da Operação: `antere-automacao/docs/proposta_formulario_email_1610.md`). Lado do site pronto em `proposta.html`; o combinado com a Operação está em `propostas/formulario_email_operacao_1610.md`.
- **Sugestão de correção:** erros comuns de digitação no domínio (lista de 10 domínios; distância 1 até 5 letras antes do ponto e 2 acima, com a mesma primeira letra; mais o `.br` sobrando, como `gmail.com.br`; regra do Rodrigo de 16/10, igual à da `lib/` da Operação) mostram "Você quis dizer …?" com "Sim, trocar" e "Não, está certo". Não troca sozinho; o envio espera a resposta.
- **Domínio sem e-mail:** quem confere é o servidor; com `422` `dominio_sem_email`, a tela mostra "Esse endereço não recebe e-mail. Confira o que vem depois do @." e a sugestão do servidor, se houver.
- **Link de lote ou campanha com `lead_id` e `token`:** a página tira os dois da URL, busca nome e e-mail em `GET /webhook/form-proposta-dados` e preenche; o envio leva `lead_id_cadastro`, `token_cadastro` e `email_alterado`. Sem resposta do endpoint, abre vazio, como antes.
- Depende do servidor (regra 1, endpoint e campos novos), que é da Operação. A chave do formulário foi ligada em 17/10/2026; enquanto o endpoint `form-proposta-dados` não existir, o formulário abre vazio, como antes.

### Formulário: ajustes de 17/10/2026 (Rodrigo)

- **Tema escuro em tudo:** etapa 1, etapa 2, tela da PDVet, tela final, erros, "Você quis dizer…?" e carregando. Inclui os controles nativos (`color-scheme: dark`: opções, caixas, a lista de faixas e as setas dos números), o preenchimento automático do navegador e os links e botões de contorno em roxo claro (`--indigo-ink`). O teste "tema escuro em todas as telas e estados" confere fundo, contraste ≥ 4,5 e controles, com o aparelho em modo claro e em modo escuro.
- **Bloco da empresa:** "✓ Dados corretos" (preenchido) e "Corrigir" (contorno), pequenos (36 px), lado a lado, sem quebrar linha.
- **Conta PJ C6:** a pergunta saiu da etapa 2 e, desde 17/10, o campo `conta_pj_c6` também deixou de ir no envio (`CONTA_PJ_ENVIO = ""` em `_src/componentes.py`), porque saiu do contrato (Operação, commit 58cb38f do `antere-automacao`). A Operação publicou no n8n a versão que aceita a etapa 2 sem o campo (Formulario_Site_Proposta 03852d6f, merge em c349255), e o teste de ponta a ponta passou.

### Formulário: produtos na etapa 1 (17/10/2026)

"O que você procura?" vira múltipla escolha com 4 opções (TEF, C6 Pay, link, PDVet; pelo menos uma). Só PDVet vai ao cadastro da PDVet; PDVet com outro produto segue para a etapa 2, que mostra só os campos dos produtos escolhidos (TEF: sistema PDV, lojas e caixas; C6 Pay: vendas no cartão e prazo de recebimento; link: volume de transações). Contrato publicado pela Operação em 17/10, 10h50; o site segue o contrato publicado (nº de caixas na etapa 1; sistema PDV e lojas na etapa 2 para todos os produtos; com PDVet junto, a tela final oferece o portal da PDVet, com o `url_pdvet` da resposta da etapa 2 desde 17/10). Telas aprovadas pelo Rodrigo e no ar desde 17/10/2026 (a chave do formulário está ligada).

### Formulário: C6 Pay só com TEF (17/10/2026)

Marcar C6 Pay marca também o TEF ("O C6 Pay é oferecido junto com o TEF integrado ao caixa."); desmarcar o TEF desmarca o C6 Pay. "Nº de caixas" (etapa 1), "Sistema PDV" e "Nº de lojas" (etapa 2) só aparecem, só são obrigatórios e só são enviados com TEF. O n8n aceita desde 17/10, 15h32 (`antere-automacao/docs/aviso_site_regras_tef_1710.md`) e recusa C6 Pay sem TEF com o erro `c6pay_sem_tef`; a tela mostra "O C6 Pay é oferecido junto com o TEF integrado ao caixa. Marque também \"TEF integrado ao caixa\"." (na etapa 2, com "Volte à etapa 1 para ajustar."). Na `main` desde 17/10/2026; a chave do formulário continua desligada.

### Formulário: opt-in do WhatsApp na etapa 1 (30/10/2026, pedido da Operação)

Pedido em `docs/pedido_site_optin_3010.md` (repositório `antere-automacao`), aprovado pelo Rodrigo em 30/10. Logo abaixo do campo de WhatsApp, a caixa "Quero receber a proposta e o acompanhamento da Antere pelo WhatsApp": opcional, desmarcada, sem `required`, separada da caixa da LGPD (que continua obrigatória e com o mesmo texto). No envio da etapa 1 vão `optin_whatsapp` (`true`/`false`) e `optin_whatsapp_texto` (o texto da caixa, lido da própria tela, `#t-optin`). A etapa 2 não muda. Até a Operação publicar a parte dela (02/11/2026, 20h), o webhook ignora os dois campos, sem erro.

## WhatsApp (15/10/2026)

Botão flutuante "Fale com a gente" no canto inferior direito de todas as páginas, inclusive as de `legal/`, menos no formulário. Leva ao número do atendimento com IA (`WHATSAPP_NUMERO` em `_src/componentes.py`, hoje 5511955032670) com a mensagem "Olá! Vim pelo site da Antere e quero saber mais sobre as soluções." e, quando a visita veio com UTM, a linha "Origem: fonte / meio / campanha". O botão some quando estaria por cima de um botão de proposta (celular). O clique em qualquer link do WhatsApp vira o evento `whatsapp_click` do Google Ads, sem conversão.

## Sobre (15/10/2026)

O bloco "Quem assina" virou "Quem acompanha você" / "Equipe comercial Antere". O nome da pessoa saiu do site. A razão social da empresa (F. de Carvalho Spahn Consultoria em Tecnologia da Informação LTDA) continua no rodapé e nas páginas legais, porque identifica o controlador dos dados.

## Aviso de cookies (LGPD) (15/10/2026; ligado em 17/10/2026 com o Consent Mode v2)

**Ligado** desde 17/10/2026, no modo de consentimento do Google (Consent Mode v2, "modo avançado"), a pedido do Rodrigo.

- **Onde fica:** `public/site-config.js`, linha `window.ANTERE_COOKIES = true;` (no gerador, `SITE_CONFIG_JS` em `_src/componentes.py`). O carregador da tag e o consentimento estão em `GTAG_HEAD`/`GTAG_HEAD_LEGAL` e a faixa em `COOKIE_SCRIPT`, ambos em `_src/componentes.py` e copiados iguais para as 11 páginas de `public/`.
- **Faixa:** na primeira visita aparece no rodapé: "Usamos cookies do Google Ads para medir o resultado dos nossos anúncios. Sem o seu aceite, nenhum cookie de anúncio é gravado e o Google recebe só sinais sem identificação. Saiba mais na Política de Privacidade." (link para `https://legal.antere.com.br/privacidade.html`), com os botões "Recusar" e "Aceitar".
- **Consentimento:** a tag do Google Ads carrega em toda visita. Antes do `config`, o site envia `gtag('consent', 'default', …)` com `ad_storage`, `ad_user_data` e `ad_personalization` em `denied` (ou `granted` para quem já aceitou antes) e liga `ads_data_redaction`. "Aceitar" envia `gtag('consent', 'update', …)` com os três em `granted`; "Recusar" os mantém em `denied`.
- **Essenciais, sempre liberados:** o que o site precisa para funcionar não depende do aceite: a própria escolha (`localStorage`, `antere_cookies`), a origem da visita (UTM/gclid em `sessionStorage`) e o formulário. Com "Recusar", o formulário (etapas 1 e 2) e o WhatsApp funcionam normalmente; a conversão da etapa 1 e o evento `whatsapp_click` continuam indo ao `dataLayer` e o Google os recebe sem cookies.
- **A escolha fica gravada:** `localStorage` `antere_cookies` (`{escolha, em}`), e a faixa não volta nas visitas seguintes. Vale por domínio: `www.antere.com.br` e `legal.antere.com.br` guardam cada um a sua. O rodapé tem o link "Preferências de cookies", que reabre a faixa para mudar a escolha (as páginas de `legal/` não têm esse rodapé; lá a faixa aparece até a primeira escolha).
- Enquanto a faixa está aberta, o botão do WhatsApp sobe para ficar acima dela.
- **Política de Privacidade:** a linha do Google Ads (seção 5 de `public/legal/privacidade.html`) foi atualizada em 17/10/2026 com o texto sugerido abaixo e a menção aos dados essenciais.
- **Voltar (desligar):** trocar para `window.ANTERE_COOKIES = false;` em `public/site-config.js` e em `SITE_CONFIG_JS`; no `testes/site.test.js`, o teste "cookies: site-config.js publicado…" passa a conferir `false`. Desligado, a tag carrega em toda visita, sem faixa e sem nenhum comando de consentimento.
- **Testes:** `testes/site.test.js` confere o `site-config.js` publicado (e o gerador) com `true`; com a chave publicada, a faixa e o consentimento negado nas 11 páginas e no formulário, o "Recusar" gravado sem perguntar de novo, o WhatsApp (link, mensagem, `whatsapp_click`) e o formulário de ponta a ponta (etapas 1 e 2, conversão) depois do "Recusar"; simulados, o "Aceitar" e o "Preferências de cookies", e o caminho de volta (desligado: nada muda).

### Consent Mode v2 (proposta de 16/10/2026, aplicada em 17/10/2026)

A proposta ficou em `propostas/consent-mode-v2.patch` (histórico). Antes dela, o aviso bloqueava a tag inteira de quem recusava (modo básico).

**Diferença entre as duas formas:**

| | Bloqueio da tag (forma anterior, não publicada) | Consent Mode v2 (no ar) |
|---|---|---|
| Quem aceita | tag carrega, cookies e conversões normais | igual |
| Quem recusa ou ignora a faixa | a tag não carrega; nada vai ao Google | a tag carrega sem gravar cookies de anúncio; envia ao Google sinais sem cookies (o estado do consentimento e dados técnicos do acesso, sem identificador de anúncio) |
| Conversões de quem recusa | perdidas, sem estimativa | não contadas uma a uma, mas o Google estima por modelagem e soma às conversões da conta |
| Equivale, no vocabulário do Google, a | modo básico | modo avançado |

**Impacto esperado na contagem de conversões:**
- **Bloqueio da tag (forma anterior):** a contagem passa a ser só das conversões de quem aceitou. Ela cai na proporção de quem recusa ou não responde à faixa, e os lances automáticos do Google Ads recebem menos sinal.
- **Consent Mode v2:** as conversões de quem aceitou continuam iguais (observadas). Para quem recusou, o Google Ads acrescenta conversões **modeladas** (estimadas), que aparecem somadas na coluna de conversões, sem detalhe por clique. O total tende a ficar mais perto do real.
- **Ressalva de volume:** a modelagem só entra quando a conta tem volume suficiente. Pela documentação do Google, a referência é da ordem de 700 cliques em anúncios em 7 dias por país e domínio; conferir na conta (Metas → Conversões → diagnóstico do modo de consentimento). Abaixo disso, a contagem fica parecida com a do bloqueio da tag, só com as conversões de quem aceitou.
- O Google divulga uma recuperação média, por modelagem, de boa parte das conversões perdidas por recusa (na casa de dois terços), mas isso é média do Google, não garantia para esta conta.
- Em qualquer das duas formas, a conversão que hoje conta no clique de todo visitante vai cair em relação aos números de hoje assim que o aviso for ligado.

**Pontos que foram decididos ao aplicar:**
- **LGPD:** no modo avançado, a tag fala com o Google mesmo sem aceite (sem cookies e sem identificador de anúncio). A Política de Privacidade precisa dizer isso. Texto usado na linha do Google Ads (seção 5), publicado em 17/10/2026: "Nosso site usa a tag do Google Ads para medir o desempenho dos nossos anúncios. Os cookies de anúncios só são gravados se você aceitar no aviso de cookies; sem o aceite, a tag envia ao Google apenas sinais sem cookies e sem identificador de anúncio, usados para estimar resultados de forma agregada. Você pode mudar sua escolha a qualquer momento em "Preferências de cookies", no rodapé do site." Vale a validação do Rodrigo (e, se houver, do jurídico).
- **`url_passthrough`** (levar o `gclid` pelos links internos quando os cookies são negados) **não** está na proposta: ele acrescenta parâmetros aos links do site. Pode ser avaliado depois, se a modelagem não entrar por falta de volume.

**Para aplicar (no dia de ligar o aviso):** `git apply propostas/consent-mode-v2.patch`, conferir com `git diff`, trocar `ANTERE_COOKIES` para `true` (ver "Ligar" acima), atualizar a Política de Privacidade, rodar `NODE_PATH=$(npm root -g) node testes/site.test.js` e gravar na `main`. Se o patch não aplicar porque as páginas mudaram, refazer a partir de `_src/componentes.py` (funções `gtag_head` e `COOKIE_SCRIPT`), que concentram a mudança.
