# -*- coding: utf-8 -*-
"""UHealthFit × WiseQuest — English pages (/en/) · NTD Digital 2026-11

Built by build.py (python3 build-src/build.py builds both languages). This file holds the English data
and templates; it reuses build.py's helpers (write, clean links, lastmod, CSS/JS versions) through `B`.

The English copy is NOT a translation of the Chinese pages: it is written for mainstream US readers
(see build-src/BRIEF_EN.md). Every fact must match the English product pages on uhealthfit.com,
which is where every "Buy" button goes.

Tracking: uhealthfit.com's own Google Tag Manager container (GTM-KR36VL29), which carries GA4
G-BM2J1L0NM9 and Meta Pixel 1617768182710522. It loads only on us.uhealthfit.com, behind the same
consent logic uhealthfit.com uses (geo cookie uh-ip-country from functions/en/_middleware.js;
consent cookie uh-consent; Global Privacy Control turns marketing off).
"""
import os, json, re, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOP = 'https://uhealthfit.com'                     # English store: every Buy button goes to /products/<handle>
U = 'https://uhealthfit.com'                        # image host
LOGO_EN = f'{U}/uhealthfit/uhealthfit_logo.svg'
GTM_EN = 'GTM-KR36VL29'
GA4_EN = 'G-BM2J1L0NM9'                           # inside GTM_EN; page events need send_to this ID (see main.js track())                             # uhealthfit.com container (GA4 G-BM2J1L0NM9 + Meta Pixel 1617768182710522 inside)
CONSENT_SCOPE = ["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE","AX","GF","GP","MQ","RE","YT","MF","IS","LI","NO","GB","GG","JE","IM","GI","CH","US-WA","US-NV","US-CT"]  # same list as uhealthfit.com

def esc(s): return H.escape(s, quote=True)
def opt(path, w=1200): return f'{U}/_optimized/{path}-{w}.avif'
def ing_img(key): return opt(f'ingredients/{key}', 800) if key else None
def shop(handle): return f'{SHOP}/products/{handle}'

# ───────────────────────────── Collections ─────────────────────────────
COLL_ORDER = ['eye', 'dental', 'vitality', 'sleep', 'skin', 'digestive']   # uhealthfit.com nav order
COLL = {
 'eye': dict(slug='eye-health', name='Eye Health', tag='Night, day and from within',
   h1='For eyes that work a full screen day',
   lead="Your eyes clock in before your first email and rarely clock out. This collection covers the whole day: cooling patches for a wind-down ritual at night, a botanical eye cream for daytime, and LumiView, a seven-herb daily formula that supports long-term eye health from within.†",
   situations=["Six or more hours a day on screens, then a phone in bed", "Already using eye drops or an eye vitamin, and looking for the next layer", "Wanting a daily habit for the long run, alongside regular eye exams"],
   reframe=[("In the moment", "Eye drops and warm compresses do an important job: comfort right now. They're built for the moment, not the long stretch."),
            ("Overnight", "Sleep is the longest break your eyes get. Cooling hydrogel patches turn the last minutes of the day into a ritual, then stay comfortable while you sleep."),
            ("From within", "Classical Chinese formulas link eye comfort with the body's overall nourishment — which is why LumiView pairs eye-focused herbs like chrysanthemum with tonic herbs like goji.†")],
   products=['eye-patches', 'lumiview', 'eye-cream'],
   combo=("How the three fit together", "Patches at night (outside), LumiView twice a day with meals (inside), eye cream between patch nights (daytime). Three times of day, not three competing choices — start with whichever fits your routine."),
   faq=[("How are cooling patches different from a warm eye mask?", "A warm or steam mask relaxes with heat for a short session. Our patches are cooling hydrogel you can wear for hours, overnight if you like, with botanical extracts on the skin around the eyes. Different feel, different moment — some people use both."),
        ("I already take an eye vitamin. Can I add these?", "The patches and eye cream are topical, so they don't overlap with a supplement. LumiView is a different approach from a lutein or zeaxanthin supplement; if you'd like to take both, check with your doctor or pharmacist first."),
        ("Do the patches go in the eye?", "No. They sit on the skin at the inner corner, outer corner and below the eye — never on the eye itself. They're made in Japan and preservative-free; do a 24-hour patch test before first use."),
        ("Do I still need eye exams?", "Yes. Nothing here replaces glasses, contacts, prescribed eye drops or regular eye exams.")],
   photo=opt('concerns/eye-care'), og=f'{U}/concerns/eye-care.png'),
 'dental': dict(slug='dental-health', name='Teeth & Gums', tag='A daily layer beyond brushing',
   h1='Gum care that goes beyond the brush',
   lead="Brushing, flossing and twice-yearly cleanings take care of the surface. Dentaforte adds a daily nutritional layer: ten botanicals from a classical formula that supports healthy gums and teeth from within.† It's a common pick for people over 40 — and for adult children shopping for their parents.",
   situations=["You brush and floss carefully and want to do a little more for your gums over the long run", "Setting up a simple daily routine for a parent", "Looking for something between “just brushing” and the dentist's chair"],
   reframe=[("Surface care", "Toothpaste, floss, water flossers and professional cleanings handle what you can see and reach. They're the non-negotiable basics."),
            ("Deeper nourishment", "The Chinese herbal tradition holds that “the kidneys govern the bones, and teeth are the surplus of bone” — a way of saying oral health is tied to the body's overall reserves. Dentaforte's ten botanicals start from that idea.†"),
            ("A long-term habit", "Gum care is a decades-long project. Two servings a day with meals, plus regular dental checkups, turn it into a routine.")],
   products=['dentaforte'],
   combo=("How to start", "Take Dentaforte with breakfast and dinner — no change to your brushing routine. Keep your regular dental visits, and see your dentist about any discomfort."),
   faq=[("Does this replace seeing a dentist?", "No. Dentaforte is a dietary supplement, not a treatment. Keep your cleanings, exams and anything your dentist recommends; think of it as nutritional support that runs in parallel."),
        ("How long until I notice anything?", "We can't promise a timeline. The formula is designed for steady daily use over months rather than a short course, and individual experiences vary."),
        ("I take a blood thinner. Can I use it?", "Talk to your doctor first. Several botanicals in the formula, including salvia and schisandra, can interact with anticoagulants."),
        ("Is it easy for an older parent to take?", "It's six capsules a day, three with breakfast and three with dinner — keeping the bottle next to the breakfast table is the easiest reminder. If your parent takes medication, check with their doctor or pharmacist first.")],
   photo=opt('concerns/dental-health'), og=f'{U}/concerns/dental-health.png'),
 'vitality': dict(slug='energy-vitality', name='Energy & Vitality', tag='Caffeine-free · stimulant-free',
   h1='Steady energy, without the caffeine',
   lead="Coffee at seven, another at noon, and you're eyeing a third by three. EnerBalance is a different kind of option: a classical herbal paste of American ginseng, astragalus and five more botanicals, concentrated into capsules for steady everyday energy — no caffeine, no stimulants.†",
   situations=["Long days and late nights, running on coffee", "Wanting to cut back a cup without losing the afternoon", "Curious about traditional herbal tonics, but not about spooning paste from a jar"],
   reframe=[("Borrowed vs. built", "Caffeine borrows alertness for a few hours. Tonic herbs take a different route: supporting the body's own steady energy over time.†"),
            ("A classic pairing", "American ginseng — native to North America and prized in China since the 1700s — paired with astragalus, one of the tradition's best-known tonic herbs.†"),
            ("Paste, modernized", "A traditional herbal paste (gao) is simmered for hours and kept in a jar. EnerBalance seals the same kind of concentrate into capsules: a measured serving, no added sugar, easy to take anywhere.")],
   products=['enerbalance'],
   combo=("How to start", "Three capsules twice a day with meals. If you're pregnant or nursing, under 18, or take any medication, talk to your doctor first."),
   faq=[("Will it keep me up at night like coffee?", "EnerBalance contains no caffeine and no stimulants; it takes a nourishing approach rather than a jolt. Everyone is different, so take it with meals and see how it fits your day."),
        ("What is a “gao”?", "A traditional Chinese herbal paste: botanicals simmered together, strained and reduced to a thick concentrate. EnerBalance keeps that kind of concentrate but seals it into capsules."),
        ("American ginseng or Asian ginseng — what's the difference?", "They're cousins. American ginseng (Panax quinquefolius) is traditionally considered the gentler, “cooler” of the two, which is why it's often chosen for everyday use. EnerBalance balances it with warming astragalus."),
        ("How long should I take it?", "Herbal tonics are traditionally taken steadily over time. We don't promise a timeline; individual experiences vary.")],
   photo='https://cdn.shopify.com/s/files/1/0676/4675/0818/files/c4001f0d-6d94-4413-9958-8a31fc2e4367.jpg?v=1786711467&width=1200',
   og='https://cdn.shopify.com/s/files/1/0676/4675/0818/files/c4001f0d-6d94-4413-9958-8a31fc2e4367.jpg?v=1786711467&width=1200'),
 'sleep': dict(slug='sleep-health', name='Sleep', tag='Melatonin-free · non-hormonal',
   h1='Ease the day, so the night comes easier',
   lead="When the mind is still running at 11 p.m., the evening often started going sideways at 2 p.m. Calmoon is a melatonin-free, non-hormonal formula built around roasted jujube seed — the tradition's best-known calming herb — taken at midday and in the evening to support calm through the day and natural, restful sleep.†",
   situations=["Lying down while the mind replays the to-do list", "Looking for a melatonin-free option", "Workday stress that follows you home"],
   reframe=[("Start with the day", "In the tradition, the heart “houses the mind” — and a mind that hasn't wound down by evening is often carrying the whole day. Calmoon's midday dose is there for that reason.†"),
            ("Calm, mood, stress", "Jujube seed, poria and lily bulb for calm; albizia bark and self-heal for mood and tension; eleuthero, a classic adaptogen, for everyday stress.†"),
            ("No melatonin", "Calmoon doesn't supply a sleep hormone. It's designed to support your body's own rhythm — and a clear-headed morning.†")],
   products=['calmoon'],
   combo=("How to start", "Three capsules with lunch, three with dinner. Pair them with a screen-free last hour and a consistent wake-up time — good habits make the herbs' job easier."),
   faq=[("Why take it at midday?", "Because the formula looks after the day's tension, not just the last hour. The midday dose helps ease the morning's stress before it builds; the evening dose supports a natural wind-down.†"),
        ("Will I feel groggy in the morning?", "Calmoon contains no melatonin or other hormones and is formulated for a clear-headed wake-up. Everyone responds differently, so start with the suggested use and see how you feel. Don't drive or operate machinery after taking it."),
        ("Can I combine it with other sleep aids?", "Please don't stack sleep products on your own. If you take any sleep aid, sedative or other medication, talk to your doctor first.")],
   photo=opt('concerns/sleep-health'), og=f'{U}/concerns/sleep-health.png'),
 'skin': dict(slug='skin-health', name='Skin Health', tag='Botanical-led · gentle for every day',
   h1='Calm, balanced, rested-looking skin',
   lead="Three botanical formulas for three common skin moods: dry and reactive-feeling, shiny and uneven-looking, or simply tired-looking. Each pairs herbs from the Chinese tradition with ingredients a dermatologist would recognize — colloidal oatmeal, cica, ceramides, peptides.",
   situations=["Skin that feels tight or reactive when the seasons change", "An oily T-zone with cheeks that still feel dry", "Late nights showing up in the mirror"],
   reframe=[("Barrier first", "Skin that feels unsettled is usually asking for fewer actives and a stronger moisture barrier, not more products."),
            ("Botanicals with history", "Centella, purple gromwell root and dandelion have long histories in traditional topical care; colloidal oatmeal is a skin-comfort classic in the West."),
            ("Gentle enough to keep using", "The routine you actually stick with beats the strongest product in the drawer.")],
   products=['soothing-cream', 'clarifying-cream', 'lifting-serum'],
   combo=("How to choose", "Dry, reactive-feeling, after sun or a change of season → Soothing & Repair Cream. Oily or combination → Clarifying Cream. Tired-looking, wanting firmer-looking skin → Lifting & Revitalizing Serum (serum first, then cream)."),
   faq=[("Are these medicines?", "No. They're cosmetics for everyday skincare. If a doctor has prescribed a topical product for you, keep using it as directed."),
        ("Can children use the Soothing & Repair Cream?", "Ask your pediatrician first, and patch test on a small area."),
        ("Will the Clarifying Cream dry my skin out?", "It's acid-free and made without harsh actives, with plant-derived moisturizers to keep the barrier comfortable. If an area feels dry, use it only where you're shiny and use the Soothing & Repair Cream elsewhere."),
        ("Is the serum for men too?", "Yes. It's for anyone who wants firmer-looking, more radiant-looking skin.")],
   photo=opt('concerns/skin-health'), og=f'{U}/concerns/skin-health.png'),
 'digestive': dict(slug='digestive-health', name='Digestive Comfort', tag='No senna · non-stimulant',
   h1='Lighter after meals, regular by nature',
   lead="Long desk days, dinners out, travel — and that heavy, bloated feeling that follows. HerbalFlow is a non-stimulant formula built around hemp seed, with no senna, pairing two traditional actions — moisten and move — for everyday regularity and post-meal comfort.†",
   situations=["Sitting most of the day and eating out often", "Wanting something gentle enough to take every day", "Preferring to skip stimulant laxative teas"],
   reframe=[("Moisten", "Hemp seed, rehmannia and angelica are traditionally used to keep things moving smoothly by moistening.†"),
            ("Move", "Magnolia bark and radish seed are the tradition's go-to herbs for that full, gassy feeling.†"),
            ("Rhythm", "Taken with meals twice a day, without senna — designed for steady daily use rather than a quick push.†")],
   products=['herbalflow'],
   combo=("How to start", "Three capsules twice a day with meals. Add water through the day, a ten-minute walk after dinner and an unhurried morning routine."),
   faq=[("Can I take it with probiotics or fiber?", "They take different approaches, so they don't overlap. If you take several supplements or any medication, check with your doctor or pharmacist about combining them."),
        ("Can I take it every day?", "Yes — HerbalFlow is designed for steady daily use with meals and contains no senna or stimulant herbs. Follow the suggested use."),
        ("When should I see a doctor instead?", "If you have ongoing abdominal pain, blood in the stool, unexplained weight change or a sudden change in your habits, see a doctor rather than relying on a supplement.")],
   photo=opt('products/herbalflow/herbalflow-product-shot-wide'), og=f'{U}/products/herbalflow/herbalflow-product-shot-wide.png'),
}

