# Formulário novo: e-mail conferido antes do envio — combinado da sessão Site com a Operação (16/10/2026)

Resposta da sessão Site a `antere-automacao/docs/proposta_formulario_email_1610.md` (aprovada pelo Rodrigo para o formulário novo).
O lado do site está pronto em `public/proposta.html` (gerador: `_src/componentes.py`) e testado com o servidor simulado
(`testes/site.test.js`). A chave do formulário foi ligada em 17/10/2026 (`window.ANTERE_FORM_NOVO = true`), depois do teste de ponta a ponta do Rodrigo.

Observação: em 16/10, 16h39 UTC, a proposta estava no branch `claude/adoring-keller-tj3bpx` e ainda não na `main` do `antere-automacao`.

## O que o site já faz

### Regra 1: domínio que não recebe e-mail (servidor)

- O site não consulta DNS. Quem confere é o n8n, na etapa 1.
- Se a etapa 1 responder `422` com `erros: [{ campo: 'email', erro: 'dominio_sem_email', sugestao? }]`, o site:
  - marca o campo e mostra "Esse endereço não recebe e-mail. Confira o que vem depois do @.";
  - não conta conversão e não deixa seguir.
- Se vier `sugestao`, o site mostra "Você quis dizer …?" com ela. Aceita os dois formatos: só o domínio (`empresa.com.br`) ou o e-mail
  inteiro (`compras@empresa.com.br`).
- Falha da consulta de DNS: o site não precisa saber. O servidor aceita e marca `mx_nao_conferido`, como na proposta.

### Regra 2: sugestão de correção (site, o lead confirma)

- Mesma lista da proposta: gmail.com, hotmail.com, outlook.com, live.com, yahoo.com, yahoo.com.br, icloud.com, uol.com.br, bol.com.br
  e terra.com.br.
- **Regra decidida pelo Rodrigo (16/10), a mesma da `lib/`:**
  - distância de digitação (Damerau-Levenshtein restrita: letra a mais, a menos, trocada ou duas vizinhas invertidas) até **1** quando o
    nome antes do primeiro ponto do domínio digitado tem até 5 letras, e até **2** quando tem mais;
  - a **primeira letra** do domínio digitado tem de ser a mesma do domínio da lista (sem isso, `olive.com` estaria a 1 letra de
    `live.com`);
  - mais a regra do `.br` sobrando, abaixo.
- **Regra a mais, para o exemplo `gmail.com.br` da proposta:** um domínio da lista seguido de `.br` que não está na lista
  (`gmail.com.br`, `hotmail.com.br`) sugere o da lista. Sem essa regra, `gmail.com.br` fica a distância 3 de `gmail.com` e não teria
  sugestão. **Peço que a função da `lib/` tenha a mesma regra**, para o site e o n8n darem a mesma resposta.
- A sugestão aparece ao sair do campo e, de novo, no "Continuar". Ela não troca sozinha: o lead escolhe "Sim, trocar" ou
  "Não, está certo". Enquanto não responder, o envio espera. A resposta vale para aquele valor.
- Casos testados (para a `lib/` usar os mesmos): recebem sugestão gmial.com, gmail.con, hotmial.com, outlok.com, outllok.com, gmail.com.br,
  yaho.com.br, gmal.com, gmai.com, hotmal.com e yhaoo.com. Não recebem: olive.com, blive.com, gmaxyz.com, uol.com, gmail.com,
  empresaexemplo.com.br, yahoo.com.br e terra.com.br.
- **Risco dos domínios curtos:** resolvido pela regra de 16/10 acima.
- Quando a `lib/` da Operação sair, o site troca a sua cópia da lista e da função pela mesma regra, e um teste compara as duas respostas.

### Regra 3: abrir já preenchido (site + endpoint novo)

- Quando a URL de `/proposta.html` traz `lead_id` (24 hex) e `token` (32 hex), o site:
  1. tira os dois da barra de endereço logo ao abrir (as UTM ficam);
  2. chama `GET https://raregoat-n8n.cloudfy.live/webhook/form-proposta-dados?lead_id=…&token=…` (tempo máximo de 8 s);
  3. com resposta `200` e `email`, preenche e-mail e nome (`nome_contato`) se estiverem vazios. O lead pode editar. `empresa` não é
     usada na etapa 1, porque a razão social vem da consulta do CNPJ;
  4. com `404`, erro ou tempo esgotado, abre vazio, como hoje, e não manda nada de cadastro.
- No envio da etapa 1, só quando o preenchimento deu certo, o corpo leva três campos a mais:

| Campo | Valor |
|---|---|
| `lead_id_cadastro` | o `lead_id` do link |
| `token_cadastro` | o `token` do link |
| `email_alterado` | `true` se o e-mail enviado for diferente do cadastrado (sem diferenciar maiúsculas), senão `false` |

