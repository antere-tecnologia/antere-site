# Opt-in do WhatsApp no formulário: combinado com a Operação (30/10/2026)

Pedido: `docs/pedido_site_optin_3010.md` no `antere-automacao` (branch `claude/adoring-keller-tj3bpx`), aprovado pelo Rodrigo em 30/10.

## No ar desde 30/10/2026, 13h06 UTC (10h06 em Brasília)

- Commit `02f5a06` na `main`; deploy Netlify `6ae4965877c7dec6afef708b` (produção, *ready*), só `proposta.html` mudou.
- Etapa 1: caixa "Quero receber a proposta e o acompanhamento da Antere pelo WhatsApp", logo abaixo do campo de WhatsApp,
  desmarcada, opcional, separada da LGPD (que segue obrigatória e com o mesmo texto).
- Corpo da etapa 1: `optin_whatsapp` (`true`/`false`, sempre enviado) e `optin_whatsapp_texto` (o texto da caixa). Etapa 2 sem mudança.
- Testes do site conferidos com a `formulario_site.js` da `main` (ignora os campos) e com a do branch da Operação (grava `'sim'`/vazio).

## Envios de teste (segunda, 02/11/2026, depois das 20h em Brasília, quando a Operação publicar)

Feitos pela sessão Site, pelo formulário no ar (`/proposta.html`), só a etapa 1:

| | nome | e-mail | caixa |
|---|---|---|---|
| 1 | ZZ TESTE Optin Sim | delivered@resend.dev | marcada |
| 2 | ZZ TESTE Optin Nao | delivered@resend.dev | desmarcada |

Pedidos à Operação:
1. Avisar quando a parte dela estiver publicada (o envio só sai depois disso).
2. Garantir que nenhum WhatsApp da cadência saia para essas duas linhas (nome começando com "ZZ TESTE").
3. Conferir as duas linhas da base (`optin_whatsapp` = `sim` na 1 e vazio na 2, data em Brasília, texto, origem `formulario_site`) e o card.
4. Depois da conferência, **remover as duas linhas de teste da base e os dois cards no RD** e avisar.
