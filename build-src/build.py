# -*- coding: utf-8 -*-
"""優健堂 UHealthFit × WiseQuest 靜態網站產生器 · NTD Digital 2026-10-19
位置：repo/build-src/build.py　執行：python3 build-src/build.py　→ 直接輸出到 repo 根目錄（GitHub Pages 的發布根）
改文案的地方：本檔的 SERIES / PRODUCTS / QUIZ / FAQS 資料區、posts/ 內的選購指南文章、src/style.css、src/main.js
"""
import json, os, re, shutil, hashlib, html as H
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
# 依內容產生版本號，加在 CSS／JS 網址後面：內容一改，瀏覽器就會重新下載，不會拿到舊快取
def _ver(path):
    return hashlib.md5(open(os.path.join(ROOT,'src',path),'rb').read()).hexdigest()[:8]
CSS_VER = _ver('style.css'); JS_VER = _ver('main.js')
DIST = os.path.dirname(ROOT)  # repo 根目錄
SHOP = 'https://zh.uhealthfit.com/zh-hant-us'  # 強制美國市場（USD）；根路徑預設為 EUR 市場
SITE_URL = 'https://us.uhealthfit.com'  # 正式網域（Cloudflare Pages 自訂網域；uhealthfit-zh.pages.dev 為 Cloudflare 預設網址）
def page_url(path):
    # Cloudflare Pages 的乾淨網址：index.html → 資料夾網址（/、/blog/），其他 .html 去掉副檔名（會 308 轉址到這裡）
    if path.endswith('index.html'): path=path[:-len('index.html')]
    elif path.endswith('.html'): path=path[:-len('.html')]
    return f'{SITE_URL}/{path}'
IMG = 'https://uhealthfit.com'
LOGO = f'{IMG}/uhealthfit/uhealthfit_zh_logo.svg'  # 導覽列：優健堂（同 uhealthfit.com/zh-TW）
LOGO_WHITE = 'img/uhealthfit-logo-white.svg'  # 頁尾：UHealthFit 白色字標（同 zh.uhealthfit.com 商店頁首）
SHOP_CDN = 'https://zh.uhealthfit.com/cdn/shop'  # 官方商店（Shopify）素材：六大系列情境照、產品實拍
def shop_img(path, width=800):
    return f'{SHOP_CDN}/{path}&width={width}'
KLAVIYO_COMPANY = 'Xxa5rp'
KLAVIYO_LIST = 'TKC3Bu'
# 測驗結果頁的免費電子書（PDF 放在 repo 根目錄 downloads/；護眼結果送護眼指南，其餘送身體調養指南）
EBOOKS = {
  'eye-care': {'title':'螢幕族護眼自救指南','file':'downloads/wisequest-eye-care-guide.pdf'},
  'body-balance': {'title':'現代人身體調養指南','file':'downloads/wisequest-body-balance-guide.pdf'},
}
# Klaviyo 寄電子書的 Flow（觸發事件：Requested Quiz Ebook）上線前保持 False：測驗頁不承諾寄信，只提供下載連結。
# Flow 上線後改成 True 並重建，就會換回「寄到信箱」的說法。
EBOOK_EMAIL_FLOW_LIVE = False
TODAY = '2026-10-19'

def shop_url(handle):
    return f'{SHOP}/products/{quote(handle, safe="-")}'

# ───────────────────────────── 資料 ─────────────────────────────
SERIES = {
 'eye': dict(name='護眼保健', short='護眼', en='Eye Health', color='var(--c-eye)', organ='肝開竅於目',
   tag='外、內、日夜一次到位', h1='睡覺時，讓眼睛好好休息',
   lead='長時間盯螢幕的一天結束後，眼睛也需要自己的「下班時間」。眼貼負責睡前的外部舒緩、膠囊從內支持、眼霜負責白天——三件合稱「護眼三寶」。',
   situations=['每天盯螢幕超過 8 小時，到了下午眼睛就覺得乾澀、沒電','睡前還在滑手機，早上起來眼睛沒有休息到的感覺','葉黃素吃了一陣子，但長時間用眼後的疲勞感還在'],
   reframe=[('即時舒緩','眼藥水、熱敷眼罩負責「這一刻舒服一點」，它們很重要，但用完就結束。'),('夜間休息','睡著的六到八個小時，是眼睛最長的一段休息時間——冷敷眼貼在這段時間陪著它。'),('內在支持','中醫傳統認為「肝開竅於目」，七味東方養目草本從內支持眼睛的長期健康。')],
   products=['eye-patches','lumiview','eye-cream'], bundle='eye-care-trio',
   combo=('護眼三寶怎麼搭','睡前貼眼貼（外），每天兩次 LumiView（內），白天不方便貼眼貼時擦眼霜（日）。三個產品不是三個選擇，而是一天二十四小時的三個時段。'),
   faq=[('眼貼和蒸氣眼罩有什麼不同？','蒸氣眼罩是熱敷放鬆，十五分鐘結束；冷敷眼貼貼在眼周肌膚上，草本透過肌膚緩緩釋放，陪你度過整晚。兩者用途不同，可以依習慣選擇。'),('我已經在吃葉黃素，還需要嗎？','葉黃素補充的是視網膜相關的營養；長時間用眼後的乾澀疲勞感是另一個面向。兩者不衝突，是否同時使用建議先與醫師或藥師討論。'),('眼貼會進到眼睛裡嗎？','不會。眼貼貼在內眼角、外眼角與下眼瞼下方的肌膚上，不入眼；日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。首次使用前先做局部皮膚測試，孕婦請勿使用。')],
   photo=shop_img('collections/1_46cb0e74-a579-49cb-92db-27a44cc036be.jpg?v=1776886629',900), image=f'{IMG}/_optimized/concerns/eye-care-1200.avif', image_fallback=f'{IMG}/products/eye-patches/eye-patches-box-front.png'),
 'dental': dict(name='固齒健齦', short='固齒', en='Dental Health', color='var(--c-dental)', organ='腎主骨，齒為骨之餘',
   tag='刷牙之外的日常', h1='健康牙齦，穩固牙齒',
   lead='刷牙與牙線照顧的是看得見的表面。每天一次草本膠囊，從內在為牙齦與牙齒的日常健康多加一層支持——也是很多子女替爸媽準備的一份心意。',
   situations=['刷牙很認真，但還是想為牙齦的長期健康多做一點','爸媽年紀漸長，想替他們準備一份每天做得到的口腔保養','在「只有刷牙」與「大工程」之間，想找一個日常的中間選項'],
   reframe=[('表面清潔','牙膏、牙線、漱口水與洗牙負責看得見的表面，是每天不能少的基本功。'),('內在支持','中醫傳統認為「腎主骨，齒為骨之餘」——牙齒的穩固與整體的滋養有關，十味草本從這個角度出發。'),('長期管理','口腔健康是一輩子的事。每天隨餐一次、搭配定期牙科檢查，把保養變成習慣。')],
   products=['dentaforte'], bundle=None,
   combo=('怎麼開始','DentaForte 每天隨餐服用，不需要改變原有刷牙習慣；請持續定期牙科檢查，有任何口腔不適請先就醫。'),
   faq=[('這能取代看牙醫嗎？','不能。DentaForte 是膳食補充劑，不是藥品，也不能取代牙醫的檢查與處置。它的位置是「刷牙之外、看牙之間」的日常保養。'),('要吃多久？','建議至少給自己 4–8 週，作為長期口腔健康管理的一部分；效果因人而異。'),('替長輩購買要注意什麼？','長輩若正在服藥或有慢性健康狀況，請先與醫師或藥師確認。全植物膠囊、隨餐服用，放在早餐旁最容易記得。')],
   photo=shop_img('collections/2_d6d295f9-6329-4973-aad6-05f2a9b122ca.jpg?v=1776886620',900), image=f'{IMG}/products/dentaforte/dentaforte-product-shot-wide.png', image_fallback=f'{IMG}/products/dentaforte/dentaforte-bottle-front.png'),
 'sleep': dict(name='睡眠健康', short='睡眠', en='Sleep Health', color='var(--c-sleep)', organ='心主神明',
   tag='不含褪黑素・配方溫和、不設計為長期依賴', h1='白天放鬆，夜裡好眠',
   lead='壓力大的日子，腦子到了晚上還停不下來。這個系列的原則很簡單：先安撫白天的壓力，支持身體原本的睡眠節律——不靠外力「關機」，狀態穩定後可以停用。',
   situations=['躺下了，腦子還在跑今天的待辦事項','想找不含褪黑素的選項，怕隔天昏沉','工作壓力大，希望夜晚能真正放鬆下來'],
   reframe=[('白天的壓力','中醫傳統認為「心主神明」——夜裡難以放鬆，常常是因為白天沒有「下線」。'),('草本安神','炒酸棗仁、合歡皮、茯神等七味草本，傳統上用於幫助安神放鬆，不含褪黑素。'),('不依賴','中午飯後與睡前各一次，先幫忙放下緊繃；節律穩定後可以停用，之後依需要再開始。')],
   products=['calmoon'], bundle=None,
   combo=('怎麼開始','Calmoon 建議中午飯後與晚飯後／睡前一小時各 3 粒。搭配睡前一小時放下手機、固定起床時間，效果更容易累積。'),
   faq=[('為什麼中午也要吃？','因為這個配方照顧的是「白天的壓力」。中午那一次幫忙放下上午的緊繃，晚上那一次支持自然入睡。'),('會不會隔天昏沉？','Calmoon 不含褪黑素，配方溫和。每個人的感受不同，建議先從建議用量開始觀察。'),('可以和其他助眠產品一起用嗎？','若正在使用任何助眠產品或藥物，請先與醫師或藥師討論，不要自行疊加。')],
   photo=shop_img('collections/Bedtime-Habits-scaled.jpg?v=1785620068',900), image=f'{IMG}/products/calmoon/calmoon-product-shot-wide.png', image_fallback=f'{IMG}/products/calmoon/calmoon-bottle-front.png'),
 'digestive': dict(name='腸胃舒暢', short='腸胃', en='Digestive Health', color='var(--c-digestive)', organ='脾主運化',
   tag='不含番瀉葉', h1='順暢自然，不靠刺激',
   lead='不是不通，是通了還是脹——潤腸與行氣是兩件事。以火麻仁為核心的六味草本，溫和支持腸道的自然節律，不含番瀉葉，節律穩定後可以停用。',
   situations=['久坐一整天、外食應酬後，肚子常常頂著一股氣','想找溫和的選項，不想越吃越多','希望腸道回到自己的節奏，而不是被「催」'],
   reframe=[('潤','火麻仁、生地黃、當歸——傳統上用於潤養，讓腸道不乾澀。'),('行氣','萊菔子、厚朴——傳統上用於行氣消脹，中醫說「脾主運化」，通也要不脹。'),('養節律','每天兩次隨餐，不含番瀉葉；節律穩定後可鞏固一段時間再停用。')],
   products=['herbalflow'], bundle=None,
   combo=('怎麼開始','HerbalFlow 每天 2 次、每次 3 粒隨餐。搭配每天固定時間如廁、多喝溫水、飯後散步十分鐘，更容易養成節律。'),
   faq=[('和益生菌衝突嗎？','益生菌照顧的是菌相，HerbalFlow 的思路是潤腸與行氣，兩者角度不同。是否同時使用請先與醫師或藥師討論。'),('會不會越吃越多？','HerbalFlow 不含番瀉葉等刺激性成分，設計原則是支持節律而非刺激；節律穩定後可以停用。'),('什麼情況該去看醫師？','若有持續性的腹痛、體重明顯變化、排便型態突然改變或出血，請直接就醫，不要只依賴保健品。')],
   photo=shop_img('collections/Inside-1bloating.jpg?v=1785620047',900), image=f'{IMG}/products/herbalflow/herbalflow-product-shot-wide.png', image_fallback=f'{IMG}/products/herbalflow/herbalflow-bottle-front.png'),
 'skin': dict(name='肌膚健康', short='肌膚', en='Skin Health', color='var(--c-skin)', organ='肺主皮毛',
   tag='草本為核心・溫和到可以天天用', h1='舒緩、淨化、煥顏，一步一步來',
   lead='以東方草本為核心的肌膚保養，照顧三種常見膚況：乾燥敏感、容易出油長痘，以及看起來暗沉、疲倦。舒緩修護霜負責保濕與屏障、淨顏霜負責油脂平衡、煥顏提升精華液負責緊緻與光澤——溫和到可以天天用，美國製造。',
   situations=['換季時肌膚容易敏感、乾燥脫皮','油脂與屏障想一起照顧，不只是壓油','熬夜、壓力大，鏡子裡的自己看起來很累、暗沉'],
   reframe=[('屏障','肌膚反覆不穩定，往往是屏障沒有照顧好。保濕與屏障保養要一起做。'),('草本舒緩','蒲公英、紫草、積雪草等草本，傳統上用於舒緩；舒緩修護霜與淨顏霜皆無類固醇，溫和到可以天天用。'),('支撐與光澤','人參、當歸、白芍、茯苓、積雪草 × 胜肽、神經醯胺 NP、透明質酸——幫助肌膚看起來更緊緻、更明亮。')],
   products=['soothing-cream','clarifying-cream','lifting-serum'], bundle=None,
   combo=('怎麼選','乾燥、換季敏感、曬後、蚊蟲叮咬後 → 草本舒緩修護霜；易出油、容易長痘的膚況 → 草本淨顏霜；看起來疲倦、想要緊緻與光澤 → 草本煥顏提升精華液（潔面後先擦精華，再接霜）。'),
   faq=[('無類固醇是什麼意思？','配方中不含類固醇成分。這是一款日常保養品，不是藥品；若醫師已為你開立外用藥，請依醫囑使用，不要自行替換。'),('小孩可以用嗎？','草本舒緩修護霜設計為全家可用。嬰幼兒或有特殊膚況者，使用前請先諮詢醫師，並先在小範圍測試。'),('淨顏霜會不會太乾？','淨顏霜的思路是「調理油脂＋支持屏障」，含維生素 C 衍生物；若覺得乾，可以只用於易出油部位，其他部位搭配舒緩修護霜。'),('精華液男生可以用嗎？','可以。男女適用，35 歲以上尤其合適；質地清爽，早晚潔面後使用。')],
   photo=shop_img('collections/3_e69c85a3-7756-4f7b-8d78-f189c2138e6d.jpg?v=1776886599',900), image=f'{IMG}/products/herbal-soothing-repair-cream/soothing-repair-cream-product-shot-wide.png', image_fallback=f'{IMG}/products/herbal-soothing-repair-cream/herbal-soothing-repair-cream-jar-front.png'),
 'vitality': dict(name='元氣活力', short='元氣', en='Energy & Vitality', color='var(--c-vitality)', organ='腎主藏精',
   tag='不含咖啡因與刺激物', h1='穩定的元氣，不靠咖啡因',
   lead='每天靠咖啡撐著，下午還是沒電？這個系列的思路是日常滋養，而不是短暫提神：把傳統黑膏滋濃縮成膠囊，西洋參、黃芪、山藥等七味草本協同，支持穩定、持續的日常活力，不含咖啡因與刺激物。',
   situations=['每天靠咖啡撐著，想換一種更穩定的方式','熬夜、壓力大，總覺得元氣不足、容易累','想延續傳統膏方的滋養，又嫌膏狀不方便'],
   reframe=[('提神與滋養','咖啡因與能量飲負責「這一刻撐住」；草本滋養的思路是支持身體日常的穩定狀態，兩者角度不同。'),('穩定活力','西洋參、黃芪、山藥等七味草本協同，不靠咖啡因的短暫刺激，支持持續穩定的日常活力。'),('能持續的才算數','每天隨餐兩次，膠囊方便攜帶——溫和到可以一直吃，才是真正會留下來的保養。')],
   products=['enerbalance'], bundle=None,
   combo=('怎麼開始','EnerBalance 每天 2 次、每次 3 粒隨餐。孕婦、哺乳期、服藥中請先諮詢醫師。'),
   faq=[('EnerBalance 會像咖啡一樣讓人睡不著嗎？','EnerBalance 不含咖啡因與強刺激性成分，思路是日常滋養而非提神。每個人體質不同，建議隨餐服用並觀察。'),('黑膏滋是什麼？','黑膏滋是傳統的草本膏方；EnerBalance 把它濃縮成膠囊，更方便、更衛生、也更容易每天持續。'),('要吃多久？','建議至少給自己 4–8 週，並當作日常保養的一部分；效果因人而異。')],
   photo='https://cdn.shopify.com/s/files/1/0676/4675/0818/files/c4001f0d-6d94-4413-9958-8a31fc2e4367.jpg?v=1786711467&width=900', image=f'{IMG}/products/enerbalance/enerbalance-product-shot-wide.png', image_fallback=f'{IMG}/products/enerbalance/enerbalance-bottle-front.png'),
}
SERIES_ORDER = ['eye','skin','dental','vitality','sleep','digestive']  # 與 uhealthfit.com 導覽列順序相同

