#!/bin/sh
# 下載文章封面用的產品與草本實拍（uhealthfit.com 官網素材）到 build-src/covers/src/（不進 git）
# 用法：sh build-src/covers/fetch.sh
cd "$(dirname "$0")" && mkdir -p src && cd src || exit 1
B=https://uhealthfit.com
for p in \
  products/herbal-soothing-repair-eye-cream/eye-cream-product-shot-wide.png \
  products/herbal-soothing-repair-eye-cream/herbal-soothing-repair-eye-cream-jar-front.png \
  products/eye-patches/2-day-trial.png products/eye-patches/eye-patches-box-front.png \
  products/eye-patches/3-boxes.png products/eye-patches/six-boxes.png products/eye-patches/9-boxes.png \
  products/herbal-soothing-repair-cream/herbal-soothing-repair-cream-jar-front.png \
  products/herbal-clarifying-cream/herbal-clarifying-cream-jar-front.png \
  products/herbal-lifting-revitalizing-serum/herbal-lifting-revitalizing-serum-bottle-front.png \
  products/calmoon/calmoon-ingredients-collage.png products/calmoon/calmoon-bottle-front.png \
  products/lumiview/lumiview-bottle-front.png products/enerbalance/enerbalance-bottle-front.png \
  products/dentaforte/dentaforte-bottle-front.png products/herbalflow/herbalflow-bottle-front.png \
  products/herbalflow/plan-dietary-fiber.png \
  ingredients/dendrobium.png ingredients/astragalus.png ingredients/panax-ginseng.png \
  ingredients/chinese-yam.png ingredients/poria.png ingredients/goji.png ingredients/chrysanthemum.png
do
  n=$(echo "$p" | tr '/' '_')
  [ -s "$n" ] || curl -sf -o "$n" "$B/$p" || echo "下載失敗：$p"
done
echo "完成：$(ls | wc -l | tr -d ' ') 個檔案"