# ───────────────────────────── Products ─────────────────────────────
# kind: supplement (dietary supplement, † claims) | cosmetic (appearance and feel only)
PRODUCT_ORDER = ['eye-patches', 'lumiview', 'eye-cream', 'dentaforte', 'enerbalance', 'calmoon', 'soothing-cream', 'clarifying-cream', 'lifting-serum', 'herbalflow']
# in_stock=False on a product switches its JSON-LD offer to OutOfStock (default: in stock). Check uhealthfit.com before changing.
P = {
 'eye-patches': dict(coll='eye', kind='cosmetic', name='WiseQuest Eye Patches', short='Eye Patches', line='Cooling hydrogel eye patches', badge=('badge-star', 'Star product'),
   hook='A cooling wind-down ritual for screen-heavy days',
   desc='Japanese cooling hydrogel patches worn on the skin around the eyes — a fresh, relaxing feel at bedtime or during a screen break. Preservative-free.',
   long="After ten hours of spreadsheets, video calls and one more scroll in bed, your eyes deserve more than a quick blink break. WiseQuest Eye Patches are soft, preservative-free hydrogel patches made in Japan. Placed at the inner corner, outer corner and under each eye, they start to feel cool within about a minute — borneol and peppermint bring the cooling, while licorice root, chrysanthemum and poria extracts condition the skin. Wear six at bedtime and sleep in them, or two to four for a quick break at your desk.",
   key='Borneol, peppermint, licorice root, chrysanthemum, poria',
   made='Made in Japan', form='Cooling hydrogel patches (topical)', spec='60 patches per box · ~10 nights at 6 a night',
   handle='wisequest-eye-patches', price=29.90, price_note='1 box · 60 patches · ~10 nights',
   variants=[("2-night trial", "$6.00", "Shipping included", False), ("1 box · 60 patches", "$29.90", "~10 nights", False), ("3 boxes · 1 month", "$84.00", "A full month of nights", True), ("6 boxes · 2 months", "$162.00", "", False), ("9 boxes · 3 months", "$234.00", "Lowest price per patch", False)],
   trial=True,
   usage="Cleanse and dry the skin. Before bed, place 6 patches — at the inner corner, outer corner and below each eye — and sleep with them on; remove in the morning. During the day, use 2–4 patches for a quick cooling break. One box covers about 10 nights; a month of nightly use is 3 boxes.",
   caution="For external use only. Patch test on the inner forearm for 24 hours before first use. Never place on the eye itself. The cooling ingredients can make some people's eyes water a little; if you feel stinging or irritation, remove the patches and rinse with water. Not recommended for anyone under 18, pregnant or nursing, taking blood thinners, or planning eye surgery within 2 weeks.",
   yes=["Six-plus-hour screen days, at work or school", "Anyone who wants a wind-down ritual that isn't another screen", "Contact-lens wearers (take lenses out first)", "People who'd like to try two nights for $6 first"],
   no=["Under 18", "Pregnant or nursing", "Taking blood thinners", "Eye surgery planned within 2 weeks", "Broken or irritated skin around the eyes"],
   ing_title="Cooling botanicals, in a soft hydrogel",
   ing_intro="The cooling comes from borneol and peppermint; the botanical extracts condition the delicate skin around the eyes. Ingredient roles describe how the patches feel and what they do for the skin — they're a cosmetic, not a medicine.",
   ings=[("Borneol", "Bing pian", None, "The source of the cool, fresh sensation on the skin, long used in traditional topical blends for its cooling feel."),
         ("Peppermint extract", "Mentha", None, "Adds to the cool, refreshing feel."),
         ("Camphor", "Zhang nao", None, "A cool, fresh scent."),
         ("Licorice root extract", "Gan cao", None, "Skin conditioning. In classical formulas, licorice is the herb that “harmonizes” a blend."),
         ("Chrysanthemum extract", "Ju hua", 'chrysanthemum', "The flower behind the classic Chinese eye-comfort tea."),
         ("Poria extract", "Fu ling", 'poria', "A fungus used across Chinese formulas; here, skin conditioning.")],
   other="Soft, preservative-free hydrogel.",
   how=[("Clean, dry skin", "Wash your face and pat the eye area dry so the hydrogel sits flat."), ("Place six patches", "Inner corner, outer corner and below each eye — on the skin, never on the eye itself."), ("Sleep or take a break", "Keep them on overnight and remove in the morning, or wear 2–4 for a short break during the day.")],
   faq=[("Is it normal for my eyes to water a little?", "The cooling ingredients can make some people's eyes water a little. If you feel stinging or irritation, remove the patches and rinse with water."),
        ("Why do you suggest bedtime?", "It's the easiest time to give the patches their full wear time: they become part of your wind-down and come off in the morning. Daytime use works too, as a shorter cooling break."),
        ("How is this different from a warm eye mask?", "A warm or steam mask relaxes with heat for a short session. These are cooling hydrogel patches you can wear for hours, with botanical extracts on the skin. Some people use both, at different times."),
        ("Can I use them with eye drops?", "Yes — apply the patches about 30 minutes after drops so the drops absorb first. If you use prescription eye medication, check with your eye doctor."),
        ("Can contact-lens wearers use them?", "Yes. Take your lenses out first."),
        ("Is there an allergy risk?", "The formula is preservative-free and made to be gentle, but any botanical can irritate some people. Do a 24-hour patch test on the inner forearm before first use, especially if your skin tends to react."),
        ("How much is the trial?", "$6 for two nights, shipping included — the smallest way to see whether the routine fits your evenings.")],
   image=opt('products/eye-patches/eye-patches-product-shot-wide'), og=f'{U}/og/eye-patches.png', cross=['lumiview', 'eye-cream', 'calmoon']),
 'lumiview': dict(coll='eye', kind='supplement', name='WiseQuest LUMIVIEW', short='LumiView', line='Daily eye-health capsules · 7 botanicals',
   hook='Seven botanicals for long-term eye health, from within†',
   desc='A classical seven-herb eye formula — goji, chrysanthemum, cassia seed and more — in vegan capsules. Pairs with the patches for an inside-and-outside routine.†',
   long="If you know lutein and zeaxanthin, you already know half of goji's story: it's one of the richest food sources of zeaxanthin. LumiView builds on that with a family of botanicals that classical Chinese formulas have long grouped together for the eyes — chrysanthemum and cassia seed (the traditional eye pairing), goji and Chinese yam as the tonic base, astragalus and dong quai, and poria to balance the blend. In the tradition, eye comfort sits at the end of a longer chain of overall nourishment, which is why this is a formula rather than a single extract.†",
   key='Goji, chrysanthemum, cassia seed, astragalus, dong quai, Chinese yam, poria',
   made='Made in USA (imported ingredients) · cGMP', form='Vegan capsules (HPMC)', spec='180 capsules · ~30 days',
   handle='wisequest-lumiview', price=119, price_note='180 capsules · ~30 days',
   variants=[("1 bottle · 1 month", "$119.00", "", True), ("2 bottles · 2 months", "$226.10", "", False), ("3 bottles · 3 months", "$303.45", "Best price per bottle", False)],
   usage="3 capsules after breakfast and 3 after dinner (6 a day, 3,000 mg), always with food — never on an empty stomach. One bottle lasts about 30 days. For ongoing maintenance, many people move to 3 capsules once a day.",
   caution="Not recommended for anyone under 18, pregnant or nursing, taking blood thinners (e.g., warfarin), or planning eye surgery within 2 weeks. If you have plant allergies, check the ingredient list. LumiView is not a vision-correction tool — keep your glasses, contacts and regular eye exams.",
   yes=["Long screen days, with an interest in supporting the eyes from within†", "People already using the patches who want an inside-and-outside routine", "Anyone who prefers a vegan, fully listed botanical formula"],
   no=["Under 18", "Pregnant or nursing", "Taking blood thinners — talk to your doctor", "Eye surgery planned within 2 weeks"],
   ing_title="A classical eye formula, in seven botanicals",
   ing_intro="Each herb has a role: the classical eye pairing, a tonic base, a traditional “qi and blood” duo, and a balancing herb. Traditional descriptions explain the formula's design; they aren't medical claims.",
   ings=[("Goji berry", "Lycium barbarum", 'goji', "A tonic staple of Chinese kitchens and one of the richest food sources of zeaxanthin."),
         ("Chrysanthemum flower", "Chrysanthemum indicum", 'chrysanthemum', "Brewed as an eye-comfort tea for centuries; a natural source of plant flavonoids."),
         ("Cassia seed", "Cassia obtusifolia", None, "Jue ming zi — the classical partner of chrysanthemum in eye formulas."),
         ("Astragalus root", "Astragalus membranaceus", 'astragalus', "Huang qi — one of the tradition's best-known tonic herbs."),
         ("Dong quai root", "Angelica sinensis", 'angelica', "Paired with astragalus as a classic “qi and blood” duo; a source of ferulic acid."),
         ("Chinese yam", "Dioscorea opposita", 'chinese-yam', "Shan yao — a gentle tonic and an everyday food."),
         ("Poria", "Poria cocos", 'poria', "Fu ling — a fungus that classical formulas pair with tonic herbs to keep the blend balanced.")],
   facts=[("Serving size", "3 capsules · 60 servings per bottle"), ("Herbal proprietary blend", "1,500 mg per serving†"), ("Other ingredients", "Hydroxypropyl methylcellulose (vegetable capsule), magnesium stearate")],
   how=[("After breakfast", "3 capsules with food."), ("After dinner", "3 capsules with food."), ("Every day", "Consistency matters more than any single day — don't double up after a missed dose.")],
   faq=[("Can I use LumiView and the patches together?", "Yes — that's the most complete routine. The capsules work from the inside every day; the patches add external, cooling comfort at night. They work along different paths rather than overlapping."),
        ("What's the exact daily amount?", "3 capsules after breakfast and 3 after dinner: 6 capsules, 3,000 mg a day. One bottle of 180 capsules lasts about 30 days. Always take with food."),
        ("Can I take it with an eye vitamin or lutein supplement?", "They take different approaches. If you'd like to combine supplements, check with your doctor or pharmacist first."),
        ("Can I use it with eye drops?", "Yes. The capsules are taken with meals, so there's no timing conflict. If you use prescription eye medication, check with your eye doctor."),
        ("What should I know before taking it?", "The capsules are made with food-grade botanical ingredients in a US GMP facility and third-party tested for purity. Talk to your doctor first if you take blood thinners such as warfarin, are pregnant or nursing, or have known plant allergies."),
        ("Can it replace glasses or contacts?", "No. LumiView is not a vision-correction tool. If you need glasses to see clearly, you still need them — and keep up with regular eye exams."),
        ("Is it vegan?", "Yes. The capsules are made from plant-based HPMC.")],
   image=opt('products/lumiview/lumiview-product-shot-wide'), og=f'{U}/og/lumiview.png', cross=['eye-patches', 'eye-cream', 'dentaforte']),
 'eye-cream': dict(coll='eye', kind='cosmetic', name='WiseQuest Herbal Soothing & Repair Eye Cream', short='Soothing & Repair Eye Cream', line='Botanical eye cream · 20 g', badge=('badge-new', 'New'),
   hook='Daytime care for the delicate under-eye area',
   desc='A botanical eye cream with dendrobium, chrysanthemum and a touch of eucalyptus — hydrating, cooling care for between patch nights.',
   long="Patches aren't always practical at 2 p.m. in an open-plan office. This 20 g botanical eye cream takes over during the day — or works as a lighter nightly step. Dendrobium conditions and hydrates, chrysanthemum and cassia seed bring antioxidant botanicals, poria and angelica root condition the skin, and eucalyptus adds a cool, refreshing touch. We think of it as care for the skin around your eyes, not an anti-wrinkle promise.",
   key='Dendrobium, chrysanthemum, cassia seed, poria, angelica root, eucalyptus',
   made='Made in USA (imported ingredients) · cGMP', form='Cosmetic eye cream', spec='20 g jar · ~60 days of nightly use',
   handle='wisequest-herbal-soothing-repair-eye-cream', price=59, price_note='20 g jar · ~60 nights',
   usage="Nightly on clean skin before sleep, and during the day when you need a refresh. Use a rice-sized amount per eye and pat gently along the orbital bone. Avoid the eyelid and waterline.",
   caution="For external use only. Avoid direct contact with the eyes. Not for use on broken skin. Discontinue if irritation occurs. If pregnant or nursing, consult your physician before use.",
   yes=["Screen days when patches aren't practical", "Under-eye skin that feels dry or looks tired", "Anyone pairing it with the patches for day-and-night care"],
   no=["Broken or irritated skin", "Sensitivity to eucalyptus or essential oils (patch test first)"],
   ing_title="Six botanicals for the under-eye area",
   ing_intro="A short botanical list chosen to hydrate, condition and refresh the look and feel of the skin around the eyes.",
   ings=[("Dendrobium", "Shi hu", 'dendrobium', "A prized orchid stem in Chinese herbalism; conditions and hydrates to soften the look of fine lines."),
         ("Chrysanthemum + cassia seed", "Ju hua · jue ming zi", 'chrysanthemum', "Antioxidant botanicals that help refresh the look of the under-eye area."),
         ("Poria", "Fu ling", 'poria', "Skin conditioning for a smoother, firmer look."),
         ("Angelica root", "Dang gui", 'angelica', "Conditions the skin for a brighter-looking finish."),
         ("Eucalyptus", "", 'eucalyptus-menthol', "A cooling touch for an instantly refreshed feel.")],
   how=[("Clean skin", "At night before sleep, or between screens."), ("Rice-sized", "One small amount per eye, patted along the orbital bone."), ("Keep clear", "Avoid the eyelid and waterline.")],
   faq=[("When and how much?", "Nightly on clean skin, and during the day when you need it. A rice-sized amount per eye, patted along the orbital bone, avoiding the eyelid and waterline."),
        ("Does it replace the patches?", "It's the daytime relay, not a replacement. When you have time at night, the patches give the full cooling ritual."),
        ("Can men use it?", "Yes."),
        ("Is it okay for sensitive skin?", "It's made to be gentle, but do a patch test first — especially if eucalyptus or essential oils tend to bother your skin."),
        ("Will it sting?", "Eucalyptus gives a cool feel. Keep the cream on the skin around the eyes, not in them; if it gets into the eye, rinse with water."),
        ("How long does a jar last?", "About 60 days of nightly use.")],
   image=opt('products/herbal-soothing-repair-eye-cream/eye-cream-product-shot-wide'), og=f'{U}/og/soothing-eye-cream.png', cross=['eye-patches', 'lumiview', 'lifting-serum']),
 'dentaforte': dict(coll='dental', kind='supplement', name='WiseQuest Dentaforte', short='Dentaforte', line='Daily teeth & gum capsules · 10 botanicals',
   hook='Daily support for healthy gums and teeth, from within†',
   desc='Ten botanicals from a classical formula, in vegan capsules — a daily layer that runs alongside brushing, flossing and dental visits.†',
   long="Brushing and flossing are the non-negotiables, and your dentist sees what you can't. Dentaforte adds something different: a daily nutritional layer. The Chinese herbal tradition holds that “the kidneys govern the bones, and teeth are the surplus of bone” — oral health as part of the body's deeper reserves. Dentaforte's ten botanicals, led by prepared and raw rehmannia, follow that logic, with salvia, schisandra, wild chrysanthemum, astragalus, goji and more. It's built for steady, long-term use — alongside professional care, never instead of it.†",
   key='Rehmannia (prepared + raw), salvia, schisandra, wild chrysanthemum, astragalus, goji',
   made='Made in a cGMP-registered US facility', form='Vegan capsules', spec='180 capsules · ~30 days',
   handle='wisequest-dentaforte', price=269, price_note='180 capsules · ~30 days',
   variants=[("1 bottle", "$269.00", "", True), ("2 bottles", "$511.10", "", False), ("3 bottles", "$686.00", "Best price per bottle", False)],
   usage="3 capsules with breakfast and 3 with dinner (6 a day, 3,000 mg of the herbal blend). Take with food. Keep brushing, flossing and your regular dental checkups. If you miss a day, just restart — don't double up.",
   caution="Talk to your doctor first if you are pregnant or nursing, under 18, taking blood thinners (salvia and schisandra can interact with anticoagulants), scheduled for dental surgery within 2 weeks, or have known plant allergies. Not a substitute for dental care — see your dentist about any discomfort.",
   yes=["Adults who want to do more for gum health over the long run†", "Adult children setting up a simple daily routine for a parent", "People who already have good habits and regular checkups"],
   no=["Taking blood thinners — talk to your doctor first", "Pregnant or nursing", "Dental surgery planned within 2 weeks", "Under 18"],
   ing_title="Ten botanicals, one daily blend",
   ing_intro="Botanicals sourced from licensed growers across East Asia, where these plants are native, and encapsulated in a cGMP-registered US facility. Traditional descriptions explain the formula's design; they aren't medical claims.",
   ings=[("Prepared rehmannia", "Shu di huang", 'prepared-rehmannia', "The steamed root — a cornerstone tonic herb the tradition associates with the body's deeper reserves."),
         ("Raw rehmannia", "Sheng di huang", 'raw-rehmannia', "Paired with the prepared form to keep the formula balanced."),
         ("Salvia root", "Dan shen", 'salvia', "Red sage, valued in the tradition for circulation and studied in modern research for microcirculation."),
         ("Schisandra", "Wu wei zi", 'schisandra', "The “five-flavor berry” — a classic adaptogen."),
         ("Wild chrysanthemum", "Ye ju hua", 'chrysanthemum', "A flavonoid-rich flower traditionally included in formulas for the mouth and gums."),
         ("Astragalus", "Huang qi", 'astragalus', "One of the tradition's best-known tonic herbs."),
         ("Goji berry", "Gou qi zi", 'goji', "Antioxidant-rich; used in the tradition to nourish."),
         ("Chinese yam", "Shan yao", 'chinese-yam', "Traditionally used to support how the body takes up nutrition."),
         ("Poria", "Fu ling", 'poria', "Balances the tonic herbs in the formula."),
         ("Dodder seed", "Tu si zi", 'dodder-seed', "Traditionally paired with Chinese yam in tonic formulas.")],
   facts=[("Serving size", "3 capsules · 1,500 mg herbal blend per serving†"), ("Daily use", "2 servings (6 capsules) with food"), ("Other ingredients", "Hypromellose (vegetable capsule), magnesium stearate"), ("Free from", "GMOs, gluten, artificial colors, flavors and preservatives")],
   how=[("Breakfast", "3 capsules with food."), ("Dinner", "3 capsules with food."), ("Alongside", "Brushing, flossing and your regular dental visits.")],
   faq=[("Does this replace seeing a dentist?", "No. Dentaforte is a dietary supplement, not a treatment. Keep your cleanings, exams and anything your dentist recommends."),
        ("How long until I notice anything?", "We can't promise a timeline. The formula is designed for steady daily use over months rather than a short course, and we'd rather be honest about that than overpromise."),
        ("Can I take it if I'm on blood thinners?", "Several botanicals in the formula, including salvia and schisandra, have known interactions with anticoagulants. Please talk to your doctor before starting."),
        ("Why six capsules a day instead of one?", "A 3,000 mg daily blend won't fit in one capsule you'd want to swallow. Splitting it into two servings also spreads it across the day."),
        ("What if I miss a day or a week?", "Don't try to catch up by doubling the dose — just restart the normal routine. Consistency over months matters more than any single day."),
        ("Where are the herbs grown?", "They're sourced from licensed growers across East Asia, where these plants are native, and encapsulated in a cGMP-registered facility in the US.")],
   image=opt('products/dentaforte/dentaforte-product-shot-wide'), og=f'{U}/og/dentaforte.png', cross=['enerbalance', 'calmoon', 'lumiview']),
 'calmoon': dict(coll='sleep', kind='supplement', name='WiseQuest CALMOON', short='Calmoon', line='Calm & sleep capsules · melatonin-free',
   hook='Calm days, restful nights — melatonin-free†',
   desc='A seven-herb, melatonin-free formula taken at midday and in the evening — easing the day so the night comes easier.†',
   long="Most sleep products focus on the last hour of the day. Calmoon starts earlier. Built on the classical idea that every herb in a formula has a role, it works along four lines at once: roasted jujube seed, poria and lily bulb for calm and natural sleep; albizia bark and self-heal for mood and the tension that builds through the day; eleuthero, a classic adaptogen, for everyday stress; and salvia for the mind and circulation. No melatonin, no hormones — designed to support your body's own rhythm and a clear-headed morning.†",
   key='Roasted jujube seed, poria, lily bulb, albizia bark, self-heal, eleuthero, salvia',
   made='Made in USA (imported ingredients)', form='Vegetarian capsules (HPMC)', spec='180 capsules · ~30 days',
   handle='wisequest-calmoon', price=139, price_note='180 capsules · ~30 days',
   usage="3 capsules with lunch and 3 with dinner (6 a day, 3,000 mg). Do not exceed the suggested use.",
   caution="Not for use by pregnant or nursing women. If you are under 18, take blood thinners (e.g., warfarin), sedatives or any other medication, have a medical condition, or are under a doctor's care, consult your doctor before use. Do not drive or operate heavy machinery after use. Discontinue and consult a healthcare professional if any discomfort occurs.",
   yes=["Busy minds that are still running at bedtime", "People who'd rather skip melatonin", "Anyone who wants to start winding down earlier in the day"],
   no=["Pregnant or nursing", "Taking sedatives or sleep medication — talk to your doctor", "Taking blood thinners — talk to your doctor"],
   ing_title="Four lines of support, seven botanicals",
   ing_intro="Calm, mood, stress and mind — each herb has its role, in the classical lead-support-balance structure. Traditional descriptions explain the formula's design; they aren't medical claims.",
   ings=[("Roasted jujube seed", "Suan zao ren", None, "The best-known calming seed in Chinese herbalism; roasting is the traditional preparation.†"),
         ("Poria with hostwood", "Fu shen", 'poria', "The part of poria that grows around pine root, traditionally reserved for calming formulas."),
         ("Lily bulb", "Bai he", None, "A gentle, food-like herb traditionally used to settle a restless mind."),
         ("Albizia bark", "He huan pi", None, "Known in the tradition as the bark of “collective happiness”, used for mood."),
         ("Self-heal spike", "Xia ku cao", None, "Traditionally used to ease the tension that builds through the day."),
         ("Eleuthero", "Ci wu jia", None, "A classic adaptogen, traditionally used for stamina and resilience to everyday stress.†"),
         ("Salvia root", "Dan shen", 'salvia', "Traditionally used for the mind and healthy circulation.")],
   facts=[("Daily use", "3 capsules at midday + 3 in the evening, with food"), ("Free from", "Melatonin, hormones, gluten, sugar"), ("Capsule", "Vegan capsule (HPMC)")],
   how=[("Midday", "3 capsules with lunch — easing the day's tension early.†"), ("Evening", "3 capsules with dinner, so the evening can settle.†"), ("Habits", "A screen-free last hour and a regular wake-up time help the routine do its job.")],
   faq=[("Why do I take it at midday?", "Because the formula looks after the day's tension, not just the last hour. The midday dose eases the morning's stress before it builds; the evening dose supports a natural wind-down.†"),
        ("No melatonin — so how does it work?", "It relies on a traditional multi-herb formula that supports the body's own rhythm, rather than supplying a sleep hormone.†"),
        ("Will I feel groggy in the morning?", "Calmoon is formulated for a clear-headed wake-up and contains no hormones. Everyone responds differently, so start with the suggested use and notice how you feel. Don't drive or operate machinery after taking it."),
        ("How much do I take each day?", "6 capsules (3,000 mg): 3 with lunch and 3 with dinner."),
        ("Why seven herbs?", "Classical formulas give each herb a role. Jujube seed, poria and lily bulb for calm; albizia and self-heal for mood and tension; eleuthero for everyday stress; salvia for the mind and circulation.†"),
        ("Can I take it with other medication?", "If you take blood thinners such as warfarin, sedatives, sleep medication or any other medication, or have a health condition, talk to your doctor first. Not for use during pregnancy or while nursing.")],
   image=opt('products/calmoon/calmoon-product-shot-wide'), og=f'{U}/og/calmoon.png', cross=['herbalflow', 'enerbalance', 'eye-patches']),
 'herbalflow': dict(coll='digestive', kind='supplement', name='WiseQuest HERBALFLOW', short='HerbalFlow', line='Digestive comfort capsules · no senna',
   hook='Regular, naturally — no senna, no stimulants†',
   desc='Six botanicals led by hemp seed, pairing two traditional actions — moisten and move — for everyday regularity and post-meal comfort.†',
   long="Stimulant laxative teas work by making the bowel contract — useful for a short stretch, but not something many people want to lean on. HerbalFlow takes a gentler route built on two traditional actions. To moisten: hemp seed, rehmannia and angelica. To move: magnolia bark and radish seed, the tradition's herbs for that full, gassy feeling, with purslane to round out the blend. No senna, no stimulant herbs — designed for steady daily use and comfort after meals.†",
   key='Hemp seed, radish seed, magnolia bark, rehmannia, angelica, purslane',
   made='Made in USA (imported ingredients)', form='Plant-based capsules', spec='180 capsules per bottle',
   handle='wisequest-herbalflow', price=139, price_note='180 capsules',
   usage="3 capsules twice a day with meals (6 a day). Take it regularly — consistency is what counts. Do not exceed the suggested use.",
   caution="Not for use by pregnant or nursing women or by anyone under 18. If you take blood thinners (e.g., warfarin) or any other medication, or have a digestive condition, consult your doctor before use. Stop use and see a doctor if you experience ongoing diarrhea, abdominal pain or other discomfort.",
   yes=["Desk-bound days and frequent dining out", "People who prefer a gentle, non-stimulant approach", "Anyone who wants regularity and post-meal comfort together†"],
   no=["Pregnant or nursing", "Under 18", "Ongoing abdominal pain or any sudden change — see a doctor first"],
   ing_title="Moisten and move: six botanicals",
   ing_intro="Two traditional actions in one formula, with no senna and no stimulant herbs. Traditional descriptions explain the formula's design; they aren't medical claims.",
   ings=[("Hemp seed", "Huo ma ren", 'hemp-seed', "A familiar superfood and the formula's lead herb, traditionally used to moisten.†"),
         ("Radish seed", "Lai fu zi", 'radish-seed', "Traditionally used for that full, heavy feeling after meals.†"),
         ("Magnolia bark", "Hou po", 'magnolia-bark', "The tradition's classic herb for a gassy, bloated feeling.†"),
         ("Rehmannia", "Sheng di huang", 'raw-rehmannia', "Traditionally used to moisten and nourish."),
         ("Angelica", "Dang gui", 'angelica', "Paired with rehmannia to moisten."),
         ("Purslane", "Ma chi xian", 'purslane', "A leafy green eaten around the world, rounding out the blend.")],
   facts=[("Daily use", "3 capsules twice a day with meals"), ("Free from", "Senna and stimulant herbs, gluten, added sugar"), ("Capsule", "Plant-based")],
   how=[("With breakfast", "3 capsules with food."), ("With dinner", "3 capsules with food."), ("Everyday habits", "Water through the day, a short walk after meals and an unhurried morning routine.")],
   faq=[("Can I take it every day?", "Yes — it's designed for steady daily use with meals and contains no senna or stimulant herbs. Follow the suggested use."),
        ("How is it different from a senna tea?", "Senna is a stimulant herb that makes the bowel contract and is meant for short stretches. HerbalFlow takes a gentler route — moistening and moving — for everyday use.†"),
        ("Can I take it with probiotics or fiber?", "They take different approaches. If you take several supplements or any medication, check with your doctor or pharmacist about combining them."),
        ("When should I see a doctor instead?", "If you have ongoing abdominal pain, blood in the stool, unexplained weight change or a sudden change in your habits, see a doctor rather than relying on a supplement.")],
   image=opt('products/herbalflow/herbalflow-product-shot-wide'), og=f'{U}/og/herbalflow.png', cross=['calmoon', 'dentaforte', 'enerbalance']),
 'soothing-cream': dict(coll='skin', kind='cosmetic', name='WiseQuest Herbal Soothing & Repair Cream', short='Soothing & Repair Cream', line='Botanical moisturizer · face to toe', badge=('badge-star', 'Head to toe'),
   hook='Comfort for dry, reactive-feeling skin — face to toe',
   desc='Colloidal oatmeal, cica and purple gromwell root in a gentle daily moisturizer, with a cooling touch of eucalyptus and menthol.',
   long="Some days skin just feels unsettled — the weather turns, you've been out in the sun, or you've layered one active too many. This cream keeps it simple. It starts with colloidal oatmeal, a skin-comfort classic, and adds botanicals with long histories in traditional topical care: centella (the “cica” of K-beauty), purple gromwell root, angelica and sophora root. Sodium hyaluronate and vitamin C, E and A derivatives form the base, and eucalyptus with menthol gives a cool, calming feel as you apply it. Face, elbows, knees, hands — anywhere that feels dry or tight.",
   key='Colloidal oatmeal, centella (cica), purple gromwell root, angelica, sophora, eucalyptus + menthol',
   made='Made in USA (imported ingredients) · cGMP', form='Cosmetic moisturizer', spec='30 g jar · ~60 days, AM + PM',
   handle='wisequest-herbal-soothing-repair-cream', price=69, price_note='30 g jar · ~60 days',
   usage="AM and PM on clean skin, after toner or essence. Press a pea-sized amount gently into the areas that need it. At night you can apply a slightly thicker layer.",
   caution="For external use only. Patch test on the inner forearm for 24 hours before first use. Do not apply to broken skin. Discontinue if irritation occurs. This is a cosmetic moisturizer, not a medicine; if a doctor has prescribed a topical product for you, keep using it as directed.",
   yes=["Skin that feels dry or reactive when the seasons change", "After sun or a day outdoors", "Elbows, knees and hands that feel tight"],
   no=["Broken skin", "Sensitivity to eucalyptus, menthol or any listed ingredient"],
   ing_title="What's inside — and why",
   ing_intro="Colloidal oatmeal first, then time-tested botanicals around it, on a base of sodium hyaluronate and vitamin C, E and A derivatives. No harsh actives.",
   ings=[("Colloidal oatmeal", "Avena sativa", None, "Finely milled oats — a skin-comfort ingredient trusted for generations."),
         ("Centella asiatica (cica)", "Ji xue cao", 'centella-cica', "One of the most familiar botanicals in sensitive-skin care; soothes the look of redness."),
         ("Purple gromwell root", "Zi cao", None, "A classic in traditional topical care; comforts the look of stressed skin."),
         ("Angelica root", "Bai zhi", 'angelica', "Lightweight and conditioning, for a more even-looking complexion."),
         ("Sophora root", "Ku shen", 'sophora', "Traditionally used to balance and condition skin."),
         ("Eucalyptus + menthol", "", 'eucalyptus-menthol', "A natural cooling touch, for an instant sense of comfort.")],
   how=[("Morning", "First step after cleansing. Layers well under makeup."), ("Night", "A slightly thicker layer before bed; wake up to skin that feels calmer."), ("After sun or a season change", "Use it as a calming step when skin feels warm or tight."), ("Head to toe", "Elbows, knees, hands — anywhere skin feels dry.")],
   faq=[("When and how much?", "Morning and night after cleansing (and toner, if you use one). A pea-sized amount, pressed gently into the skin."),
        ("Can I use it on my face?", "Yes — and anywhere else that feels dry. Patch test first."),
        ("Can children use it?", "Ask your pediatrician first, and patch test on a small area."),
        ("How is it different from the Clarifying Cream?", "Soothing & Repair is for dry, reactive-feeling skin; Clarifying is for oily and combination skin. Combination skin can use both, each where it's needed."),
        ("Does it work under makeup?", "Yes. Let it absorb for a minute, then continue with your routine."),
        ("How long does a jar last?", "About 60 days, morning and night.")],
   image=opt('products/herbal-soothing-repair-cream/soothing-repair-cream-product-shot-wide'), og=f'{U}/og/soothing-cream.png', cross=['clarifying-cream', 'lifting-serum', 'eye-cream']),
 'clarifying-cream': dict(coll='skin', kind='cosmetic', name='WiseQuest Herbal Clarifying Cream', short='Clarifying Cream', line='Botanical cream · oily & combination skin',
   hook='Balanced, clearer-looking skin for oily & combination types',
   desc='Kaolin clay, centella and chrysanthemum in a gentle, acid-free cream that balances the look of shine without stripping.',
   long="Oily skin often gets the harshest treatment — strong cleansers, acids, drying spot products — and ends up feeling tight and unsettled. This cream takes the opposite approach. Kaolin clay helps absorb excess surface oil; chrysanthemum, salvia root, dandelion, honeysuckle and codonopsis are botanicals with long histories in traditional skincare; centella and purple gromwell root keep things comfortable. No acids, no harsh actives — just a fresher, more even-looking complexion you can keep up morning and night.",
   key='Kaolin clay, chrysanthemum, centella, salvia root, dandelion, honeysuckle',
   made='Made in USA (imported ingredients) · cGMP', form='Cosmetic facial cream', spec='30 g jar · ~60 days, AM + PM',
   handle='wisequest-herbal-clarifying-cream', price=69, price_note='30 g jar · ~60 days',
   usage="AM and PM on clean skin, after toner or essence. Smooth a pea-sized amount across the face (avoid the eye area), or use it only on shinier areas.",
   caution="For external use only. Patch test on the inner forearm for 24 hours before first use. Do not apply to broken skin. Discontinue if irritation occurs. Use sunscreen during the day.",
   yes=["Shine within an hour of washing", "Combination skin: oily T-zone, drier cheeks", "Skin that doesn't get along with acids"],
   no=["Broken skin", "Sensitivity to any listed ingredient"],
   ing_title="A short list, nothing harsh",
   ing_intro="Clay to absorb surface oil, botanicals for a calm, even look, plant-derived moisturizers to keep the barrier comfortable.",
   ings=[("Kaolin clay", "", None, "A gentle mineral clay that helps absorb excess surface oil."),
         ("Chrysanthemum", "Ju hua", 'chrysanthemum', "An antioxidant botanical traditionally used for a calm, clear-looking complexion."),
         ("Centella (cica)", "Ji xue cao", 'centella-cica', "Keeps skin comfortable while you balance the shine."),
         ("Salvia root", "Dan shen", 'salvia', "A traditional botanical for a fresh, even-looking tone."),
         ("Dandelion + honeysuckle", "Pu gong ying · jin yin hua", None, "Two classics of traditional skin formulas."),
         ("Codonopsis + purple gromwell root", "Dang shen · zi cao", None, "Round out the blend and keep it gentle.")],
   how=[("Morning", "After cleansing, a pea-sized amount; follow with sunscreen."), ("Night", "Same amount on clean skin."), ("Spot strategy", "Shiny areas only, if your cheeks run dry.")],
   faq=[("Which skin types is it for?", "Oily skin that's shiny soon after washing, and combination skin with an oily T-zone. Because it's acid-free and gentle, it also suits skin that reacts to stronger products — patch test first."),
        ("Will it make my skin feel tight?", "It's designed to balance the look of shine without the stripped feeling of harsh cleansers. If an area feels dry, use it only where you're shiny and the Soothing & Repair Cream elsewhere."),
        ("Can I use it with retinol or acids?", "Space them out and watch how your skin feels; patch test when introducing anything new."),
        ("Do I need sunscreen?", "Yes — daily sunscreen is the foundation of any face routine."),
        ("How long does a jar last?", "About 60 days, morning and night.")],
   image=opt('products/herbal-clarifying-cream/clarifying-cream-product-shot-wide'), og=f'{U}/og/clarifying-cream.png', cross=['soothing-cream', 'lifting-serum', 'eye-cream']),
 'lifting-serum': dict(coll='skin', kind='cosmetic', name='WiseQuest Herbal Lifting & Revitalizing Serum', short='Lifting & Revitalizing Serum', line='Botanical serum · 30 ml', badge=('badge-star', 'Featured'),
   hook='Firmer-looking, more radiant-looking skin',
   desc='Panax ginseng and cica with a peptide complex, ceramides and hyaluronic acid — a focused serum for skin that looks tired.',
   long="The goal isn't to look like someone else. It's to stop looking so tired. This serum keeps a short ingredient story where each part has a clear job: panax ginseng — a cornerstone of Asian luxury skincare — for a radiant, energized look; centella for comfort; a peptide complex for a firmer-looking finish over time; and ceramides with multi-weight hyaluronic acid for plump, hydrated-looking skin. Three to four drops, morning and night.",
   key='Panax ginseng, centella (cica), peptide complex, ceramides + hyaluronic acid',
   made='Made in USA (imported ingredients) · cGMP', form='Cosmetic serum', spec='30 ml bottle · ~60 days, AM + PM',
   handle='wisequest-herbal-lifting-revitalizing-serum', price=189, price_note='30 ml · ~60 days',
   usage="AM and PM on clean skin, before moisturizer. Press 3–4 drops gently into the face and neck.",
   caution="For external use only. Avoid direct contact with the eyes. Patch test on the inner forearm for 24 hours before first use. Discontinue if irritation occurs. If pregnant or nursing, consult your physician before use. Use sunscreen during the day.",
   yes=["Late nights and busy weeks showing up as dullness", "Noticing fine lines and less bounce", "Anyone who wants a gentle, focused serum to use long term"],
   no=["Broken or irritated skin", "Pregnant or nursing — check with your physician first"],
   ing_title="Four focus ingredients, chosen with intention",
   ing_intro="Not twenty ingredients at trace amounts — a focused formula where each one has a clear role.",
   ings=[("Panax ginseng", "Ren shen", 'panax-ginseng', "Rich in ginsenosides with antioxidant properties — for a radiant, energized-looking complexion."),
         ("Centella (cica)", "Ji xue cao", 'centella-cica', "One of skincare's most-loved calming botanicals; soothes the look of redness."),
         ("Peptide complex", "", 'peptide-complex', "Helps improve the appearance of fine lines for a firmer-looking finish."),
         ("Ceramides + hyaluronic acid", "", 'ceramides-ha', "Support the moisture barrier so skin holds on to hydration and looks plump.")],
   how=[("Cleanse", "Morning and night."), ("3–4 drops", "Press gently into face and neck."), ("Seal", "Follow with your moisturizer — and sunscreen in the morning.")],
   faq=[("How do I use it?", "Morning and night after cleansing, before moisturizer: 3–4 drops pressed into the face and neck. Patch test first."),
        ("Who is it for?", "Anyone noticing fine lines, dullness after busy weeks, or skin that looks less firm than it used to. Men and women alike."),
        ("How does it compare with retinol?", "Different approaches. This serum takes a gentle botanical-and-peptide route designed for steady long-term use. If you use retinol, introduce one product at a time."),
        ("Can I use it with the eye cream?", "Yes — the serum for the face and neck, the eye cream around the eyes."),
        ("How long does a bottle last?", "About 60 days, morning and night."),
        ("Can I use it while pregnant or nursing?", "Please check with your physician first.")],
   image=opt('products/herbal-lifting-revitalizing-serum/lifting-serum-product-shot-wide'), og=f'{U}/og/lifting-serum.png', cross=['eye-cream', 'soothing-cream', 'enerbalance']),
 'enerbalance': dict(coll='vitality', kind='supplement', name='WiseQuest EnerBalance', short='EnerBalance', line='Energy & vitality capsules · caffeine-free', badge=('badge-sale', 'Sale'), compare=299,
   hook='Steady everyday energy — no caffeine, no stimulants†',
   desc='American ginseng, astragalus and five more botanicals from a traditional herbal paste, in capsules. Gluten-free and sugar-free.†',
   long="Caffeine borrows alertness for a few hours. EnerBalance starts further back, with the thinking behind a traditional Chinese herbal paste (gao): botanicals simmered together, strained and reduced to a concentrate. We keep that co-simmered concentrate — American ginseng, astragalus, Chinese yam, angelica, citrus peel, chrysanthemum and corn silk — and seal it into capsules at a stated 5:1 extract ratio. A measured serving, no added sugar, nothing to spoon from a jar. Nourishing, not borrowing.†",
   key='American ginseng, astragalus, Chinese yam, angelica, citrus peel, chrysanthemum, corn silk',
   made='Made in USA (imported ingredients) · cGMP · FDA-registered facility', form='Plant-based capsules (HPMC)', spec='180 capsules · 60 servings',
   handle='wisequest-enerbalance', price=166, price_note='180 capsules · 60 servings',
   usage="3 capsules twice a day, preferably with food (6 a day, 3,000 mg), or as directed by a healthcare professional.",
   caution="Do not exceed the suggested use. Do not use if the safety seal is broken or missing. Not for use by pregnant or nursing women. If you are under 18, take blood thinners (e.g., warfarin) or any other medication, have a medical condition, or are under a doctor's care, consult your doctor before use.",
   yes=["Long days and late nights", "Cutting back on coffee or energy drinks", "Older adults who want gentle, everyday support†", "Training without leaning on caffeine"],
   no=["Pregnant or nursing", "Under 18", "Taking blood thinners or other medication — talk to your doctor"],
   ing_title="Seven botanicals, working together",
   ing_intro="Energy that lasts comes from the body working together, not from one thing pushing it. Traditional descriptions explain the formula's design; they aren't medical claims.",
   ings=[("American ginseng", "Xi yang shen", 'panax-ginseng', "Native to North America and prized in the Chinese tradition as the gentler, “cooler” ginseng; supports natural vitality.†"),
         ("Astragalus", "Huang qi", 'astragalus', "Traditionally used to support qi — the tradition's word for functional energy.†"),
         ("Chinese yam", "Shan yao", 'chinese-yam', "Traditionally used to support how well nutrients are used."),
         ("Angelica sinensis", "Dang gui", 'angelica', "Traditionally used to support recovery and healthy circulation.†"),
         ("Citrus peel", "Chen pi", 'citrus-peel', "Aged tangerine peel, traditionally used to support digestion."),
         ("Chrysanthemum", "Ju hua", 'chrysanthemum', "Helps keep the warming herbs in balance."),
         ("Corn silk", "Yu mi xu", 'corn-silk', "Traditionally used to support normal fluid balance.")],
   facts=[("Serving size", "3 capsules · 60 servings per bottle"), ("Herbal proprietary blend", "1,500 mg per serving · 5:1 extract†"), ("Other ingredients", "Plant-based capsule (hydroxypropyl methylcellulose)"), ("Free from", "Caffeine, stimulants, gluten, sugar")],
   cmp=dict(title="From herbal paste to capsule", intro="A traditional gao is simmered, strained and reduced to a thick paste, then kept in a jar. EnerBalance seals the same kind of concentrate into capsules.",
     cols=["Traditional herbal paste", "EnerBalance capsules"],
     rows=[("Hygiene", "Spooned from an open jar over months", "Individually sealed capsules"),
           ("Dosing", "Scooped by eye", "A standardized serving: 3 capsules, twice a day"),
           ("Storage", "Thick and sticky; often refrigerated", "Room temperature, in a cool, dry place"),
           ("Portability", "Rarely leaves the house", "Travels with you"),
           ("What else is in it", "Often set with rock sugar or honey", "No added sugar; plant-based capsule"),
           ("Extract ratio", "Varies by maker, rarely disclosed", "A stated 5:1 extract ratio")]),
   how=[("Morning", "3 capsules with breakfast."), ("Afternoon or evening", "3 capsules with a meal."), ("Every day", "Tonic herbs are traditionally taken steadily, as part of a routine.")],
   faq=[("Will it keep me up like coffee?", "EnerBalance contains no caffeine and no stimulants. It takes a nourishing approach, so take it with meals and see how it fits your day."),
        ("What is a herbal paste (gao)?", "A traditional preparation: botanicals simmered together, strained and reduced to a concentrate. EnerBalance keeps that kind of concentrate and seals it into capsules."),
        ("American or Asian ginseng — why American?", "American ginseng is traditionally considered the gentler, “cooler” ginseng, suited to everyday use. EnerBalance pairs it with warming astragalus for balance."),
        ("How much do I take?", "3 capsules twice a day with food — 6 capsules, 3,000 mg. One bottle holds 60 servings."),
        ("Who is it for?", "People working long days, anyone cutting back on caffeine, older adults who want gentle everyday support, and people training without leaning on stimulants.†"),
        ("Who shouldn't take it?", "It's not for pregnant or nursing women. If you're under 18, take blood thinners or other medication, or have a medical condition, talk to your doctor first. Don't use if the safety seal is broken.")],
   image=opt('products/enerbalance/enerbalance-product-shot-wide'), og=f'{U}/og/enerbalance.png', cross=['calmoon', 'herbalflow', 'lifting-serum']),
}