PRODUCTS = {
 'eye-patches': dict(series='eye', name='WiseQuest 明目冷敷眼貼', en='Herbal Cooling Eye Patches', badge=('badge-star','明星產品'),
   hook='清涼、放鬆，睡飽的雙眼', desc='睡前貼在眼周，草本透過肌膚緩緩釋放，讓長時間用眼後的雙眼在夜裡好好休息。不入眼、不含防腐劑，日本製造。',
   long='一天盯著螢幕十個小時之後，眼睛需要的不只是「這一刻舒服一點」，而是一段真正的休息。明目冷敷眼貼貼在內眼角、外眼角與下眼瞼下方的肌膚上，桉葉、菊花、薄荷、甘草等草本透過肌膚緩緩釋放，在你睡著的時候陪著眼睛。',
   herbs='桉葉、菊花、薄荷、甘草', actives='—（純草本配方）', made='日本製造', form='外用透皮冷敷眼貼', spec='1 盒 60 片（每晚 6 片，約 10 晚）；體驗裝 12 片（約兩晚）',
   usage='清潔眼周後，睡前貼於內眼角、外眼角與下眼瞼下方，建議每晚 6 片，約 30 分鐘或整晚；早上撕下。第一次使用可先從 2 片開始；白天可用 2–4 片做短暫放鬆。', caution='僅供外用；首次使用前先做局部皮膚測試；孕婦請勿使用；如有不適請停止使用。',
   price=29.99, price_note='1 盒 60 片 · 約 10 晚', handle='草本冷敷眼貼-十天包裝-贈試用裝一袋-價值-5',
   variants=[('兩晚體驗裝（12 片）','$6.00','先試再決定',False),('1 盒 · 60 片','$29.99','約 10 晚',False),('3 盒 · 一個月組','$84.00','推薦入門',True),('6 盒 · 兩個月組','$162.00','',False),('9 盒 · 三個月組','$234.00','單片成本最低',False)],
   trial_handle='試用裝-2日份-wise-quest-草本冷敷眼貼',
   yes=['每天盯螢幕超過 8 小時的上班族與學生','睡前習慣滑手機、想讓眼睛好好休息的人','想先用 $6 試兩晚再決定的人'], no=['孕婦','眼周肌膚有傷口或正在發炎者','對配方任一成分過敏者'],
   faq=[('會進到眼睛裡嗎？','不會。眼貼貼在眼周肌膚上，不入眼。日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。'),('白天可以用嗎？','可以。白天用 2–4 片做一次螢幕空檔的輕量護理；睡前再貼滿。白天不方便貼時，可以改用草本舒緩修護眼霜。'),('為什麼建議睡前使用？','因為這是最容易用滿完整配戴時間的時段：眼貼成為睡前放鬆的一部分，隔天早上再取下即可。白天也可以用，當作一段較短的清涼小歇。'),('剛貼上會泛淚嗎？','部分人剛貼上會泛淚，通常很快緩解，若持續不適請停用。'),('戴隱形眼鏡的人可以用嗎？','可以，請先取下隱形眼鏡再貼。通勤族、學生、長輩、整天看螢幕的人都適合，任何想為眼周留一段清涼、放鬆時光的人都可以使用。'),('可以和眼藥水一起用嗎？','可以，只要稍微錯開時間：建議點完眼藥水約 30 分鐘後再貼，讓眼藥水先吸收。正在使用醫師開立的眼藥，請先諮詢醫師。'),('會過敏嗎？','配方不含防腐劑、力求溫和，但任何草本成分都可能讓部分人的肌膚起反應。首次使用前，請先在前臂內側做 24 小時貼膚測試；肌膚容易敏感的人更應如此。'),('多久會有感覺？','多數人在使用時就能感受到清涼放鬆；整體的舒適感通常隨著幾週的持續使用慢慢累積，效果因人而異。'),('體驗裝多少錢？','兩晚體驗裝 12 片 $6，是最低門檻的開始；實際金額與運費以官方商店結帳頁為準。')],
   image=shop_img('files/XXT36515.jpg?v=1781960251'), cross=['lumiview','eye-cream','eye-care-trio']),
 'lumiview': dict(series='eye', name='LumiView 草本明目膠囊', en='Herbal Eye Support Capsules', badge=None,
   hook='由內支持眼睛的長期健康', desc='七種東方養目草本濃縮成膠囊，從營養與整體狀態支持眼睛；搭配眼貼，外內更完整。180 粒／約 1 個月。',
   long='中醫傳統認為「肝開竅於目、肝腎同源」——眼睛的狀態，與身體整體的滋養有關。LumiView 以枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪七味傳統草本，從內在支持眼睛的長期健康，是護眼三寶裡負責「內」的那一件。',
   herbs='枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪（七味）', actives='—（純草本複方）', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐服用，作為長期眼部健康管理的一部分。', caution='孕婦、哺乳期、服藥中或有健康疑慮者，使用前請諮詢醫師。',
   price=119, price_note='180 粒 · 約 1 個月', handle='wisquest-草本明目膠囊',
   variants=[('1 瓶','$119','',True),('2 瓶','$226.10','',False),('3 瓶','$303.45','單瓶成本最低',False)], trial_handle=None,
   yes=['已經在用眼貼、想「內外一起」的人','長時間用眼、想從內在支持眼睛長期健康的人','偏好全素、成分公開的草本配方'], no=['孕婦與哺乳期（請先諮詢醫師）','正在服用處方藥者（請先諮詢醫師）','對配方任一成分過敏者'],
   faq=[('膠囊和眼貼可以一起用嗎？','可以，這也是最完整的搭配。膠囊每天從內在支持，眼貼在睡前提供外部的清涼舒緩；兩者路徑不同，並不衝突。'),('一天要吃多少？','早餐後 3 粒、晚餐後 3 粒，每天共 6 粒（約 3,000 mg），一瓶 180 粒約 30 天。請隨餐服用，不要空腹。進入長期維持階段後，有些人會改為每天一次、每次 3 粒。'),('可以和眼藥水一起用嗎？','可以。膠囊隨餐服用即可，和眼藥水沒有時間上的衝突；若同時貼眼貼，建議點完眼藥水約 30 分鐘後再貼。正在使用醫師開立的眼藥，請先諮詢醫師。'),('和葉黃素可以一起吃嗎？','兩者角度不同。是否同時使用請先與醫師或藥師討論。'),('服用前需要知道什麼？','膠囊採用食品級草本成分，於美國 GMP 工廠生產，並經第三方檢測。正在服用抗凝血藥物（如華法林）、孕期或哺乳期、已知對植物過敏者，請先諮詢醫師並核對成分表；未滿 18 歲、兩週內計畫進行眼部手術者不建議使用。'),('可以取代眼鏡或隱形眼鏡嗎？','不能。LumiView 不是視力矯正工具，而是日常的護眼補充品；需要配戴眼鏡的人仍然需要配戴，也請定期做眼科檢查。'),('需要一直吃嗎？','建議至少給自己 4–8 週；狀態穩定後可以鞏固一段時間再停用，之後依需要再開始。'),('素食者可以吃嗎？','可以。全植物膠囊，全素。')],
   image=shop_img('files/ChatGPT_Image_2026_3_29_12_19_42.png?v=1776262574'), cross=['eye-patches','eye-cream','eye-care-trio']),
 'eye-cream': dict(series='eye', name='草本舒緩修護眼霜', en='Herbal Soothing & Repair Eye Cream', badge=('badge-new','新品'),
   hook='看不見的眼貼，白天的眼周呵護', desc='3C 與花粉季節、不方便貼眼貼的時候，隨身為脆弱的眼周肌膚保濕與舒緩。無酒精、無人工香精、無合成色素。',
   long='白天在辦公室不方便貼眼貼，但眼周肌膚一樣需要照顧。這款眼霜以石斛、菊花、決明子、茯苓、當歸根與尤加利葉精油，為脆弱的眼周肌膚做日間的保濕與舒緩，是護眼三寶裡負責「日」的那一件。我們把它定位為護眼，而不是抗老。',
   herbs='石斛、菊花、決明子、茯苓、當歸根、尤加利葉精油', actives='無苯氧乙醇、無化學防腐劑、無人工香精、無合成色素、無酒精', made='原料研發日本・生產灌裝美國', form='外用眼霜', spec='20g / 0.7 oz',
   usage='早晚或白天用眼空檔，取米粒大小輕點眼周，由內向外輕輕按壓至吸收。', caution='僅供外用；避免直接接觸眼睛；開封後建議 6 個月內用完。',
   price=59, price_note='20g / 0.7 oz', handle='wisequest-草本舒緩修護眼霜', variants=None, trial_handle=None,
   yes=['白天長時間用眼、想隨身照顧眼周的人','花粉季節眼周容易乾燥不適的人','搭配眼貼，想把日夜都顧到的人'], no=['眼周肌膚有傷口者','對精油類成分敏感者（先局部測試）'],
   faq=[('什麼時候擦？擦多少？','每晚入睡前擦在潔淨的肌膚上，白天用眼空檔也可以補擦。每隻眼取米粒大小，沿眼眶骨輕柔點拍，避開眼瞼與睫毛根部。'),('可以取代眼貼嗎？','它是白天的接力，不是取代。晚上有時間時仍建議使用眼貼。'),('會不會長脂肪粒？','質地設計為清爽型，每次用量米粒大小即可。若有疑慮請先小範圍測試。'),('男生可以用嗎？','可以，男女適用。'),('敏感肌可以用嗎？','可以，適合所有膚質，包括敏感肌；配方不含苯氧乙醇、化學防腐劑、人工香精、合成色素與酒精。首次使用仍建議先做局部測試。'),('擦了會刺眼嗎？','配方中的桉葉帶來清涼觸感。請只擦在眼周肌膚、避免直接接觸眼睛；若不慎入眼，請以清水沖洗。'),('一罐可以用多久？','20g，每次只需米粒大小；開封後建議 6 個月內用完。'),('在哪裡製造？','原料研發來自日本，在美國灌裝生產。')],
   image=shop_img('files/Untitled_design_3924dd0b-b2a7-4689-9fe5-931caa8ffc9a.jpg?v=1781959479'), cross=['eye-patches','lumiview','eye-care-trio']),
 'eye-care-trio': dict(series='eye', name='護眼三寶（眼貼＋LumiView＋眼霜）', en='Eye Care Trio', badge=('badge-star','招牌組合'), is_bundle=True,
   hook='外、內、日夜，一次到位', desc='睡前眼貼從外舒緩、白天眼霜接力、LumiView 從內支持——三個產品不是三個選擇，而是一天二十四小時的三個時段。',
   long='很多顧客從 $6 的眼貼體驗裝開始，用了一陣子之後問我們：「還能多做什麼？」護眼三寶就是答案——不是「買三樣更划算」的折扣語言，而是一套方案的三個部分：夜裡（眼貼）、白天（眼霜）、內在（膠囊）。',
   herbs='眼貼：桉葉、菊花、薄荷、甘草｜LumiView：枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪｜眼霜：石斛、菊花、決明子、茯苓、當歸根', actives='詳見各單品頁', made='眼貼日本製造；膠囊與眼霜美國製造', form='外用眼貼＋全植物膠囊＋外用眼霜', spec='依組合頁選擇 1／2／3 個月方案',
   usage='睡前貼眼貼；每天 2 次各 3 粒 LumiView 隨餐；白天用眼空檔擦眼霜。', caution='孕婦請勿使用眼貼；服藥中請先諮詢醫師再使用膠囊。',
   price=None, price_note='組合價以 zh.uhealthfit.com 護眼三寶頁為準', handle=None, page_url=f'{SHOP}/pages/%E8%AD%B7%E7%9C%BC%E4%B8%89%E5%AF%B6', variants=None, trial_handle='試用裝-2日份-wise-quest-草本冷敷眼貼',
   yes=['已經用過眼貼、想把護眼做完整的人','每天螢幕 10 小時以上、想一次把日夜都顧到的人','重視成分公開與長期習慣的人'], no=['還沒試過眼貼的人——建議先從 $6 體驗裝開始','孕婦與哺乳期（請先諮詢醫師）'],
   faq=[('一定要三樣一起用嗎？','不一定。可以從眼貼開始，再依需要加入膠囊或眼霜；三寶是為了想一次到位的人準備的。'),('膠囊和眼貼會衝突嗎？','不會。膠囊每天從內在支持，眼貼在睡前提供外部的清涼舒緩，眼霜則照顧白天；三者路徑不同，可以一起使用。'),('可以和眼藥水一起用嗎？','可以，只要稍微錯開時間：膠囊隨餐服用即可；眼貼建議在點完眼藥水約 30 分鐘後再貼。正在使用醫師開立的眼藥，請先諮詢醫師。'),('三個月方案適合誰？','已經用過一個月、確定適合自己習慣的人。單次購買，沒有訂閱。'),('有免運嗎？','美國地區眼貼訂單滿 $79、其他商品滿 $200 免運；組合訂單依結帳頁顯示為準。')],
   image=f'{IMG}/_optimized/concerns/eye-care-1200.avif', cross=['eye-patches','lumiview','eye-cream']),
 'dentaforte': dict(series='dental', name='DentaForte 草本固齒膠囊', en='Herbal Formula for Teeth & Gum Health', badge=None,
   hook='照顧牙刷到不了的地方', desc='十味傳統草本複方，搭配認真刷牙與定期牙科檢查，作為長期口腔健康管理的一部分。隨餐服用，不必改變原有習慣。',
   long='刷牙、牙線、洗牙負責看得見的表面——這些是每天不能少的基本功。DentaForte 從另一個角度出發：中醫傳統認為「腎主骨，齒為骨之餘」，十味草本從內在支持牙齦與牙齒的日常健康。它不是取代牙醫的東西，而是「刷牙之外、看牙之間」每天做得到的保養。',
   herbs='熟地黃、生地黃、山藥、丹參、五味子、野菊花、黃芪、茯苓、枸杞、菟絲子（十味）', actives='—（純草本複方）', made='美國 cGMP 製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐服用；搭配認真刷牙、牙線與定期牙科檢查。', caution='孕婦、哺乳期、服藥中或有慢性健康狀況者，使用前請諮詢醫師。有口腔不適請先就醫。',
   price=269, price_note='180 粒 · 約 1 個月', handle='wisequest-草本固齿胶囊',
   variants=[('1 瓶','$269','',True),('2 瓶','$511.10','',False),('3 瓶','$686','單瓶成本最低',False)], trial_handle=None,
   yes=['35–55 歲、想為牙齦長期健康多做一點的人','替父母準備日常口腔保養的子女','重視成分公開、美國製造的人'], no=['正在接受牙科治療者（請先詢問牙醫）','孕婦、哺乳期（請先諮詢醫師）','對配方任一成分過敏者'],
   faq=[('可以取代看牙醫嗎？','不能。這是膳食補充劑，不是藥品；請持續定期牙科檢查。'),('要吃多久？','建議至少 4–8 週，作為長期管理的一部分；效果因人而異。'),('長輩吃方便嗎？','全植物膠囊、隨餐服用，放在早餐旁邊最容易記得，不需要家人在旁盯著。')],
   image=f'{IMG}/_optimized/products/dentaforte/dentaforte-product-shot-wide-1200.avif', cross=['herbalflow','calmoon','lumiview']),
 'calmoon': dict(series='sleep', name='Calmoon 安睡草本膠囊', en='Herbal Sleep Support Capsules', badge=None,
   hook='白天放鬆，夜裡好眠', desc='不含褪黑素的草本安神配方。午後與睡前各一次，先幫忙放下白天的緊繃，支持自然的睡眠節律。狀態穩定後可停用。',
   long='夜裡難以放鬆，常常不是夜晚的問題，而是白天沒有「下線」。中醫傳統認為「心主神明」——Calmoon 以炒酸棗仁、合歡皮、茯神、百合、刺五加、丹參、夏枯草七味草本，先安撫白天的壓力，支持身體進入夜間的恢復狀態。不含褪黑素，狀態穩定後可以停用。',
   herbs='炒酸棗仁、合歡皮、茯神、百合、刺五加、丹參、夏枯草（七味）', actives='不含褪黑素；配方溫和、狀態穩定後可停用', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒：中午飯後一次、晚飯後或睡前一小時一次。', caution='孕婦、哺乳期、服藥中（尤其是鎮靜或助眠類藥物）者，使用前請諮詢醫師。',
   price=139, price_note='180 粒 · 約 1 個月', handle='wisequest-草本助眠膠囊', variants=None, trial_handle=None,
   yes=['壓力大、晚上腦子停不下來的上班族','想避開褪黑素、怕隔天昏沉的人','希望狀態穩定後可以停用、不想長期依賴的人'], no=['正在服用鎮靜或助眠類藥物者（請先諮詢醫師）','孕婦、哺乳期','對配方任一成分過敏者'],
   faq=[('一天要吃多少？','每天 2 次、每次 3 粒，每日共 6 粒（約 3,000 mg）：午餐隨餐一次、晚餐或睡前約一小時一次。建議規律使用，並給自己 4–8 週觀察；效果因人而異。'),('為什麼中午也要吃？','這個配方照顧的是白天的壓力。中午那一次幫忙放下上午的緊繃，晚上那一次支持自然入睡。'),('不含褪黑素，那它靠什麼？','靠傳統上用於安神放鬆的草本複方，思路是支持身體原本的節律，而不是外力「關機」。'),('多久會有感覺？','多數人在前幾週先感受到放鬆感，節律的穩定通常需要 4–8 週；效果因人而異。'),('早上醒來會昏沉嗎？','配方的目標是醒來清爽，而不是昏昏沉沉；不含褪黑素等激素。每個人體質不同，剛開始請先觀察自己的感受；服用後請勿駕駛或操作機械。'),('會不會越吃越依賴？','Calmoon 不含激素，思路是溫和的日常草本支持，而不是強行催眠；狀態穩定後可以停用，之後依需要再開始。'),('為什麼是七味複方？','中醫傳統講「君臣佐使」：炒酸棗仁、茯神、百合傳統上用於安神；合歡皮、夏枯草用於舒緩情緒；刺五加用於幫助身體因應日常壓力；丹參與刺五加則照顧白天的精神與專注。從睡眠、情緒、壓力幾個層次一起照顧。'),('正在服用其他藥物可以吃嗎？','正在服用抗凝血藥物（如華法林）、鎮靜或助眠類藥物、其他藥物，或有健康狀況者，使用前請先諮詢醫師。孕婦及哺乳期女性請勿使用。')],
   image=shop_img('files/ChatGPTImage2026_6_17_05_36_03.jpg?v=1782815977'), cross=['herbalflow','enerbalance','eye-patches']),
 'herbalflow': dict(series='digestive', name='HerbalFlow 草本潤暢膠囊', en='Herbal Digestive Flow Capsules', badge=None,
   hook='順暢自然，不靠刺激', desc='不含番瀉葉。以火麻仁為核心的六味草本複方，兼顧「潤」與「行氣」，溫和支持腸道的自然節律與餐後的輕盈感。',
   long='不是不通，是通了還是脹——潤腸與行氣是兩件事。HerbalFlow 以火麻仁、萊菔子、厚朴、生地黃、當歸、馬齒莧六味草本，一邊潤養、一邊行氣，中醫傳統說「脾主運化」。不含番瀉葉，設計原則是陪腸道找回節奏，而不是逼它；節律穩定後可以停用。',
   herbs='火麻仁、萊菔子、厚朴、生地黃、當歸、馬齒莧（六味）', actives='不含番瀉葉', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐或飯後服用；節律穩定後可鞏固一段時間再停用。', caution='孕婦、哺乳期、服藥中或有腸胃相關健康狀況者，使用前請諮詢醫師；有持續腹痛或出血請直接就醫。',
   price=139, price_note='180 粒 · 約 1 個月', handle='wisequest-草本通氣膠囊', variants=None, trial_handle=None,
   yes=['久坐、外食應酬多的上班族','想找不含番瀉葉、溫和選項的人','希望節律穩定後可以停用的人'], no=['孕婦、哺乳期','有持續腹痛、出血等情況者（請先就醫）','對配方任一成分過敏者'],
   faq=[('會不會越吃越多？','HerbalFlow 不含番瀉葉等刺激性成分，設計原則是支持節律；節律穩定後可以停用。'),('和益生菌衝突嗎？','角度不同。是否同時使用請先與醫師或藥師討論。'),('多久會有感覺？','多數人在前幾週先感受到餐後的輕盈感，節律的穩定通常需要 4–8 週；效果因人而異。')],
   image=shop_img('files/26ffef70cacb47ecb0b0b1e2fc667031_3eb53544-8644-47c2-85e1-519efa90b88c.jpg?v=1782815981'), cross=['calmoon','dentaforte','enerbalance']),
 'soothing-cream': dict(series='skin', name='草本舒緩修護霜', en='Herbal Soothing & Repair Cream', badge=('badge-star','家庭必備'),
   hook='家庭必備的無類固醇修護霜', desc='七種草本＋透明質酸、維生素 E，為乾燥脫皮、換季敏感、曬後與蚊蟲叮咬後的肌膚舒緩保濕、強韌屏障。全身可用，早晚各一次。',
   long='一罐放在家裡、全家都用得到的霜：乾燥脫皮時、換季肌膚敏感時、曬後、蚊蟲叮咬後。蒲公英、紫草、白芷、積雪草、苦參、尤加利、薄荷七種草本，加上透明質酸、維生素 E 與維生素 C 衍生物，做的是舒緩、保濕與屏障保養——無類固醇，溫和到可以天天用。',
   herbs='蒲公英、紫草、白芷、積雪草、苦參、尤加利、薄荷（七種）', actives='透明質酸、維生素 E、維生素 C 衍生物；無類固醇', made='美國製造', form='外用霜', spec='全身可用',
   usage='每天 2 次，取適量塗抹於需要保養的部位；首次使用先在小範圍局部測試。', caution='僅供外用；避開眼睛與傷口；若醫師已開立外用藥，請依醫囑使用，不要自行替換。',
   price=69, price_note='外用霜 · 全家可用', handle='wisequest-草本舒緩修護霜', variants=None, trial_handle=None,
   yes=['換季時肌膚容易敏感、乾燥脫皮的人','想找一罐全家可用的無類固醇舒緩霜','曬後、蚊蟲叮咬後需要舒緩保濕的人'], no=['對配方任一成分（含精油類）過敏者','有開放性傷口的部位'],
   faq=[('什麼時候用？用多少？','早晚各一次，在潔面、化妝水或精華液之後使用；取約豌豆大小，輕柔按壓於需要的部位。夜晚可以塗稍厚一層，早上醒來肌膚感覺更平靜、舒適。'),('小孩可以用嗎？','設計為全家可用；嬰幼兒或特殊膚況者請先諮詢醫師並先小範圍測試。'),('可以擦臉嗎？','可以，全身可用；臉部建議先局部測試。'),('和淨顏霜怎麼分？','乾燥、敏感、曬後 → 舒緩修護霜；易出油、容易長痘 → 淨顏霜。可依部位分開使用。'),('可以當妝前保養嗎？','可以。早晨潔面後使用，尤加利與薄荷帶來清涼觸感，吸收後可以接著上底妝。'),('除了臉，身體哪裡可以用？','手肘、膝蓋、乾燥的雙手，任何覺得乾燥、緊繃的部位都可以；換季、曬後或戶外活動後，也可以用來帶來清涼與舒適。'),('一罐可以用多久？','30g 一罐，早晚使用約 60 天。'),('第一次使用要注意什麼？','先在前臂內側做 24 小時皮膚測試；僅供外用，避開眼睛與傷口。這是日常保養品，不是藥品；若醫師已開立外用藥，請依醫囑使用。')],
   image=shop_img('files/PicCopilot_image2.jpg?v=1776249690'), cross=['clarifying-cream','eye-cream','lifting-serum']),
 'clarifying-cream': dict(series='skin', name='草本淨顏霜', en='Herbal Clarifying Cream', badge=None,
   hook='為易長痘肌膚精選的草本', desc='溫和調理油脂、支持肌膚屏障，讓膚況看起來更勻淨、更安定。搭配清淡飲食與規律作息，一起把肌膚帶回平衡。',
   long='容易出油、容易長痘的膚況，往往一邊壓油、一邊屏障又變得脆弱。草本淨顏霜以蒲公英、金銀花、丹參、黨參、紫草根油，搭配維生素 C 衍生物與視黃醇棕櫚酸酯，一邊調理油脂、一邊支持屏障，讓膚況看起來更勻淨、更安定。',
   herbs='蒲公英、金銀花、丹參、黨參、紫草根油', actives='維生素 C 衍生物、視黃醇棕櫚酸酯', made='美國製造', form='外用霜', spec='臉部日常保養',
   usage='潔面後取適量塗抹於易出油部位，早晚各一次；搭配清淡飲食、忌辛辣油膩。', caution='僅供外用；首次使用先局部測試；若同時使用高濃度 A 醇類產品請留意耐受；大面積或疼痛硬塊請就醫。',
   price=69, price_note='外用霜', handle='wisequest-草本淨顏霜', variants=None, trial_handle=None,
   yes=['容易出油、容易長痘的膚況','想一起照顧油脂與屏障的人','偏好草本、溫和日常保養的人'], no=['對配方任一成分過敏者','大面積或反覆疼痛硬塊者（請先看皮膚科醫師）'],
   faq=[('適合什麼樣的肌膚？','油性、容易泛油光：幫助平衡表面油脂的外觀，同時照顧肌膚屏障。混合性：T 字部位油亮、兩頰卻緊繃的人，可以只擦在易出油的部位。容易泛紅、敏感：以草本為主、質地溫和，首次使用請先做局部測試。'),('什麼時候用？用多少？','早晚各一次，在潔面、化妝水或精華液之後使用；取約豌豆大小，均勻塗抹全臉（避開眼周），或只擦在易出油的部位。'),('擦了會不會覺得乾、緊繃？','草本淨顏複方的思路是平衡表面油脂的外觀，同時以植物來源的保濕成分支持屏障，不追求強力潔淨的緊繃感。若覺得乾，可以只擦在易出油部位，其他部位搭配舒緩修護霜。'),('多久能看到變化？','膚況的安定需要時間，建議至少 4–8 週並搭配作息與飲食；效果因人而異。'),('可以全臉用嗎？','可以，也可以只用於易出油部位，其他部位搭配舒緩修護霜。'),('白天用需要防曬嗎？','建議白天搭配防曬，這是所有臉部保養的基本。'),('一罐可以用多久？','30g 一罐，早晚使用約 60 天。'),('第一次使用要注意什麼？','先在前臂內側做 24 小時皮膚測試；僅供外用。若同時使用高濃度 A 醇或酸類產品，建議錯開使用，並留意肌膚的耐受。')],
   image=shop_img('files/Untitled_design_c0b7bac5-b45b-48f9-bb62-96d6d17052a5.jpg?v=1781960121'), cross=['soothing-cream','lifting-serum','eye-cream']),
 'lifting-serum': dict(series='skin', name='草本煥顏提升精華液', en='Herbal Lifting & Revitalizing Serum', badge=('badge-star','精選'),
   hook='更緊緻、更有光澤的肌膚', desc='五種東方草本 × 胜肽、神經醯胺 NP、透明質酸，日復一日幫助肌膚看起來更緊緻、更明亮。男女適用，35 歲以上尤其合適。',
   long='你要的不是變年輕，是不要看起來很累。人參、當歸、白芍、茯苓、積雪草五種東方草本，加上胜肽、神經醯胺 NP 與透明質酸，從支撐、屏障、保濕多個面向，幫助肌膚看起來更緊緻、更有光澤——溫和到可以一直用，能持續的才是會留下來的保養。',
   herbs='人參、當歸、白芍、茯苓、積雪草（五種）', actives='胜肽、神經醯胺 NP、透明質酸', made='美國製造', form='外用精華液', spec='早晚使用',
   usage='潔面後、面霜之前取 3–4 滴，輕柔按壓於臉部與頸部至吸收，早晚各一次。', caution='僅供外用；首次使用先局部測試；白天建議搭配防曬。',
   price=189, price_note='精華液', handle='wisequest-草本煥顏提升精華液', variants=None, trial_handle=None,
   yes=['35 歲以上、熬夜壓力大、不想看起來很累的人','想找溫和、能長期持續的初老保養','男女皆適用'], no=['對配方任一成分過敏者','肌膚有傷口或正在發炎的部位'],
   faq=[('怎麼用？用量多少？','早晚潔面後、面霜之前使用；取 3–4 滴，輕柔按壓於臉部與頸部至吸收。首次使用請先在前臂內側做 24 小時皮膚測試。'),('適合什麼樣的肌膚狀態？','開始注意到眼周、嘴角或額頭的細紋，熬夜、忙碌後膚色看起來暗沉疲憊，或覺得肌膚不如以前緊緻、上妝不太服貼的人。敏感肌也可以使用，首次請先做局部測試。'),('和 A 醇類精華比呢？','各有定位。這款走東方草本 × 胜肽的溫和路線，適合想長期持續使用的人。'),('多久有感？','光澤感通常先出現，緊緻感需要更長時間累積；效果因人而異。'),('可以和眼霜一起用嗎？','可以。眼周建議用草本舒緩修護眼霜，全臉用精華液。'),('配方的重點成分是什麼？','我們不追求二十種成分的微量堆砌，重點放在四組主要成分：人參讓膚色看起來更有活力、積雪草舒緩、胜肽複合物幫助肌膚看起來更緊緻、神經醯胺 NP ＋透明質酸鎖住水分；再搭配當歸、白芍、茯苓等東方草本。'),('一瓶可以用多久？','30ml 一瓶，早晚使用約 60 天。'),('懷孕或哺乳期可以用嗎？','懷孕或哺乳期間，使用前請先諮詢醫師。')],
   image=shop_img('files/1_9cefe0d6-9848-412c-98c1-462e0c23660b.png?v=1782816030'), cross=['eye-cream','soothing-cream','enerbalance']),
 'enerbalance': dict(series='vitality', name='EnerBalance 黑膏滋膠囊', en='Herbal Vitality Capsules', badge=('badge-new','現貨'), compare=299,
   hook='不靠咖啡因，日日滋養', desc='傳統黑膏滋濃縮成膠囊。七味草本協同配方，支持穩定、持續的日常活力；不含咖啡因與強刺激性成分，無麩質、無添加糖。',
   long='咖啡因給的是短暫的提神，而且常常要付出隔天的代價。EnerBalance 把傳統黑膏滋濃縮成膠囊：西洋參、黃芪、山藥、當歸、陳皮、菊花、玉米鬚七味草本協同，中醫傳統認為可用於日常調養，支持穩定、持續的活力。不含咖啡因，無麩質、無添加糖。',
   herbs='西洋參、黃芪、山藥、當歸、陳皮、菊花、玉米鬚（七味）', actives='不含咖啡因與強刺激性成分；無麩質、無添加糖', made='美國製造', form='全植物膠囊', spec='180 粒／瓶 ≈ 1 個月',
   usage='成人每天 2 次、每次 3 粒，建議隨餐服用。', caution='孕婦、哺乳期、服藥中或有慢性健康狀況者，使用前請諮詢醫師。',
   price=179, price_note='180 粒 · 約 1 個月 · 原價 $299', handle='wisequest-黑膏滋膠囊', variants=None, trial_handle=None,
   yes=['工作壓力大、常覺得精力不足的成年人','想減少對咖啡因依賴的人','重視天然草本日常調養的人'], no=['孕婦、哺乳期','正在服用處方藥者（請先諮詢醫師）','18 歲以下'],
   faq=[('會像咖啡一樣讓人睡不著嗎？','不含咖啡因與強刺激性成分，思路是日常滋養而非提神；建議隨餐服用並觀察。'),('黑膏滋是什麼？','傳統的草本膏方，EnerBalance 把它濃縮成膠囊，更方便、更衛生。'),('和傳統黑膏滋有什麼不同？','膏滋是把草本反覆煎煮、去渣濃縮成膏的傳統工藝，開罐後要長期存放、反覆挖取。EnerBalance 保留同樣的七味配方，濃縮進獨立膠囊：每份劑量標準化、常溫保存、方便攜帶，也不用冰糖或蜂蜜收膏。'),('一天要吃多少？','成人每天 2 次、每次 3 粒，每日共 6 粒（約 3,000 mg），建議隨餐服用；一瓶 180 粒共 60 份，約 30 天。'),('現在的價格是多少？','商店目前以 $179 供應（原價 $299），實際金額以 zh.uhealthfit.com 結帳頁顯示為準。'),('適合哪些人？','經常熬夜、工作節奏緊湊的上班族，運動後想多一份日常滋養的人，希望日常溫補的中老年人，以及想減少咖啡因、改用草本支持活力的人。'),('體質偏寒或腸胃比較弱，適合嗎？','中醫傳統認為西洋參性偏涼，單用不一定適合每種體質；EnerBalance 以西洋參搭配性溫的黃芪，再加入山藥、陳皮等健脾草本平衡，設計為較多人都能日常食用的複方。仍不確定時，請先諮詢醫師或中醫師。'),('哪些人不適合？','孕婦及哺乳期女性請勿使用；18 歲以下、正在服用抗凝血藥物（如華法林）或其他藥物、有健康狀況或正在接受醫療照護者，使用前請先諮詢醫師。瓶口封膜破損請勿使用。')],
   image=f'{IMG}/_optimized/products/enerbalance/enerbalance-product-shot-wide-1200.avif', cross=['calmoon','herbalflow','lifting-serum']),
}
PRODUCT_ORDER = ['eye-patches','lumiview','eye-cream','eye-care-trio','dentaforte','calmoon','herbalflow','soothing-cream','clarifying-cream','lifting-serum','enerbalance']