- Os nomes têm o sufixo `_cadastro` para não confundir com o `lead_id` e o `pedido_token` que a etapa 1 devolve para a etapa 2.

## O que o site precisa do servidor (lado da Operação)

1. **Etapa 1 (`site-proposta-etapa1`):**
   - conferir MX/A do domínio e responder `422` `dominio_sem_email`, com `sugestao` quando houver;
   - aceitar `lead_id_cadastro`, `token_cadastro` e `email_alterado`;
   - com token válido, usar o lead cadastrado em vez de criar outro, marcar `email_alterado` e seguir a regra da proposta (proposta para o
     digitado; se ele não passar na regra 1, para o cadastrado);
   - com token inválido, ignorar os três campos e seguir como pedido novo, sem erro e sem dizer se o lead existe.
2. **Endpoint novo (`form-proposta-dados`):** `GET`, só leitura, `200` com `{ email, nome_contato, empresa }` quando o token confere e
   `404` sem corpo útil nos outros casos. Precisa do mesmo CORS das etapas (só `https://www.antere.com.br` e `https://antere.com.br`)
   e de limite por IP.
3. **Links de lote e campanha:** levar `lead_id` e `token` para `https://www.antere.com.br/proposta.html` (não para `/form/proposta`).
   A chave do formulário foi ligada em 17/10/2026, então os links novos já podem apontar para `/proposta.html` assim que o endpoint
   `form-proposta-dados` e o token nos links existirem.
4. **`lib/`:** a lista de domínios e a função de distância, com a regra do `.br` a mais (acima), para o site usar a mesma.
5. **Contrato (`docs/contrato_formulario_site.md`):** a parte das telas está nesta página; peço que entre no contrato junto com a parte do
   n8n, ou me avise para eu mandar o texto no formato do contrato.

## Teste de ponta a ponta

Entra no mesmo teste já pendente do formulário (`/proposta.html?previa=1`, com CNPJ e e-mail internos combinados com a Operação):
um envio com domínio sem MX (deve dar `422`), um com erro comum (sugestão na tela) e, quando os links com token existirem, um link de
lote com `lead_id` e `token`.

## 17/10/2026: a pergunta da conta PJ C6 saiu da etapa 2 (decisão do Rodrigo)

- A tela não pergunta mais "Tem ou vai abrir conta PJ no C6 Bank?" nem mostra o texto da isenção da implantação.
- **Enquanto o contrato exigir `conta_pj_c6`** (hoje é obrigatório em `docs/contrato_formulario_site.md` e em
  `validarEtapa2`, na `lib/formulario_site.js`), o site manda `conta_pj_c6: "nao"`. Assim não promete a isenção, e a etapa 2 não volta
  com `422`.
- **Pedido à Operação:**
  - tirar a exigência do campo no contrato e na `validarEtapa2`, aceitando a etapa 2 sem ele;
  - decidir o que a Geração de Proposta usa no lugar de "Conta PJ C6" (`pedidoGeracao`), por exemplo, a proposta sempre explicando
    a isenção com a conta PJ.
  - Depois de publicado, avisar a sessão Site: ela troca `CONTA_PJ_ENVIO` para `""` em `_src/componentes.py` e o campo deixa de ir.
    O teste "formulário C6 Pay" muda junto.

**17/10/2026, depois:** a Operação tirou o campo do contrato e da `validarEtapa2` (commit 58cb38f, branch `claude/clever-faraday-76ga3f`,
"pronto no repositório, a publicar"). O site deixou de mandar `conta_pj_c6` (`CONTA_PJ_ENVIO = ""`). O corpo da etapa 2 do site passa na
`validarEtapa2` desse commit e não passa na versão da `main` (d9ee493), que ainda exige o campo. **O teste de ponta a ponta depende da
publicação desse patch no n8n.**

**17/10/2026, fim do dia:** a Operação publicou no n8n o Formulario_Site_Proposta 03852d6f, que aceita a etapa 2 sem `conta_pj_c6` (merge
na `main` do `antere-automacao` em c349255). O Rodrigo fez o teste de ponta a ponta com `?previa=1` e passou (proposta gerada às 03h19, com origem e UTM corretas). A chave do formulário foi
ligada (`window.ANTERE_FORM_NOVO = true`). Seguem pendentes, do lado da Operação: a conferência de MX na etapa 1 (`dominio_sem_email`), o
endpoint `form-proposta-dados` e o token nos links de lote e campanha.

## 17/10/2026: produtos na etapa 1 (pedido do Rodrigo) — proposta de contrato para a Operação