def price_s(v):
    return f'${v:,.2f}'
def price_html(p, compare=True):
    s = price_s(p['price'])
    if compare and p.get('compare'):
        s += f' <s style="color:var(--ink-3);font-weight:600;font-size:.7em;margin-left:6px">{price_s(p["compare"])}</s>'
    return s

# ───────────────────────────── Guides (build-src/posts-en/) ─────────────────────────────
POSTS = []
_pdir = os.path.join(ROOT, 'posts-en')
if os.path.isdir(_pdir):
    for fn in sorted(os.listdir(_pdir)):
        if not fn.endswith('.html'): continue
        s = open(os.path.join(_pdir, fn), encoding='utf8').read()
        meta, body = s.split('---END-META---', 1)
        m = json.loads(meta.strip()); m['body'] = body.strip(); POSTS.append(m)
POST_ORDER = ['screen-tired-eyes-evening-routine', 'melatonin-free-sleep-support', 'caffeine-free-energy-american-ginseng',
              'gum-care-after-40', 'senna-free-digestive-support', 'cica-oatmeal-reactive-skin-routine',
              'goji-chrysanthemum-eye-nutrition', 'herbal-supplement-safety-checklist']
POSTS.sort(key=lambda p: POST_ORDER.index(p['slug']) if p['slug'] in POST_ORDER else 99)
POST_COVERS = {
 'screen-tired-eyes-evening-routine': (opt('concerns/eye-care'), f'{U}/concerns/eye-care.png'),
 'goji-chrysanthemum-eye-nutrition': (opt('ingredients/goji'), f'{U}/ingredients/goji.png'),
 'melatonin-free-sleep-support': (opt('concerns/sleep-health'), f'{U}/concerns/sleep-health.png'),
 'herbal-supplement-safety-checklist': (f'{U}/_optimized/blog/botanical-wellness-hero-1200.avif', f'{U}/blog/botanical-wellness-hero.png'),
 'senna-free-digestive-support': (opt('ingredients/hemp-seed'), f'{U}/ingredients/hemp-seed.png'),
 'caffeine-free-energy-american-ginseng': (COLL['vitality']['photo'], COLL['vitality']['og']),
 'gum-care-after-40': (opt('concerns/dental-health'), f'{U}/concerns/dental-health.png'),
 'cica-oatmeal-reactive-skin-routine': (opt('ingredients/centella-cica'), f'{U}/ingredients/centella-cica.png'),
}
GENERAL = dict(name='Everyday wellness', slug=None)
def pcoll(p): return GENERAL if p.get('collection', 'general') == 'general' else COLL[p['collection']]
def cover(p, og=False):
    c = POST_COVERS.get(p['slug'])
    if c: return c[1] if og else c[0]
    k = p.get('collection')
    if k in COLL: return COLL[k]['og'] if og else COLL[k]['photo']
    return f'{U}/home/all-products-lineup.png'