# 部落格
POSTS = []
for fn in sorted(os.listdir(os.path.join(ROOT,'posts'))):
    s = open(os.path.join(ROOT,'posts',fn),encoding='utf8').read()
    meta, body = s.split('---END-META---',1)
    m = json.loads(meta.strip()); m['body'] = body.strip(); POSTS.append(m)
POST_BY_SLUG = {p['slug']:p for p in POSTS}
POST_ORDER = ['eye-patch-vs-steam-mask-vs-eye-drops','beyond-lutein-eye-care','eye-patch-how-to-use-guide','eye-care-gift-for-parents','eye-patch-ingredients-explained','melatonin-free-sleep-aid-guide','stress-daytime-relax-night-sleep','gentle-digestive-support-no-senna','bloating-after-sitting-herbal-flow','gum-care-supplement-for-parents','brushing-plus-herbal-support','steroid-free-soothing-cream-guide','acne-prone-skin-herbal-cream-guide','anti-fatigue-look-serum-guide','caffeine-free-energy-herbal-guide','winter-tonic-herbal-guide','gaozi-paste-vs-capsule','american-ginseng-vs-ginseng']
POSTS = [POST_BY_SLUG[s] for s in POST_ORDER]

# ───────────────────────────── 共用片段 ─────────────────────────────
def esc(s): return H.escape(s, quote=True)

def buy_url(p, slug):
    if p.get('page_url'): return p['page_url']
    return shop_url(p['handle'])

def price_str(p, with_compare=False):
    if p['price'] is None: return '組合價'
    v = p['price']; base = f'${v:,.2f}' if v != int(v) else f'${int(v)}'
    if with_compare and p.get('compare'):
        c = p['compare']; cs = f'${c:,.2f}' if c != int(c) else f'${int(c)}'
        return f'{base} <s style="color:var(--ink-3);font-weight:600;font-size:.7em;margin-left:6px">{cs}</s>'
    return base


# ───── 產品頁「主題花體字」橫幅：取自 uhealthfit.com/zh-TW 首頁輪播（花體字 SVG、簡介、底色）─────
SLIDES = {
 'eye-patches':      dict(svg='eye-patches',         bg='#D9E2EE', headline='清涼 放鬆／睡飽的雙眼',        intro='日本製冷敷眼貼——休息時貼上，給盯了一整天螢幕的雙眼一份草本呵護。', shot='eye-patches/eye-patches-box-front', avif=False),  # 此圖的 avif 版本沒有透明背景，只用 PNG
 'lumiview':         dict(svg='herbalflow-capsules', bg='#D6DEC7', headline='草本濃縮進膠囊／搭配眼貼更完整', intro='七味東方養目草本濃縮成膠囊，從內在支持眼睛的長期健康；搭配眼貼，外內更完整。', shot='lumiview/lumiview-product-shot-wide'),
 'eye-cream':        dict(svg='eye-patches-3c',      bg='#F8F2E8', headline='看不見的眼貼／3C 花粉 全呵護',   intro='為脆弱眼周設計的植萃眼霜——不便使用眼貼時的隨身養護。', shot='herbal-soothing-repair-eye-cream/eye-cream-product-shot-wide'),
 'dentaforte':       dict(svg='dentaforte',          bg='#F2DCB4', headline='健康牙齦／穩固牙齒',            intro='每日草本膠囊，由內支持牙齦與牙齒——照顧牙刷到不了的深處。', shot='dentaforte/dentaforte-product-shot-wide'),
 'calmoon':          dict(svg='calmoon',             bg='#C8D9F3', headline='白天放鬆／夜裡好眠',            intro='草本安神配方——睡前慢慢放鬆，自然入睡。', shot='calmoon/calmoon-product-shot-wide'),
 'herbalflow':       dict(svg='herbalflow',          bg='#E4EBDD', headline='通腹順暢自然／不靠刺激',        intro='以火麻仁為核心的草本複方，溫和支持腸道自然節律。', shot='herbalflow/herbalflow-product-shot-wide'),
 'soothing-cream':   dict(svg='calming',             bg='#F2DDC6', headline='鎮靜 舒適／更柔軟的肌膚',        intro='不含刺激性活性成分的植萃修護，為乾燥與壓力肌帶來每日的溫和呵護。', shot='herbal-soothing-repair-cream/soothing-repair-cream-product-shot-wide'),
 'clarifying-cream': dict(svg='clarifying-cream',    bg='#F6E9D9', headline='為易長痘肌膚／精選的草本',      intro='溫和淨顏的植萃面霜，讓膚色看起來更勻淨、更安定。', shot='herbal-clarifying-cream/clarifying-cream-product-shot-wide'),
 'lifting-serum':    dict(svg='lifting-serum',       bg='#D3CFAD', headline='更緊緻 更亮澤／更年輕的肌膚',    intro='高濃度植萃精華，日復一日，見證肌膚的提升與煥亮。', shot='herbal-lifting-revitalizing-serum/lifting-serum-product-shot-wide'),
 'enerbalance':      dict(svg='enerbalance',         bg='#ECE4D4', headline='咖啡因短暫提神／不如日日滋養',    intro='真正持久的活力，來自身體整體協調。戒掉咖啡因，不用再靠刺激。', shot='enerbalance/enerbalance-bottle-open-capsules', avif=False),
}
def series_hero(k, rel):
    """系列頁頁首輪播：同 uhealthfit.com/zh-TW 首頁 slides——滿版、左文右圖、自動切換。
    第一張是系列介紹（含 h1），後面每個產品一張（花體字標題）。"""
    s=SERIES[k]; guide=[p for p in POSTS if p['series']==k][0]['slug']
    slides=[f'''<article class="slide slide-intro" aria-label="{esc(s['name'])}">
    <div class="wrap slide-inner">
      <div class="slide-text"><div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><a href="{rel}series/index.html">六大系列</a><span>›</span><span>{s['name']}</span></div>
        <span class="series-tag s-{k}"><span class="dot"></span>{s['name']} · {esc(s['tag'])}</span>
        <h1>{esc(s['h1'])}</h1><p class="lead">{esc(s['lead'])}</p>
        <div class="hero-cta"><a class="btn btn-primary" href="#products">看這個系列的產品</a><a class="btn btn-ghost" href="{rel}blog/{guide}.html">先讀選購指南</a></div>
        <ul class="hero-trust"><li>{esc(s['organ'])}（中醫傳統觀點）</li><li>成分全部公開</li><li>效果因人而異，誠實交代時間</li></ul></div>
      <div class="slide-photo"><img src="{s['photo']}" alt="{esc(s['name'])}" width="900" height="900" fetchpriority="high"></div>
    </div>
  </article>''']
    for slug in s['products']:
        sl=SLIDES.get(slug); p=PRODUCTS[slug]
        if not sl: continue
        avif='' if sl.get('avif') is False else f'<source srcset="{IMG}/_optimized/products/{sl["shot"]}-1200.avif" type="image/avif">'
        slides.append(f'''<article class="slide" style="--slide-bg:{sl['bg']}" aria-label="{esc(p['name'])}">
    <div class="wrap slide-inner">
      <div class="slide-text">
        <div class="slide-name">WISEQUEST {esc(p['name'].replace('WiseQuest ',''))}</div>
        <img class="slide-title" src="{IMG}/home/hero-title-{sl['svg']}-zh-hant.svg" alt="{esc(sl['headline'])}" loading="lazy">
        <p class="slide-intro-text">{esc(sl['intro'])}</p>
        <p class="slide-herbs">主要成分：{esc(p['herbs'])}</p>
        <div class="hero-cta"><a class="btn btn-primary ext" data-product="{slug}" href="{buy_url(p,slug)}">立即選購</a><a class="btn btn-ghost" href="{rel}products/{slug}.html">了解產品</a></div>
      </div>
      <div class="slide-pic"><picture>{avif}<img src="{IMG}/products/{sl['shot']}.png" alt="{esc(p['name'])}" loading="lazy"></picture></div>
    </div>
  </article>''')
    cur_attr=' aria-current="true"'
    dots=''.join(f'<button type="button" aria-label="前往第 {i+1} 張"{cur_attr if i==0 else ""}></button>' for i in range(len(slides)))
    return f'''<section class="slides" aria-roledescription="carousel" aria-label="{esc(s['name'])}">
  <div class="slides-track">{''.join(slides)}</div>
  <button type="button" class="slides-prev" aria-label="上一張">‹</button><button type="button" class="slides-next" aria-label="下一張">›</button>
  <div class="slides-dots">{dots}</div>
</section>
'''


# ───── 買家評價與示範影片：依《見證與 KOL 影片合規盤點》（2026-10-21）只收 A 類「可用、原文照登」 ─────
# 規則：原文照登（簡體字不改繁體）；負評必須一併公開（FTC 16 CFR 465）；不收 B 類（待補真人證明／本人同意）與 C 類（下架）；
#       不收品牌或代理商人員撰寫的評價（B9 待確認，暫不收）。資料擷取自兩個官方商店的 Judge.me 評價，2026-10-22。
UH_EYE_PATCHES = 'https://uhealthfit.com/zh-TW/products/wisequest-eye-patches'
UH_EYE_CREAM = 'https://uhealthfit.com/zh-TW/products/wisequest-herbal-soothing-repair-eye-cream'
REVIEWS = {
 'eye-patches': [
  dict(author='nancy', verified=True, date='2026-10-09', rating=4, text='眼貼感覺很好，只是運輸時間太長了', item='明目冷敷眼貼', src='uhealthfit.com', url=UH_EYE_PATCHES),
  dict(author='Yin Z.', verified=True, date='2026-10-05', rating=5, text='很好的產品，用在穴位上即可', item='明目冷敷眼貼', src='uhealthfit.com', url=UH_EYE_PATCHES),
  dict(author='Ming Yao', verified=True, date='2026-02-17', rating=5, text='体验很好，清凉润眼，有rosemary的感觉。', item='明目冷敷眼貼', src='zh.uhealthfit.com', url='SHOP:eye-patches'),
  dict(author='QING Liang', verified=True, date='2026-02-16', rating=5, text='感覺很好', item='兩晚體驗裝', src='zh.uhealthfit.com', url='SHOP_TRIAL:eye-patches'),
  dict(author='刘宏庆 刘', verified=True, date='2026-02-05', rating=1, text='还好效不明显', item='明目冷敷眼貼', src='zh.uhealthfit.com', url='SHOP:eye-patches'),
  dict(author='心敏 羅', verified=True, date='2026-02-01', rating=1, text='不知是否有任何問題，拆開信封袋內空無一物，並沒有任何東西可以試用的。', item='兩晚體驗裝', src='zh.uhealthfit.com', url='SHOP_TRIAL:eye-patches'),
  dict(author='力工 谭', verified=True, date='2025-12-31', rating=5, text='很好', item='明目冷敷眼貼', src='zh.uhealthfit.com', url='SHOP:eye-patches'),
  dict(author='A.W.', verified=True, date='2025-11-18', rating=5, text='good', item='兩晚體驗裝', src='zh.uhealthfit.com', url='SHOP_TRIAL:eye-patches'),
 ],
 'eye-cream': [
  dict(author='nancy', verified=True, date='2026-10-02', rating=5, text='很好用，清清涼涼的', item='草本舒緩修護眼霜', src='uhealthfit.com', url=UH_EYE_CREAM),
  dict(author='Tay Chea kiang', verified=False, date='2026-07-29', rating=5, text='很好', item='草本舒緩修護眼霜', src='zh.uhealthfit.com', url='SHOP:eye-cream'),
 ],
}
# 合規盤點 A6：眼貼使用示範影片可用；原頁文字「瞬間帶走酸澀」「重拾明亮眼神」已改為中性描述
DEMOS = {
 'eye-patches': dict(src='https://cdn.shopify.com/videos/c/o/v/dc358b61932e4aee89b25db5585fa201.mp4', title='簡單 3 步，給雙眼一段草本放鬆時間',
   steps=[('即開即用','撕開包裝，取出草本眼貼，隨時隨地開始放鬆。'),('輕輕一貼','順著眼周曲線，貼在內眼角、外眼角與下眼瞼下方的肌膚上，不入眼，帶來清涼感。'),('靜靜休息','閉上雙眼，讓雙眼放鬆。白天可短暫使用，睡前可貼整晚。')]),
}
def _rev_url(r):
    u=r['url']
    if u.startswith('SHOP_TRIAL:'): return shop_url(PRODUCTS[u.split(':',1)[1]]['trial_handle'])
    if u.startswith('SHOP:'): return shop_url(PRODUCTS[u.split(':',1)[1]]['handle'])
    return u
def _zh_date(d):
    y,m,dd=d.split('-'); return f'{y} 年 {int(m)} 月 {int(dd)} 日'
def reviews_section(slug):
    rs=sorted(REVIEWS.get(slug,[]), key=lambda r:r['date'], reverse=True)
    if not rs: return ''
    avg=sum(r['rating'] for r in rs)/len(rs)
    def stars(n): return f'<span class="stars" role="img" aria-label="5 分中的 {n} 分">'+'★'*n+'<i>'+'★'*(5-n)+'</i></span>'
    cards=''.join(f'''<article class="rev"><div class="rev-top">{stars(r['rating'])}<span class="rev-item">購買品項：{esc(r['item'])}</span></div>
      <p class="rev-body">{esc(r['text'])}</p>
      <div class="rev-meta"><b>{esc(r['author'])}</b><span class="{'rev-ok' if r['verified'] else 'rev-na'}">{'已驗證買家' if r['verified'] else '未標示為已驗證買家'}</span><span>{_zh_date(r['date'])}</span><a class="ext" href="{_rev_url(r)}" target="_blank" rel="noopener">{r['src']}</a></div></article>''' for r in rs)
    return f'''<section class="sec" id="reviews"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">買家評價</span><h2>買家怎麼說</h2>
    <p class="rev-sum">{stars(round(avg))}<b>{avg:.1f}</b> / 5 · {len(rs)} 則評價</p>
    <p class="note">評價取自 uhealthfit.com 與 zh.uhealthfit.com 兩個官方商店的 Judge.me 評價，原文照登（簡體字保留原文），正面與負面評價一併呈現，不含品牌或代理商人員撰寫的評價。每則為個人使用感受，效果因人而異。</p></div>
  <div class="rev-grid">{cards}</div>
</div></section>
'''
def demo_section(slug):
    d=DEMOS.get(slug)
    if not d: return ''
    steps=''.join(f'<li><b>Step {i+1}　{esc(t)}</b><span>{esc(x)}</span></li>' for i,(t,x) in enumerate(d['steps']))
    return f'''<section class="sec"><div class="wrap demo">
  <div class="demo-video"><video src="{d['src']}#t=0.5" controls muted playsinline preload="metadata" aria-label="{esc(d['title'])}（使用示範影片）"></video></div>
  <div><span class="eyebrow">使用示範</span><h2>{esc(d['title'])}</h2><ol class="demo-steps">{steps}</ol>
    <p class="note">影片為使用方式示範；建議用量與注意事項，請以上方「用法與注意」為準。</p></div>
</div></section>
'''


