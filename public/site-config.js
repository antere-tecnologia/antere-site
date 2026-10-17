/* Chave do formulário de proposta em 2 etapas (antere-site, README, seção "Chave do formulário").
   false: os botões "Quero minha proposta" levam ao formulário antigo do n8n (/form/proposta) e a conversão do Google Ads
          dispara no clique do botão.
   true:  os botões levam a /proposta.html (formulário em 2 etapas) e a conversão dispara no envio com sucesso da etapa 1.
   Só ligar depois de os webhooks site-proposta-etapa1/2 estarem publicados e do teste de ponta a ponta. */
window.ANTERE_FORM_NOVO = true;  /* religada em 17/10/2026, depois do teste final do Rodrigo (proposta no modelo novo) */

/* Chave do aviso de cookies (LGPD), README, seção "Aviso de cookies".
   false: a tag do Google Ads carrega em toda visita, como antes, e não aparece aviso.
   true:  aparece a faixa "Aceitar" / "Recusar" (Consent Mode v2): a tag carrega com os cookies de anúncios negados e o "Aceitar" os
          libera; a escolha fica guardada no navegador.
   Voltar para false desliga a faixa e o Consent Mode (a tag segue carregando, como antes). */
window.ANTERE_COOKIES = true;  /* ligada em 17/10/2026, com o Consent Mode v2 (anúncios negados até o "Aceitar") */
