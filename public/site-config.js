/* Chave do formulário de proposta em 2 etapas (antere-site, README, seção "Chave do formulário").
   false: os botões "Quero minha proposta" levam ao formulário antigo do n8n (/form/proposta) e a conversão do Google Ads
          dispara no clique do botão.
   true:  os botões levam a /proposta.html (formulário em 2 etapas) e a conversão dispara no envio com sucesso da etapa 1.
   Só ligar depois de os webhooks site-proposta-etapa1/2 estarem publicados e do teste de ponta a ponta. */
window.ANTERE_FORM_NOVO = false;

/* Chave do aviso de cookies (LGPD), README, seção "Aviso de cookies".
   false: a tag do Google Ads carrega em toda visita, como antes, e não aparece aviso.
   true:  aparece a faixa "Aceitar" / "Recusar"; a tag só carrega depois do "Aceitar" e a escolha fica guardada no navegador.
   Só ligar depois da validação da conversão do Google Ads. */
window.ANTERE_COOKIES = false;