**Estado:** pronto no site, num branch, **não publicado**. A chave do formulário está ligada desde 46646fa, então esta mudança só pode ir
para a `main` do site junto com a publicação do contrato novo no n8n (senão o formulário no ar quebra).

### Etapa 1

| Campo | Mudança |
|---|---|
| `produtos` | **novo, obrigatório:** lista com 1 a 4 de `tef`, `c6pay`, `link`, `pdvet` (pergunta "O que você procura?", múltipla escolha). |
| `caixas` | **sai da etapa 1** (vai para a etapa 2, só com `tef`). |
| `procura` | O site continua mandando, por compatibilidade: `pdvet` quando `produtos` é só `["pdvet"]`, senão `c6pay`. Pode ser ignorado quando o n8n usar `produtos`. |

- Resposta: `proximo: "pdvet"` (com `url`) quando `produtos` é só `["pdvet"]`; `proximo: "etapa2"` em qualquer outro caso, inclusive PDVet com
  outro produto. O n8n guarda `produtos` no pedido, para a etapa 2.
- A conversão do Google Ads continua no envio com sucesso da etapa 1 (os dois casos).

### Etapa 2

- Sai a pergunta "Produtos". O site manda `produtos` (a mesma lista da etapa 1, para conferência) e só os campos dos produtos escolhidos:

| Produto | Campos (todos obrigatórios quando o produto foi escolhido) |
|---|---|
| sempre | `lead_id`, `pedido_token`, `razao_social`, `produtos`, `website` (isca, vazio) |
| `tef` | `sistema_pdv` (texto até 80), `lojas` (1 a 999), `caixas` (1 a 999) |
| `c6pay` | `vendas_cartao` (`ate_8mil`, `8_30mil`, `acima_30mil`) e `recebimento` (`d1`, `d31`) |
| `link` | `faixa_link` (as 8 faixas de hoje; `acima_10000` = escalonar) |
| `pdvet` | nenhum campo a mais |

- Mudança de sentido: `vendas_cartao` e `recebimento` passam a ser do **C6 Pay** (antes vinham com o TEF). `sistema_pdv` e `lojas` deixam de
  ser sempre obrigatórios: só com `tef`.
- **Pedido à Operação:** atualizar `validarEtapa1`/`validarEtapa2` (`lib/formulario_site.js`), o `pedidoGeracao` (o que a Geração usa quando
  não houver `sistema_pdv`/`lojas`, por exemplo só C6 Pay ou só link) e o contrato; publicar e avisar a sessão Site, que então grava na
  `main` a versão do branch (testes prontos: `testes/site.test.js`, com conferência pela `lib/` assim que ela tiver o contrato novo).

**17/10/2026, tarde: contrato publicado pela Operação às 10h50** (`antere-automacao/docs/aviso_site_produtos_etapa1_1710.md`, main 258d546).
O site, no branch `claude/kind-galileo-2wjuc2` (fora da `main`), segue o contrato publicado:
- etapa 1 manda `produtos` (lista) e `caixas`, e **não manda mais `procura`**;
- etapa 2 manda sempre `sistema_pdv` e `lojas`, mais `vendas_cartao`/`recebimento` com `c6pay` e `faixa_link` com `link`; não manda `produtos`;
- com PDVet junto de outro produto, a tela final oferece o portal da PDVet (`interesse_adicional` e `url_pdvet` da resposta).
Diferenças em relação ao pedido original das telas (a decidir pelo Rodrigo): o **nº de caixas ficou na etapa 1** e **sistema PDV e lojas aparecem
para todos os produtos**, porque o contrato publicado exige assim. Os corpos passam na `validarEtapa1`/`validarEtapa2` de 258d546.
Depois de ir para a `main`, avisar a Operação para tirar o `procura` do contrato.

**17/10/2026: telas aprovadas pelo Rodrigo; versão gravada na `main` do site.** O site não manda mais `procura`. **Pedido à Operação:** tirar o
`procura` do contrato e da validação (o pedido antigo, que já começou com `procura`, só termina no formato antigo).

## 17/10/2026, 17h50: chave desligada — "Não encontramos seu pedido" na etapa 2 (teste do Rodrigo no ar, link + PDVet)

- A chave do formulário foi desligada (`window.ANTERE_FORM_NOVO = false`, commit 15e62eb, no ar às 17:50 UTC). Os botões voltaram ao
  formulário antigo do n8n e a conversão voltou para o clique.
- **Lado do site conferido (teste com valores aleatórios de `lead_id` e `pedido_token`, link + PDVet, com recarga da página no meio):**
  - etapa 1 envia `produtos: ["link","pdvet"]`, `caixas` e sem `procura`; recebe `lead_id` (24 hex) e `pedido_token` (32 hex);
  - etapa 2 envia **exatamente** esse `lead_id` e esse `pedido_token`, mais `razao_social`, `sistema_pdv`, `lojas`, `faixa_link` e `website`;
  - os dois corpos passam na `validarEtapa1`/`validarEtapa2` da `lib/` da `main` (4e5fb0f) quando a linha do pedido é a da etapa 1.
