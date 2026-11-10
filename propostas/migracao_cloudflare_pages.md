# Migração do site e de legal.antere.com.br do Netlify para o Cloudflare Pages (plano de 10/11/2026)

**Decisão do Rodrigo (10/11):** www.antere.com.br e legal.antere.com.br saem do Netlify e vão para o Cloudflare Pages, com tudo no ar
até terça, 01/12/2026. O DNS fica na GoDaddy: mudam só os apontamentos de `www`, `legal` e da raiz. Nada de levar o DNS inteiro para a
Cloudflare. Até a migração, o Netlify fica no plano Free, sem upgrade.

**Motivo:** o plano Free do Netlify tem 300 créditos por mês e cada deploy de produção custa 15 (no máximo 20 por mês). O ciclo atual
estourou (305,6 créditos) e só renova em 16/11. Até lá nada publica (o deploy de `11e0a3e` ficou "Skipped").

## Regras até a migração

- Juntar as mudanças e publicar na `main` no máximo uma vez por semana, salvo urgência.
- `netlify.toml` tem a regra `ignore`: não publica quando nada em `public/` mudou desde o último deploy (conferido com o git: um commit
  só de `propostas/` sai 0 e cancela; um que muda `public/` sai 1 e publica; sem o commit anterior, publica).
- No Netlify, os deploy previews já estão como "Don't deploy pull requests" e os branch deploys só na produção.
- Os dois ajustes de 10/11 (`11e0a3e`: menu do 404 e razão social no topo de `exclusao-dados.html`) entram na primeira publicação
  possível: no Netlify depois de 16/11 ou já no Cloudflare Pages, o que vier primeiro.

## (a) O que o Netlify faz hoje

| Item | Onde | O que faz |
|---|---|---|
| Publicação | `netlify.toml` | `publish = "public"`, sem build (`command = ""`), mais a regra `ignore` acima. |
| Domínios | painel do Netlify | `www.antere.com.br` (principal), `antere.com.br` (raiz, redireciona para www) e `legal.antere.com.br` (desde 04/11). Certificados do Let's Encrypt emitidos pelo Netlify. |
| Regras do legal | `public/_redirects` | `https://legal.antere.com.br/` mostra `/legal/privacidade.html` (200). `https://legal.antere.com.br/*` mostra `/legal/:splat` (200). `http://legal…` redireciona para `https://` (301). |
| Cabeçalhos | `public/_headers` | `/assets/*`: `Cache-Control: public, max-age=31536000, immutable`. Todas as páginas: `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY`. |
| 404 | `public/404.html` | Página de erro do site, servida com status 404 em qualquer endereço que não existe. |
| HTTP para HTTPS | automático | Redireciona todo `http://` para `https://`. |
| Endereços `.html` | automático | Serve `/sobre.html` com 200, sem redirecionar. Os links do site, o sitemap, os canonicals e os endereços da Meta usam `.html`. |
| Variáveis de ambiente | — | Nenhuma (o time não tem variáveis e o site não tem build). A configuração em tempo de execução está em `public/site-config.js`. |
| Formulários, funções, Edge | — | Nenhum. O formulário de proposta vai direto para os webhooks do n8n. |

Fora do Netlify, mas dependendo do domínio:
- **CORS dos webhooks do n8n:** só aceitam a origem `https://www.antere.com.br` e `https://antere.com.br`
  (`antere-automacao/n8n/patches/site/cors_e_monitor_aplicar.json`). Num endereço `.pages.dev`, o formulário falha até a Operação
  liberar essa origem.
- **Monitor de entregas da Operação** (`Monitor_Entregas_Clientes`): confere as 3 páginas de legal.antere.com.br e o site.
- **Páginas legais:** carregam `https://www.antere.com.br/site-config.js` pelo endereço completo, o que continua funcionando.

## (b) Configuração no Cloudflare Pages (a partir do GitHub)

Dois projetos, ligados ao repositório `antere-tecnologia/antere-site`, branch de produção `main`. O Pages não aceita regras por domínio
no `_redirects` (as do legal), então o legal vira um segundo projeto, com as 3 páginas na raiz. O script `cloudflare/montar.sh` monta a
saída de cada um (testado localmente).

