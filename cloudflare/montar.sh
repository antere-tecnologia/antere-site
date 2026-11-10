#!/bin/sh
# Monta a saída de um projeto do Cloudflare Pages a partir de public/ (plano em propostas/migracao_cloudflare_pages.md).
#   sh cloudflare/montar.sh www    -> dist-www/   (www.antere.com.br)
#   sh cloudflare/montar.sh legal  -> dist-legal/ (legal.antere.com.br: as 3 páginas legais na raiz)
# O public/_redirects é do Netlify (regras por domínio, que o Pages não aceita) e não vai para o Pages.
# O Pages redireciona /x.html para /x (308); as regras 200 abaixo servem cada página no endereço com .html, sem redirecionar.
set -eu
alvo="${1:-}"
case "$alvo" in
  www)
    d=dist-www; rm -rf "$d"; mkdir -p "$d"
    cp -R public/. "$d"/; rm -f "$d/_redirects"
    : > "$d/_redirects"
    for f in public/*.html; do n=$(basename "$f" .html); [ "$n" = 404 ] && continue; [ "$n" = index ] && continue
      printf '/%s.html  /%s  200\n' "$n" "$n" >> "$d/_redirects"; done
    for f in public/legal/*.html; do n=$(basename "$f" .html)
      printf '/legal/%s.html  /legal/%s  200\n' "$n" "$n" >> "$d/_redirects"; done
    ;;
  legal)
    d=dist-legal; rm -rf "$d"; mkdir -p "$d"
    cp public/legal/*.html "$d"/
    : > "$d/_redirects"
    for f in public/legal/*.html; do n=$(basename "$f" .html)
      printf '/%s.html  /%s  200\n' "$n" "$n" >> "$d/_redirects"; done
    printf '/  /privacidade  200\n' >> "$d/_redirects"
    printf '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n' > "$d/_headers"
    ;;
  *) echo "uso: sh cloudflare/montar.sh www|legal" >&2; exit 2 ;;
esac
echo "ok: $d ($(find "$d" -type f | wc -l | tr -d ' ') arquivos)"
