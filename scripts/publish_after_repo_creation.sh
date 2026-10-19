#!/usr/bin/env bash
# Publicar somente quando o usuário já tiver criado DevPrijoz/bi-snp-360 vazio e privado.
# NUNCA publica GitHub Pages ou conecta fontes institucionais automaticamente.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/release_guard.py
python scripts/validate_assets.py
python -m pytest -q
node --check web/assets/app.js
TARGET="https://github.com/DevPrijoz/bi-snp-360.git"
if git remote get-url origin >/dev/null 2>&1; then
  EXISTING="$(git remote get-url origin)"
  if [[ "$EXISTING" != "$TARGET" ]]; then
    echo "BLOQUEIO: remote origin diferente do repositório principal esperado." >&2
    exit 1
  fi
else
  git remote add origin "$TARGET"
fi
if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "BLOQUEIO: a publicação só poderá ocorrer pela branch main." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "BLOQUEIO: não é permitido publicar árvore de trabalho suja." >&2
  exit 1
fi
echo "Verificações aprovadas. O push requer autenticação GitHub autorizada."
git push -u origin main
git push origin v0.2.0
