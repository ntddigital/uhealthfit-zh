# 優健堂 UHealthFit × WiseQuest 介紹網站（靜態 HTML）
製作：NTD Digital · 2026-10-19

## 結構
- index.html 首頁 ｜ series/ 六大系列頁 ｜ products/ 11 個單品／組合頁 ｜ blog/ 選購指南首頁＋32 篇
- quiz.html 30 秒測驗（結果→系列／產品／指南；Email 留資送 Klaviyo Email List）｜ about-us.html 關於我們（優健堂）｜ about.html 研發者黃醫師與品牌理念 ｜ faq.html
- css/style.css、js/main.js 共用 ｜ sitemap.xml、robots.txt

## 部署
Cloudflare Pages：連結 GitHub repo 的 main 分支，push 後自動部署。正式網址 https://us.uhealthfit.com/（自訂網域，DNS 在 GoDaddy：CNAME us → uhealthfit-zh.pages.dev）；Cloudflare 預設網址 https://uhealthfit-zh.pages.dev/。更換網域時改 build-src/build.py 的 SITE_URL 重建。Cloudflare 會把 .html 網址 308 轉址成乾淨網址（/about、/products/calmoon、/blog/），標準網址、sitemap 與結構化資料都已使用乾淨網址（build.py 的 page_url）。GitHub Pages 已不再使用。

## 怎麼改網站
不要直接改根目錄的 HTML（34 頁會不同步）。改 `build-src/` 裡的資料與模板，然後在 repo 根目錄執行 `python3 build-src/build.py`，再 commit & push：
- 產品、系列、FAQ、測驗題目：`build-src/build.py` 上半部的 SERIES / PRODUCTS / QUIZ / FAQS
- 導購文章：`build-src/posts/<slug>.html`（第一行 JSON meta → `---END-META---` → HTML 片段）；新增文章請加入 build.py 的 POST_ORDER
- 樣式／互動：`build-src/src/style.css`、`build-src/src/main.js`
- 文案合規規範：`build-src/BRIEF.md`
- Logo 與圖片：導覽列用 uhealthfit.com 的優健堂 SVG（LOGO）、頁尾用 zh.uhealthfit.com 商店頁首的 UHealthFit 白色字標（`build-src/src/img/`）；六大系列情境照與產品實拍取自 zh.uhealthfit.com（Shopify CDN，見 build.py 的 SHOP_CDN／shop_img，`&width=` 可調尺寸），其餘產品圖取自 uhealthfit.com
上線前：
1. 自訂網域 us.uhealthfit.com 已上線，SITE_URL 已設為正式網域；
2. 追蹤碼已安裝（build.py 的 GTM_ID／GA4_ID／META_PIXEL_ID，與 zh.uhealthfit.com 相同）：GTM GTM-W58N8HRV、GA4 G-M63Z9F6FR7（gtag.js）、Meta Pixel 2216128798841618。js/main.js 會在購買點擊時送出 begin_checkout_redirect 與 ShopRedirect、測驗完成送 quiz_complete、留資送 generate_lead 與 Lead；
3. 所有「購買」按鈕都指向 zh.uhealthfit.com 商品頁：訪客若從廣告或帶 UTM 的連結進站，會原樣帶上原本的 UTM 與點擊編號（fbclid、gclid 等）；沒有來源時才加上 utm_source=uhealthfit-site、utm_medium=referral。Meta 事件不帶產品、頁面或電子書類別；
4. Klaviyo：公開 company_id Xxa5rp、List TKC3Bu（Email List, single opt-in）；留資會帶 quiz_result 屬性，可用來建 Flow。