# ───── 成分解析：改寫自 zh.uhealthfit.com 各產品頁的成分說明（2026-10-22 擷取），依 BRIEF.md 合規紅線改寫 ─────
# 原則：中醫概念以「中醫傳統認為／傳統上用於」表述；不寫疾病名稱、不用療效動詞；外用品只描述使用感受與外觀。
# 眼貼、固齒膠囊的成分清單在商店不同頁面互相矛盾，待客戶確認後再補，這裡暫不收。
INGREDIENTS = {
 'calmoon': dict(
   title='七味草本，依「君臣佐使」分工',
   intro='中醫方劑講究「君臣佐使」：君藥定方向，臣藥輔助君藥，佐藥從旁協調，使藥調和諸藥。Calmoon 的七味草本依這套傳統結構配伍，不靠單一成分，而是讓每一味各司其職。',
   items=[('君','炒酸棗仁','中醫傳統上用於養心安神，是整個配方的核心，決定「幫助身心放鬆、支持自然睡眠節律」的方向。'),
          ('臣','合歡皮','傳統上用於舒緩情緒，幫助身心放鬆下來。'),
          ('臣','刺五加','傳統上用於幫助身體因應日常壓力，支持白天的精神狀態。'),
          ('佐','茯神','傳統上用於寧心安神，溫和支持夜晚的放鬆。'),
          ('佐','百合','中醫常見的清補草本，傳統上用於滋養身心。'),
          ('佐','丹參','傳統上用於養血安神，在配方中與其他草本協同。'),
          ('使','夏枯草','中醫傳統認為可清肝火；在配方中負責調和寒熱，讓整體更平和、適合日常持續使用。')],
   facts=[('建議用法','午餐後與晚餐後各 3 粒'),('規格','180 粒／瓶'),('不含','褪黑素'),('劑型','全植物膠囊（全素）、無麩質')]),
 'enerbalance': dict(
   title='七味草本，依「君臣佐使」分工',
   intro='傳統膏方常見的七味草本配伍，依「君臣佐使」設計：一溫一涼的補氣組合打底，再以健脾、養血、調和的草本平衡，讓配方更平和、更適合日常持續。',
   items=[('君','西洋參','中醫傳統認為可益氣養陰，性偏涼，支持日常的活力狀態。'),
          ('君','黃芪','傳統上用於補氣，性偏溫；與西洋參一溫一涼，讓整體藥性平和。'),
          ('臣','山藥','傳統上用於健脾補氣，補而不膩，讓配方更容易長期使用。'),
          ('臣','陳皮','傳統上用於理氣健脾，平衡西洋參偏滋潤的特性。'),
          ('佐','當歸','傳統上用於養血。中醫講「氣血同補」，在補氣配方中負責養血。'),
          ('使','菊花','性偏涼，傳統上作為清補配方中的調和草本。'),
          ('使','玉米鬚','傳統上用於支持正常的水液代謝，讓配方補中有泄、更適合日常調養。')],
   facts=[('每份','3 粒，約 1,500 毫克草本精粹'),('建議用法','每天 2 次，每次 3 粒，隨餐'),('規格','180 粒／瓶（60 份）'),('濃縮比例','5:1'),('不含','咖啡因、麩質、添加糖'),('製造','美國 cGMP 規範生產；生產設施具 FDA 登記（登記不等於 FDA 核准）')]),
 'herbalflow': dict(
   title='六味草本，依「君臣佐使」分工',
   intro='HerbalFlow 不採用番瀉葉等刺激性成分，而是依中醫「君臣佐使」的配伍思路，讓六味草本各司其職：潤、行、通、養、清。草本採購自東亞合法種植者，於美國 cGMP 註冊廠房封裝。',
   items=[('潤・核心','火麻仁（THC-Free）','富含 Omega 脂肪酸，傳統上用於潤腸，幫助保持柔軟、支持腸道潤滑；久坐族群與長輩都適合日常調理。'),
          ('行','萊菔子','傳統上用於消食下氣，支持胃腸的日常動力，舒緩飯後「頂著一股氣」的飽脹感。'),
          ('通・核心','厚朴','傳統上用於行氣、燥濕除滿，幫助舒緩腹部的飽脹感，支持胃腸舒適。'),
          ('養','生地黃','傳統上用於清熱、養陰生津，幫助維持腸道的濕潤環境。'),
          ('養','當歸','傳統上用於養血潤燥，是中醫常見、適合長期溫和調理的草本。'),
          ('清・調','馬齒莧','傳統上用於清熱、利水，幫助維持舒適、平衡的腸道環境。')],
   facts=[('建議用法','每天 2 次，每次 3 粒，隨餐'),('規格','180 粒／瓶'),('不含','番瀉葉等刺激性成分'),('劑型','全植物膠囊')]),
 'lumiview': dict(
   title='七味藥食同源草本，從整體支持',
   intro='中醫傳統認為「肝開竅於目」「五臟六腑之精氣，皆上注於目」。LumiView 的七味草本從這個整體觀出發：枸杞、當歸、菊花偏重滋養肝腎；決明子、菊花偏重清肝；黃芪、當歸、茯苓、山藥則補益氣血。',
   items=[('滋養','枸杞','中醫傳統認為可滋補肝腎、益精明目。'),
          ('清肝','菊花','傳統上用於清肝明目，是常見的藥食同源草本。'),
          ('清肝','決明子','傳統上用於清肝明目。'),
          ('氣血','黃芪','傳統上用於補氣，支持整體的元氣。'),
          ('氣血','當歸','傳統上用於養血活血。'),
          ('氣血','山藥','傳統上用於益氣養陰，脾腎同養。'),
          ('氣血','茯苓','傳統上用於健脾利濕。')],
   facts=[('每份','3 粒，草本複合配方 1,500 毫克'),('建議用法','每天 2 次，每次 3 粒，隨餐'),('規格','180 粒／瓶'),
          ('草本複合配方','決明子萃取物（Cassia obtusifolia）、枸杞子萃取物（Lycium barbarum）、菊花萃取物（Chrysanthemum indicum）、黃耆萃取物（Astragalus membranaceus）、山藥萃取物（Dioscorea opposita）、當歸萃取物（Angelica sinensis）、茯苓萃取物（Poria cocos）'),
          ('其他成分','羥丙基甲基纖維素（植物膠囊）、硬脂酸鎂')]),
 'soothing-cream': dict(
   title='七種東方植萃，加上三種保濕成分',
   intro='東方草本搭配現代保濕成分，目的不是暫時蓋過不適，而是每天把肌膚的保濕與屏障照顧好。',
   items=[('植萃','積雪草','現代護膚常見的舒緩植萃，幫助維持肌膚屏障，讓膚觸柔潤穩定。'),
          ('植萃','紫草','傳統東方護膚成分，滋潤乾燥、脆弱的肌膚，保持柔潤。'),
          ('植萃','苦參','東方傳統草本護理成分，提供清爽的日常護理。'),
          ('植萃','尤加利 × 薄荷','天然的清涼觸感，塗抹時帶來清新、舒適的感受。'),
          ('植萃','蒲公英','幫助舒緩因環境變化而感覺不適的肌膚，維持舒適膚感。'),
          ('植萃','白芷','東方美容傳統植萃，幫助肌膚看起來更細緻。')],
   facts=[('保濕成分','透明質酸（補水保濕，減少乾燥緊繃感）、維生素 E（抗氧化護理，維持柔潤）、維生素 C 衍生物（讓膚色看起來更明亮）'),('容量','30g'),('製造','美國製造'),('不含','類固醇'),('使用','臉部與身體皆可；首次使用請先在小範圍測試')]),
 'dentaforte': dict(
   title='十味草本，一份每日配方',
   intro='中醫傳統認為「腎主骨，齒為骨之餘」——牙齒的穩固，與整體的滋養有關。DentaForte 的十味草本依「滋養、健脾、循環、清熱」四個方向配伍；每份 3 粒含 1,500 毫克草本配方。',
   items=[('滋養','熟地黃','Rehmannia glutinosa，蒸製根。中醫傳統上用於滋養肝腎，是配方「滋養」這一組的核心。'),
          ('滋養','生地黃','Rehmannia glutinosa，生根。與熟地黃搭配，傳統上用於清熱，讓配方不過於溫熱。'),
          ('滋養','枸杞','Lycium barbarum。中醫傳統上用於滋養肝腎，也是常見的藥食同源草本。'),
          ('滋養','五味子','Schisandra chinensis。經典的「五味」草本，傳統上用於收斂、滋養。'),
          ('滋養','菟絲子','Cuscuta chinensis。傳統上與上述草本搭配，用於日常調養，支持身體對營養的利用。'),
          ('健脾','黃芪','Astragalus membranaceus。傳統上用於補氣，是中醫最常使用的補益草本之一。'),
          ('健脾','山藥','Dioscorea opposita。傳統上用於健脾補氣，支持日常的營養吸收與平衡。'),
          ('健脾','茯苓','Poria cocos。傳統上用於健脾，平衡配方中的其他補益草本。'),
          ('循環','丹參','Salvia miltiorrhiza。中醫傳統認為丹參與血脈循環有關，在配方中支持牙齦組織的日常循環。'),
          ('清熱','野菊花','Chrysanthemum indicum。傳統上用於清熱，幫助維持口腔的清新與舒適。')],
   facts=[('每份','3 粒，草本配方 1,500 毫克'),('建議用法','每天 2 次，每次 3 粒，隨餐'),('規格','180 粒／瓶（60 份，約 30 天）'),
          ('草本複方','熟地黃（蒸製根）、生地黃（生根）、山藥、丹參、五味子、野菊花、黃芪、茯苓、枸杞、菟絲子'),
          ('其他成分','羥丙甲纖維素（植物膠囊）、硬脂酸鎂'),('不含','基因改造成分、麩質、人工色素、香料、防腐劑')]),
 'clarifying-cream': dict(
   title='東方植萃 × 現代保養成分',
   intro='為易出油、易長痘的肌膚設計的輕盈面霜：天然礦物泥負責清爽，東方植萃負責舒緩與滋養，再加上三種現代保養成分。',
   items=[('清爽','皂土','天然礦物泥，幫助吸附多餘油脂，讓肌膚感覺清爽。'),
          ('植萃','蒲公英油','舒緩外在環境對肌膚帶來的不適感。'),
          ('植萃','金銀花油','傳統上用於清熱，幫助肌膚感覺舒緩、穩定。'),
          ('植萃','丹參根油','幫助肌膚看起來氣色紅潤。'),
          ('植萃','黨參根油','滋養肌膚。'),
          ('植萃','紫草根油','東方傳統護膚成分，幫助維持肌膚屏障。'),
          ('保養','維生素 C（SAP）','幫助肌膚看起來更明亮。'),
          ('保養','維生素 A 酯（Retinyl Palmitate）','讓膚觸與毛孔看起來更平滑細緻。'),
          ('保養','精氨酸（Arginine）','幫助肌膚保濕。')],
   facts=[('容量','30g'),('製造','美國製造'),('不含','類固醇、人工香料、刺激性酸類'),('使用','早晚於精華液後，取適量塗抹於臉部與頸部')]),
 'eye-cream': dict(
   title='六種草本，與眼貼、膠囊同源',
   intro='眼霜沿用護眼系列同源的草本體系，做成輕透乳霜，讓不方便貼眼貼的白天，也能用指尖完成一次眼周保養。',
   items=[('滋潤','石斛','中醫傳統上用於養陰，在配方中負責滋潤乾燥的眼周肌膚。'),
          ('舒緩','菊花','傳統上用於清熱，帶來舒緩的使用感受。'),
          ('舒緩','決明子','護眼系列同源的東方草本，與菊花搭配使用。'),
          ('保濕','茯苓','傳統上用於健脾利濕；在眼霜中幫助眼周肌膚保持水潤。'),
          ('光采','當歸根','東方傳統養顏草本，幫助眼周看起來更有光采。'),
          ('清涼','尤加利葉精油','帶來清涼、提神的使用感受。')],
   facts=[('容量','20g'),('製造','原料研發：日本；生產灌裝：美國'),('不含','苯氧乙醇、化學防腐劑、人工香精、合成色素、酒精'),('防護','採用氧化銀與植酸')]),
 'lifting-serum': dict(
   title='五種東方草本 × 現代保養成分',
   intro='東方草本負責滋養，現代保養成分負責保濕與彈性，做成清爽、好吸收的精華。',
   items=[('草本','人參','東方傳統養顏草本，幫助肌膚看起來更有彈性。'),
          ('草本','當歸','幫助肌膚看起來潤澤、有光采。'),
          ('草本','白芍','幫助膚色看起來更均勻。'),
          ('草本','茯苓','幫助肌膚保濕、維持清爽。'),
          ('草本','積雪草','舒緩植萃，幫助肌膚維持穩定。'),
          ('保養','胜肽','棕櫚醯三胜肽-1、棕櫚醯三胜肽-7，幫助肌膚看起來更緊緻。'),
          ('保養','神經醯胺 NP','幫助維持肌膚屏障。'),
          ('保養','透明質酸鈉','補水保濕。')],
   facts=[('容量','30ml'),('使用','潔面後、面霜之前取 3–4 滴，輕柔按壓於臉部與頸部；早晚皆可')],
   full='Water (Aqua), Glycerin, Caprylic/Capric Triglyceride, Limnanthes alba (Meadowfoam) Seed Oil, Squalane, Camellia sinensis Leaf Extract, Panax Ginseng Root Oil, Paeonia lactiflora Root Oil, Angelica sinensis Root Oil, Poria cocos Oil, Centella asiatica Oil, Glyceryl Stearate, Polysorbate 60, Polyglyceryl-10 Stearate, Bifida Ferment Lysate, Sodium Hyaluronate, Xanthan Gum, Palmitoyl Tripeptide-1, Palmitoyl Tripeptide-7, Ceramide NP, Bisabolol, Panthenol, Tetrahexyldecyl Ascorbate, Tocopherol, Dipotassium Glycyrrhizate, Parfum, Propanediol, Caprylhydroxamic Acid.'),
}
def ingredients_section(slug):
    g=INGREDIENTS.get(slug)
    if not g: return ''
    p=PRODUCTS[slug]; capsule='膠囊' in p['name']
    imgs=[ing_img(n) for _,n,_ in g['items']]; show_pics=sum(1 for x in imgs if x)*2>=len(imgs)
    def pic(n,u):
        if not show_pics: return ''
        return f'<div class="ing-pic"><img src="{u}" alt="{esc(n)}" loading="lazy"></div>' if u else f'<div class="ing-pic ing-pic-blank"><span>{esc(n[0])}</span></div>'
    cards=''.join(f'<div class="ing{" has-pic" if show_pics else ""}">{pic(n,u)}<span class="ing-role">{esc(r)}</span><h3>{esc(n)}</h3><p>{esc(t)}</p></div>' for (r,n,t),u in zip(g['items'],imgs))
    facts=''.join(f'<li><b>{esc(k)}</b><span>{esc(v)}</span></li>' for k,v in g.get('facts',[]))
    full=f'<details class="ing-full"><summary>完整成分表（INCI）</summary><p>{esc(g["full"])}</p></details>' if g.get('full') else ''
    note=('以上為中醫傳統觀點的說明，用於理解配方設計，不是醫療效果的宣稱。本品為膳食補充劑，不是藥品。' if capsule
          else '以上為成分在配方中的角色說明，描述的是使用感受與肌膚外觀。本品為日常保養品，不是藥品；首次使用請先做局部測試。')
    return f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">成分解析</span><h2>{esc(g['title'])}</h2><p class="lead" style="font-size:16px">{esc(g['intro'])}</p></div>
  <div class="ing-grid">{cards}</div>
  {f'<ul class="ing-facts">{facts}</ul>' if facts else ''}
  {full}
  <p class="note" style="margin-top:14px">{note}</p>