# ───────────────────────────── Paths & language alternates ─────────────────────────────
def cpath(k): return f'en/collections/{COLL[k]["slug"]}.html'
def ppath(s): return f'en/products/{s}.html'
def gpath(s): return f'en/guides/{s}.html'
def L(path): return '/' + path   # absolute link; build.py's clean_links turns it into the clean URL

def register(B):
    """Fill build.py's ALT (strict hreflang pairs) and ALT_SWITCH (language-switch target only). Call before building."""
    pairs = [('index.html', 'en/index.html'), ('series/index.html', 'en/collections/index.html'),
             ('products/index.html', 'en/products/index.html'), ('blog/index.html', 'en/guides/index.html'),
             ('quiz.html', 'en/quiz.html'), ('about-us.html', 'en/about.html'), ('faq.html', 'en/faq.html')]
    pairs += [(f'series/{k}.html', cpath(k)) for k in COLL]
    pairs += [(f'products/{s}.html', ppath(s)) for s in P]
    for zh, en in pairs:
        B.ALT[zh] = en; B.ALT[en] = zh
    B.ALT_SWITCH.update({'about.html': 'en/about.html', 'products/eye-care-trio.html': 'en/collections/eye-health.html',
                         'en/approach.html': 'about.html', 'en/404.html': 'index.html'})
    for p in POSTS: B.ALT_SWITCH[gpath(p['slug'])] = 'blog/index.html'