- **Hipótese no n8n (para a Operação conferir):** o nó "26 Validar a etapa 2" usa `pedidos[0]`, a **primeira** linha da `form_site_pedidos` com o
  `lead_id`. Se o mesmo `lead_id` tiver mais de uma linha (por exemplo, o teste das 03h19 com os mesmos dados, se o RD reaproveitar a
  negociação/lead), a comparação é feita com a linha antiga, o token não bate e a resposta é `404` `pedido_nao_encontrado` — exatamente a
  mensagem vista. Reproduzido na `lib/`: com uma linha antiga do mesmo `lead_id`, `validarEtapa2` devolve `nao_encontrado`.
  Correção sugerida: escolher a linha cujo `pedido_token` bate com o enviado (ou a mais recente), e conferir se o `lead_id` pode se repetir.
- Outras causas que dão o mesmo 404: a linha da etapa 1 não ter sido gravada (ou gravada sem `pedido_token`), ou `procura` gravado fora de
  `c6pay`/`proposta`. A execução da etapa 2 do teste do Rodrigo mostra qual foi.

**17/10/2026, 18h10:** a Operação corrigiu o "pedido não encontrado" (`antere-automacao` 0b13f74: a etapa 2 usa a linha do `lead_id` e do
token; lead repetido dava 404), como na hipótese acima.

## 18/10/2026: C6 Pay só com TEF; caixas, sistema PDV e lojas só com TEF (pedido do Rodrigo) — pedido à Operação

**Estado:** pronto no site, no branch `claude/kind-galileo-2wjuc2`, **fora da `main`**. Só vai para a `main` quando a Operação confirmar que
o n8n aceita o envio abaixo (hoje, `validarEtapa1` exige `caixas` e `validarEtapa2` exige `sistema_pdv` e `lojas` para qualquer produto).

- **Tela:** marcar C6 Pay marca também o TEF e mostra "O C6 Pay é oferecido junto com o TEF integrado ao caixa."; desmarcar o TEF desmarca o
  C6 Pay. Ou seja, o site nunca manda `c6pay` sem `tef`.
- **Etapa 1:** `caixas` só vai (e só é obrigatório) quando `produtos` tem `tef`. Sem TEF, o campo não vai.
- **Etapa 2:** `sistema_pdv` e `lojas` só vão (e só são obrigatórios) quando o pedido tem `tef`. Sem TEF (por exemplo, só link, ou link +
  PDVet), a etapa 2 manda `lead_id`, `pedido_token`, `razao_social`, `website` e `faixa_link`.
- **Pedido à Operação:**
  1. `validarEtapa1`: exigir `caixas` só com `tef`;
  2. `validarEtapa2`: exigir `sistema_pdv` e `lojas` só quando o pedido da etapa 1 tem `tef`;
  3. se quiser, recusar `c6pay` sem `tef` (`422` `produtos` `invalido`), já que o site não manda mais essa combinação;
  4. `pedidoGeracao`: o que vai em "Sistema PDV", "Quantidade de lojas" e "Quantidade de PDVs" quando não houver TEF;
  5. atualizar o contrato, publicar e avisar a sessão Site. Os testes do site (`testes/site.test.js`) passam a conferir esses corpos com a
     `lib/` assim que ela aceitar a etapa 1 sem `caixas`.

**17/10/2026, 15h32 (Operação) e gravação no site:** o n8n aceita caixas, sistema PDV e lojas vazios sem TEF e recusa `c6pay` sem `tef`
(`422` `produtos` `c6pay_sem_tef`, aviso `docs/aviso_site_regras_tef_1710.md`). Os testes do site passam com a `lib/` publicada (901606e),
inclusive os envios sem TEF. O site mostra uma mensagem para `c6pay_sem_tef` nas duas etapas. Versão gravada na `main`; a chave segue desligada.

**17/10/2026, noite:** a etapa 2 do n8n passou a trazer `interesse_adicional: ["pdvet"]` e `url_pdvet` quando a PDVet vem com outro produto
(aviso `docs/aviso_teste_final_pdvet_rd_1710.md`, Formulario_Site_Proposta `dba42d66`). A tela final "Sua proposta foi enviada." usa esse
`url_pdvet` no bloco "Você também marcou o Sistema PDV (PDVet)." (se não vier, usa o da etapa 1, quando houver). Gravado na `main`; a chave
segue desligada. Falta o reteste do Rodrigo com link + PDVet em `?previa=1`.