</div></section>
'''


# ───── 追蹤碼：與 zh.uhealthfit.com 相同（2026-10-23 自商店頁面讀取）─────
# GTM 容器 GTM-W58N8HRV：商店佈景主題裡的同一個容器（內含 GA4 Google 代碼但 send_page_view=false、點擊／表單事件、Ads 轉換連結器）
# GA4 G-M63Z9F6FR7：商店經 Shopify Google 應用程式送網頁瀏覽；本站以 gtag.js 載入，負責網頁瀏覽與 main.js 的自訂事件
# Meta Pixel 2216128798841618：商店經 Shopify Facebook 應用程式載入；本站以官方基本碼載入（GTM 容器內沒有 Pixel）
GTM_ID = 'GTM-W58N8HRV'
GA4_ID = 'G-M63Z9F6FR7'
META_PIXEL_ID = '2216128798841618'
# 載入順序很重要：gtag.js 必須在 GTM 之前。若 GTM 先載入，同一個 GA4 ID 只會保留 GTM 那份（send_page_view=false），
# 本站的網頁瀏覽與自訂事件都不會送出（2026-10-23 實測）。gtag 先載入時，page_view 與各事件都只送一次，不重複。
TRACKING_HEAD_TOP = ("<!-- Google tag (gtag.js) -->\n"
  "<script async src=\"https://www.googletagmanager.com/gtag/js?id=__GA4__\"></script>\n"
  "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','__GA4__');</script>\n"
  "<!-- Google Tag Manager -->\n"
  "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','__GTM__');</script>\n"
  "<!-- End Google Tag Manager -->").replace('__GA4__', GA4_ID).replace('__GTM__', GTM_ID)
TRACKING_HEAD_END = ("<!-- Meta Pixel -->\n"
  "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','__PIXEL__');fbq('track','PageView');</script>\n"
  "<!-- End Meta Pixel -->").replace('__PIXEL__', META_PIXEL_ID)
TRACKING_BODY_TOP = ("<!-- Google Tag Manager (noscript) --><noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=__GTM__\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\n"
  "<noscript><img height=\"1\" width=\"1\" style=\"display:none\" alt=\"\" src=\"https://www.facebook.com/tr?id=__PIXEL__&amp;ev=PageView&amp;noscript=1\"></noscript>").replace('__GTM__', GTM_ID).replace('__PIXEL__', META_PIXEL_ID)


# ───── 產品頁充實內容：改寫自 uhealthfit.com/zh-TW 各產品頁（2026-10-25 擷取），依 BRIEF.md 合規紅線改寫 ─────
# 售價一律以 zh.uhealthfit.com 為準（PRODUCTS 裡的 price），這裡只放介紹、用法、配圖。
# 不採用：疾病名稱、療效宣稱、前後對比照、未核實數據（如回購率）、貶抑其他品類的比較。
# 眼貼、固齒膠囊的成分清單待客戶確認，這裡不改動它們的成分，只補用法與配圖。
U_IMG = 'https://uhealthfit.com'
def u_opt(path, w=1200):   # uhealthfit.com 的最佳化圖
    return f'{U_IMG}/_optimized/{path}-{w}.avif'
def u_png(path):
    return f'{U_IMG}/{path}.png'
# 成分實物照（uhealthfit.com/ingredients/）
ING_IMG = {
 '西洋參':'panax-ginseng','人參':'panax-ginseng','黃芪':'astragalus','山藥':'chinese-yam','當歸':'angelica','當歸根':'angelica',
 '陳皮':'citrus-peel','菊花':'chrysanthemum','玉米鬚':'corn-silk','丹參':'salvia','丹參根油':'salvia','枸杞':'goji','茯苓':'poria',
 '火麻仁（THC-Free）':'hemp-seed','生地黃':'raw-rehmannia','厚朴':'magnolia-bark','萊菔子':'radish-seed','馬齒莧':'purslane',
 '積雪草':'centella-cica','紫草':'comfrey','紫草根油':'comfrey','苦參':'sophora','尤加利 × 薄荷':'eucalyptus-menthol','尤加利葉精油':'eucalyptus-menthol',
 '石斛':'dendrobium','白芍':'white-peony','尤加利 × 薄荷':'eucalyptus-menthol','熟地黃':'prepared-rehmannia','五味子':'schisandra','野菊花':'chrysanthemum','菟絲子':'dodder-seed','胜肽':'peptide-complex','神經醯胺 NP':'ceramides-ha',
}
def ing_img(name):
    k=ING_IMG.get(name); return u_opt(f'ingredients/{k}',800) if k else None

DETAILS = {
 'enerbalance': dict(
   image='https://cdn.shopify.com/s/files/1/0676/4675/0818/files/c4001f0d-6d94-4413-9958-8a31fc2e4367.jpg?v=1786711467&width=1000',  # zh 黑膏滋介紹頁主圖：瓶身與草本切片
   promo_image='https://cdn.shopify.com/s/files/1/0706/1287/7467/files/heigaozi-single-thanksgiving-clean-v2.png?v=1791939199&width=1000',  # 商店「感恩回饋 40% OFF $179」特價圖；活動結束請刪除這一行
   stats=[('0%','咖啡因'),('7 味','傳統草本'),('1,500 mg','每份草本精粹')],
   showcase=dict(img=u_png('products/enerbalance/enerbalance-bottle-open-capsules'), eyebrow='產品介紹', title='傳統黑膏滋，做成每天方便吃的膠囊',
     text='膏滋，是中醫把草本反覆煎煮、去渣後濃縮成膏的傳統工藝。EnerBalance 保留同樣的合煎精華，濃縮進標準化的植物膠囊：每份劑量固定、獨立取用、常溫保存，出門也方便帶。',
     bullets=['植物性膠囊殼（羥丙甲纖維素），適合素食者','明確標示 5:1 濃縮比例，無添加糖','每份 3 粒，每瓶 60 份','不含咖啡因與強刺激性成分，不以短暫提神為目的']),
   compare=dict(title='傳統膏滋與膠囊，差在哪裡', cols=['傳統膏滋','EnerBalance 膠囊'], rows=[
     ('衛生與取用','開罐後反覆用勺挖取，長期接觸空氣','獨立密封膠囊，取用不接觸空氣與器具'),
     ('劑量','自行舀取，用量因人而異','每份劑量標準化，每日兩次、每次 3 粒'),
     ('保存','質地黏稠，多需冷藏，保存期較短','常溫陰涼乾燥處保存'),
     ('攜帶','不易分裝，外出不方便','膠囊輕巧，隨身攜帶、隨餐服用'),
     ('添加','常以冰糖、蜂蜜收膏','草本精粉直接封裝，無添加糖'),
     ('濃縮比例','依製作經驗而異，多不對外揭露','標示 5:1，批次標準化、可追溯')]),
   how=[('每日兩次','每次 3 粒，每日共 6 粒（約 3,000 mg）。'),('隨餐服用','放在早餐、午餐或晚餐旁，最容易記得。'),('以月為單位','一瓶 180 粒約一個月；持續使用，效果因人而異。')],
   yes=['經常熬夜、工作節奏緊湊的上班族','運動後想多一份日常滋養的人','希望日常溫和進補的中老年人','想減少咖啡因、改用草本支持活力的人','注重天然植物營養的養生族群'],
   caution='請勿超過建議用量。孕婦及哺乳期女性請勿使用。18 歲以下、正在服用抗凝血藥物（如華法林）或其他藥物，或有健康狀況、正在接受醫療照護者，使用前請先諮詢醫師。使用中如有不適，請停止使用並諮詢專業醫療人員。瓶口封膜破損請勿使用；請置於兒童無法取得處，陰涼乾燥保存。'),
 'calmoon': dict(
   stats=[('7 味','君臣佐使草本'),('0','褪黑素'),('2 次','每日：午後、睡前')],
   showcase=dict(img=u_opt('products/calmoon/calmoon-ingredients-collage'), eyebrow='產品介紹', title='四個方向，一起照顧夜晚',
     text='Calmoon 不靠單一成分讓人「關機」。七味草本依中醫「君臣佐使」的傳統結構，分成四個方向，同時照顧夜晚的放鬆、白天累積的情緒與壓力，以及隔天的精神。',
     bullets=['安神：炒酸棗仁、茯神、百合，傳統上用於養心安神','舒緩情緒：合歡皮、夏枯草，幫助睡前放鬆','因應壓力：刺五加，傳統上用於幫助身體因應日常壓力','白天精神：刺五加、丹參，支持隔天的專注與精神']),
   compare=dict(title='和市面上其他助眠選擇，差別在哪？', hl=0,
     intro='每一種選擇都有它的位置。這張表不是比較誰比較好，而是說明它們各自負責什麼，方便你判斷哪一種比較貼近自己的需求。',
     cols=['Calmoon 安睡草本','褪黑素','單方草本'], rows=[
     ('思路','七味草本複方，同時照顧安神、情緒、壓力與白天精神','補充身體本來就會分泌的睡眠相關激素','以單一草本為主，作用方向較單純'),
     ('照顧情緒','合歡皮、夏枯草，傳統上用於舒緩情緒、幫助睡前放鬆','不是主要用途','視所選的草本而定'),
     ('壓力調適','刺五加，傳統上用於幫助身體因應日常壓力','不是主要用途','視所選的草本而定'),
     ('使用時段','午後與睡前各一次，從白天開始放鬆','多在睡前使用','依產品建議'),
     ('是否含激素','不含褪黑素等激素','屬於激素類補充','多數不含激素')],
     note='若正在使用任何助眠產品或藥物，請先諮詢醫師或藥師，不要自行疊加。效果因人而異。'),
   how=[('午後一次','午餐後隨餐 3 粒，先幫白天的緊繃鬆一步。'),('睡前一次','晚餐後或睡前約一小時 3 粒，讓夜晚自然放鬆。'),('規律使用，給自己 4–8 週','每日共 6 粒（約 3,000 mg）；建議規律使用，並給自己 4–8 週觀察；效果因人而異。')],
   caution='請勿超過建議用量。孕婦及哺乳期女性請勿使用。18 歲以下、正在服用抗凝血藥物（如華法林）、鎮靜類藥物或其他藥物，或有健康狀況者，使用前請先諮詢醫師。服用後請勿駕駛或操作機械。如有不適，請停止使用。請置於兒童無法取得處，陰涼乾燥保存。'),
 'dentaforte': dict(
   stats=[('10 味','傳統草本'),('1,500 mg','每份草本配方'),('隨餐','每日兩次')],
   showcase=dict(img=u_png('editorial/capsule-open'), eyebrow='產品介紹', title='刷牙之外，每天從內在多做一點',
     text='DentaForte 不是牙膏、漱口水這類清潔產品，而是放在餐桌旁的日常草本補充。它設計為和刷牙、牙線、定期洗牙並行，不取代任何一項。',
     bullets=['與牙醫照護並行，不取代專業檢查','以月為單位、每日規律食用而設計，不是短期療程','植物膠囊；非基因改造、不含麩質，不含人工色素、香料與防腐劑','草本採購自東亞，於美國 cGMP 登記廠房封裝']),
   pillars=dict(img=u_opt('products/dentaforte/dentaforte-hero'), eyebrow='養護什麼', title='草本固齒膠囊養護什麼',
     intro='同一套配方，從五個方向支持牙齒與牙齦的日常狀態。每一個方向，都是長期口腔保養的一項每日投入。',
     items=[('根本：從整體滋養出發','中醫傳統認為「腎主骨，齒為骨之餘」，牙齒的穩固與整體的滋養有關。熟地黃、枸杞、菟絲子等，傳統上用於日常調養。'),
            ('牙齦舒適','野菊花、五味子，傳統上用於支持平靜、舒適的牙齦。'),
            ('日常循環','中醫傳統認為丹參與血脈循環有關，在配方中支持牙齦組織的日常循環。'),
            ('營養利用','山藥與菟絲子傳統上常搭配使用，支持身體對營養的利用。'),
            ('整體元氣','黃芪與茯苓是傳統上最常用的補益草本，支持整體的日常狀態。')]),
   faq=[('吃了一定會有感覺嗎？','我們無法保證，也無法預測每個人的反應。我們能說明的是配方的設計方向：以月為單位、每日規律食用的草本營養支持。效果因人而異，與其過度承諾，我們寧願坦誠。'),
        ('多久才會有感覺？','我們不承諾時間表。這套配方是為以月為單位、每日規律食用而設計，不是短期療程；建議至少給自己 4–8 週，並當作長期口腔保養的一部分。'),
        ('可以取代看牙醫嗎？','不能。DentaForte 是膳食補充劑，不是藥品，也不能取代牙醫的檢查與處置。請持續定期洗牙、檢查，以及牙醫建議的照護。'),
        ('正在服用抗凝血藥物，可以吃嗎？','配方中的丹參、五味子已知可能與抗凝血藥物產生交互作用。開始服用前，請先諮詢醫師。'),
        ('為什麼一天要吃 6 粒，而不是一顆？','每日約 3,000 毫克的配方，無法裝進一顆好吞嚥的膠囊；分成早晚兩次，也能讓一天的攝取更平均。'),
        ('漏吃一天或一週怎麼辦？','不要加倍補回，直接恢復正常用量即可。長期規律，比任何單獨的一天更重要。'),
        ('草本來自哪裡？','草本採購自東亞（這些植物的原生地）的合法種植者，最後在美國通過 cGMP 登記的廠房封裝。'),
        ('有沒有需要注意的反應？','最常見的是第一週輕微的消化適應，隨餐服用可以減輕；部分人的糞便顏色會因草本色素略有變化，屬於正常現象。若有任何異常，請停止服用並與我們聯繫。'),
        ('替長輩購買要注意什麼？','長輩若正在服藥或有慢性健康狀況，請先與醫師或藥師確認。全植物膠囊、隨餐服用，放在早餐旁邊最容易記得。')],
   how=[('每日兩次','早晚隨餐各 3 粒，每日共 6 粒（約 3,000 mg）。'),('一定隨餐','隨餐服用吸收更好，也能減少首週的消化適應。'),('以月為單位','一瓶 180 粒約 30 天；部分人在諮詢牙醫後改為每日一次維持。漏服時直接恢復，不要加倍補回。')],
   caution='孕婦及哺乳期女性、未滿 18 歲、正在服用抗凝血藥物（配方中的丹參、五味子可能與其交互作用）、兩週內預定進行牙科手術，或已知對植物過敏者，使用前請先諮詢醫師。請持續定期洗牙與牙科檢查。'),
 'herbalflow': dict(
   image=None,
   stats=[('6 味','傳統草本'),('0','番瀉葉等刺激性成分'),('THC-Free','火麻仁')],
   showcase=dict(img=u_png('products/herbalflow/herbalflow-bottle-open-capsules'), eyebrow='產品介紹', title='不只是今天順，而是以後每一天都自然',
     text='很多人只在意「今天有沒有順」，卻忽略了飯後頂著的那股「氣」。HerbalFlow 的思路是不強迫腸道：一邊潤養、一邊行氣，同時照顧腸道環境，陪它找回自己的節律。',
     bullets=['非刺激性配方，以日常調理為定位','兼顧規律順暢與飯後腹部舒適','全植物膠囊，無麩質、無添加糖','美國製造（使用進口原料）']),
   pillars=dict(img=f'{IMG}/_optimized/products/herbalflow/herbalflow-in-hand-1145.avif', eyebrow='三步協同', title='潤．行．調，更完整的日常支持',
     intro='六味草本各有分工，從「乾」、「脹」到腸道環境，建立更完整的日常調理思路。',
     items=[('第一步｜潤：照顧「乾」','火麻仁富含 Omega-3／6 脂肪酸，搭配當歸、生地黃溫和滋養，傳統上用於久坐族群的日常順暢支持。'),
            ('第二步｜行：照顧「脹」','HerbalFlow 最大的不同。厚朴傳統上用於行氣、舒緩腹部飽脹，搭配萊菔子消食下氣，照顧「老覺得有一股氣」的不適感。'),
            ('第三步｜調：照顧腸道環境','馬齒莧傳統上用於清熱、利水，幫助維持舒適、平衡的腸道環境，為規律的節奏打好基礎。')]),
   compare=dict(title='四種常見選擇，差別在哪？', hl=0,
     intro='HerbalFlow 追求的不是「更猛」，而是兼顧順暢、腹部舒適與日常使用的感受。每一種選擇都有它適合的情境，這張表說明它們各自的思路。',
     cols=['HerbalFlow 草本潤暢','刺激性草本（如番瀉葉）','高劑量檸檬酸鎂','一般膳食纖維'], rows=[
     ('作用思路','潤養＋行氣，支持腸道的自然節律','刺激腸道蠕動','以滲透作用增加腸道水分','增加內容物的體積'),
     ('飯後脹氣感','厚朴、萊菔子，傳統上用於行氣','不是主要用途','不是主要用途','部分人會覺得較脹，因人而異'),
     ('使用定位','每日溫和調理','多建議短期使用','依產品建議，不宜自行長期高劑量','可長期作為飲食的一部分'),
     ('配方屬性','火麻仁（THC-Free）等六味植物複方','單一刺激性草本','單一礦物質','單一膳食纖維')],
     note='若有持續的腸胃不適、腹痛或出血，請先就醫；正在使用其他產品或藥物，請先諮詢醫師或藥師，不要自行疊加。'),
   faq=[('會不會越吃越多？','HerbalFlow 不含番瀉葉等刺激性成分，設計原則是支持節律；節律穩定後可以停用。'),
        ('和含番瀉葉的產品有什麼不同？','番瀉葉等刺激性成分多建議短期使用。HerbalFlow 不含刺激性草本，定位是每日溫和的腸道支持——我們在意的不只是今天順不順，而是陪腸道找回自己工作的節奏。'),
        ('為什麼是六味複方，而不是單一草本？','中醫經典方講究「君、臣、佐、使」——不同草本各有分工，一起完成同一個目標。HerbalFlow 也是如此：火麻仁負責潤、萊菔子負責行、厚朴負責通、當歸與生地黃負責養、馬齒莧負責清與調。'),
        ('和益生菌衝突嗎？','角度不同。是否同時使用請先與醫師或藥師討論。'),
        ('多久會有感覺？','多數人在前幾週先感受到餐後的輕盈感，節律的穩定通常需要 4–8 週；效果因人而異。')],
   how=[('每次 3 粒','建議隨餐服用，讓草本溫和配合消化過程。'),('每日 2 次','分配在兩餐，維持全天的節律。'),('溫和路線，貴在持續','規律使用，給腸道一段時間找回自己的節奏；效果因人而異。')],
   yes=['久坐少動、希望兼顧節律與飯後舒適的上班族','偏好溫和、循序漸進路線的中老年人','應酬外食頻繁，希望兼顧消化與順暢的人'],
   caution='請勿超過建議用量。孕婦、哺乳期女性及未滿 18 歲者請勿使用。正在服用抗凝血藥物（如華法林）或其他藥物，或有腸胃道健康狀況者，使用前請先諮詢醫師。如出現持續的腸胃不適，請停止使用並就醫。請置於兒童無法取得處，陰涼乾燥保存。'),
 'lumiview': dict(
   stats=[('7 種','植物精華'),('1,500 mg','每份草本配方'),('隨餐','每日兩次')],
   showcase=dict(img=u_opt('products/lumiview/lumiview-ingredients'), eyebrow='產品介紹', title='七味藥食同源草本，從整體出發',
     text='中醫傳統把眼睛看成一條長鏈的末端，這條鏈始於肝與腎，所以 LumiView 是複方，而不是單一萃取物。七味草本都是古典方劑裡長久搭配使用的組合。',
     bullets=['枸杞、山藥：配方的滋補基底，也是玉米黃素的膳食來源','菊花、決明子：古典方劑裡常見的搭配，富含植物類黃酮','黃芪、當歸：傳統的氣血配對','茯苓：平衡配方中的其他補益草本']),
   how=[('每日兩次','早餐後、晚餐後各 3 粒，每日共 6 粒（約 3,000 mg）。'),('務必隨餐','不要空腹服用。'),('以月為單位','一瓶 180 粒約 30 天；長期維持時，許多人改為每日一次、每次 3 粒。這是服用時程，不是效果預測。')],
   yes=['每天面對螢幕 6 小時以上的上班族','想建立日常保養習慣、並定期做眼科檢查的 40–60 歲族群','從求學時期就與螢幕為伴的數位世代','白天在戶外、晚上還要看螢幕的人','喜歡完整日常流程、能持之以恆的人'],
   caution='未滿 18 歲、孕期或哺乳期、正在服用抗凝血藥物，或兩週內計畫進行眼部手術者，請先諮詢醫師。請隨餐服用，勿空腹。'),
 'eye-patches': dict(
   stats=[('6 片','每晚建議用量'),('約 10 晚','每盒 60 片'),('0','防腐劑')],
   how_title=('使用時的感受','貼上之後，清涼感會這樣慢慢展開'),
   how=[('約 30 秒','眼周開始出現清涼感。'),('約 1 分鐘','清涼感擴散到整個眼周。'),('3–5 分鐘','眼睛周圍一片清爽。'),('整晚','柔軟的水凝膠保持濕潤，配戴數小時依然舒適；隔天早上取下。')]),
 'eye-cream': dict(
   stats=[('6 種','草本精萃'),('20g','隨身裝'),('0','苯氧乙醇、人工香精')],
   showcase=dict(img=u_png('products/herbal-soothing-repair-eye-cream/herbal-soothing-repair-eye-cream-ingredients'), eyebrow='產品介紹', title='不方便貼眼貼的時候，點一點就好',
     text='長時間用眼、熬夜、旅途，最先顯現在嬌嫩的眼周。辦公室、通勤或出差時不方便貼眼貼，指尖取米粒大小，沿眼眶骨輕輕點拍，30 秒完成一次眼周保養。',
     bullets=['伏案工作的午後：眼周看起來比較疲憊的時候','飛行、出差的旅途中','晚上出門前，讓眼周看起來更有神采']),
   how=[('時間','早晚或睡前，於潔淨肌膚上使用。'),('用量','每隻眼取米粒大小，沿眼眶骨輕柔點拍至吸收。'),('避開','眼瞼與睫毛根部，只用於眼周肌膚。')],
   caution='僅供外用，避免直接接觸眼睛；請勿用於破損肌膚。如懷孕或哺乳，使用前請諮詢醫師。如有不適，請停止使用。'),
 'soothing-cream': dict(
   stats=[('7 種','東方植萃'),('0','類固醇'),('30g','早晚使用約 60 天')],
   showcase=dict(img=u_opt('products/herbal-soothing-repair-cream/herbal-soothing-repair-cream-package'), eyebrow='產品介紹', title='一罐面霜，陪你一天的每個時刻',
     text='東方植萃加上透明質酸與維生素 E、C 衍生物，溫和到可以天天用，臉部和身體都適用。',
     bullets=['早晨：潔面後的第一步，尤加利與薄荷帶來清涼感，可疊在底妝之下','夜晚：睡前塗稍厚一層，醒來時肌膚感覺更平靜、更舒適','換季、曬後：天候轉變或戶外活動後，為泛紅、發熱的外觀帶來清涼與舒適','從頭到腳：手肘、膝蓋、乾燥的雙手，任何感到緊繃的部位']),
   how=[('時機','早晚，於潔淨肌膚使用化妝水或精華液之後。'),('用量','取約豌豆大小，輕柔按壓於需要的部位。'),('第一次使用','先在前臂內側做 24 小時皮膚測試。')]),
 'clarifying-cream': dict(
   stats=[('9 種','植萃與保養成分'),('0','類固醇、刺激性酸類'),('30g','早晚使用約 60 天')],
   showcase=dict(img=u_opt('products/herbal-clarifying-cream/herbal-clarifying-cream-texture'), eyebrow='產品介紹', title='適合什麼樣的肌膚？',
     text='輕盈的乳霜質地，觸膚即融，不黏膩。不含強效刺激成分，以草本與溫和的保養成分為主。',
     bullets=['油性、易泛油光：洗臉後不久就泛油的肌膚，幫助吸附多餘表面油脂，同時不破壞屏障','混合性：T 字部位油亮、兩頰卻緊繃，平衡油光，讓屏障保持舒適','泛紅、敏感：不含酸類與刺激性活性成分，溫和到適合容易受刺激的肌膚']),
   how=[('時機','早晚，於潔淨肌膚使用化妝水或精華液之後。'),('用量','取約豌豆大小，均勻塗抹全臉，避開眼周。'),('第一次使用','先在前臂內側做 24 小時皮膚測試。')]),
 'lifting-serum': dict(
   stats=[('5 種','東方草本'),('2 種','胜肽'),('30ml','早晚使用約 60 天')],
   showcase=dict(img=u_opt('products/herbal-lifting-revitalizing-serum/herbal-lifting-revitalizing-serum-package'), eyebrow='產品介紹', title='細紋、光澤、彈潤，每個人在意的不一樣',
     text='不追求堆砌二十種成分，而是讓每一種成分各司其職：東方草本負責滋養，胜肽、神經醯胺與透明質酸負責彈潤與保濕。',
     bullets=['初現細紋：眼周、嘴角與額頭的細紋，在拍照與明亮光線下更明顯','暗沉、疲憊：熬夜與忙碌讓膚色看起來平淡、沒有光澤','彈潤感不如從前：妝容的服貼度也和幾年前不同']),
   how=[('時間','早晚，於潔淨肌膚上、面霜之前。'),('用量','3–4 滴，輕柔按壓於臉部與頸部。'),('第一次使用','先在前臂內側做 24 小時皮膚測試。')],
   caution='僅供外用，避免直接接觸眼睛。如有不適，請停止使用。敏感肌首次使用前請先做皮膚測試。如懷孕或哺乳，使用前請諮詢醫師。'),
}
# 套用到產品資料：主圖、適合誰、注意事項
for _k,_d in DETAILS.items():
    if _d.get('image'): PRODUCTS[_k]['image']=_d['image']
    if _d.get('yes'): PRODUCTS[_k]['yes']=_d['yes']
    if _d.get('caution'): PRODUCTS[_k]['caution']=_d['caution']
    if _d.get('faq'): PRODUCTS[_k]['faq']=_d['faq']

def stats_row(slug):
    st=DETAILS.get(slug,{}).get('stats')
    if not st: return ''
    return '<ul class="pstats">'+''.join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a,b in st)+'</ul>'
def zebra(html):
    # 產品頁中段區塊依出現順序白／米色交替，不受個別區塊有無影響
    n=[0]
    def f(m):
        n[0]+=1; return '<section class="sec'+('' if n[0]%2 else ' bg-cream')+'"'
    return re.sub(r'<section class="sec(?: bg-cream| bg-green-light)?"',f,html)
def showcase_section(slug):
    sc=DETAILS.get(slug,{}).get('showcase')
    if not sc: return ''
    bl=''.join(f'<li>{esc(x)}</li>' for x in sc.get('bullets',[]))
    return f'''<section class="sec"><div class="wrap showcase">
  <div class="showcase-pic"><img src="{sc['img']}" alt="{esc(PRODUCTS[slug]['name'])}" loading="lazy"></div>
  <div><span class="eyebrow">{esc(sc.get('eyebrow','產品介紹'))}</span><h2>{esc(sc['title'])}</h2><p class="lead" style="font-size:16px">{esc(sc.get('text',''))}</p>{f'<ul class="showcase-list">{bl}</ul>' if bl else ''}</div>
</div></section>
'''
def pillars_section(slug):
    pl=DETAILS.get(slug,{}).get('pillars')
    if not pl: return ''
    items=''.join(f'<li><b>{esc(t)}</b><span>{esc(x)}</span></li>' for t,x in pl['items'])
    return f'''<section class="sec bg-cream"><div class="wrap pillars">
  <div class="pillars-pic"><img src="{pl['img']}" alt="{esc(PRODUCTS[slug]['name'])}" loading="lazy"></div>
  <div><span class="eyebrow">{esc(pl.get('eyebrow','養護什麼'))}</span><h2>{esc(pl['title'])}</h2><p class="lead" style="font-size:16px">{esc(pl.get('intro',''))}</p><ol class="pillars-list">{items}</ol></div>
</div></section>
'''
def how_section(slug):
    d=DETAILS.get(slug,{}); hw=d.get('how')
    if not hw: return ''
    eb,h2=d.get('how_title',('使用方式','每天這樣用'))
    steps=''.join(f'<li><span class="how-k">{i+1}</span><b>{esc(t)}</b><span>{esc(x)}</span></li>' for i,(t,x) in enumerate(hw))
    return f'''<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{esc(eb)}</span><h2>{esc(h2)}</h2></div>
  <ol class="how">{steps}</ol>
</div></section>
'''
def compare_section(slug):
    c=DETAILS.get(slug,{}).get('compare')
    if not c: return ''
    hl=c.get('hl', len(c['cols'])-1)  # 要標示（綠底）的欄位，預設最後一欄
    cls=lambda i: ' class="hl"' if i==hl else ''
    head='<tr><th></th>'+''.join(f'<th{cls(i)}>{esc(x)}</th>' for i,x in enumerate(c['cols']))+'</tr>'
    rows=''.join('<tr><th>'+esc(r[0])+'</th>'+''.join(f'<td{cls(i)}>{esc(v)}</td>' for i,v in enumerate(r[1:]))+'</tr>' for r in c['rows'])
    intro=f'<p class="lead" style="font-size:16px">{esc(c["intro"])}</p>' if c.get('intro') else ''
    note=f'<p class="note" style="margin-top:12px">{esc(c["note"])}</p>' if c.get('note') else ''
    return f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">比較</span><h2>{esc(c['title'])}</h2>{intro}</div>
  <div class="cmp-wrap"><table class="cmp"><thead>{head}</thead><tbody>{rows}</tbody></table></div>
  {note}
</div></section>
'''

def og_png(url):
    # 社群分享預覽不支援 AVIF：把 uhealthfit.com 的 _optimized/...-1200.avif 換回原始 PNG
    m=re.match(r'(https://uhealthfit\.com)/_optimized/(.+)-\d+\.avif$', url)
    return f'{m.group(1)}/{m.group(2)}.png' if m else url

def head(title, desc, rel, canonical_path, page_id, og_image=None, extra=''):
    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{TRACKING_HEAD_TOP}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{page_url(canonical_path)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_png(og_image) if og_image else IMG + '/home/all-products-lineup.png'}">
<meta property="og:locale" content="zh_TW">
<link rel="icon" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}css/style.css?v={CSS_VER}">
{extra}
{TRACKING_HEAD_END}
</head>
<body data-page="{page_id}">
{TRACKING_BODY_TOP}
'''

def series_products(k):
    # 系列內的產品（含組合），供導覽列與全部產品頁使用
    s=SERIES[k]; return s['products']+([s['bundle']] if s.get('bundle') else [])

def nav(rel, active=''):
    dd = ''.join(f'<a class="s-{k}" href="{rel}series/{k}.html"><span class="dot"></span><span>{SERIES[k]["name"]}<small>{SERIES[k]["h1"]}</small></span></a>' for k in SERIES_ORDER)
    dd += f'<a class="dd-all" href="{rel}series/index.html">看六大系列匯總 →</a>'
    mob_sub = ''.join(f'<a href="{rel}series/{k}.html">{SERIES[k]["name"]}</a>' for k in SERIES_ORDER)
    pname = lambda p: PRODUCTS[p]['name'].split('（')[0].replace('WiseQuest ','')  # 組合名去掉括號內的品項，選單才不換行
    dd_prod = ''.join(f'<div class="dd-col s-{k}"><a class="dd-h" href="{rel}series/{k}.html"><span class="dot"></span>{SERIES[k]["name"]}</a>'
                      +''.join(f'<a href="{rel}products/{p}.html">{esc(pname(p))}</a>' for p in series_products(k))+'</div>' for k in SERIES_ORDER)
    dd_prod += f'<a class="dd-all" href="{rel}products/index.html">瀏覽全部 {len(PRODUCT_ORDER)} 款產品 →</a>'
    mob_prod = ''.join(f'<span class="sub-h">{SERIES[k]["name"]}</span>'+''.join(f'<a href="{rel}products/{p}.html">{esc(pname(p))}</a>' for p in series_products(k)) for k in SERIES_ORDER)
    def a(href,label,key):
        cls = ' class="active"' if active==key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<div class="topbar">美國地區：眼貼滿 <b>USD $79</b>、其他商品滿 <b>USD $200</b> 免運 · 30 天內未拆封可退 · 官方商店安全結帳</div>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{rel}index.html" aria-label="優健堂 UHealthFit 首頁"><img src="{LOGO}" alt="優健堂 UHealthFit" width="101" height="34"></a>
    <nav aria-label="主選單"><ul class="nav-links">
      <li>{a(rel+'index.html','主頁','home')}</li>
      <li>{a(rel+'series/index.html','六大系列','series')}<div class="dd">{dd}</div></li>
      <li>{a(rel+'products/index.html','全部產品','products')}<div class="dd dd-prod">{dd_prod}</div></li>
      <li>{a(rel+'blog/index.html','選購指南','blog')}</li>
      <li>{a(rel+'quiz.html','30 秒測驗','quiz')}</li>
      <li>{a(rel+'about-us.html','關於我們','aboutus')}</li>
      <li>{a(rel+'about.html','黃醫師','about')}</li>
      <li>{a(rel+'faq.html','常見問題','faq')}</li>
    </ul></nav>
    <div class="nav-cta"><a class="btn btn-primary btn-sm" href="{rel}series/index.html">選購系列</a><button class="menu-btn" aria-label="開啟選單" aria-expanded="false"><span></span></button></div>
  </div>
  <div class="mobile-menu"><div class="wrap">
    <a href="{rel}index.html">主頁</a>
    <a href="{rel}series/index.html">六大系列</a><div class="sub">{mob_sub}</div>
    <details class="mm-dd"><summary>全部產品</summary><div class="sub">{mob_prod}<a class="sub-all" href="{rel}products/index.html">瀏覽全部產品 →</a></div></details>
    <a href="{rel}blog/index.html">選購指南</a><a href="{rel}quiz.html">30 秒測驗</a><a href="{rel}about-us.html">關於我們</a><a href="{rel}about.html">黃醫師</a><a href="{rel}faq.html">常見問題</a>
  </div></div>
</header>
<main>
'''

