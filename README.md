# Site institucional Antere

Publicado no Netlify (projeto `antere-site`) a partir da pasta `public/`.

- `public/`: tudo que vai ao ar — páginas (`index.html`, `como-funciona.html`, `solucoes.html`, `sobre.html`, `contato.html`, `calculadora.html`, `404.html`), `assets/`, `legal/`, `robots.txt`, `sitemap.xml`, `_headers` e `_redirects`.
- `public/legal/`: Política de Privacidade, Termos de Uso e Exclusão de Dados. Continuam acessíveis em `legal.antere.com.br` pelas regras de `_redirects` (o domínio precisa estar adicionado ao projeto no Netlify).
- `_src/`: gerador das páginas (`build_site.py`) e logos originais. Não é publicado. Depois de gerar, copie os HTML para `public/`.
- `netlify.toml`: `publish = "public"`, sem comando de build.

Formulário de contato envia POST para `https://raregoat-n8n.cloudfy.live/webhook/site-contato`.
CTA de proposta aponta para `https://raregoat-n8n.cloudfy.live/form/proposta?ref=site_institucional`.
UTM (28/09/2026): um script em todas as páginas guarda `utm_source`, `utm_medium`, `utm_campaign` e `gclid` da chegada (sessionStorage) e acrescenta esses parâmetros aos links de proposta, mantendo o `ref`. Testes e fonte do script: `antere-automacao/n8n/ferramentas/site_utm/utm_inline.js` e `n8n/testes/site_utm.test.js`.