# ───────────────────────────── Shared fragments ─────────────────────────────
def head(B, title, desc, path, page_id, og_image=None, noindex=False, extra=''):
    scope = json.dumps(CONSENT_SCOPE)
    consent = ("<!-- Consent + Google Tag Manager (uhealthfit.com container __GTM__): same logic as uhealthfit.com. "
      "GTM loads only on __HOST__, and only when consent isn't required for the visitor's region (cookie uh-ip-country, set by functions/en/_middleware.js) or the visitor has chosen. -->\n"
      "<script>(function(){try{var h=location.hostname,isProd=h==='__HOST__';"
      "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.gtag=gtag;window.__uhGaId='__GA4__';"
      "function ck(n){var m=document.cookie.match('(?:^|; )'+n+'=([^;]*)');return m?decodeURIComponent(m[1]):null;}"
      "var q=/[?&]uh-geo=([A-Za-z]{2}(?:-[A-Za-z0-9]{1,3})?)/.exec(location.search);if(q&&!isProd){document.cookie='uh-ip-country='+q[1].toUpperCase()+'; path=/';}"
      "var choice=/^v1:a([01])m([01])$/.exec(ck('uh-consent')||''),country=ck('uh-ip-country'),list=__SCOPE__,cc=country?country.toUpperCase():'';"
      "var inScope=country?(list.indexOf(cc)>=0||list.indexOf(cc.split('-')[0])>=0):null,a,m,status;"
      "if(choice){a=choice[1]==='1';m=choice[2]==='1';status='chosen';}else if(inScope===false){a=m=true;status='not-required';}else{a=m=false;status=inScope?'required':'unknown';}"
      "var gpc=navigator.globalPrivacyControl===true;if(gpc)m=false;"
      "function g(on){return on?'granted':'denied';}"
      "gtag('consent','default',{ad_storage:g(m),ad_user_data:g(m),ad_personalization:g(m),analytics_storage:g(a)});gtag('set','url_passthrough',true);"
      "if(!m){var nf=function(){};nf.__uhBlocked=true;window.fbq=nf;gtag('set','ads_data_redaction',true);}"
      "window.__uhConsent={status:status,analytics:a,marketing:m,gpc:gpc};"
      "var loaded=false;window.__uhLoadGtm=function(){if(loaded||!isProd)return;loaded=true;window.__uhGtmLoaded=true;"
      "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','__GTM__');};"
      "if(status==='not-required'||(status==='chosen'&&(a||m)))window.__uhLoadGtm();"
      "}catch(e){}})();</script>\n<!-- End consent + GTM -->").replace('__GTM__', GTM_EN).replace('__GA4__', GA4_EN).replace('__HOST__', B.PROD_HOST).replace('__SCOPE__', scope)
    robots = '<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{B.page_url(path)}">'
    og = og_image or f'{U}/og/uhealthfit-en.jpg'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{consent}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<!--HREFLANG-->
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="UHealthFit">
<link rel="icon" href="{LOGO_EN}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v={B.CSS_VER}">
{extra}
</head>
<body data-page="{page_id}">
'''

def nav(active=''):
    dd = ''.join(f'<a class="s-{k}" href="{L(cpath(k))}"><span class="dot"></span><span>{COLL[k]["name"]}<small>{esc(COLL[k]["h1"])}</small></span></a>' for k in COLL_ORDER)
    dd += f'<a class="dd-all" href="{L("en/collections/index.html")}">All six collections →</a>'
    dd_prod = ''.join(f'<div class="dd-col s-{k}"><a class="dd-h" href="{L(cpath(k))}"><span class="dot"></span>{COLL[k]["name"]}</a>'
                      + ''.join(f'<a href="{L(ppath(s))}">{esc(P[s]["short"])}</a>' for s in COLL[k]['products']) + '</div>' for k in COLL_ORDER)
    dd_prod += f'<a class="dd-all" href="{L("en/products/index.html")}">Browse all {len(P)} products →</a>'
    mob_sub = ''.join(f'<a href="{L(cpath(k))}">{COLL[k]["name"]}</a>' for k in COLL_ORDER)
    mob_prod = ''.join(f'<span class="sub-h">{COLL[k]["name"]}</span>' + ''.join(f'<a href="{L(ppath(s))}">{esc(P[s]["short"])}</a>' for s in COLL[k]['products']) for k in COLL_ORDER)
    def a(href, label, key):
        cls = ' class="active"' if active == key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<div class="topbar"><span class="tb-l">Free US shipping on eye patches over <b>$79</b> and everything else over <b>$200</b> · 30-day returns on unopened items · Secure checkout at uhealthfit.com</span><span class="tb-s">Free US shipping: patches over <b>$79</b>, all else over <b>$200</b></span></div>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{L('en/index.html')}" aria-label="UHealthFit home"><img src="{LOGO_EN}" alt="UHealthFit" width="139" height="26" style="height:26px"></a>
    <nav aria-label="Main"><ul class="nav-links">
      <li>{a(L('en/collections/index.html'), 'Shop by concern', 'collections')}<div class="dd">{dd}</div></li>
      <li>{a(L('en/products/index.html'), 'Products', 'products')}<div class="dd dd-prod">{dd_prod}</div></li>
      <li>{a(L('en/guides/index.html'), 'Guides', 'guides')}</li>
      <li>{a(L('en/quiz.html'), 'Quiz', 'quiz')}</li>
      <li>{a(L('en/approach.html'), 'Our approach', 'approach')}</li>
      <li>{a(L('en/about.html'), 'About', 'about')}</li>
      <li>{a(L('en/faq.html'), 'FAQ', 'faq')}</li>
    </ul></nav>
    <div class="nav-cta"><a class="lang-switch" href="__ALT__" hreflang="zh-Hant" lang="zh-Hant" aria-label="切換到中文網站">中文</a><a class="btn btn-primary btn-sm" href="{L('en/collections/index.html')}">Shop</a><button class="menu-btn" aria-label="Open menu" aria-expanded="false"><span></span></button></div>
  </div>
  <div class="mobile-menu"><div class="wrap">
    <a href="{L('en/index.html')}">Home</a>
    <a href="{L('en/collections/index.html')}">Shop by concern</a><div class="sub">{mob_sub}</div>
    <details class="mm-dd"><summary>Products</summary><div class="sub">{mob_prod}<a class="sub-all" href="{L('en/products/index.html')}">All products →</a></div></details>
    <a href="{L('en/guides/index.html')}">Guides</a><a href="{L('en/quiz.html')}">30-second quiz</a><a href="{L('en/approach.html')}">Our approach to herbs</a><a href="{L('en/about.html')}">About</a><a href="{L('en/faq.html')}">FAQ</a>
    <a href="__ALT__" hreflang="zh-Hant" lang="zh-Hant">中文網站</a>
  </div></div>
</header>
<main>
'''

def disclaimer():
    return '''<section class="disclaimer" aria-label="Disclaimer"><div class="wrap">
<p><b>†These statements have not been evaluated by the Food and Drug Administration. These products are not intended to diagnose, treat, cure, or prevent any disease.</b></p>
<p>The capsules on this site are dietary supplements; the eye patches, creams and serum are cosmetics. None of them is a medicine. Information here is for general education and is not a substitute for advice from your physician, dentist, eye doctor or other healthcare professional; don't use it to diagnose or treat a health problem. If you are pregnant or nursing, under 18, take prescription medication (especially blood thinners) or have a medical condition, talk to your doctor before use. Descriptions of traditional Chinese medicine explain traditional use; they are not medical claims. “FDA-registered facility” refers to facility registration and does not mean FDA approval. Individual experiences vary. Some images are illustrative and actual packaging may vary. All purchases are completed at uhealthfit.com, and prices shown at checkout apply.</p>
</div></section>
'''

def footer(B):
    colls = ''.join(f'<li><a href="{L(cpath(k))}">{COLL[k]["name"]}</a></li>' for k in COLL_ORDER)
    pays = ''.join(f'<img src="{U}/payment/{p}.svg" alt="{p}">' for p in ['visa', 'mastercard', 'american-express', 'discover', 'apple-pay', 'google-pay', 'shop-pay'])
    return f'''</main>
{disclaimer()}
<footer class="site"><div class="wrap">
  <div><img class="logo" src="/{B.LOGO_WHITE}" alt="UHealthFit" width="146" height="26"><p>A tradition-meets-science wellness platform, and the online home of WiseQuest.</p><p style="margin-top:10px">Uhealth Trading Inc.<br>90 North St, Suite D, Middletown, NY 10940, USA<br><a href="mailto:service@uhealthfit.com">service@uhealthfit.com</a></p><div class="pay">{pays}</div></div>
  <div><h4>Shop by concern</h4><ul>{colls}</ul></div>
  <div><h4>Learn</h4><ul><li><a href="{L('en/guides/index.html')}">Guides</a></li><li><a href="{L('en/quiz.html')}">30-second quiz</a></li><li><a href="{L('en/approach.html')}">Our approach to herbs</a></li><li><a href="{L('en/about.html')}">About UHealthFit</a></li><li><a href="{L('en/faq.html')}">FAQ</a></li><li><a href="__ALT__" hreflang="zh-Hant" lang="zh-Hant">中文網站</a></li></ul></div>
  <div><h4>Shopping &amp; help</h4><ul><li><a class="ext" href="{SHOP}/collections">Shop at uhealthfit.com</a></li><li><a class="ext" href="{SHOP}/policies/shipping-policy">Shipping</a></li><li><a class="ext" href="{SHOP}/policies/refund-policy">Returns</a></li><li><a class="ext" href="{SHOP}/policies/privacy-policy">Privacy</a></li><li><a class="ext" href="{SHOP}/policies/consumer-health-data">Consumer health data</a></li><li><a class="ext" href="{SHOP}/privacy-choices">Privacy choices</a></li><li><a class="ext" href="{SHOP}/policies/terms-of-service">Terms</a></li><li><button type="button" class="cc-open">Cookie settings</button></li></ul></div>
  <div class="copy">© 2026 Uhealth Trading Inc. All rights reserved. This site introduces the WiseQuest line; purchases are completed at uhealthfit.com.</div>
</div></footer>
<div class="cc" id="uh-consent" role="dialog" aria-live="polite" aria-label="Cookie choices" hidden><div class="cc-in">
  <p><b>Your privacy choices.</b> We'd like to use cookies and similar tools for analytics and marketing (Google Analytics, Google Ads, Meta). Some places, including Washington, Nevada and Connecticut, treat browsing data on wellness sites as consumer health data, so we ask first. <a class="ext" href="{SHOP}/policies/consumer-health-data" target="_blank" rel="noopener">Consumer health data</a> · <a class="ext" href="{SHOP}/policies/privacy-policy" target="_blank" rel="noopener">Privacy policy</a></p>
  <div class="cc-btns"><button type="button" class="btn btn-ghost btn-sm" data-cc="0">Necessary only</button><button type="button" class="btn btn-ghost btn-sm" data-cc="a">Analytics only</button><button type="button" class="btn btn-primary btn-sm" data-cc="1">Accept all</button></div>
</div></div>
<button class="to-top" type="button" aria-label="Back to top" hidden>↑</button>
<script src="/js/main.js?v={B.JS_VER}" defer></script>
</body></html>
'''

def buy_attrs(slug, label=None):
    return f'class="btn btn-primary{" btn-sm" if label == "sm" else ""} ext" data-product="{slug}" href="{shop(P[slug]["handle"])}" target="_blank" rel="noopener"'

def product_card(slug, wide=False):
    p = P[slug]
    badge = f'<span class="badge {p["badge"][0]}">{p["badge"][1]}</span>' if p.get('badge') else ''
    return f'''<article class="prod{' wide' if wide else ''}">
  <a class="pic cut" href="{L(ppath(slug))}">{badge}<img src="{p['image'].replace('-1200.avif', '-800.avif')}" alt="{esc(p['name'])}" loading="lazy"></a>
  <div class="body">
    <div class="name"><a href="{L(ppath(slug))}">{esc(p['short'])}</a><small>{esc(p['line'])}</small></div>
    <div class="hook">{esc(p['hook'])}</div>
    <p class="desc">{esc(p['desc'])}</p>
    <p class="herbs"><b>Key ingredients:</b> {esc(p['key'])}</p>
    <div class="foot"><div class="price">{price_html(p)}<small>{esc(p['price_note'])}</small></div><div style="display:flex;gap:8px"><a class="btn btn-ghost btn-sm" href="{L(ppath(slug))}">Details</a><a {buy_attrs(slug, 'sm')}>Buy</a></div></div>
  </div>
</article>'''

def coll_card(k, short=False):
    c = COLL[k]
    items = ' · '.join(P[s]['short'] for s in c['products'])
    body = '' if short else f'<p>{esc(c["lead"][:120].rsplit(" ", 1)[0])}…</p><div class="items">{esc(items)}</div>'
    return f'''<a class="scard s-{k}" href="{L(cpath(k))}"><div class="scard-pic"><img src="{c['photo']}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{esc(c['tag'])}</span><h3>{c['name']}</h3><div class="hook">{esc(c['h1'])}</div>{body}<span class="go">Explore →</span></a>'''

def post_card(p):
    c = pcoll(p); k = p.get('collection', 'general')
    return f'''<article class="post-card s-{k}" data-series="{k}">
  <a class="thumb" href="{L(gpath(p['slug']))}"><img src="{cover(p)}" alt="" loading="lazy"></a>
  <div class="body"><div class="meta"><span class="series-tag s-{k}"><span class="dot"></span>{c['name']}</span><span>· {p['reading_min']} min read</span></div>
  <h3><a href="{L(gpath(p['slug']))}">{esc(p['title'])}</a></h3><p>{esc(p['excerpt'])}</p>
  <a class="go" style="color:var(--green);font-weight:700;font-size:14px" href="{L(gpath(p['slug']))}">Read the guide →</a></div>
</article>'''

def faq_block(items):
    return ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items)

def faq_ld(items):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False)

def posts_for(k): return [p for p in POSTS if p.get('collection') == k]

def journey(stage, coll=None, post=None, product=None):
    cards = []
    if stage in ('home', 'about', 'faq', 'approach'):
        cards.append(('STEP 1', 'Not sure where to start?', 'Six questions, thirty seconds. We\'ll point you to the collection, product and guide that fit best.', L('en/quiz.html'), 'Take the quiz'))
        cards.append(('STEP 2', 'Read a buying guide', 'Each guide compares the common options honestly — what each one is built to do, and what it isn\'t.', L('en/guides/index.html'), 'Browse guides'))
    elif stage == 'collection':
        ps = posts_for(coll)
        if ps: cards.append(('Read first', 'How to choose', ps[0]['excerpt'], L(gpath(ps[0]['slug'])), 'Read the guide'))
        cards.append(('Not sure?', 'Find your starting point', 'Care about several things at once? The quiz helps you decide what to start with.', L('en/quiz.html'), 'Take the quiz'))
    elif stage == 'guide' and post:
        pp = post.get('primary_product')
        if pp in P: cards.append(('Next step', P[pp]['short'], P[pp]['desc'], L(ppath(pp)), 'See the product'))
        else: cards.append(('Next step', 'Our approach to herbs', 'How we use Chinese herbalism, and where we draw the lines on quality and claims.', L('en/approach.html'), 'Read our approach'))
        cards.append(('Or', '30-second quiz', 'Not just this one thing? Find the collection worth starting with.', L('en/quiz.html'), 'Take the quiz'))
    elif stage == 'product' and product:
        k = P[product]['coll']; ps = posts_for(k)
        if ps: cards.append(('Read next', ps[0]['title'], ps[0]['excerpt'], L(gpath(ps[0]['slug'])), 'Read the guide'))
        cards.append(('See the collection', COLL[k]['name'], COLL[k]['h1'] + '.', L(cpath(k)), 'Explore the collection'))
    elif stage == 'quiz':
        cards.append(('Skip the quiz', 'Shop by concern', 'Start from the one thing you care about most — each collection works on its own.', L('en/collections/index.html'), 'Shop by concern'))
        cards.append(('Read first', 'Buying guides', 'How to choose, collection by collection.', L('en/guides/index.html'), 'Browse guides'))
    html_cards = ''.join(f'<div class="jcard"><div class="k">{k}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="btn btn-ghost btn-sm" href="{h}">{b}</a></div>' for k, t, d, h, b in cards)
    return f'''<section class="sec-tight journey"><div class="wrap">
  <div class="lead-box"><span class="eyebrow">Your next step</span><h2>Starting beats perfect</h2><p class="lead" style="font-size:16px">Everyday care adds up. Begin with one small thing — we'll help with the rest.</p></div>
  {html_cards}
</div></section>
'''

def sticky():
    return f'<div class="sticky-cta" aria-label="Quick actions"><a class="btn btn-ghost" href="{L("en/quiz.html")}">30-sec quiz</a><a class="btn btn-primary" href="{L("en/collections/index.html")}">Shop by concern</a></div>'

def ing_section(slug):
    p = P[slug]; items = p.get('ings')
    if not items: return ''
    pics = sum(1 for x in items if x[2]) * 2 >= len(items)
    def pic(n, key):
        if not pics: return ''
        return f'<div class="ing-pic"><img src="{ing_img(key)}" alt="{esc(n)}" loading="lazy"></div>' if key else f'<div class="ing-pic ing-pic-blank"><span>{esc(n[0])}</span></div>'
    cards = ''.join(f'<div class="ing{" has-pic" if pics else ""}">{pic(n, key)}{f"<span class=ing-role>{esc(aka)}</span>" if aka else ""}<h3>{esc(n)}</h3><p>{esc(t)}</p></div>' for n, aka, key, t in items)
    facts = ''.join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in p.get('facts', []))
    note = ('Traditional descriptions explain how the formula is designed; they are not medical claims. This is a dietary supplement, not a medicine.' if p['kind'] == 'supplement'
            else 'Ingredient roles describe how the product feels and what it does for the look of the skin. This is a cosmetic, not a medicine; patch test before first use.')
    return f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">What's inside</span><h2>{esc(p['ing_title'])}</h2><p class="lead" style="font-size:16px">{esc(p['ing_intro'])}</p></div>
  <div class="ing-grid">{cards}</div>
  {f'<ul class="ing-facts">{facts}</ul>' if facts else ''}
  <p class="note" style="margin-top:14px">{note}</p>
</div></section>
'''

def how_section(slug):
    hw = P[slug].get('how')
    if not hw: return ''
    steps = ''.join(f'<li><span class="how-k">{i + 1}</span><b>{esc(t)}</b><span>{esc(x)}</span></li>' for i, (t, x) in enumerate(hw))
    return f'''<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How to use</span><h2>Your daily routine</h2></div>
  <ol class="how">{steps}</ol>
</div></section>
'''

def compare_section(slug):
    c = P[slug].get('cmp')
    if not c: return ''
    head = '<tr><th></th>' + ''.join(f'<th{" class=hl" if i == len(c["cols"]) - 1 else ""}>{esc(x)}</th>' for i, x in enumerate(c['cols'])) + '</tr>'
    rows = ''.join('<tr><th>' + esc(r[0]) + '</th>' + ''.join(f'<td{" class=hl" if i == len(r) - 2 else ""}>{esc(v)}</td>' for i, v in enumerate(r[1:])) + '</tr>' for r in c['rows'])
    return f'''<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Compare</span><h2>{esc(c['title'])}</h2><p class="lead" style="font-size:16px">{esc(c['intro'])}</p></div>
  <p class="cmp-hint">Scroll the table sideways →</p>
  <div class="cmp-wrap"><table class="cmp"><thead>{head}</thead><tbody>{rows}</tbody></table></div>