def journey(rel, stage, series_key=None, post=None, product=None):
    """客戶旅程「下一步」模組。stage: home / series / product / blog / quiz / about"""
    cards = []
    if stage in ('home','about','faq'):
        cards.append(('STEP 1','還不確定從哪裡開始？','6 題、30 秒，找到最值得先照顧的那一件事，並對應到系列與選購指南。',f'{rel}quiz.html','開始 30 秒測驗'))
        cards.append(('STEP 2','先讀一篇選購指南','我們把每個系列「怎麼選」寫成指南——就算不買，也能更懂自己的身體。',f'{rel}blog/index.html','看選購指南'))
    elif stage=='series' and series_key:
        posts=[p for p in POSTS if p['series']==series_key]
        cards.append(('讀一讀','這個系列怎麼選',posts[0]['excerpt'],f'{rel}blog/{posts[0]["slug"]}.html','閱讀指南'))
        cards.append(('不確定？','30 秒找到起點','如果你同時在意好幾件事，先做測驗，我們幫你排序。',f'{rel}quiz.html','開始測驗'))
    elif stage=='blog' and post:
        p=PRODUCTS[post['primary_product']]
        cards.append(('下一步','看對應產品',p['hook']+'——'+p['desc'][:40]+'…',f'{rel}products/{post["primary_product"]}.html','查看產品'))
        cards.append(('或是','30 秒測驗','不只在意這一件事？先做測驗，找到最值得先開始的系列。',f'{rel}quiz.html','開始測驗'))
    elif stage=='product' and product:
        sk=PRODUCTS[product]['series']; posts=[p for p in POSTS if p['series']==sk]
        cards.append(('延伸閱讀',posts[0]['title'][:22]+('…' if len(posts[0]['title'])>22 else ''),posts[0]['excerpt'],f'{rel}blog/{posts[0]["slug"]}.html','閱讀指南'))
        cards.append(('看整個系列',SERIES[sk]['name'],SERIES[sk]['lead'][:48]+'…',f'{rel}series/{sk}.html','前往系列頁'))
    elif stage=='quiz':
        cards.append(('不想測？','直接看六大系列','從最在意的那一件事開始，每個系列都可以單獨開始。',f'{rel}series/index.html','看六大系列'))
        cards.append(('先讀一篇','選購指南','每個系列的「怎麼選」都寫成了指南。',f'{rel}blog/index.html','看選購指南'))
    html_cards=''.join(f'<div class="jcard"><div class="k">{k}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="btn btn-ghost btn-sm" href="{h}">{b}</a></div>' for k,t,d,h,b in cards)
    return f'''<section class="sec-tight journey"><div class="wrap">
  <div class="lead-box"><span class="eyebrow">你的下一步</span><h2>開始，比完美更重要</h2><p class="lead" style="font-size:16px">養護是累積出來的。從一件小事開始，剩下的我們陪你慢慢來。</p></div>
  {html_cards}
</div></section>
'''

def disclaimer():
    return '''<section class="disclaimer" aria-label="免責聲明"><div class="wrap">
<p><b>免責聲明：</b>本站所述膠囊類產品為膳食補充劑，乳霜、精華液與眼貼為日常保養用品，皆非藥品。相關敘述未經美國食品藥物管理局（FDA）評估；本產品不用於診斷、治療、治癒或預防任何疾病。「生產設施具 FDA 登記」指設施登記資訊，不代表 FDA 核准或背書任何產品。</p>
<p>These statements have not been evaluated by the Food and Drug Administration. These products are not intended to diagnose, treat, cure, or prevent any disease.</p>
<p>本站資訊僅供參考，不可取代醫師或其他專業醫療人員的建議；請勿依據本站內容自行診斷或處理任何健康問題。若有或疑似有任何健康問題，請諮詢你的醫療照護人員。使用者分享與買家評價皆為個人經驗，效果因人而異。孕婦、哺乳期、18 歲以下、服藥中或有慢性健康狀況者，使用前請先諮詢醫師。中醫相關敘述為傳統觀點的說明，非醫療診斷。部分情境圖片可能為示意圖；實際包裝可能與圖片略有差異。所有購買於 zh.uhealthfit.com 完成，價格以結帳頁顯示為準。</p>
</div></section>
'''

def footer(rel):
    series_links=''.join(f'<li><a href="{rel}series/{k}.html">{SERIES[k]["name"]}</a></li>' for k in SERIES_ORDER)
    pays=''.join(f'<img src="{IMG}/payment/{p}.svg" alt="{p}">' for p in ['visa','mastercard','american-express','discover','apple-pay','google-pay','shop-pay'])
    return f'''</main>
{disclaimer()}
<footer class="site"><div class="wrap">
  <div><img class="logo" src="{rel}{LOGO_WHITE}" alt="UHealthFit" width="146" height="26"><p>融合傳統智慧與現代科學的健康養護平台。</p><p style="margin-top:10px">Uhealth Trading Inc.<br>90 North St, Suite D, Middletown, NY 10940, USA<br><a href="mailto:service@uhealthfit.com">service@uhealthfit.com</a></p><div class="pay">{pays}</div></div>
  <div><h4>六大系列</h4><ul>{series_links}</ul></div>
  <div><h4>探索</h4><ul><li><a href="{rel}blog/index.html">選購指南</a></li><li><a href="{rel}quiz.html">30 秒測驗</a></li><li><a href="{rel}about-us.html">關於我們</a></li><li><a href="{rel}about.html">研發者・黃醫師</a></li><li><a href="{rel}faq.html">常見問題</a></li><li><a href="{rel}products/eye-care-trio.html">護眼三寶</a></li></ul></div>
  <div><h4>購買與客服</h4><ul><li><a class="ext" href="{SHOP}">前往 zh.uhealthfit.com 商店</a></li><li><a class="ext" href="{SHOP}/policies/shipping-policy">運送說明</a></li><li><a class="ext" href="{SHOP}/policies/refund-policy">退貨政策</a></li><li><a class="ext" href="{SHOP}/policies/privacy-policy">隱私權政策</a></li><li><a class="ext" href="{SHOP}/policies/terms-of-service">服務條款</a></li></ul></div>
  <div class="copy">© 2026 Uhealth Trading Inc. 版權所有。本站為 WiseQuest 系列的介紹網站，購買於 zh.uhealthfit.com 完成。</div>
</div></footer>
<script src="{rel}js/main.js?v={JS_VER}" defer></script>
</body></html>
'''

def sticky(rel):
    return f'<div class="sticky-cta" aria-label="快速行動"><a class="btn btn-ghost" href="{rel}quiz.html">30 秒測驗</a><a class="btn btn-primary" href="{rel}series/index.html">選購系列</a></div>'

def product_card(slug, rel, wide=False, promo=False):
    p=PRODUCTS[slug]
    img=(DETAILS.get(slug,{}).get('promo_image') if promo else None) or p['image']
    badge=f'<span class="badge {p["badge"][0]}">{p["badge"][1]}</span>' if p.get('badge') else ''
    pr = price_str(p); note=p['price_note']
    return f'''<article class="prod{' wide' if wide else ''}">
  <a class="pic" href="{rel}products/{slug}.html">{badge}<img src="{img}" alt="{esc(p['name'])}" loading="lazy"></a>
  <div class="body">
    <div class="name"><a href="{rel}products/{slug}.html">{esc(p['name'])}</a><small>{esc(p['en'])} · {esc(p['made'])}</small></div>
    <div class="hook">{esc(p['hook'])}</div>
    <p class="desc">{esc(p['desc'])}</p>
    <p class="herbs"><b>主要成分：</b>{esc(p['herbs'])}</p>
    <div class="foot"><div class="price">{pr}<small>{esc(note)}</small></div><div style="display:flex;gap:8px"><a class="btn btn-ghost btn-sm" href="{rel}products/{slug}.html">了解</a><a class="btn btn-primary btn-sm ext" data-product="{slug}" href="{buy_url(p,slug)}">購買</a></div></div>
  </div>
</article>'''


# ───── 選購指南縮圖：參考 zh.uhealthfit.com 博客文章配圖（2026-10-22 挑選），每篇一張、不重複 ─────
# 未採用疾病聯想太強的畫面（看診、抓癢、馬桶等）；找不到合適的才用商品或品牌情境圖。
def _blog_img(path, width=900): return f'{SHOP_CDN}/articles/{path}&width={width}'
POST_IMAGES = {
 'eye-patch-vs-steam-mask-vs-eye-drops': _blog_img('6e79cd1e0b94426229c58cc80bb26721_b8d47d89-ece5-4fcb-93c1-02afc98f393b.jpg?v=1784110970'),
 'beyond-lutein-eye-care':               _blog_img('c9dac13fffc18fd3e639d59e46699f14_17d6bb59-7edc-4ac0-b61e-988c0d3affaf.jpg?v=1784729594'),
 'eye-patch-how-to-use-guide':           _blog_img('3C.webp?v=1784445802'),
 'eye-care-gift-for-parents':            f'{IMG}/_optimized/concerns/eye-care-1200.avif',
 'eye-patch-ingredients-explained':      shop_img('files/XXT36536.jpg?v=1781960015', 900),
 'melatonin-free-sleep-aid-guide':       _blog_img('0061e896aaa054d2a26531e15f4665f1_26556a12-6c00-445d-9748-6e292f9c592b.jpg?v=1784729443'),
 'stress-daytime-relax-night-sleep':     _blog_img('Uhealth_3_04ff309d-c7e1-4ba4-a9c8-c2569c80fabd.jpg?v=1788305863'),
 'gentle-digestive-support-no-senna':    shop_img('files/26ffef70cacb47ecb0b0b1e2fc667031_3eb53544-8644-47c2-85e1-519efa90b88c.jpg?v=1782815981', 900),
 'bloating-after-sitting-herbal-flow':   _blog_img('4b833d8ed2df5069e87f5e67ab4884f8_aefba7d6-6c86-43f1-bd05-37e3c8d97b95.jpg?v=1784730659'),
 'gum-care-supplement-for-parents':      _blog_img('Uhealth_1_4a866430-080b-436c-9675-5b00208bb3f5.jpg?v=1787836791'),
 'brushing-plus-herbal-support':         _blog_img('Uhealth_3_7a272e3f-62f2-47fc-bb99-68481a91a46a.jpg?v=1790149469'),
 'steroid-free-soothing-cream-guide':    _blog_img('75d0c6b723e108b98dba5d9e3a358a41.webp?v=1784443184'),
 'acne-prone-skin-herbal-cream-guide':   _blog_img('6b8903ce6bbb733467feb660618b47d6.jpg?v=1784124384'),
 'anti-fatigue-look-serum-guide':        shop_img('collections/4_0cd12e86-74cf-4588-b39b-7b5c570db219.jpg?v=1776886625', 900),
 'caffeine-free-energy-herbal-guide':    'https://cdn.shopify.com/s/files/1/0676/4675/0818/files/db7afe76-0eda-4a8e-b8ae-e7633ec3ae0e.jpg?v=1786712333&width=900',  # zh 黑膏滋介紹頁：日常隨餐的情境照
 'winter-tonic-herbal-guide':            _blog_img('1fe980194242617ee83bf7d924b9915f_31870d96-4aef-4f95-905c-ab096322e3d2.png?v=1790143942'),
 'gaozi-paste-vs-capsule':               'https://cdn.shopify.com/s/files/1/0676/4675/0818/files/c4001f0d-6d94-4413-9958-8a31fc2e4367.jpg?v=1786711467&width=900',  # zh 黑膏滋介紹頁主圖：膠囊瓶與草本切片
 'american-ginseng-vs-ginseng':          f'{IMG}/blog/botanical-wellness-hero.png',
}
def post_image(p):
    if p['slug'] in POST_IMAGES: return POST_IMAGES[p['slug']]
    return SERIES[p['series']]['photo']

def post_card(p, rel):
    prod=PRODUCTS[p['primary_product']]; s=SERIES[p['series']]
    thumb = post_image(p)
    return f'''<article class="post-card s-{p['series']}" data-series="{p['series']}">
  <a class="thumb" href="{rel}blog/{p['slug']}.html"><img src="{thumb}" alt="" loading="lazy"></a>
  <div class="body"><div class="meta"><span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']}</span><span>· 約 {p['reading_min']} 分鐘</span></div>
  <h3><a href="{rel}blog/{p['slug']}.html">{esc(p['title'])}</a></h3><p>{esc(p['excerpt'])}</p>
  <a class="go" style="color:var(--green);font-weight:700;font-size:14px" href="{rel}blog/{p['slug']}.html">閱讀指南 →</a></div>
</article>'''

def faq_block(items):
    return ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in items)

def faq_ld(items):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]},ensure_ascii=False)

def externalize(content):
    # 所有連到 zh.uhealthfit.com 的連結另開新分頁，讓使用者能回到本站
    def fix(m):
        tag=m.group(0)
        if 'target=' in tag: return tag
        return tag[:-1]+' target="_blank" rel="noopener">'
    return re.sub(r'<a\s[^>]*href="https://zh\.uhealthfit\.com[^"]*"[^>]*>', fix, content)

def write(path, content):
    full=os.path.join(DIST,path); os.makedirs(os.path.dirname(full),exist_ok=True)
    if path.endswith('.html'): content=externalize(content)
    open(full,'w',encoding='utf8').write(content)

# ───────────────────────────── 首頁 ─────────────────────────────
def gallery(slug):
    # 產品頁主圖；有特價圖時特價圖為第一張、原主圖為第二張，以輪播呈現
    p=PRODUCTS[slug]; d=DETAILS.get(slug,{})
    imgs=[x for x in [d.get('promo_image'), p['image']] if x]
    cls='gallery'+(' contain' if d.get('gallery_contain') else '')
    if len(imgs)==1:
        return f'<div class="{cls}"><img src="{imgs[0]}" alt="{esc(p["name"])}" width="800" height="800" fetchpriority="high"></div>'
    slides=''.join(f'<div class="gslide"><img src="{u}" alt="{esc(p["name"])}" width="800" height="800"'+(' fetchpriority="high"' if i==0 else ' loading="lazy"')+'></div>' for i,u in enumerate(imgs))
    dots=''.join(f'<button type="button" aria-label="第 {i+1} 張"'+(' aria-current="true"' if i==0 else '')+'></button>' for i in range(len(imgs)))
    return f'<div class="{cls} slides"><div class="slides-track">{slides}</div><button class="slides-prev" type="button" aria-label="上一張">‹</button><button class="slides-next" type="button" aria-label="下一張">›</button><div class="slides-dots">{dots}</div></div>'

def series_card(k, rel):
    # 系列卡片（首頁與六大系列匯總頁共用）
    return f'''<a class="scard s-{k}" href="{rel}series/{k}.html"><div class="scard-pic"><img src="{SERIES[k]['photo']}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{SERIES[k]['en']}</span><h3>{SERIES[k]['name']}</h3><div class="hook">{SERIES[k]['h1']}</div><p>{esc(SERIES[k]['lead'][:60])}…</p><div class="items">{'・'.join(PRODUCTS[s]['name'].replace('WiseQuest ','') for s in SERIES[k]['products'])}</div><span class="go">看系列 →</span></a>'''

def build_home():
    rel=''
    series_cards=''.join(series_card(k,rel) for k in SERIES_ORDER)
    posts=''.join(post_card(p,rel) for p in [POST_BY_SLUG[s] for s in ['eye-patch-vs-steam-mask-vs-eye-drops','melatonin-free-sleep-aid-guide','gum-care-supplement-for-parents']])
    featured=''.join(product_card(s,rel) for s in ['eye-patches','calmoon','dentaforte'])
    body=f'''
<section class="hero"><div class="wrap">
  <div><span class="eyebrow">優健堂 UHealthFit × WiseQuest · 醫師研發草本保健</span>
    <h1>不壓制、不依賴，<br><em>從根源支持身體</em></h1>
    <p class="lead">護眼、固齒、舒眠、順暢、肌膚、活力——六大日常養護系列，由中國中西醫結合執業醫師黃醫師研發。傳統草本配方、現代萃取工藝，美國・日本製造，成分全部公開。</p>
    <div class="hero-cta"><a class="btn btn-primary" href="quiz.html">30 秒找到我的起點</a><a class="btn btn-ghost" href="series/index.html">直接看六大系列</a></div>
    <ul class="hero-trust"><li>無添加 · 非轉基因</li><li>第三方純度檢測</li><li>全植物膠囊 · 全素</li></ul>
  </div>
  <div class="hero-visual cutout"><picture><source type="image/avif" srcset="{IMG}/_optimized/all-products-product-shot-wide-800.avif 800w, {IMG}/_optimized/all-products-product-shot-wide-1200.avif 1200w, {IMG}/_optimized/all-products-product-shot-wide-1448.avif 1448w" sizes="(max-width:900px) 100vw, 600px"><source type="image/webp" srcset="{IMG}/_optimized/all-products-product-shot-wide-800.webp 800w, {IMG}/_optimized/all-products-product-shot-wide-1200.webp 1200w, {IMG}/_optimized/all-products-product-shot-wide-1448.webp 1448w" sizes="(max-width:900px) 100vw, 600px"><img src="{IMG}/all-products-product-shot-wide.png" alt="WiseQuest 全系列產品，膠囊瓶、乳霜罐、精華液與眼貼盒" width="1448" height="1086" fetchpriority="high"></picture></div>
</div></section>
<section class="trustbar" aria-label="品質保證"><div class="wrap"><ul>
  <li>美國・日本製造<small>cGMP 規範生產</small></li><li>第三方純度檢測<small>成品送驗</small></li><li>成分全部公開<small>每一味都查得到</small></li><li>無添加 · 非轉基因<small>無人工色素、防腐劑</small></li><li>執業醫師研發<small>二十年臨床經驗</small></li><li>30 天未拆封可退<small>service@uhealthfit.com</small></li>
</ul></div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">六大系列 · 11 款產品</span><h2>從最在意的那一件事開始</h2><p class="lead">每個系列都可以單獨開始，也可以彼此搭配。點進系列頁，看怎麼選、怎麼用、怎麼開始。</p></div>
  <div class="grid-3">{series_cards}</div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">為什麼是草本日常養護</span><h2>現代生活，常常把身體排在最後</h2><p class="lead">一天盯螢幕十個小時、晚睡、外食、壓力停不下來——身體會用各種小訊號提醒我們。即時舒緩很重要；但長期的日常養護，是另一件值得開始的事。</p></div>
  <div class="grid-3">
    <div class="card white"><div class="num">01</div><h3>訊號，不只是訊號</h3><p>長時間用眼後的乾澀疲勞感、換季時容易敏感的肌膚、難以放鬆的夜晚、久坐後的腹脹——它們往往是生活型態累積出來的結果。</p></div>
    <div class="card white"><div class="num">02</div><h3>舒緩當下，也要照顧長期</h3><p>市面上多數方案專注於「這一刻舒服一點」。我們尊重這些選擇，也認為日常養護值得有自己的位置。</p></div>
    <div class="card white"><div class="num">03</div><h3>一套邏輯，六個系列</h3><p>以中醫的整體觀看待身體，用傳統使用數百年的草本、搭配現代萃取與品質檢測，把「日常養護」做成每天做得到的小習慣。</p></div>
  </div>
  <div class="pull">「身體一直在努力照顧你。現在，換我們照顧它。」<small>WiseQuest 品牌理念 · 草本是支持，不是取代身體；我們尊重現代醫學，也珍惜傳統草本智慧。</small></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見的起點</span><h2>三個常見的起點</h2></div>
  <div class="pgrid">{featured}</div>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">選購指南</span><h2>先懂怎麼選，再決定要不要買</h2><p class="lead">我們把每個系列「市面上有哪些選項、各自負責什麼、選購時該看什麼」寫成指南。就算最後沒有購買，也希望你更懂自己的身體。</p></div>
  <div class="bgrid">{posts}</div>
  <p style="margin-top:22px"><a class="btn btn-ghost" href="blog/index.html">看全部 {len(POSTS)} 篇選購指南</a></p>
</div></section>

<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{IMG}/home/dr-h.png" alt="黃醫師 Dr. Huang，中國中西醫結合執業醫師" loading="lazy"></div>
  <div><span class="eyebrow">研發者 · 黃醫師 Dr. Huang</span><h2>由一位看了二十年「整個人」的醫師研發</h2>
  <p>黃醫師是中國中西醫結合執業醫師、中醫全科醫師，擁有二十年臨床經驗與草本配方研發專長。她師從多位國家級名老中醫、各科教授與清末御醫傳人；臨床涉及內科、皮膚科、婦科、兒科，並專研中醫美容二十年，自主研發的中藥化妝品曾獲國家發明專利。</p>
  <blockquote>「很多時候讓症狀暫時消失，不等於身體真的恢復。我想做的，是幫身體重新找回自己健康的狀態——用承傳千年的草本經驗，幫助身體恢復平衡。」<footer>— 黃醫師 · WiseQuest 配方研發者</footer></blockquote>
  <a class="btn btn-light" href="about.html">認識黃醫師與品牌理念</a></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">購買流程</span><h2>在這裡了解，到官方商店安全結帳</h2><p class="lead">本站專注於幫你「選對」；按下購買後會前往我們的官方商店 zh.uhealthfit.com 完成結帳。整個流程三步：</p></div>
  <div class="steps">
    <div class="step"><div class="k">1</div><h3>在本站選好產品與規格</h3><p>看系列頁、單品頁與選購指南，確定適合自己的起點與用量。</p><div class="why">不確定？做 30 秒測驗。</div></div>
    <div class="step"><div class="k">2</div><h3>前往商店安全結帳</h3><p>按「購買」會開啟 zh.uhealthfit.com 商品頁；支援 Visa、Mastercard、Apple Pay、Google Pay、PayPal、Shop Pay 等。</p><div class="why">美國眼貼滿 $79、其他商品滿 $200 免運。</div></div>
    <div class="step"><div class="k">3</div><h3>48 小時內出貨</h3><p>工作日 48 小時內處理並寄出出貨通知；30 天內未拆封可退。</p><div class="why">有問題隨時來信 service@uhealthfit.com。</div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="offer-box">
  <div class="l"><span class="eyebrow">最低門檻的開始</span><h2>先試兩個晚上，再決定要不要走下去</h2><p>護眼系列的入口，是一包兩晚份的明目冷敷眼貼體驗裝——日本製造、不含防腐劑，剛好夠你感受它適不適合自己的睡前習慣。</p>
    <div class="big">$6<small> / 兩晚體驗裝</small></div>
    <ul><li>日本製造 · 不入眼 · 不含防腐劑 · 過敏回報極少（依品牌內部客服紀錄）</li><li>喜歡再升級：1 盒 $29.99 · 3 盒一個月組 $84（推薦入門）</li><li>所有商品 30 天內未拆封可退</li></ul>
    <a class="btn btn-accent ext" data-product="eye-patches-trial" href="{shop_url(PRODUCTS['eye-patches']['trial_handle'])}">以 $6 體驗兩晚</a></div>
  <div class="r"><img src="{shop_img('files/free-trial-package.jpg?v=1758563648',700)}" alt="WiseQuest 明目冷敷眼貼兩晚體驗裝" loading="lazy"></div>
</div></div></section>
{journey(rel,'home')}
{sticky(rel)}
'''
    write('index.html', head('優健堂 UHealthFit × WiseQuest｜醫師研發草本保健 · 護眼・肌膚・固齒・元氣・睡眠・腸胃','由中國中西醫結合執業醫師黃醫師研發的 WiseQuest 草本保健系列：明目冷敷眼貼、草本明目膠囊、固齒膠囊、安睡膠囊、潤暢膠囊、舒緩修護霜等。美國・日本製造，成分全部公開，$6 試用裝起。',rel,'index.html','home')+nav(rel,'home')+body+footer(rel))

