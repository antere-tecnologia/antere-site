# Formulário novo: e-mail conferido antes do envio — combinado da sessão Site com a Operação (16/10/2026)

Resposta da sessão Site a `antere-automacao/docs/proposta_formulario_email_1610.md` (aprovada pelo Rodrigo para o formulário novo).
O lado do site está pronto em `public/proposta.html` (gerador: `_src/componentes.py`) e testado com o servidor simulado
(`testes/site.test.js`). A chave do formulário continua desligada (`window.ANTERE_FORM_NOVO = false`).

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
   Com a chave do formulário desligada, `/proposta.html` manda o visitante ao formulário antigo e os dois parâmetros se perdem. Então os
   links novos só devem entrar depois de a chave ser ligada.
4. **`lib/`:** a lista de domínios e a função de distância, com a regra do `.br` a mais (acima), para o site usar a mesma.
5. **Contrato (`docs/contrato_formulario_site.md`):** a parte das telas está nesta página; peço que entre no contrato junto com a parte do
   n8n, ou me avise para eu mandar o texto no formato do contrato.

## Teste de ponta a ponta

Entra no mesmo teste já pendente do formulário (`/proposta.html?previa=1`, com CNPJ e e-mail internos combinados com a Operação):
um envio com domínio sem MX (deve dar `422`), um com erro comum (sugestão na tela) e, quando os links com token existirem, um link de
lote com `lead_id` e `token`.
