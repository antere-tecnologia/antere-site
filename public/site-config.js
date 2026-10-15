/* Chave do formulário de proposta em 2 etapas (antere-site, README, seção "Chave do formulário").
   false: os botões "Quero minha proposta" levam ao formulário antigo do n8n (/form/proposta) e a conversão do Google Ads
          dispara no clique do botão.
   true:  os botões levam a /proposta.html (formulário em 2 etapas) e a conversão dispara no envio com sucesso da etapa 1.
   Só ligar depois de os webhooks site-proposta-etapa1/2 estarem publicados e do teste de ponta a ponta. */
window.ANTERE_FORM_NOVO = false;
