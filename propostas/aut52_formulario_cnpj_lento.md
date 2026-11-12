# AUT-52: tela do formulário quando o CNPJ demora (lado do site)

Pedido da Operação: `antere-automacao/docs/aviso_site_aut52_1211.md` (branch `claude/operacao-zz-ecoplast-tef-mgmcgb`), aprovado pelo
Rodrigo em 12/11/2026.

## Preparado em 12/11 (branch `claude/kind-galileo-2wjuc2`, fora da main)

- Espera de até 60 s nas duas etapas (antes: 30 s), com "Estamos preparando sua proposta…".
- Sem resposta em 60 s, queda da rede no meio do envio ou erro do servidor (5xx e qualquer outro código que não seja 200, 422 ou 429):
  tela final "Recebemos seu pedido." / "Vamos falar com você em instantes.", sem conversão, sem deixar reenviar, e o pedido guardado na
  sessão é apagado. "Não foi possível enviar" não aparece mais depois de o pedido sair.
- Sem internet antes de enviar (nada sai): "Você está sem internet. Confira a conexão e tente de novo." e o botão continua liberado.
- 422 (campos) e 429 (limite) seguem como antes e liberam o botão.
- Botão travado do primeiro clique até a resposta ou os 60 s; segundo clique, Enter e `requestSubmit` não reenviam.
- Gerador (`_src/componentes.py`) e `public/proposta.html` iguais; testes "AUT-52" (34 ok).

## Pendente

1. **Forma da resposta da etapa 1** (a Operação publica no aviso até 17/11). A etapa 1 passa a responder antes da consulta do CNPJ e da
   criação do lead; a tela de hoje usa `lead_id`, `pedido_token`, `produtos` e `empresa` (razão social, cidade, CNPJ confirmado) dessa
   resposta, e o `lead_id` vai na etapa 2. Ajustar a tela quando a forma chegar, inclusive a resposta de "pedido já aberto" (mesmo CNPJ e
   e-mail em 10 min).
2. **Publicar** só depois da confirmação, no aviso, da publicação da Operação (qua 18/11, 21h02), e responder no aviso com a data em que
   a tela entrou no ar.
   - Os builds do Netlify param em 16/11; a publicação na `main` vai para o Cloudflare Pages (`antere-site.pages.dev`) e entra no ar em
     www.antere.com.br com a troca do DNS de qui 19/11, 21h.
   - Entre 18/11 21h02 e a troca, o site no ar (Netlify) segue com a tela antiga falando com o n8n novo: a Operação precisa manter a
     resposta da etapa 1 compatível com a tela antiga nesse intervalo (ou aceitar que, nele, a tela antiga pule a etapa 2).