</div></section>
'''

def zebra(html):
    n = [0]
    def f(m):
        n[0] += 1; return '<section class="sec' + ('' if n[0] % 2 else ' bg-cream') + '"'
    return re.sub(r'<section class="sec(?: bg-cream| bg-green-light)?"', f, html)

EXPECT_SUPP = "herbal formulas are built for steady, everyday use. We don't promise timelines, and individual experiences vary."
EXPECT_COSM = 'skincare is a routine, not a one-off. Use it consistently, patch test first, and judge it by how your skin looks and feels day to day.'
FREE_SHIP = lambda slug: 'Free US shipping over $79' if slug == 'eye-patches' else 'Free US shipping over $200'

# ───────────────────────────── Pages ─────────────────────────────
def build_home(B):
    path = 'en/index.html'
    colls = ''.join(coll_card(k) for k in COLL_ORDER)
    featured = ''.join(product_card(s) for s in ['eye-patches', 'calmoon', 'enerbalance'])
    guides = ''.join(post_card(p) for p in POSTS[:3])
    herbs = [("Goji berry", 'goji', "A tonic staple of Chinese kitchens — and one of the richest food sources of zeaxanthin, the eye nutrient you may know from eye vitamins.", 'lumiview', 'Dentaforte too'),
             ("Chrysanthemum", 'chrysanthemum', "The flower in the pale-gold tea served across Asia, brewed for centuries for tired eyes and “internal heat”.", 'lumiview', ''),
             ("American ginseng", 'panax-ginseng', "Native to the forests of North America and exported to China since the 1700s, where it's valued as the gentler, “cooler” ginseng.", 'enerbalance', ''),
             ("Centella (cica)", 'centella-cica', "The “cica” of K-beauty — a calming botanical used in traditional skincare long before it reached Sephora shelves.", 'soothing-cream', ''),
             ("Schisandra", 'schisandra', "The “five-flavor berry” — sweet, sour, salty, bitter and pungent at once — and a classic adaptogen.", 'dentaforte', ''),
             ("Poria", 'poria', "A fungus that grows on pine roots, found in many classical formulas as the herb that keeps tonic blends balanced.", 'calmoon', '')]
    herb_cards = ''.join(f'<div class="ing has-pic"><div class="ing-pic"><img src="{ing_img(key)}" alt="{esc(n)}" loading="lazy"></div><h3>{esc(n)}</h3><p>{esc(t)}</p><a class="herb-in" href="{L(ppath(s))}">Found in {esc(P[s]["short"])} →</a></div>' for n, key, t, s, _ in herbs)
    body = f'''
<section class="hero"><div class="wrap">
  <div><span class="eyebrow">WiseQuest herbal formulas · developed with Dr. Huang</span>
    <h1>Chinese herbal formulas, <em>made for modern routines</em></h1>
    <p class="lead">Six everyday collections — eyes, teeth &amp; gums, energy, sleep, skin and digestion — built on classical botanical formulas, made in the USA and Japan, third-party tested, with every ingredient on the label. No mystique and no miracle claims: just steady, daily support.†</p>
    <div class="hero-cta"><a class="btn btn-primary" href="{L('en/quiz.html')}">Find your starting point</a><a class="btn btn-ghost" href="{L('en/collections/index.html')}">Shop by concern</a></div>
    <ul class="hero-trust"><li>Third-party tested for purity</li><li>cGMP manufacturing</li><li>Full ingredient lists</li></ul>
  </div>
  <div class="hero-visual cutout"><picture><source type="image/avif" srcset="{U}/_optimized/all-products-product-shot-wide-800.avif 800w, {U}/_optimized/all-products-product-shot-wide-1200.avif 1200w, {U}/_optimized/all-products-product-shot-wide-1448.avif 1448w" sizes="(max-width:900px) 100vw, 600px"><img src="{U}/all-products-product-shot-wide.png" alt="The WiseQuest line: capsule bottles, cream jars, a serum and a box of eye patches" width="1448" height="1086" fetchpriority="high"></picture></div>
</div></section>
<section class="trustbar" aria-label="Quality"><div class="wrap"><ul>
  <li>Made in USA &amp; Japan<small>cGMP facilities</small></li><li>Third-party tested<small>for purity</small></li><li>Every ingredient listed<small>with Latin names</small></li><li>No additives · non-GMO<small>no artificial colors</small></li><li>Developed with Dr. Huang<small>two decades of practice</small></li><li>30-day returns<small>on unopened items</small></li>
</ul></div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Shop by concern · {len(P)} products</span><h2>Start with the one thing you care about most</h2><p class="lead">Each collection works on its own, and they pair well. Every page explains how to choose, how to use it, and who should skip it.</p></div>
  <div class="grid-3">{colls}</div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Why Chinese herbalism</span><h2>An old tradition, held to modern standards</h2><p class="lead">You don't need to adopt a whole philosophy to benefit from what Chinese herbalism does well: combining plants thoughtfully, for steady everyday support. Here's what we take from it.</p></div>
  <div class="grid-3">
    <div class="card white"><div class="num">01</div><h3>Formulas, not single ingredients</h3><p>The tradition rarely relies on one hero ingredient. Classical formulas give each herb a role — a lead herb, supporting herbs, and herbs that balance the blend — the way a good recipe works. Every WiseQuest product starts from that logic.</p></div>
    <div class="card white"><div class="num">02</div><h3>Tradition, checked by modern standards</h3><p>Traditional use tells us where to start. Modern manufacturing tells us what's actually in the bottle: cGMP facilities, third-party purity testing, and complete ingredient lists you can look up.</p></div>
    <div class="card white"><div class="num">03</div><h3>Built for everyday, not emergencies</h3><p>Eye drops, coffee and melatonin all have their place in the moment. Our formulas are designed for the long middle: steady, daily support you can fold into a routine.†</p></div>
  </div>
  <div class="pull">“Your body has been working hard for you. Now it's our turn to look after it.”<small>Herbs are support, not a substitute for your doctor. We respect modern medicine and value traditional herbal knowledge. <a href="{L('en/approach.html')}" style="color:var(--green);font-weight:700">Read our approach to herbs →</a></small></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Herbs you may already know</span><h2>Less exotic than you might think</h2><p class="lead">Plenty of the botanicals in our formulas are already in American kitchens, cafés and skincare aisles. Here are six of them, and where you'll find them in the WiseQuest line.</p></div>
  <div class="ing-grid ing-grid-3">{herb_cards}</div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Easy starting points</span><h2>Three popular ways to begin</h2></div>
  <div class="pgrid">{featured}</div>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Buying guides</span><h2>Understand the options before you buy</h2><p class="lead">We compare the common choices — eye drops and patches, melatonin and herbal formulas, senna teas and fiber — and explain what each is built to do. Useful even if you never buy from us.</p></div>
  <div class="bgrid">{guides}</div>
  <p style="margin-top:22px"><a class="btn btn-ghost" href="{L('en/guides/index.html')}">All {len(POSTS)} guides</a></p>
</div></section>

<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{U}/home/dr-h.png" alt="Dr. Huang, who developed the WiseQuest formulas" loading="lazy"></div>
  <div><span class="eyebrow">Developed with Dr. Huang</span><h2>Two decades of looking at the whole person</h2>
  <p>Dr. Huang is a New York State–licensed acupuncturist with two decades of practice and botanical-formulation experience. She graduated from the China Academy of Chinese Medical Sciences and trained with nationally recognized practitioners in Beijing, and she holds a Chinese national invention patent for a herbal cosmetic formula she developed.</p>
  <p style="margin-top:12px">Her approach looks at the whole person rather than a single complaint — the starting point for every WiseQuest formula: support the body, don't override it.</p>
  <div class="hero-cta" style="margin-top:22px"><a class="btn btn-light" href="{L('en/about.html')}#dr-huang">About Dr. Huang and UHealthFit</a></div></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How buying works</span><h2>Learn here, check out at uhealthfit.com</h2><p class="lead">This site helps you choose. When you're ready, the Buy button opens the matching product page on uhealthfit.com — WiseQuest's own store — for secure checkout.</p></div>
  <div class="steps">
    <div class="step"><div class="k">1</div><h3>Choose here</h3><p>Read the collection and product pages, or a buying guide, to find the right starting point and quantity.</p><div class="why">Not sure? Take the 30-second quiz.</div></div>
    <div class="step"><div class="k">2</div><h3>Check out at uhealthfit.com</h3><p>Buy opens the product page on uhealthfit.com. Pay with major cards, Apple Pay, Google Pay or Shop Pay.</p><div class="why">Free US shipping: patches over $79, everything else over $200.</div></div>
    <div class="step"><div class="k">3</div><h3>Shipped within 48 hours</h3><p>Orders are handled within 48 business hours, with tracking by email. Unopened items can be returned within 30 days.</p><div class="why">Questions? service@uhealthfit.com</div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="offer-box">
  <div class="l"><span class="eyebrow">The easiest way to start</span><h2>Try two nights for $6</h2><p>A two-night trial of our Japanese cooling eye patches — enough to see whether the ritual fits your evenings. Shipping is included.</p>
    <div class="big">$6<small> / 2-night trial</small></div>
    <ul><li>Made in Japan · preservative-free · worn on the skin, never on the eye</li><li>Like them? 1 box $29.90 · 3-box month pack $84</li><li>30-day returns on unopened items</li></ul>
    <a {buy_attrs('eye-patches').replace('btn btn-primary', 'btn btn-accent').replace('data-product="eye-patches"', 'data-product="eye-patches-trial"')}>Try two nights for $6</a></div>
  <div class="r"><img src="{U}/products/eye-patches/2-day-trial.png" alt="WiseQuest Eye Patches two-night trial pack" loading="lazy"></div>
</div></div></section>
{journey('home')}
{sticky()}
'''
    B.write(path, head(B, 'UHealthFit × WiseQuest | Chinese Herbal Formulas for Modern Routines', 'WiseQuest herbal formulas for eyes, teeth & gums, energy, sleep, skin and digestion — classical botanicals, made in the USA & Japan, third-party tested. Try the eye patches for $6.', path, 'en-home') + nav('home') + body + footer(B))

def build_collections(B):
    for k in COLL_ORDER:
        c = COLL[k]; path = cpath(k)
        cards = ''.join(product_card(s, wide=(len(c['products']) == 1)) for s in c['products'])
        ps = posts_for(k)
        guides = f'''<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Buying guides</span><h2>Read before you choose</h2></div>
  <div class="bgrid">{''.join(post_card(p) for p in ps)}</div>
</div></section>''' if ps else ''
        reframe = ''.join(f'<div class="card white"><div class="num">0{i + 1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(c['reframe']))
        sits = ''.join(f'<li>{esc(x)}</li>' for x in c['situations'])
        others = ''.join(coll_card(o, short=True) for o in COLL_ORDER if o != k)
        supp = any(P[s]['kind'] == 'supplement' for s in c['products'])
        body = f'''
<section class="hero"><div class="wrap">
  <div><div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><a href="{L('en/collections/index.html')}">Shop by concern</a><span>›</span><span>{c['name']}</span></div>
    <span class="series-tag s-{k}"><span class="dot"></span>{c['name']} · {esc(c['tag'])}</span>
    <h1>{esc(c['h1'])}</h1><p class="lead">{esc(c['lead'])}</p>
    <div class="hero-cta"><a class="btn btn-primary" href="#products">See the products</a>{f'<a class="btn btn-ghost" href="{L(gpath(ps[0]["slug"]))}">Read the buying guide</a>' if ps else ''}</div>
    <ul class="hero-trust"><li>Full ingredient lists</li><li>Third-party tested</li><li>Honest about who should skip it</li></ul></div>
  <div class="hero-visual {'contain' if 'product-shot' in c['photo'] else 'photo'}"><img src="{c['photo']}" alt="{esc(c['name'])} — WiseQuest" width="1200" height="900" fetchpriority="high"></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Sound familiar?</span><h2>Who this collection is for</h2></div>
  <div class="grid-2" style="align-items:start">
    <ul class="hero-trust" style="display:grid;gap:12px;margin:0;font-size:16px">{sits}</ul>
    <div class="timeline" style="margin:0"><div class="ic">⏱</div><div><b>About timing, we'd rather be upfront:</b> herbal formulas are built for steady, everyday use. We don't promise timelines, and individual experiences vary — treat it as a habit, not a quick fix.</div></div>
  </div>
</div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">How we think about it</span><h2>Understand first, then choose</h2></div>
  <div class="grid-3">{reframe}</div>
</div></section>
<section class="sec" id="products"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{c['name']} · products</span><h2>What to choose, and how to use it</h2><p class="lead">Prices in USD. “Buy” opens the product page on uhealthfit.com for secure checkout; “Details” has the full ingredient list, directions and FAQs.</p></div>
  <div class="pgrid{' pgrid-1' if len(c['products']) == 1 else ''}">{cards}</div>
  <div class="pull" style="margin-top:24px">{esc(c['combo'][0])}<small style="font-size:15px;color:var(--ink)">{esc(c['combo'][1])}</small></div>
  <p class="note" style="margin-top:18px;text-align:center">{'Capsules are dietary supplements' + (' and topicals are cosmetics' if not all(P[s]['kind'] == 'supplement' for s in c['products']) else '') if supp else 'These are cosmetics'} — not medicines, and not intended to diagnose, treat, cure or prevent any disease. Individual experiences vary.</p>
</div></section>
{guides}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">FAQ</span><h2>About {c['name']}</h2></div>
  <div class="faq-list">{faq_block(c['faq'])}</div>
</div></section>
{journey('collection', coll=k)}
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Other collections</span><h2>Same approach, six everyday needs</h2></div><div class="grid-3">{others}</div></div></section>
{sticky()}
<script type="application/ld+json">{faq_ld(c['faq'])}</script>
'''
        B.write(path, head(B, f'{c["name"]}: {c["h1"]} | WiseQuest by UHealthFit', re.sub(r'\s+\S*$', '', c['lead'][:158]).replace('†', '') + '…', path, f'en-coll-{k}', og_image=c['og']) + nav('collections') + body + footer(B))

def build_collections_index(B):
    path = 'en/collections/index.html'
    cards = ''.join(coll_card(k) for k in COLL_ORDER)
    body = f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>Shop by concern</span></div>
  <span class="eyebrow">Shop by concern · {len(P)} products</span><h1>Six everyday needs, one approach</h1>
  <p class="lead" style="max-width:760px">Eye Health, Teeth &amp; Gums, Energy &amp; Vitality, Sleep, Skin Health and Digestive Comfort. Each collection works on its own, and they pair well together. Not sure where to start? Take the 30-second quiz.</p>
  <div class="hero-cta"><a class="btn btn-primary" href="{L('en/quiz.html')}">Find your starting point</a><a class="btn btn-ghost" href="{L('en/products/index.html')}">See all products</a></div>
</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="grid-3">{cards}</div></div></section>
{journey('home')}
{sticky()}
'''
    B.write(path, head(B, 'Shop by Concern: Eyes, Gums, Energy, Sleep, Skin, Digestion | UHealthFit', 'Six WiseQuest collections — Eye Health, Teeth & Gums, Energy & Vitality, Sleep, Skin Health and Digestive Comfort. Classical herbal formulas, third-party tested.', path, 'en-collections') + nav('collections') + body + footer(B))