| | Projeto 1: `antere-site` | Projeto 2: `antere-legal` |
|---|---|---|
| Framework preset | None | None |
| Build command | `sh cloudflare/montar.sh www` | `sh cloudflare/montar.sh legal` |
| Build output directory | `dist-www` | `dist-legal` |
| Root directory | (raiz do repositório) | (raiz do repositório) |
| Domínio personalizado | `www.antere.com.br` | `legal.antere.com.br` |
| Preview deployments (Branch control) | None (só `main`) | None (só `main`) |
| Build watch paths (opcional) | incluir `public/*` e `cloudflare/*` | incluir `public/legal/*` e `cloudflare/*` |
| Variáveis | nenhuma | nenhuma |

O que o script faz:
- **www:** copia `public/` inteiro, inclusive `_headers` (que o Pages entende igual). Troca o `_redirects` do Netlify por regras
  `/<página>.html → /<página> 200`, uma para cada página do site e das legais.
- **legal:** copia as 3 páginas legais para a raiz. Cria `_redirects` com `/ → /privacidade 200` e as 3 regras `.html`, e
  `_headers` com os 3 cabeçalhos de segurança.

Por que as regras `.html`: o Pages, por padrão, redireciona `/x.html` para `/x` (308). As regras 200 servem a página no mesmo endereço
`.html`, sem redirecionar, como hoje e como cadastrado na Meta. **Isso precisa ser confirmado no teste (d).** Se o Pages ainda
redirecionar:
1. Plano B: uma Pages Function só nos 3 endereços legais (dentro do plano gratuito).
2. Plano C: aceitar o 308, com a Operação ajustando o monitor e conferindo com a Meta.

Limites do plano gratuito: 500 builds por mês, banda e requisições ilimitadas, até 100 domínios por projeto. Builds de commits que só
mexem em `propostas/` não custam nada; com os "build watch paths", nem rodam.

## (c) Troca na GoDaddy (só www, legal e a raiz)

**Não tocar:** o TXT da Meta, o SPF, o DKIM, o DMARC, os MX, os registros do Brevo e do Resend e qualquer outro TXT ou CNAME que não
seja `www`, `legal` ou o `@` (A).

**Antes da noite da troca (D-1):**
1. Fotografar (print ou exportação) a zona DNS inteira de `antere.com.br` na GoDaddy. É a referência da volta.
2. Anotar os valores atuais de `www` (CNAME), `legal` (CNAME → `antere-site.netlify.app`) e `@` (registros A).
3. Baixar o TTL de `www`, `legal` e `@` para 600 s (ou o menor que a GoDaddy permitir).

**Na noite da troca:**

| Registro | Hoje | Depois |
|---|---|---|
| `www` (CNAME) | Netlify (anotar) | `antere-site.pages.dev` (o endereço que o projeto 1 mostrar) |
| `legal` (CNAME) | `antere-site.netlify.app` | `antere-legal.pages.dev` (o endereço que o projeto 2 mostrar) |
| `@` raiz (A) | Netlify (anotar) | Encaminhamento da GoDaddy ("Forwarding") de `antere.com.br` para `https://www.antere.com.br`, permanente (301), sem mascaramento |

Sobre a raiz: o Pages só aceita o domínio raiz quando o DNS inteiro está na Cloudflare, o que foi descartado. Por isso a raiz vira um
encaminhamento da GoDaddy, que troca só os registros A do `@` e não mexe em TXT nem em MX. Conferir se o encaminhamento atende
`https://antere.com.br` (com certificado) e não só `http://`. Se não atender, a raiz fica no Netlify como está, só redirecionando para o
www, até achar outra solução. Isso não gasta deploy.

**Ordem:**
1. No Pages, adicionar o domínio personalizado em cada projeto. Ele mostra o CNAME esperado.
2. Trocar `legal` e conferir.
3. Trocar `www` e conferir.
4. Trocar a raiz e conferir.

**Volta (se algo falhar):**
1. Repor os valores anotados: `www` e `legal` voltam aos CNAME do Netlify, e `@` volta aos registros A anotados (desligando o
   encaminhamento).
2. O projeto do Netlify continua existindo, com os domínios cadastrados, até 2 semanas depois da troca. Não apagar antes disso.
3. Atenção: até 16/11 o Netlify está sem créditos. Uma volta antes dessa data cai num projeto que não publica nada novo, mas segue
   servindo o último deploy. Por isso a troca deve ser depois de 16/11.

## (d) Teste completo antes da troca (nos endereços .pages.dev)