# ───────────────────────────── 系列頁 ─────────────────────────────
def build_series():
    for k in SERIES_ORDER:
        s=SERIES[k]; rel='../'
        cards=''.join(product_card(p,rel,wide=(len(s['products'])==1)) for p in s['products'])
        bundle=''
        if s.get('bundle'):
            b=PRODUCTS[s['bundle']]
            bundle=f'''<div class="pull" style="margin-top:24px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:center"><div>{esc(s['combo'][0])}：{esc(s['combo'][1])}</div><a class="btn btn-primary btn-sm" href="{rel}products/{s['bundle']}.html">看護眼三寶組合</a></div>'''
        else:
            bundle=f'''<div class="pull" style="margin-top:24px">{esc(s['combo'][0])}<small style="font-size:15px;color:var(--ink)">{esc(s['combo'][1])}</small></div>'''
        posts=''.join(post_card(p,rel) for p in POSTS if p['series']==k)
        reframe=''.join(f'<div class="card white"><div class="num">0{i+1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i,(t,d) in enumerate(s['reframe']))
        sits=''.join(f'<li>{esc(x)}</li>' for x in s['situations'])
        others=''.join(f'<a class="scard s-{o}" href="{rel}series/{o}.html"><div class="scard-pic"><img src="{SERIES[o]["photo"]}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{SERIES[o]["en"]}</span><h3>{SERIES[o]["name"]}</h3><div class="hook">{SERIES[o]["h1"]}</div><span class="go">看系列 →</span></a>' for o in SERIES_ORDER if o!=k)
        body=f'''
{series_hero(k,rel)}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">如果你也是這樣</span><h2>這個系列為誰而做</h2></div>
  <div class="grid-2" style="align-items:start">
    <ul class="hero-trust" style="display:grid;gap:12px;margin:0;font-size:16px">{sits}</ul>
    <div class="timeline" style="margin:0"><div class="ic">⏱</div><div><b>關於時間，我們寧願第一天就說清楚：</b>多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異；把它當作一個生活習慣來持續。</div></div>
  </div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">我們的思路</span><h2>先理解，再選擇</h2></div>
  <div class="grid-3">{reframe}</div>
</div></section>

<section class="sec" id="products"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{s['name']} · 產品</span><h2>怎麼選、怎麼用</h2><p class="lead">價格為美金（USD），點「購買」前往官方商店安全結帳；點「了解」看完整成分、用法與常見問題。</p></div>
  <div class="pgrid{' pgrid-1' if len(s['products'])==1 else ''}">{cards}</div>
  {bundle}
  <p class="note" style="margin-top:18px;text-align:center">膠囊類為膳食補充劑、外用品為日常保養品，皆非藥品，不用於診斷、治療、治癒或預防任何疾病。效果因人而異。</p>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">選購指南</span><h2>關於{s['short']}，先讀這幾篇</h2></div>
  <div class="bgrid">{posts}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見問題</span><h2>關於{s['name']}</h2></div>
  <div class="faq-list">{faq_block(s['faq'])}</div>
</div></section>
{journey(rel,'series',series_key=k)}
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">其他系列</span><h2>同一套邏輯，六個系列</h2></div><div class="grid-3">{others}</div></div></section>
{sticky(rel)}
<script type="application/ld+json">{faq_ld(s['faq'])}</script>
'''
        write(f'series/{k}.html', head(f'{s["name"]}｜{s["h1"]} · 優健堂 UHealthFit × WiseQuest', s['lead'][:150], rel, f'series/{k}.html', f'series-{k}', og_image=s['photo'])+nav(rel,'series')+body+footer(rel))

# ───────────────────────────── 單品頁 ─────────────────────────────
def build_products():
    for slug in PRODUCT_ORDER:
        p=PRODUCTS[slug]; s=SERIES[p['series']]; rel='../'
        url=buy_url(p,slug)
        variants=''
        if p.get('variants'):
            variants='<ul class="variants">'+''.join(f'<li class="{"best" if best else ""}"><span>{esc(n)}{(" <span class=tag>· "+esc(t)+"</span>") if t else ""}</span><b>{pr}</b></li>' for n,pr,t,best in p['variants'])+'</ul><p class="note">規格於 zh.uhealthfit.com 商品頁選擇；價格以結帳頁顯示為準。</p>'
        trial=''
        if p.get('trial_handle'):
            trial=f'<a class="btn btn-ghost btn-block ext" style="margin-top:8px" data-product="{slug}-trial" href="{shop_url(p["trial_handle"])}">先從 $6 兩晚體驗裝開始</a>'
        oos='<p class="note" style="margin-top:10px;color:#B84F08"><b>目前補貨中。</b>商品頁會顯示最新庫存狀態；也可以先讀選購指南，或看同系列的其他產品。</p>' if p.get('oos') else ''
        buy_label='前往護眼三寶組合頁' if p.get('is_bundle') else ('查看補貨狀態' if p.get('oos') else '立即購買')
        cross=''.join(product_card(c,rel) for c in p['cross'])
        yes=''.join(f'<li>{esc(x)}</li>' for x in p['yes']); no=''.join(f'<li>{esc(x)}</li>' for x in p['no'])
        posts=[q for q in POSTS if q['series']==p['series']]
        pr=price_str(p, with_compare=True)
        ld=json.dumps({"@context":"https://schema.org","@type":"Product","name":p['name'],"image":p['image'],"description":p['desc'],"brand":{"@type":"Brand","name":"WiseQuest"},"url":page_url(f"products/{slug}.html"),"offers":{"@type":"Offer","priceCurrency":"USD","price":str(p['price']) if p['price'] else "0","availability":"https://schema.org/OutOfStock" if p.get('oos') else "https://schema.org/InStock","url":url}},ensure_ascii=False) if not p.get('is_bundle') else ''
        body=f'''
<section class="pdp"><div class="wrap">
  {gallery(slug)}
  <div>
    <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><a href="{rel}series/{p['series']}.html">{s['name']}</a><span>›</span><span>{esc(p['name'])}</span></div>
    <span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']}</span>
    <h1>{esc(p['name'])}</h1><div class="en">{esc(p['en'])} · {esc(p['made'])}</div>
    <div class="hook">{esc(p['hook'])}</div>
    {stats_row(slug)}
    <p class="desc">{esc(p['long'])}</p>
    <ul class="facts"><li>{esc(p['form'])}</li><li>{esc(p['spec'])}</li><li>成分全部公開 · 第三方純度檢測</li><li>30 天內未拆封可退</li></ul>
    <div class="buybox">
      <div class="row"><div class="price">{pr}<small>{esc(p['price_note'])} · USD</small></div>{'<span class="badge badge-oos">補貨中</span>' if p.get('oos') else ('<span class="badge badge-star">單次購買 · 無訂閱</span>' if not p.get('is_bundle') else '<span class="badge badge-star">招牌組合</span>')}</div>
      {variants}
      <a class="btn btn-primary btn-block ext" data-product="{slug}" href="{url}">{buy_label}</a>
      {trial}{oos}
      <ul class="micro"><li>安全結帳</li><li>美國 {'眼貼滿 $79' if p['series']=='eye' and not p.get('is_bundle') else '滿 $200'} 免運</li><li>48 小時內出貨</li><li>30 天未拆封可退</li></ul>
      <ol class="flow"><li><b>選規格</b>在商品頁選擇數量／組合</li><li><b>安全結帳</b>Visa・Apple Pay・PayPal・Shop Pay</li><li><b>收到貨</b>工作日 48 小時內出貨</li></ol>
    </div>
  </div>
</div></section>
<!--zebra-->{showcase_section(slug)}
{compare_section(slug)}
{pillars_section(slug)}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">適合誰</span><h2>這款適合你嗎？</h2></div>
  <div class="who"><div class="box yes"><h3>適合</h3><ul>{yes}</ul></div><div class="box no"><h3>不適合或請先諮詢醫師</h3><ul>{no}</ul></div></div>
</div></section>
{ingredients_section(slug)}
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">成分與用法</span><h2>你知道自己每天用的是什麼</h2></div>
  <div class="spec">
    <div class="box"><h3>成分</h3><ul><li><b>草本成分</b><span>{esc(p['herbs'])}</span></li><li><b>其他成分</b><span>{esc(p['actives'])}</span></li><li><b>製造</b><span>{esc(p['made'])}</span></li><li><b>劑型</b><span>{esc(p['form'])}</span></li></ul></div>
    <div class="box"><h3>用法與注意</h3><ul><li><b>建議用法</b><span>{esc(p['usage'])}</span></li><li><b>規格</b><span>{esc(p['spec'])}</span></li><li><b>注意事項</b><span>{esc(p['caution'])}</span></li></ul></div>
  </div>
  <div class="timeline"><div class="ic">⏱</div><div><b>誠實的期待：</b>多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異；若一開始沒有太多感覺，這是正常的。</div></div>
</div></section>
{how_section(slug)}{demo_section(slug)}
{reviews_section(slug)}<!--/zebra-->
<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見問題</span><h2>購買前，你可能想知道</h2></div>
  <div class="faq-list">{faq_block(p['faq'])}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">搭配推薦</span><h2>常一起選的產品</h2></div>
  <div class="pgrid">{cross}</div>
</div></section>
{journey(rel,'product',product=slug)}
<div class="buybar"><div class="wrap"><div class="t"><span class="price">{pr}</span><span>{esc(p['name'])} · {esc(p['price_note'])}</span></div><a class="btn btn-primary ext" data-product="{slug}" href="{url}">{'查看組合' if p.get('is_bundle') else ('查看補貨狀態' if p.get('oos') else '前往購買')}</a></div></div>
<script type="application/ld+json">{faq_ld(p['faq'])}</script>
{('<script type="application/ld+json">'+ld+'</script>') if ld else ''}
'''
        body=re.sub(r'<!--zebra-->(.*?)<!--/zebra-->',lambda m:zebra(m.group(1)),body,flags=re.S)
        write(f'products/{slug}.html', head(f'{p["name"]}｜{p["hook"]} · 優健堂 × WiseQuest', p['desc'], rel, f'products/{slug}.html', f'product-{slug}', og_image=p['image'])+nav(rel,'products')+body+footer(rel))

# ───────────────────────────── 部落格 ─────────────────────────────
def build_blog():
    rel='../'
    chips='<div class="chips"><button class="chip on" data-f="all">全部</button>'+''.join(f'<button class="chip" data-f="{k}">{SERIES[k]["short"]}</button>' for k in SERIES_ORDER)+'</div>'
    cards=''.join(post_card(p,rel) for p in POSTS)
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><span>選購指南</span></div>
  <span class="eyebrow">選購指南 · {len(POSTS)} 篇</span><h1>先懂怎麼選，再決定要不要買</h1>
  <p class="lead" style="max-width:760px">我們把每個系列「市面上有哪些選項、各自負責什麼、選購時該看什麼、怎麼開始」寫成指南。每篇都誠實交代時間與不適合的人。就算最後沒有購買，也希望你更懂自己的身體、少一點焦慮。</p>
</div></div></section>
<section class="sec"><div class="wrap">{chips}<div class="bgrid">{cards}</div></div></section>
{journey(rel,'quiz')}
{sticky(rel)}
'''
    write('blog/index.html', head('選購指南｜護眼、固齒、睡眠、消化、肌膚、活力怎麼選 · 優健堂 × WiseQuest',f'{len(POSTS)} 篇草本保健選購指南：眼貼 vs 蒸氣眼罩、無褪黑素助眠、不含番瀉葉腸道保健、無類固醇修護霜、幫爸媽選口腔保健品……先懂怎麼選，再決定要不要買。',rel,'blog/index.html','blog')+nav(rel,'blog')+body+footer(rel))
    for p in POSTS:
        prod=PRODUCTS[p['primary_product']]; s=SERIES[p['series']]
        related=''.join(post_card(q,rel) for q in POSTS if q['slug']!=p['slug'] and q['series']==p['series'])
        more=''.join(post_card(q,rel) for q in POSTS if q['series']!=p['series'])[:0]
        ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":p['title'],"description":p['description'],"image":post_image(p),"datePublished":TODAY,"author":{"@type":"Organization","name":"優健堂 UHealthFit"},"publisher":{"@type":"Organization","name":"優健堂 UHealthFit","logo":{"@type":"ImageObject","url":LOGO}}},ensure_ascii=False)
        body=f'''
<section class="sec" style="padding-top:clamp(28px,4vw,52px)"><div class="wrap">
  <div class="article-head">
    <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><a href="{rel}blog/index.html">選購指南</a><span>›</span><a href="{rel}series/{p['series']}.html">{s['name']}</a></div>
    <span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']} · 選購指南</span>
    <h1>{esc(p['title'])}</h1>
    <div class="meta"><span>優健堂編輯部 · 內容依黃醫師臨床觀點與品牌產品資料整理</span><span>約 {p['reading_min']} 分鐘</span><span>更新 {TODAY}</span></div>
  </div>
  <div class="article-layout">
    <article class="article">
      {p['body']}
      <div class="disc-inline"><b>免責聲明：</b>本文為一般性資訊與選購觀點，不構成醫療建議；文中產品為膳食補充劑或日常保養品，非藥品，不用於診斷、治療、治癒或預防任何疾病。中醫相關敘述為傳統觀點的說明。效果因人而異；孕婦、哺乳期、服藥中或有健康疑慮者請先諮詢醫師。</div>
    </article>
    <aside class="aside">
      <div class="pbox"><img src="{prod['image']}" alt="{esc(prod['name'])}"><b>{esc(prod['name'])}</b><div class="price">{price_str(prod)}</div><p>{esc(prod['hook'])}</p><a class="btn btn-primary btn-sm btn-block" href="{rel}products/{p['primary_product']}.html">看產品與成分</a><a class="btn btn-ghost btn-sm btn-block ext" style="margin-top:8px" data-product="{p['primary_product']}" href="{buy_url(prod,p['primary_product'])}">前往購買</a></div>
      <div class="tbox"><h4>這篇在講什麼</h4><ul><li>市面選項各自負責什麼</li><li>選購時看的 4 件事</li><li>WiseQuest 的對應做法</li><li>誠實的期待與何時該就醫</li></ul></div>
      <div class="tbox" style="background:var(--green-light)"><h4>不只在意這一件事？</h4><p style="font-size:14px;color:var(--ink-2);margin-bottom:10px">30 秒測驗幫你排序最值得先開始的系列。</p><a class="btn btn-ghost btn-sm btn-block" href="{rel}quiz.html">開始測驗</a></div>
    </aside>
  </div>
  <div class="related"><div class="sec-head"><span class="eyebrow">延伸閱讀</span><h2>同系列的另一篇</h2></div><div class="bgrid">{related}</div></div>
</div></section>
{journey(rel,'blog',post=p)}
{sticky(rel)}
<script type="application/ld+json">{ld}</script>
'''
        write(f'blog/{p["slug"]}.html', head(f'{p["title"]} · 優健堂 × WiseQuest', p['description'], rel, f'blog/{p["slug"]}.html', f'blog-{p["slug"]}', og_image=post_image(p))+nav(rel,'blog')+body+footer(rel))

# ───────────────────────────── 測驗 ─────────────────────────────
QUIZ = [
 ('先問一個最實際的：一天裡，你有多少時間盯著螢幕？',[('8 小時以上，眼睛到下午就很乾、很累',{'eye':3}),('4–8 小時，偶爾會覺得疲勞',{'eye':2,'vitality':1}),('不多，螢幕不是我的主要困擾',{})]),
 ('晚上躺下之後，通常是什麼狀態？',[('腦子還在跑，很難放鬆',{'sleep':3}),('睡得著，但早上醒來不覺得有休息到',{'sleep':2,'vitality':1}),('大致安穩',{})]),
 ('久坐一整天、或外食應酬之後，肚子的感覺是？',[('常常頂著一股氣、不太順',{'digestive':3}),('偶爾會脹，吃清淡一點就好',{'digestive':1}),('很少有感覺',{})]),
 ('最近照鏡子，最在意的是？',[('看起來很累、暗沉、沒精神',{'skin':2,'vitality':2}),('換季時容易敏感、乾燥脫皮，或容易長痘',{'skin':3}),('還好，沒有特別在意',{})]),
 ('關於牙齒與牙齦——',[('我或家中長輩想為牙齦長期健康多做一點',{'dental':3}),('有在認真刷牙，暫時沒想太多',{'dental':1}),('不是我現在的重點',{})]),
 ('如果只能先開始一件事，你希望它是？',[('不用改變生活、睡前就能做的',{'eye':2,'sleep':1}),('每天隨餐一次、養成習慣就好',{'dental':1,'digestive':1,'vitality':1}),('一罐放在家裡、全家都用得到的',{'skin':2}),('先讓自己白天有精神、晚上能放鬆',{'sleep':2,'vitality':2})]),
]
def build_quiz():
    rel=''
    EBOOKS_JSON=esc(json.dumps({k:{'title':v['title'],'url':f"{SITE_URL}/{v['file']}"} for k,v in EBOOKS.items()},ensure_ascii=False))
    steps=''
    for i,(q,opts) in enumerate(QUIZ):
        btns=''.join(f'<button type="button" data-w=\'{json.dumps(w,ensure_ascii=False)}\'><span class="l">{"ABCD"[j]}</span><span>{esc(t)}</span></button>' for j,(t,w) in enumerate(opts))
        steps+=f'<div class="qstep{" on" if i==0 else ""}"><span class="eyebrow">第 {i+1} 題 / {len(QUIZ)}</span><h2>{esc(q)}</h2><div class="qopts">{btns}</div></div>'
    results=''
    for k in SERIES_ORDER:
        s=SERIES[k]; posts=[p for p in POSTS if p['series']==k]; main=PRODUCTS[s['products'][0]]
        results+=f'''<div data-r="{k}" style="display:none">
  <div class="rhead"><span class="dot" style="background:{s['color']}"></span><span class="eyebrow">你的起點</span></div>
  <h2 style="font-size:clamp(22px,3vw,30px);margin-bottom:8px">{s['name']}：{esc(s['h1'])}</h2>
  <p class="lead" style="font-size:16px">{esc(s['lead'])}</p>
  <div class="rgrid">
    <div class="rbox"><img src="{main['image']}" alt=""><h4>從這一款開始</h4><p><b>{esc(main['name'])}</b> — {esc(main['hook'])}</p><a class="btn btn-primary btn-sm" href="{rel}products/{s['products'][0]}.html">看產品</a></div>
    <div class="rbox"><h4>先讀這篇選購指南</h4><p>{esc(posts[0]['title'])}</p><p style="font-size:13px">{esc(posts[0]['excerpt'])}</p><a class="btn btn-ghost btn-sm" href="{rel}blog/{posts[0]['slug']}.html">閱讀指南</a></div>
  </div>
  <p><a href="{rel}series/{k}.html" style="color:var(--green);font-weight:700">看整個{s['name']} →</a></p>
</div>'''
    second=''.join(f'<span data-r2="{k}" style="display:none">其次是 <a href="{rel}series/{k}.html" style="color:var(--green);font-weight:700">{SERIES[k]["name"]}</a>。</span>' for k in SERIES_ORDER)
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div style="text-align:center;max-width:760px;margin:0 auto">
  <span class="eyebrow">30 秒測驗 · 6 題</span><h1>找到最值得先開始的那一件事</h1>
  <p class="lead">同時在意好幾件事很正常。這 6 題幫你排序，結果會直接對應到系列、產品與選購指南。不需註冊、結果立即顯示；完成後還可以免費領取黃醫師的電子書指南。僅供參考，不作為醫療診斷。</p>
</div></div></section>
<section class="sec" style="padding-top:0;margin-top:-20px"><div class="wrap"><div class="quiz-wrap"><div class="qcard" id="quiz">
  <div class="qprog"><i></i></div>
  {steps}
  <div class="qresult">
    {results}
    <p class="note" style="margin-top:6px">{second} 結果依你的回答排序，僅供參考。</p>
    <div class="email-box ebook-box">
      <div class="ebook-row">
        <div class="ebook-pic"><img data-eb="eye-care" src="{rel}downloads/eye-care-guide-cover.jpg" alt="《螢幕族護眼自救指南》封面" width="240" height="320" loading="lazy"><img data-eb="body-balance" src="{rel}downloads/body-balance-guide-cover.jpg" alt="《現代人身體調養指南》封面" width="240" height="320" loading="lazy" style="display:none"></div>
        <div class="ebook-copy"><span class="eyebrow">免費電子書 · 黃醫師</span>
          <div data-eb="eye-care"><h4>《螢幕族護眼自救指南》</h4><ul><li>眼睛為什麼越來越累：眨眼、過熱、眼藥水三個關鍵</li><li>門診最常見的 5 個護眼誤區</li><li>4 種用眼類型對照，加上居家養護小貼士</li></ul></div>
          <div data-eb="body-balance" style="display:none"><h4>《現代人身體調養指南》</h4><ul><li>眼睛、睡眠、腸胃、生活：四大面向 16 項身體訊號清單</li><li>對照你的狀態，知道這個月該先照顧哪裡</li><li>七天微調養計畫，小到一定做得到</li></ul></div>
          <p class="ebook-note">{'留下 Email，指南 PDF 會連同你的測驗結果寄到信箱。' if EBOOK_EMAIL_FLOW_LIVE else '留下 Email，立即取得指南 PDF 下載連結。'}</p>
        </div>
      </div>
      <form data-klaviyo-company="{KLAVIYO_COMPANY}" data-klaviyo-list="{KLAVIYO_LIST}" data-ebooks='{EBOOKS_JSON}' novalidate><input type="hidden" name="quiz_result" value=""><input type="hidden" name="lead_magnet" value="body-balance"><input type="email" name="email" placeholder="你的 Email" required aria-label="Email"><button class="btn btn-primary btn-sm" type="submit">{'免費寄給我' if EBOOK_EMAIL_FLOW_LIVE else '免費領取'}</button></form>
      <p class="consent">送出即表示你同意收到優健堂的健康養護內容與會員優惠 Email，可隨時取消訂閱。我們不會把你的資料提供給第三方。詳見 <a class="ext" href="https://zh.uhealthfit.com/zh-hant-us/policies/privacy-policy" style="text-decoration:underline">隱私權政策</a>。</p>
      <div class="email-ok">{'✓ 已寄出！請留意信箱（沒看到的話，查看一下垃圾郵件匣）。也可以' if EBOOK_EMAIL_FLOW_LIVE else '✓ 已收到你的 Email！指南已經準備好，'}<a class="ebook-dl" href="#" target="_blank" rel="noopener">{'現在直接下載 PDF →' if EBOOK_EMAIL_FLOW_LIVE else '點這裡下載 PDF →'}</a></div>
    </div>
  </div>
  <div class="qnav"><button type="button" class="qback" style="visibility:hidden">← 上一題</button><span class="note">僅供參考 · 非醫療診斷</span></div>
</div></div></div></section>
{journey(rel,'quiz')}
'''
    write('quiz.html', head('30 秒測驗｜找到最值得先開始的養護系列 · 優健堂 × WiseQuest','6 題、30 秒，從護眼、固齒、睡眠、消化、肌膚、活力中找到最值得先開始的那一件事，並對應到產品與選購指南。',rel,'quiz.html','quiz')+nav(rel,'quiz')+body+footer(rel))

# ───────────────────────────── 關於 / FAQ ─────────────────────────────
def build_about():
    rel=''
    body=f'''
<section class="sec doctor bg-dark doctor-top"><div class="wrap">
  <div><img src="{IMG}/home/dr-h.png" alt="黃醫師 Dr. Huang，中國中西醫結合執業醫師"></div>
  <div><div class="crumbs"><a href="index.html">首頁</a><span>›</span><span>黃醫師</span></div><span class="eyebrow">研發者 · 黃醫師 Dr. Huang</span><h1>由一位看了二十年「整個人」的醫師研發</h1>
  <p>黃醫師是中國中西醫結合執業醫師，中醫全科醫師，擁有二十年臨床經驗與草本配方研發專長。她師從多位國家級名老中醫、各科教授與清末御醫傳人，學習中醫針藥特色療法；作為全科中醫師，臨床涉及內科、皮膚科、婦科、兒科，對消化系統疾病、心理睡眠疾病、神經系統疾病、呼吸系統疾病、循環系統疾病、泌尿生殖系統疾病、皮膚科常見病與痛症等均有豐富的臨床經驗，並專研中醫醫美二十年，自主研發的中藥化妝品曾獲國家發明專利。</p>
  <blockquote>「中醫講治未病，在身體逐漸衰老的過程中會發生很多衰老相關的疾病，中醫抗衰就顯得尤為重要。很多時候讓症狀暫時消失，不等於身體真的恢復。我想做的，是幫身體重新找回自己健康的狀態——用承傳千年的草本經驗，幫助身體恢復平衡。」<footer>— 黃醫師</footer></blockquote>
  <ul class="checks"><li><div>生產設施具 FDA 登記<small>核查企業與生產設施的 FDA 登記資訊（登記不等於 FDA 核准）</small></div></li><li><div>天然／有機來源成分<small>優先選擇來源清楚的草本與植物成分</small></div></li><li><div>專業經驗配方<small>以臨床觀點對應現代人的常見日常需求</small></div></li><li><div>品質安全把關<small>原料、生產、第三方純度檢測三道關卡</small></div></li><li><div>價格合理親民<small>讓長期保健更容易持續</small></div></li><li><div>只說有依據的事<small>不誇大、不神化草本、不製造焦慮</small></div></li></ul></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">品牌理念</span><h2>不壓制、不依賴，從根源支持身體</h2><p class="lead">我們相信，真正的健康，不只是沒有疾病，而是擁有一個平衡的身體、一顆安定的心，以及面對生活的力量。我們尊重現代醫學，也珍惜傳統草本智慧。</p></div>
  <div class="grid-4">
    <div class="card"><div class="num">尊重自然</div><h3>Respect Nature</h3><p>相信身體本有自我調節力；草本是支持，幫助身體恢復平衡。</p></div>
    <div class="card"><div class="num">尊重專業</div><h3>Respect Science</h3><p>尊重現代醫學證據，也珍惜傳統草本臨床經驗，開放而嚴謹。</p></div>
    <div class="card"><div class="num">關懷每一個人</div><h3>Care for People</h3><p>我們希望通過養護好物的分享，真正的幫到每個人、少一點焦慮。</p></div>
    <div class="card"><div class="num">分享知識</div><h3>Share Knowledge</h3><p>養護知識的分享，讓人理解自己的身體，如何保持平衡健康的狀態，而不是害怕或者繼續放任不管。</p></div>
  </div>
  <div class="pull">「身體一直在努力照顧你。現在，換我們照顧它。」<small>每一篇內容動筆前後，我們都問自己三個問題：它真實嗎？它對讀者真的有幫助嗎？它對得起初心嗎？</small></div>
</div></section>
{journey(rel,'about')}
{sticky(rel)}
'''
    write('about.html', head('研發者黃醫師 Dr. Huang｜WiseQuest 草本保健研發者 · 優健堂 UHealthFit','WiseQuest 草本保健全系列由中國中西醫結合執業醫師、中醫全科醫師黃醫師研發，二十年臨床經驗與草本配方研發專長。不壓制、不依賴，從根源支持身體。',rel,'about.html','about')+nav(rel,'about')+body+footer(rel))

ABOUT_US_PICKS = [
 ('生產廠商核查','核查企業與生產設施的登記與品質資訊，例如 FDA 設施登記（登記不等於 FDA 核准）。'),
 ('天然來源成分','優先選擇來源清楚的天然植物與草本成分，成分全部公開。'),
 ('專業經驗配方','由黃醫師以二十年臨床經驗設計，針對現代人日常的健康需求。'),
 ('品質安全把關','重視生產流程與品質標準：依 cGMP 規範生產，並經第三方純度檢測。'),
 ('價格合理親民','兼顧品質與價格，讓好的保健更容易長期持續。'),
]
def build_about_us():
    rel=''
    picks=''.join(f'<div class="card white"><div class="num">0{i+1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i,(t,d) in enumerate(ABOUT_US_PICKS))
    series=''.join(f'<a class="scard s-{k}" href="series/{k}.html"><div class="scard-pic"><img src="{SERIES[k]["photo"]}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{SERIES[k]["en"]}</span><h3>{SERIES[k]["name"]}</h3><div class="hook">{SERIES[k]["h1"]}</div><span class="go">看系列 →</span></a>' for k in SERIES_ORDER)
    body=f'''
<section class="hero"><div class="wrap">
  <div><div class="crumbs"><a href="index.html">首頁</a><span>›</span><span>關於我們</span></div><span class="eyebrow">關於優健堂 UHealthFit</span>
  <h1>優質健康，選擇更安心</h1><p class="lead">優健堂 UHealthFit 由具有中醫與健康專業背景的人士，結合健康產品開發與製造領域的經驗共同發起。我們是 WiseQuest 品牌的官方網路商店，由美國紐約的 Uhealth Trading Inc. 經營。</p>
  <div class="hero-cta"><a class="btn btn-primary" href="products/index.html">瀏覽全部產品</a><a class="btn btn-ghost" href="about.html">認識研發者黃醫師</a></div></div>
  <div class="hero-visual"><img src="{IMG}/home/all-products-lineup.png" alt="WiseQuest 全系列產品陳列"></div>
</div></section>
<section class="sec"><div class="wrap" style="max-width:860px">
  <div class="sec-head"><span class="eyebrow">我們的起點</span><h2>為現代生活，找到更好的健康選擇</h2></div>
  <p class="lead" style="font-size:17px">現代生活帶來越來越多常見的健康需求：長時間盯螢幕的雙眼、越來越難放鬆的夜晚、久坐外食後不太順的腸胃、總覺得不夠用的精神，還有換季時反覆的肌膚狀態。</p>
  <p class="lead" style="font-size:17px">所以我們想做一件簡單但重要的事：從現代人真實的日常需求出發，找到更值得長期選擇的保健產品——並把成分、用法與時間，誠實地說清楚。</p>
</div></section>
<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{IMG}/home/dr-h.png" alt="黃醫師 Dr. Huang，中國中西醫結合執業醫師" loading="lazy"></div>
  <div><span class="eyebrow">研發者 · 黃醫師 Dr. Huang</span><h2>WiseQuest 全系列，由黃醫師研發</h2>
  <p>黃醫師是中國中西醫結合執業醫師、中醫全科醫師，擁有二十年臨床經驗與草本配方研發專長。WiseQuest 的每一款產品——護眼、肌膚、固齒、元氣、睡眠到腸胃——都由她以中醫整體觀設計配方，再交由現代工藝製造。</p>
  <p>她看了二十年「整個人」，而不只是單一的症狀；這也是 WiseQuest 配方的共同起點：不壓制、不依賴，從根源支持身體。</p>
  <div class="hero-cta" style="margin-top:22px"><a class="btn btn-light" href="about.html">認識黃醫師與品牌理念</a></div></div>
</div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">天然來源 × 專業配方</span><h2>我們怎麼選產品</h2><p class="lead">我們相信，傳統草本智慧與現代健康理念可以彼此結合。我們在意的不只是「天然」兩個字，還有成分從哪裡來、如何搭配、產品如何製造，以及能不能為日常健康帶來實際的價值。</p></div>
  <div class="grid-5">{picks}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">專注現代人的日常健康</span><h2>六大系列，從最在意的那一件事開始</h2><p class="lead">我們目前關注六個常見的日常健康需求，也會持續尋找更適合現代生活、能融入日常保健習慣的產品。</p></div>
  <div class="grid-3">{series}</div>
</div></section>
<section class="sec bg-green-light"><div class="wrap" style="max-width:860px">
  <div class="sec-head"><span class="eyebrow">我們相信</span><h2>好的健康產品，不應該複雜</h2></div>
  <div class="pull" style="margin-top:0">「好的健康產品，不應該複雜，也不應該高不可攀。」<small>優健堂希望透過更好的甄選、更透明的資訊與更合理的價格，讓高品質的保健成為更多人的日常選擇。</small></div>
  <p class="lead" style="margin-top:22px">客服信箱 <a href="mailto:service@uhealthfit.com" style="color:var(--green);font-weight:700">service@uhealthfit.com</a>；訂單、運送與退貨，請見 <a href="faq.html" style="color:var(--green);font-weight:700">常見問題</a>。</p>
</div></section>
{journey(rel,'about')}
{sticky(rel)}
'''
    write('about-us.html', head('關於我們｜優健堂 UHealthFit，WiseQuest 品牌官方網路商店','優健堂 UHealthFit 由具中醫與健康專業背景的人士發起，是 WiseQuest 品牌的官方網路商店，由美國紐約 Uhealth Trading Inc. 經營；WiseQuest 全系列由黃醫師研發。',rel,'about-us.html','about-us')+nav(rel,'aboutus')+body+footer(rel))

FAQS = {
 '產品與使用':[('這些產品是藥嗎？可以取代我現在的治療或藥物嗎？','不是。膠囊類為膳食補充劑，乳霜、精華液與眼貼為日常保養品，都不是藥品，也不能取代醫師的診斷、治療或處方。若你正在服藥、懷孕或哺乳、或有任何健康疑慮，請在使用前先諮詢醫師或藥師。'),('多久會有感覺？','草本日常養護是累積型的。多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異，我們不做任何時效或結果的保證。'),('膠囊怎麼吃？需要一直吃下去嗎？','每瓶 180 粒約一個月份，建議每天兩次、每次三粒，隨餐服用（Calmoon 建議午餐後與睡前一小時）。全植物膠囊、全素。我們的設計原則是「不依賴」：狀態穩定後可以鞏固一段時間再停用。'),('可以同時用好幾個系列嗎？','可以依需要搭配（例如護眼三寶）。若同時使用多種補充劑或正在服藥，請先與醫師或藥師討論。'),('眼貼會進到眼睛裡嗎？會過敏嗎？','眼貼貼在眼周肌膚上，不入眼。日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。第一次使用前建議先做局部皮膚測試；孕婦請勿使用。')],
 '品質與製造':[('產品在哪裡製造？成分安全嗎？','明目冷敷眼貼於日本製造；膠囊、乳霜與精華液於美國依 cGMP 規範生產，生產設施具 FDA 登記（登記不等於 FDA 核准）。產品經第三方純度檢測，成分全部公開，無人工色素與防腐劑、非轉基因。'),('「FDA 登記」是什麼意思？','指我們核查相關企業與生產設施在 FDA 的登記資訊。這與「FDA 核准」不同——膳食補充劑與化妝品不經 FDA 上市前核准。'),('素食者可以吃嗎？','膠囊類皆為全植物膠囊，全素。')],
 '購買、運送與退貨':[('在這個網站可以直接結帳嗎？','本站專注於幫你「選對」。按下「購買」會前往我們的官方商店 zh.uhealthfit.com 商品頁，在那裡完成安全結帳（支援 Visa、Mastercard、Apple Pay、Google Pay、PayPal、Shop Pay 等）。'),('運費與到貨時間？','訂單於 48 小時內（工作日）處理。美國地區：眼貼滿 USD $79 免運、其他商品滿 USD $200 免運；未達門檻時運費於結帳頁顯示。眼貼與其他商品由不同倉庫出貨，可能分開送達。'),('可以退貨嗎？','收到商品後 30 天內，未拆封、封條完整並附原始包裝的商品可申請退貨；基於衛生考量，已拆封的個人護理商品無法退貨。請先來信 service@uhealthfit.com 取得退貨指引。'),('商店顯示的幣別是美金嗎？','本站所有購買連結都會帶你到 zh.uhealthfit.com 的美國市場（USD）頁面，價格與本站標示一致；若你在美國以外結帳，系統可能依配送地切換幣別，實際金額以結帳頁顯示為準。')],
 '關於平台':[('優健堂 UHealthFit 和 WiseQuest 是什麼關係？','優健堂 UHealthFit 是專注於健康與保健產品的平台，由美國紐約的 Uhealth Trading Inc. 經營；WiseQuest 是平台上由黃醫師研發的草本保健系列。'),('30 秒測驗的結果準嗎？','測驗依你的回答為六個系列排序，目的是幫你找到「先從哪裡開始」，僅供參考，不是醫療診斷。')],
}
def build_series_index():
    rel='../'
    cards=''.join(series_card(k,rel) for k in SERIES_ORDER)
    organs=''.join(f'<a class="scard s-{k}" href="{rel}series/{k}.html"><span class="series-tag"><span class="dot"></span>{SERIES[k]["organ"]}</span><h3>{SERIES[k]["name"]}</h3><div class="hook">{SERIES[k]["h1"]}</div><span class="go">看系列 →</span></a>' for k in SERIES_ORDER)
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><span>六大系列</span></div>
  <span class="eyebrow">六大系列 · {len(PRODUCT_ORDER)} 款產品</span><h1>從最在意的那一件事開始</h1>
  <p class="lead" style="max-width:760px">護眼保健、肌膚健康、固齒健齦、元氣活力、睡眠健康、腸胃舒暢——每個系列都可以單獨開始，也可以彼此搭配。不確定從哪裡開始？先做 30 秒測驗。</p>
  <div class="hero-cta"><a class="btn btn-primary" href="{rel}quiz.html">30 秒找到我的起點</a><a class="btn btn-ghost" href="{rel}products/index.html">直接看全部產品</a></div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="grid-3">{cards}</div></div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">中醫整體觀 × 現代工藝</span><h2>一套邏輯，六個系列</h2><p class="lead">中醫傳統認為身體各部位彼此牽連。每個系列的配方邏輯，都從這張「整體地圖」出發；再以現代萃取濃縮、第三方純度檢測、成分全部公開。</p></div>
  <div class="grid-3">{organs}</div>
</div></section>
{journey(rel,'home')}
{sticky(rel)}
'''
    write('series/index.html', head('六大系列｜護眼・肌膚・固齒・元氣・睡眠・腸胃 · 優健堂 UHealthFit × WiseQuest','優健堂 WiseQuest 六大日常養護系列：護眼保健、肌膚健康、固齒健齦、元氣活力、睡眠健康、腸胃舒暢。每個系列都可以單獨開始，也可以彼此搭配。',rel,'series/index.html','series-index')+nav(rel,'series')+body+footer(rel))

def build_products_index():
    rel='../'
    chips='<div class="chips">'+''.join(f'<a class="chip" href="#{k}">{SERIES[k]["name"]}</a>' for k in SERIES_ORDER)+'</div>'
    secs=''
    for i,k in enumerate(SERIES_ORDER):
        sv=SERIES[k]; ps=series_products(k)
        cards=''.join(product_card(p,rel,wide=(len(ps)==1),promo=True) for p in ps)
        secs+=f'''<section class="sec{' bg-cream' if i%2 else ''}" id="{k}"><div class="wrap">
  <div class="sec-head"><span class="series-tag s-{k}"><span class="dot"></span>{sv['name']} · {esc(sv['tag'])}</span><h2>{esc(sv['h1'])}</h2><p class="lead">{esc(sv['lead'])} <a href="{rel}series/{k}.html" style="color:var(--green);font-weight:700;white-space:nowrap">看{sv['name']}系列介紹 →</a></p></div>
  <div class="pgrid{' pgrid-1' if len(ps)==1 else ''}">{cards}</div>
</div></section>
'''
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><span>全部產品</span></div>
  <span class="eyebrow">全部產品 · {len(PRODUCT_ORDER)} 款</span><h1>全部產品，一頁看完</h1>
  <p class="lead" style="max-width:760px">依六大系列整理。點「了解」看完整成分、用法與常見問題；點「購買」前往官方商店安全結帳。價格為美金（USD），以結帳頁為準。</p>
  {chips}
</div></div></section>
{secs}
<section class="sec"><div class="wrap"><p class="note" style="text-align:center">膠囊類為膳食補充劑、外用品為日常保養品，皆非藥品，不用於診斷、治療、治癒或預防任何疾病。效果因人而異。</p></div></section>
{journey(rel,'home')}
{sticky(rel)}
'''
    write('products/index.html', head('全部產品｜護眼・肌膚・固齒・元氣・睡眠・腸胃 · 優健堂 × WiseQuest','WiseQuest 草本保健全部產品：依六大系列整理，成分、用法與價格一頁看完，到官方商店安全結帳。',rel,'products/index.html','products')+nav(rel,'products')+body+footer(rel))

def build_faq():
    rel=''
    groups=''.join(f'<div class="faq-group"><h3>{g}</h3>{faq_block(items)}</div>' for g,items in FAQS.items())
    allq=[q for items in FAQS.values() for q in items]
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div><div class="crumbs"><a href="index.html">首頁</a><span>›</span><span>常見問題</span></div><span class="eyebrow">常見問題</span><h1>購買前，你可能想知道</h1><p class="lead" style="max-width:720px">關於產品、品質、購買流程與平台的常見問題。找不到答案？來信 service@uhealthfit.com。</p></div></div></section>
<section class="sec"><div class="wrap"><div class="faq-list">{groups}</div></div></section>
{journey(rel,'faq')}
{sticky(rel)}
<script type="application/ld+json">{faq_ld(allq)}</script>
'''
    write('faq.html', head('常見問題｜產品、品質、購買與退貨 · 優健堂 × WiseQuest','WiseQuest 草本保健常見問題：是不是藥、多久有感、怎麼吃、在哪裡製造、如何購買與退貨。',rel,'faq.html','faq')+nav(rel,'faq')+body+footer(rel))

def build_misc():
    pages=['index.html','about-us.html','about.html','faq.html','quiz.html','blog/index.html','series/index.html','products/index.html']+[f'series/{k}.html' for k in SERIES_ORDER]+[f'products/{s}.html' for s in PRODUCT_ORDER]+[f'blog/{p["slug"]}.html' for p in POSTS]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{page_url(p)}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in pages)+'</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    shutil.copy(os.path.join(ROOT,'src','style.css'), os.path.join(DIST,'css','style.css')) if os.path.isdir(os.path.join(DIST,'css')) else (os.makedirs(os.path.join(DIST,'css')), shutil.copy(os.path.join(ROOT,'src','style.css'), os.path.join(DIST,'css','style.css')))
    os.makedirs(os.path.join(DIST,'js'),exist_ok=True); shutil.copy(os.path.join(ROOT,'src','main.js'), os.path.join(DIST,'js','main.js'))
    os.makedirs(os.path.join(DIST,'img'),exist_ok=True)
    for f in os.listdir(os.path.join(ROOT,'src','img')): shutil.copy(os.path.join(ROOT,'src','img',f), os.path.join(DIST,'img',f))
    readme=f'''# 優健堂 UHealthFit × WiseQuest 介紹網站（靜態 HTML）
製作：NTD Digital · {TODAY}

## 結構
- index.html 首頁 ｜ series/ 六大系列頁 ｜ products/ 11 個單品／組合頁 ｜ blog/ 選購指南首頁＋{len(POSTS)} 篇
- quiz.html 30 秒測驗（結果→系列／產品／指南；Email 留資送 Klaviyo Email List）｜ about-us.html 關於我們（優健堂）｜ about.html 研發者黃醫師與品牌理念 ｜ faq.html
- css/style.css、js/main.js 共用 ｜ sitemap.xml、robots.txt

## 部署
Cloudflare Pages：連結 GitHub repo 的 main 分支，push 後自動部署。正式網址 https://us.uhealthfit.com/（自訂網域，DNS 在 GoDaddy：CNAME us → uhealthfit-zh.pages.dev）；Cloudflare 預設網址 https://uhealthfit-zh.pages.dev/。更換網域時改 build-src/build.py 的 SITE_URL 重建。Cloudflare 會把 .html 網址 308 轉址成乾淨網址（/about、/products/calmoon、/blog/），標準網址、sitemap 與結構化資料都已使用乾淨網址（build.py 的 page_url）。GitHub Pages 已不再使用。\n\n## 怎麼改網站\n不要直接改根目錄的 HTML（34 頁會不同步）。改 `build-src/` 裡的資料與模板，然後在 repo 根目錄執行 `python3 build-src/build.py`，再 commit & push：\n- 產品、系列、FAQ、測驗題目：`build-src/build.py` 上半部的 SERIES / PRODUCTS / QUIZ / FAQS\n- 導購文章：`build-src/posts/<slug>.html`（第一行 JSON meta → `---END-META---` → HTML 片段）；新增文章請加入 build.py 的 POST_ORDER\n- 樣式／互動：`build-src/src/style.css`、`build-src/src/main.js`\n- 文案合規規範：`build-src/BRIEF.md`
- Logo 與圖片：導覽列用 uhealthfit.com 的優健堂 SVG（LOGO）、頁尾用 zh.uhealthfit.com 商店頁首的 UHealthFit 白色字標（`build-src/src/img/`）；六大系列情境照與產品實拍取自 zh.uhealthfit.com（Shopify CDN，見 build.py 的 SHOP_CDN／shop_img，`&width=` 可調尺寸），其餘產品圖取自 uhealthfit.com
上線前：
1. 自訂網域 us.uhealthfit.com 已上線，SITE_URL 已設為正式網域；
2. 追蹤碼已安裝（build.py 的 GTM_ID／GA4_ID／META_PIXEL_ID，與 zh.uhealthfit.com 相同）：GTM GTM-W58N8HRV、GA4 G-M63Z9F6FR7（gtag.js）、Meta Pixel 2216128798841618。js/main.js 會在購買點擊時送出 begin_checkout_redirect 與 ShopRedirect、測驗完成送 quiz_complete、留資送 generate_lead 與 Lead；
3. 所有「購買」按鈕都指向 zh.uhealthfit.com 商品頁：訪客若從廣告或帶 UTM 的連結進站，會原樣帶上原本的 UTM 與點擊編號（fbclid、gclid 等）；沒有來源時才加上 utm_source=uhealthfit-site、utm_medium=referral。Meta 事件不帶產品、頁面或電子書類別；
4. Klaviyo：公開 company_id Xxa5rp、List TKC3Bu（Email List, single opt-in）；留資會帶 quiz_result 屬性，可用來建 Flow。
'''
    write('README.md', readme)

if __name__=='__main__':
    build_home(); build_series(); build_series_index(); build_products(); build_products_index(); build_blog(); build_quiz(); build_about_us(); build_about(); build_faq(); build_misc()
    open(os.path.join(DIST,'.nojekyll'),'w').close()  # 停用 GitHub Pages 的 Jekyll 處理
    print('built →',DIST)