def build_products(B):
    for slug in PRODUCT_ORDER:
        p = P[slug]; k = p['coll']; c = COLL[k]; path = ppath(slug)
        variants = ''
        if p.get('variants'):
            variants = '<ul class="variants">' + ''.join(f'<li class="{"best" if best else ""}"><span>{esc(n)}{(" <span class=tag>· " + esc(t) + "</span>") if t else ""}</span><b>{pr}</b></li>' for n, pr, t, best in p['variants']) + '</ul><p class="note">Choose your size on the uhealthfit.com product page; prices at checkout apply.</p>'
        trial = f'<a class="btn btn-ghost btn-block ext" style="margin-top:8px" data-product="{slug}-trial" href="{shop(p["handle"])}" target="_blank" rel="noopener">Start with the $6 two-night trial</a>' if p.get('trial') else ''
        cross = ''.join(product_card(x) for x in p['cross'])
        yes = ''.join(f'<li>{esc(x)}</li>' for x in p['yes']); no = ''.join(f'<li>{esc(x)}</li>' for x in p['no'])
        kind_label = 'Dietary supplement' if p['kind'] == 'supplement' else 'Cosmetic'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p['name'], "image": p['og'], "description": p['desc'].replace('†', ''), "brand": {"@type": "Brand", "name": "WiseQuest"}, "url": B.page_url(path),
                         "offers": {"@type": "Offer", "priceCurrency": "USD", "price": f'{p["price"]:.2f}', "availability": "https://schema.org/InStock" if p.get('in_stock', True) else "https://schema.org/OutOfStock", "url": shop(p['handle'])}}, ensure_ascii=False)
        body = f'''
<section class="pdp"><div class="wrap">
  <div class="gallery contain"><img src="{p['image']}" alt="{esc(p['name'])}" width="1200" height="800" fetchpriority="high"></div>
  <div>
    <div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><a href="{L(cpath(k))}">{c['name']}</a><span>›</span><span>{esc(p['short'])}</span></div>
    <span class="series-tag s-{k}"><span class="dot"></span>{c['name']} · {kind_label}</span>
    <h1>{esc(p['name'])}</h1><div class="en">{esc(p['line'])} · {esc(p['made'])}</div>
    <div class="hook">{esc(p['hook'])}</div>
    <div class="buybox">
      <div class="row"><div class="price">{price_html(p)}<small>{esc(p['price_note'])} · USD</small></div>{f'<span class="badge {p["badge"][0]}">{p["badge"][1]}</span>' if p.get('badge') else ''}</div>
      <a {buy_attrs(slug).replace('class="btn btn-primary', 'class="btn btn-primary btn-block')}>Buy at uhealthfit.com</a>
      {trial}
      <ul class="micro"><li>Secure checkout</li><li>{FREE_SHIP(slug)}</li><li>Ships within 48 business hours</li><li>30-day returns, unopened</li></ul>
      {variants}
      <ol class="flow"><li><b>Pick a size</b>on the uhealthfit.com product page</li><li><b>Check out</b>Cards · Apple Pay · Google Pay · Shop Pay</li><li><b>Delivered</b>Tracking by email</li></ol>
    </div>
    <p class="desc">{esc(p['long'])}</p>
    <ul class="facts"><li>{esc(p['form'])}</li><li>{esc(p['spec'])}</li><li>Full ingredient list · third-party tested</li><li>30-day returns on unopened items</li></ul>
  </div>
</div></section>
<!--zebra-->{compare_section(slug)}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Who it's for</span><h2>Is it a good fit?</h2></div>
  <div class="who"><div class="box yes"><h3>A good fit for</h3><ul>{yes}</ul></div><div class="box no"><h3>Skip it, or ask your doctor first</h3><ul>{no}</ul></div></div>
</div></section>
{ing_section(slug)}
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Ingredients &amp; directions</span><h2>Know exactly what you're using</h2></div>
  <div class="spec">
    <div class="box"><h3>Ingredients</h3><ul><li><b>Key</b><span>{esc(p['key'])}</span></li>{f"<li><b>Other</b><span>{esc(p['other'])}</span></li>" if p.get('other') else ''}<li><b>Made</b><span>{esc(p['made'])}</span></li><li><b>Format</b><span>{esc(p['form'])}</span></li></ul></div>
    <div class="box"><h3>Directions &amp; cautions</h3><ul><li><b>Use</b><span>{esc(p['usage'])}</span></li><li><b>Size</b><span>{esc(p['spec'])}</span></li><li><b>Cautions</b><span>{esc(p['caution'])}</span></li></ul></div>
  </div>
  <div class="timeline"><div class="ic">⏱</div><div><b>Honest expectations:</b> {EXPECT_SUPP if p['kind'] == 'supplement' else EXPECT_COSM}</div></div>
</div></section>
{how_section(slug)}<!--/zebra-->
<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">FAQ</span><h2>Before you buy</h2></div>
  <div class="faq-list">{faq_block(p['faq'])}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Pairs well with</span><h2>Often chosen together</h2></div>
  <div class="pgrid">{cross}</div>
</div></section>
{journey('product', product=slug)}
<div class="buybar"><div class="wrap"><div class="t"><span class="price">{price_s(p['price'])}</span><span>{esc(p['short'])} · {esc(p['price_note'])}</span></div><a {buy_attrs(slug)}>Buy</a></div></div>
<script type="application/ld+json">{faq_ld(p['faq'])}</script>
<script type="application/ld+json">{ld}</script>
'''
        body = re.sub(r'<!--zebra-->(.*?)<!--/zebra-->', lambda m: zebra(m.group(1)), body, flags=re.S)
        B.write(path, head(B, f'{p["short"]}: {p["hook"].replace("†", "")} | WiseQuest', p['desc'].replace('†', ''), path, f'en-product-{slug}', og_image=p['og']) + nav('products') + body + footer(B))

def build_products_index(B):
    path = 'en/products/index.html'
    chips = '<div class="chips">' + ''.join(f'<a class="chip" href="#{COLL[k]["slug"]}">{COLL[k]["name"]}</a>' for k in COLL_ORDER) + '</div>'
    secs = ''
    for i, k in enumerate(COLL_ORDER):
        c = COLL[k]; ps = c['products']
        secs += f'''<section class="sec{' bg-cream' if i % 2 else ''}" id="{c['slug']}"><div class="wrap">
  <div class="sec-head"><span class="series-tag s-{k}"><span class="dot"></span>{c['name']} · {esc(c['tag'])}</span><h2>{esc(c['h1'])}</h2><p class="lead">{esc(c['lead'])} <a href="{L(cpath(k))}" style="color:var(--green);font-weight:700;white-space:nowrap">About this collection →</a></p></div>
  <div class="pgrid{' pgrid-1' if len(ps) == 1 else ''}">{''.join(product_card(s, wide=(len(ps) == 1)) for s in ps)}</div>
</div></section>
'''
    body = f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>All products</span></div>
  <span class="eyebrow">All products · {len(P)}</span><h1>The whole WiseQuest line, on one page</h1>
  <p class="lead" style="max-width:760px">Grouped by concern. “Details” shows the full ingredient list, directions and FAQs; “Buy” opens the product page on uhealthfit.com for secure checkout. Prices in USD; prices at checkout apply.</p>
  {chips}
</div></div></section>
{secs}
<section class="sec"><div class="wrap"><p class="note" style="text-align:center">Capsules are dietary supplements and topicals are cosmetics — not medicines, and not intended to diagnose, treat, cure or prevent any disease. Individual experiences vary.</p></div></section>
{journey('home')}
{sticky()}
'''
    B.write(path, head(B, 'All WiseQuest Products: Herbal Capsules, Eye Patches & Botanical Skincare | UHealthFit', 'Every WiseQuest product in one place — herbal capsules for eyes, gums, energy, sleep and digestion, Japanese cooling eye patches and botanical skincare.', path, 'en-products') + nav('products') + body + footer(B))

def scroll_tables(html):
    # wide comparison tables scroll sideways on phones instead of stretching the page
    return re.sub(r'<table>(.*?)</table>', r'<div class="table-scroll"><table>\1</table></div>', html, flags=re.S)

def build_guides(B):
    path = 'en/guides/index.html'
    keys = [k for k in COLL_ORDER if posts_for(k)] + (['general'] if posts_for('general') else [])
    chips = '<div class="chips"><button class="chip on" data-f="all">All</button>' + ''.join(f'<button class="chip" data-f="{k}">{COLL[k]["name"] if k in COLL else GENERAL["name"]}</button>' for k in keys) + '</div>'
    body = f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>Guides</span></div>
  <span class="eyebrow">Buying guides · {len(POSTS)}</span><h1>Understand the options before you buy</h1>
  <p class="lead" style="max-width:760px">Plain-English guides to the choices people actually weigh — eye drops or cooling patches, melatonin or a herbal formula, senna tea or fiber. Each one explains what every option is built to do, what to look for on a label, and when to see a professional instead.</p>
</div></div></section>
<section class="sec"><div class="wrap">{chips}<div class="bgrid">{''.join(post_card(p) for p in POSTS)}</div></div></section>
{journey('quiz')}
{sticky()}
'''
    B.write(path, head(B, 'Herbal Wellness Buying Guides: Eyes, Sleep, Energy, Gums, Skin, Digestion | UHealthFit', 'Plain-English buying guides: cooling eye patches vs. drops, melatonin-free sleep support, senna-free digestion, caffeine-free energy, gum care after 40 and more.', path, 'en-guides') + nav('guides') + body + footer(B))
    for p in POSTS:
        gp = gpath(p['slug']); c = pcoll(p); k = p.get('collection', 'general')
        related = [q for q in POSTS if q['slug'] != p['slug'] and q.get('collection') == k] or [q for q in POSTS if q['slug'] != p['slug']][:3]
        pp = p.get('primary_product')
        if pp in P:
            prod = P[pp]
            box = f'<div class="pbox"><img src="{prod["image"].replace("-1200.avif", "-800.avif")}" alt="{esc(prod["name"])}" style="object-fit:contain"><b>{esc(prod["short"])}</b><div class="price">{price_html(prod)}</div><p>{esc(prod["hook"])}</p><a class="btn btn-primary btn-sm btn-block" href="{L(ppath(pp))}">See ingredients &amp; details</a><a class="btn btn-ghost btn-sm btn-block ext" style="margin-top:8px" data-product="{pp}" href="{shop(prod["handle"])}" target="_blank" rel="noopener">Buy at uhealthfit.com</a></div>'
        else:
            box = f'<div class="pbox"><b>Our approach to herbs</b><p style="margin-top:8px">How we use Chinese herbalism, and where we draw the lines on quality and claims.</p><a class="btn btn-primary btn-sm btn-block" href="{L("en/approach.html")}">Read our approach</a></div>'
        ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p['title'], "description": p['description'], "image": cover(p, og=True), "datePublished": p.get('date', '2026-11-04'), "inLanguage": "en-US",
                         "author": {"@type": "Organization", "name": "UHealthFit"}, "publisher": {"@type": "Organization", "name": "UHealthFit", "logo": {"@type": "ImageObject", "url": LOGO_EN}}}, ensure_ascii=False)
        crumb_coll = f'<a href="{L(cpath(k))}">{c["name"]}</a>' if k in COLL else f'<span>{c["name"]}</span>'
        body = f'''
<section class="sec" style="padding-top:clamp(28px,4vw,52px)"><div class="wrap">
  <div class="article-head">
    <div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><a href="{L('en/guides/index.html')}">Guides</a><span>›</span>{crumb_coll}</div>
    <span class="series-tag s-{k}"><span class="dot"></span>{c['name']} · Buying guide</span>
    <h1>{esc(p['title'])}</h1>
    <div class="meta"><span>UHealthFit editorial team · informed by Dr. Huang's practice</span><span>{p['reading_min']} min read</span><span>Updated {p.get('date', '2026-11-04')}</span></div>
  </div>
  <div class="article-cover en-cover"><img src="{cover(p)}" alt="" width="1200" height="675" fetchpriority="high"></div>
  <div class="article-layout">
    <article class="article">
      {scroll_tables(p['body'])}
      <div class="disc-inline"><b>Disclaimer:</b> This guide is general information, not medical advice. The products mentioned are dietary supplements or cosmetics, not medicines, and are not intended to diagnose, treat, cure or prevent any disease. Descriptions of traditional Chinese medicine explain traditional use. Individual experiences vary; if you're pregnant or nursing, take medication or have a health concern, talk to your doctor first.</div>
    </article>
    <aside class="aside">
      {box}
      <div class="tbox"><h4>In this guide</h4><ul><li>What each common option is built to do</li><li>Four things to check before you buy</li><li>Where WiseQuest fits</li><li>Honest expectations, and when to see a professional</li></ul></div>
      <div class="tbox" style="background:var(--green-light)"><h4>Care about more than one thing?</h4><p style="font-size:14px;color:var(--ink-2);margin-bottom:10px">The 30-second quiz helps you decide where to start.</p><a class="btn btn-ghost btn-sm btn-block" href="{L('en/quiz.html')}">Take the quiz</a></div>
    </aside>
  </div>
  <div class="related"><div class="sec-head"><span class="eyebrow">Keep reading</span><h2>Related guides</h2></div><div class="bgrid">{''.join(post_card(q) for q in related[:3])}</div></div>
</div></section>
{journey('guide', post=p)}
{sticky()}
<script type="application/ld+json">{ld}</script>
'''
        B.write(gp, head(B, f'{p["title"]} | UHealthFit', p['description'], gp, f'en-guide-{p["slug"]}', og_image=cover(p, og=True)) + nav('guides') + body + footer(B))

QUIZ = [
 ("First, the practical one: how much of your day is spent looking at screens?", [("8+ hours — and my eyes feel it by the afternoon", {'eye': 3}), ("4–8 hours, with the odd tired-eye moment", {'eye': 2, 'vitality': 1}), ("Not much — screens aren't my main thing", {})]),
 ("When you get into bed, what's your mind usually doing?", [("Still running through the day", {'sleep': 3}), ("I fall asleep, but I don't wake up feeling rested", {'sleep': 2, 'vitality': 1}), ("Mostly settled", {})]),
 ("After a long desk day or a big meal out, how does your stomach feel?", [("Often heavy or bloated", {'digestive': 3}), ("Sometimes — a lighter meal sorts it out", {'digestive': 1}), ("I rarely think about it", {})]),
 ("Looking in the mirror lately, what do you notice most?", [("I look tired and a bit dull", {'skin': 2, 'vitality': 2}), ("Skin that feels reactive or dry, or gets shiny", {'skin': 3}), ("Nothing in particular", {})]),
 ("When it comes to teeth and gums —", [("I (or a parent) want to do more for gum health long term", {'dental': 3}), ("I brush and floss, and haven't thought further", {'dental': 1}), ("Not a priority right now", {})]),
 ("If you could start one new thing this month, it would be…", [("Something at bedtime that doesn't change my day", {'eye': 2, 'sleep': 1}), ("A capsule with meals, and that's it", {'dental': 1, 'digestive': 1, 'vitality': 1}), ("One jar that works on any dry spot", {'skin': 2}), ("Steadier energy by day, easier evenings", {'sleep': 2, 'vitality': 2})]),
]
def build_quiz(B):
    path = 'en/quiz.html'
    steps = ''
    for i, (q, opts) in enumerate(QUIZ):
        btns = ''.join(f'<button type="button" data-w=\'{json.dumps(w)}\'><span class="l">{"ABCD"[j]}</span><span>{esc(t)}</span></button>' for j, (t, w) in enumerate(opts))
        steps += f'<div class="qstep{" on" if i == 0 else ""}"><span class="eyebrow">Question {i + 1} of {len(QUIZ)}</span><h2>{esc(q)}</h2><div class="qopts">{btns}</div></div>'
    results = ''
    for k in COLL_ORDER:
        c = COLL[k]; main = P[c['products'][0]]; ps = posts_for(k)
        guide = f'<div class="rbox"><h4>Read this guide first</h4><p>{esc(ps[0]["title"])}</p><p style="font-size:13px">{esc(ps[0]["excerpt"])}</p><a class="btn btn-ghost btn-sm" href="{L(gpath(ps[0]["slug"]))}">Read the guide</a></div>' if ps else ''
        results += f'''<div data-r="{k}" style="display:none">
  <div class="rhead"><span class="dot s-{k}" style="background:var(--sc)"></span><span class="eyebrow">Your starting point</span></div>
  <h2 style="font-size:clamp(22px,3vw,30px);margin-bottom:8px">{c['name']}: {esc(c['h1'])}</h2>
  <p class="lead" style="font-size:16px">{esc(c['lead'])}</p>
  <div class="rgrid">
    <div class="rbox"><img src="{main['image'].replace('-1200.avif', '-800.avif')}" alt="" style="object-fit:contain"><h4>Start with</h4><p><b>{esc(main['short'])}</b> — {esc(main['hook'])}</p><a class="btn btn-primary btn-sm" href="{L(ppath(c['products'][0]))}">See the product</a></div>
    {guide}
  </div>
  <p><a href="{L(cpath(k))}" style="color:var(--green);font-weight:700">Explore {c['name']} →</a></p>
</div>'''
    second = ''.join(f'<span data-r2="{k}" style="display:none">Your second match is <a href="{L(cpath(k))}" style="color:var(--green);font-weight:700">{COLL[k]["name"]}</a>. </span>' for k in COLL_ORDER)
    body = f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div style="text-align:center;max-width:760px;margin:0 auto">
  <span class="eyebrow">30-second quiz · 6 questions</span><h1>Find the one thing worth starting with</h1>
  <p class="lead">Caring about several things at once is normal. These six questions rank the six collections for you and point to a product and a guide. No sign-up, instant results. For orientation only — not a medical assessment.</p>
</div></div></section>
<section class="sec" style="padding-top:0;margin-top:-20px"><div class="wrap"><div class="quiz-wrap"><div class="qcard" id="quiz">
  <div class="qprog"><i></i></div>
  {steps}
  <div class="qresult">
    {results}
    <p class="note" style="margin-top:6px">{second}Results are based only on your answers and are for orientation.</p>
  </div>
  <div class="qnav"><button type="button" class="qback" style="visibility:hidden">← Back</button><span class="note">For orientation only · not a medical assessment</span></div>