Nos endereços provisórios `https://antere-site.pages.dev` e `https://antere-legal.pages.dev`, numa janela anônima:

1. **Status e endereço:** cada página abre com 200, no mesmo endereço `.html`, sem redirecionar:
   - site: `/`, `/como-funciona.html`, `/solucoes.html`, `/calculadora.html`, `/sobre.html`, `/contato.html`, `/proposta.html`;
   - legal: `/privacidade.html`, `/termos.html`, `/exclusao-dados.html`.
2. **Raiz do legal:** `https://antere-legal.pages.dev/` mostra a Política de Privacidade.
3. **404:** um endereço inexistente no site mostra a página 404 do site, com status 404, e o menu certo.
4. **Cabeçalhos:**
   - `/assets/` com `Cache-Control: public, max-age=31536000, immutable`;
   - as páginas com `X-Content-Type-Options`, `Referrer-Policy` e `X-Frame-Options`.
5. **Conteúdo do commit atual da main:** rodapé com a marca e o CNPJ; razão social sem ponto depois do F; menu do 404 com Calculadora;
   topo de `exclusao-dados.html` com a razão social.
6. **Aviso de cookies:** aparece; "Recusar" e "Aceitar" funcionam; a escolha fica gravada.
7. **WhatsApp:** o botão flutuante abre `wa.me/5511955032670` com a mensagem e a origem (UTM).
8. **Formulário:** a tela e as validações funcionam. O envio real ao n8n só funciona no `.pages.dev` se a Operação liberar
   temporariamente a origem `https://antere-site.pages.dev` no CORS dos webhooks. Se não liberar, o envio é testado logo depois da troca.
9. **Links internos:** rodapé, menu e caixa da LGPD apontam para `www.antere.com.br` e `legal.antere.com.br`.
10. **Testes do repositório:** `NODE_PATH=$(npm root -g) node testes/site.test.js` com tudo ok (rodam sobre `public/`).

**Depois da troca, nos endereços oficiais:**
- repetir os itens 1 a 7;
- `http://` vai para `https://`;
- `https://antere.com.br` vai para `https://www.antere.com.br`;
- os 3 endereços da Meta abrem com 200, sem redirecionar;
- um envio de teste do formulário ("ZZ TESTE", `delivered@resend.dev`), com a Operação conferindo e depois removendo;
- a Operação confere o monitor de entregas.

## (e) Data da troca

Proposta: **quinta-feira, 19/11/2026, às 21h (Brasília)**, com o clique do Rodrigo. Isso deixa:
- 16/11 (renovação do Netlify) antes da troca, para que uma volta caia num Netlify com créditos;
- de 16 a 18/11 para criar os projetos no Pages e fazer o teste (d);
- até 01/12 de folga, com uma segunda data reserva na **terça, 24/11, às 21h**.

**Quem faz o quê:**
- **Rodrigo (com o Claude no Chrome):** cria a conta e os 2 projetos no Cloudflare Pages, ligados ao GitHub, com a configuração de
  (b). Faz a troca na GoDaddy de (c).
- **Sessão Site:** acompanha, confere os testes (d) e ajusta o script ou as regras, se precisar.
- **Operação:** CORS temporário (opcional), monitor de entregas e conferência do envio de teste.

## Aprovado em 10/11 e próximos passos

Aprovado pelo Rodrigo: 2 projetos (`antere-site` e `antere-legal`); raiz por encaminhamento 301 da GoDaddy (ou mantida no Netlify só
redirecionando, se o 301 não funcionar com https); troca na quinta, 19/11, às 21h, reserva na terça, 24/11, às 21h. Os dois ajustes de
10/11 vão ao ar pelo Cloudflare Pages; o Netlify não publica mais nada.

- **16/11 (segunda), à noite:** parar os builds no Netlify (o site continua no ar com o último deploy) e criar os 2 projetos no Pages,
  sem domínio personalizado, pelo passo a passo enviado na conversa.
- **17/11 (terça):** teste (d) nos endereços `.pages.dev`; ajustes no `cloudflare/montar.sh`, se precisar.
- **18/11 (quarta):** véspera: foto da zona DNS, valores atuais anotados, TTL de `www`, `legal` e `@` em 600 s.
- **19/11 (quinta), 21h:** domínios personalizados no Pages e troca na GoDaddy, na ordem legal, www, raiz.