</div></div></div></section>
{journey('quiz')}
'''
    B.write(path, head(B, '30-Second Quiz: Find Your Starting Point | UHealthFit × WiseQuest', 'Six quick questions rank eyes, gums, energy, sleep, skin and digestion for you — then point to a WiseQuest product and a buying guide. No sign-up.', path, 'quiz') + nav('quiz') + body + footer(B))

def build_approach(B):
    path = 'en/approach.html'
    ideas = [("Formulas over single ingredients", "Classical formulas give each herb a job — a lead herb, supporting herbs, herbs that balance the blend and one that “guides” it (jun-chen-zuo-shi). It's closer to a well-built recipe than to a single-ingredient pill, and it's the main thing our formulas borrow."),
             ("Support, don't override", "The tradition prefers nudging the body back toward its own rhythm over forcing a result. That's why our sleep formula is melatonin-free, our digestive formula skips senna, and our energy formula has no caffeine.†"),
             ("Connections across the body", "Classical texts link eye comfort to overall nourishment, teeth to the body's “deeper reserves”, skin to the breath. Treat these as the tradition's maps, not anatomy lessons — they explain why our formulas are built the way they are."),
             ("Steady and gentle", "Tonic herbs are traditionally taken daily, in food-like amounts, over time. Our directions follow suit: a few capsules with meals, not a dramatic short course."),
             ("Food and herbs overlap", "Goji, Chinese yam, chrysanthemum, lily bulb and citrus peel are everyday foods in Chinese kitchens. Much of herbalism starts where cooking ends.")]
    idea_cards = ''.join(f'<div class="card white"><div class="num">0{i + 1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(ideas))
    gloss = [("Qi", "The tradition's word for functional energy — roughly, “how well things are running”."),
             ("Yin and yang", "Complementary qualities to keep in balance: cooling and moistening (yin) versus warming and activating (yang)."),
             ("Tonic herb", "An herb traditionally taken over time to nourish, such as goji, astragalus or Chinese yam."),
             ("Adaptogen", "A modern Western term for herbs that support the body's response to everyday stress — eleuthero, schisandra and American ginseng among them."),
             ("Formula", "A combination of herbs with assigned roles. Most traditional preparations are formulas, not single herbs."),
             ("Gao", "A traditional concentrated herbal paste. EnerBalance is a gao, sealed into capsules.")]
    gl = ''.join(f'<li><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in gloss)
    lines = [("Made where we can check it", "Capsules, creams and serum are made in the USA (with imported botanicals) in cGMP facilities; the eye patches are made in Japan."),
             ("Tested, not assumed", "Finished products are third-party tested for purity — a fair question to ask of any imported botanical."),
             ("Every ingredient on the label", "Latin names on our supplement facts. Like most herbal formulas, the label shows the blend's total per serving rather than each herb's amount; we say so plainly."),
             ("Honest about interactions", "Herbs such as salvia, dong quai and schisandra can interact with blood thinners. Each product page lists who should skip it or ask a doctor first."),
             ("No disease claims, no timelines", "We don't say our products treat anything, and we don't promise results by a date. Individual experiences vary."),
             ("No testimonials", "We'd rather show you the label than a stranger's story.")]
    ln = ''.join(f'<li><div>{esc(t)}<small>{esc(d)}</small></div></li>' for t, d in lines)
    body = f'''
<section class="hero"><div class="wrap">
  <div><div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>Our approach</span></div><span class="eyebrow">Our approach to herbs</span>
    <h1>Chinese herbalism, <em>explained without the mystique</em></h1>
    <p class="lead">Traditional Chinese medicine (TCM) is one of the world's oldest continuously documented herbal traditions. You don't have to adopt its whole philosophy to benefit from what it does well — combining plants thoughtfully, for steady everyday support. Here's how we use it, and where we draw the lines.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="{L('en/collections/index.html')}">Shop by concern</a><a class="btn btn-ghost" href="{L('en/guides/herbal-supplement-safety-checklist.html') if any(p['slug'] == 'herbal-supplement-safety-checklist' for p in POSTS) else L('en/guides/index.html')}">How to vet an herbal supplement</a></div></div>
  <div class="hero-visual photo"><img src="{U}/_optimized/blog/botanical-wellness-hero-1200.avif" alt="Dried botanicals and herbs" width="1200" height="900" fetchpriority="high"></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">The short version</span><h2>What TCM is — and what it isn't</h2></div>
  <div class="who"><div class="box yes"><h3>It is</h3><ul><li>A framework that looks for patterns across the whole body, not just one complaint</li><li>A large library of herb combinations, refined through centuries of recorded use</li><li>A daily, habit-based way of looking after yourself</li></ul></div>
  <div class="box no"><h3>It isn't</h3><ul><li>A replacement for diagnosis, prescriptions or professional care</li><li>A reason to stop any medication</li><li>Proof that something works the same way for every person</li></ul></div></div>
</div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Five ideas worth borrowing</span><h2>What we take from the tradition</h2></div>
  <div class="grid-3">{idea_cards}</div>
</div></section>
<section class="sec"><div class="wrap" style="max-width:900px">
  <div class="sec-head"><span class="eyebrow">A short glossary</span><h2>Six words you'll see on our pages</h2></div>
  <ul class="ing-facts">{gl}</ul>
</div></section>
<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{U}/home/dr-h.png" alt="Dr. Huang" loading="lazy"></div>
  <div><span class="eyebrow">Where we draw the lines</span><h2>Tradition is the starting point. Standards are the rule.</h2>
  <ul class="checks">{ln}</ul>
  <div class="hero-cta" style="margin-top:22px"><a class="btn btn-light" href="{L('en/about.html')}#dr-huang">Meet Dr. Huang</a></div></div>
</div></section>
{journey('approach')}
{sticky()}
'''
    B.write(path, head(B, 'Chinese Herbalism, Explained Without the Mystique | Our Approach · UHealthFit', 'What traditional Chinese medicine is and isn\'t, the ideas WiseQuest borrows from it, a plain-English glossary, and the quality and honesty rules we hold ourselves to.', path, 'en-approach') + nav('approach') + body + footer(B))

ABOUT_PICKS = [("Manufacturer checks", "We review the registration and quality information of the businesses and facilities behind each product."),
               ("Naturally sourced ingredients", "We prioritize clearly sourced botanical and herbal ingredients, and list every one."),
               ("Professionally developed formulas", "Formulas developed with professional expertise, around everyday health needs."),
               ("Quality & safety focus", "cGMP manufacturing, third-party purity testing and consistent production."),
               ("Accessible pricing", "A fair balance of quality and value, so a routine is something you can keep up.")]
def build_about(B):
    path = 'en/about.html'
    picks = ''.join(f'<div class="card white"><div class="num">0{i + 1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(ABOUT_PICKS))
    colls = ''.join(coll_card(k, short=True) for k in COLL_ORDER)
    body = f'''
<section class="hero"><div class="wrap">
  <div><div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>About</span></div><span class="eyebrow">About UHealthFit</span>
  <h1>Quality wellness, <em>chosen with care</em></h1><p class="lead">UHealthFit is the online home of WiseQuest — the brand's own store, run by Uhealth Trading Inc. in Middletown, New York. It was founded by health professionals with backgrounds in Chinese medicine, together with experienced partners in product development and manufacturing.</p>
  <div class="hero-cta"><a class="btn btn-primary" href="{L('en/products/index.html')}">Browse all products</a><a class="btn btn-ghost" href="{L('en/approach.html')}">Our approach to herbs</a></div></div>
  <div class="hero-visual"><img src="{U}/home/all-products-lineup.png" alt="The WiseQuest product lineup"></div>
</div></section>
<section class="sec"><div class="wrap" style="max-width:860px">
  <div class="sec-head"><span class="eyebrow">Why we started</span><h2>Better options for modern life</h2></div>
  <p class="lead" style="font-size:17px">Modern routines create their own everyday needs: eyes that work a full screen day, evenings that are hard to wind down, desk days that leave digestion sluggish, energy that dips by mid-afternoon, skin that reacts when the seasons change.</p>
  <p class="lead" style="font-size:17px;margin-top:14px">So we started with a simple idea: begin with the needs people actually have, find products worth keeping in a routine — and be straight about ingredients, directions and expectations.</p>
</div></section>
<section class="sec doctor bg-dark" id="dr-huang"><div class="wrap">
  <div><img src="{U}/home/dr-h.png" alt="Dr. Huang" loading="lazy"></div>
  <div><span class="eyebrow">Developed with Dr. Huang</span><h2>Meet the practitioner behind the formulas</h2>
  <p>Dr. Huang is a New York State–licensed acupuncturist with two decades of practice and botanical-formulation experience. She graduated from the China Academy of Chinese Medical Sciences and was selected to continue the teachings of renowned physicians in Beijing, studying herbal and acupuncture methods with nationally recognized practitioners.</p>
  <p style="margin-top:12px">Her practice has spanned digestion, sleep and stress, skin and more, using herbs, acupuncture and related methods. After two decades researching botanical skincare, she holds a Chinese national invention patent for a herbal cosmetic formula she developed.</p>
  <p style="margin-top:12px">Every WiseQuest formula starts from the way she practices: look at the whole person, and support the body rather than override it.</p></div>
</div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Naturally sourced · professionally formulated</span><h2>How we select products</h2><p class="lead">We look beyond the word “natural”: where ingredients come from, how they're formulated, how products are made, and whether they offer meaningful everyday value.</p></div>
  <div class="grid-5">{picks}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Focused on everyday health</span><h2>Six collections, one approach</h2></div>
  <div class="grid-3">{colls}</div>
</div></section>
<section class="sec bg-green-light"><div class="wrap" style="max-width:860px">
  <div class="sec-head"><span class="eyebrow">About this site</span><h2>A guide to the WiseQuest line</h2></div>
  <p class="lead" style="font-size:17px">us.uhealthfit.com explains the WiseQuest line — product details, ingredient explainers and buying guides. When you're ready to buy, every button opens the matching product page on uhealthfit.com for secure checkout. Questions about an order, shipping or returns: <a href="mailto:service@uhealthfit.com" style="color:var(--green);font-weight:700">service@uhealthfit.com</a>, or see the <a href="{L('en/faq.html')}" style="color:var(--green);font-weight:700">FAQ</a>.</p>
</div></section>
{journey('about')}
{sticky()}
'''
    B.write(path, head(B, 'About UHealthFit & Dr. Huang | The Home of WiseQuest', 'UHealthFit is the online home of WiseQuest, run by Uhealth Trading Inc. in New York. Formulas developed with Dr. Huang, a New York State–licensed acupuncturist.', path, 'en-about') + nav('about') + body + footer(B))

FAQS = {
 'Products & use': [
  ("Are these medicines? Can they replace what my doctor prescribed?", "No. The capsules are dietary supplements and the eye patches, creams and serum are cosmetics. None of them is a medicine, and none replaces a diagnosis, treatment or prescription. If you take medication, are pregnant or nursing, or have a health concern, talk to your doctor before use."),
  ("How long until I notice anything?", "We don't promise timelines. Herbal formulas are designed for steady daily use, and individual experiences vary."),
  ("How do I take the capsules?", "Most are 3 capsules twice a day with meals (Calmoon: with lunch and with dinner). Each bottle holds 180 capsules. Every product page has exact directions."),
  ("Can I combine products from different collections?", "Many people do — the eye patches and LumiView, for example. If you take several supplements or any prescription medication, check with your doctor or pharmacist first."),
  ("Do the eye patches go in my eyes?", "No. They sit on the skin at the inner corner, outer corner and below each eye. The cooling ingredients can make some people's eyes water a little; if you feel stinging or irritation, remove the patches and rinse with water. Patch test first; not for anyone under 18, pregnant or nursing, taking blood thinners or planning eye surgery within 2 weeks."),
  ("Are the capsules vegan?", "The capsule shells are plant-based (HPMC). Check each product's ingredient list for details.")],
 'Quality & safety': [
  ("Where are the products made?", "The eye patches are made in Japan. Capsules, creams and the serum are made in the USA with imported botanical ingredients, in cGMP facilities, and finished products are third-party tested for purity."),
  ("What does “FDA-registered facility” mean?", "It means the manufacturing facility is registered with the FDA. That isn't FDA approval — dietary supplements and cosmetics are not approved by the FDA before sale."),
  ("What about contaminants in Chinese herbs?", "It's a fair question for any imported botanical. Our finished products are third-party tested for purity. For product-specific questions, email service@uhealthfit.com."),
  ("Could these interact with my medication?", "Possibly. Several botanicals, including salvia, dong quai and schisandra, can interact with blood thinners such as warfarin, and Calmoon shouldn't be combined with sedatives without medical advice. Bring the label to your doctor or pharmacist.")],
 'Buying, shipping & returns': [
  ("Can I check out on this site?", "No. This site helps you choose; every Buy button opens the matching product page on uhealthfit.com — WiseQuest's own store — for secure checkout with major cards, Apple Pay, Google Pay or Shop Pay."),
  ("How much is shipping, and how fast is it?", "Orders are handled within 48 business hours. US shipping is free on eye patches over $79 and on everything else over $200; otherwise the cost is shown at checkout. Eye patches ship from a warehouse near you; capsules and skincare ship by USPS from the US warehouse, so a mixed order can arrive in separate parcels."),
  ("Can I return something?", "Unopened items can be returned within 30 days. Email service@uhealthfit.com to start a return, and see the refund policy on uhealthfit.com for details."),
  ("What does the $6 trial include?", "Two nights of WiseQuest Eye Patches, shipping included.")],
 'About us': [
  ("How are UHealthFit and WiseQuest related?", "UHealthFit is the online home of WiseQuest — the brand's own store, run by Uhealth Trading Inc. in Middletown, New York."),
  ("Who is Dr. Huang?", "A New York State–licensed acupuncturist with two decades of practice and botanical-formulation experience, who developed the WiseQuest formulas."),
  ("How accurate is the quiz?", "It ranks the six collections from your answers to help you decide where to start. It's for orientation only — not a medical assessment.")],
}
def build_faq(B):
    path = 'en/faq.html'
    groups = ''.join(f'<div class="faq-group"><h3>{esc(g)}</h3>{faq_block(items)}</div>' for g, items in FAQS.items())
    allq = [q for items in FAQS.values() for q in items]
    body = f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div><div class="crumbs"><a href="{L('en/index.html')}">Home</a><span>›</span><span>FAQ</span></div><span class="eyebrow">FAQ</span><h1>Questions before you buy</h1><p class="lead" style="max-width:720px">Products, quality, safety, shipping and returns. Can't find your answer? Email service@uhealthfit.com.</p></div></div></section>
<section class="sec"><div class="wrap"><div class="faq-list">{groups}</div></div></section>
{journey('faq')}
{sticky()}
<script type="application/ld+json">{faq_ld(allq)}</script>
'''
    B.write(path, head(B, 'FAQ: Products, Safety, Shipping & Returns | UHealthFit × WiseQuest', 'Are WiseQuest products medicines? How do you take them, where are they made, how are they tested, and how do shipping and returns work? Answers here.', path, 'en-faq') + nav('faq') + body + footer(B))

def build_404(B):
    # Cloudflare Pages serves the nearest 404.html: /en/anything-missing gets this page with HTTP 404
    path = 'en/404.html'
    body = f'''<section class="hero"><div class="wrap">
  <div><span class="eyebrow">404 · Page not found</span>
    <h1>This page doesn't exist, <em>but what you're after might</em></h1>
    <p class="lead">The address may have changed, or there may be a typo. Head home, or start from one of these.</p>
    <div class="hero-cta"><a class="btn btn-primary" href="{L('en/index.html')}">Home</a><a class="btn btn-ghost" href="{L('en/collections/index.html')}">Shop by concern</a><a class="btn btn-ghost" href="{L('en/guides/index.html')}">Guides</a></div>
  </div>
</div></section>
'''
    B.write(path, head(B, 'Page not found | UHealthFit', 'This page does not exist. Return to UHealthFit or browse WiseQuest collections and guides.', path, '404', noindex=True) + nav('') + body + footer(B))

def build(B):
    """Build every English page. Returns the indexable paths for the sitemap."""
    build_home(B); build_collections(B); build_collections_index(B); build_products(B); build_products_index(B)
    build_guides(B); build_quiz(B); build_approach(B); build_about(B); build_faq(B); build_404(B)
    return (['en/index.html', 'en/collections/index.html'] + [cpath(k) for k in COLL_ORDER] + ['en/products/index.html'] + [ppath(s) for s in PRODUCT_ORDER]
            + ['en/guides/index.html'] + [gpath(p['slug']) for p in POSTS] + ['en/quiz.html', 'en/approach.html', 'en/about.html', 'en/faq.html'])
