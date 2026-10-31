// 選購指南文章封面：1200×675 JPEG，輸出到 build-src/src/img/post-<slug>.jpg
// 背景：build-src/covers/bg/（設計好的情境圖）；產品與草本實拍：先跑 sh build-src/covers/fetch.sh
// 用法（在 repo 根目錄）：swift build-src/covers/covers.swift [slug]   不加 slug = 全部重畫
import AppKit

let W: CGFloat = 1200, H: CGFloat = 675
let HERE = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent().path
let SRC = "\(HERE)/src", BG = "\(HERE)/bg", OUT = "\(HERE)/../src/img"
let ONLY = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : nil

func hex(_ s: String, _ a: CGFloat = 1) -> NSColor {
    var v: UInt64 = 0; Scanner(string: s.replacingOccurrences(of: "#", with: "")).scanHexInt64(&v)
    return NSColor(srgbRed: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: a)
}
func font(_ size: CGFloat, _ weight: String = "Semibold") -> NSFont {
    NSFont(name: "PingFangTC-\(weight)", size: size) ?? NSFont.systemFont(ofSize: size, weight: weight == "Regular" ? .regular : .semibold)
}

struct Palette { let accent, ink: NSColor }
let PAL: [String: Palette] = [
    "eye": Palette(accent: hex("#1A6B3A"), ink: hex("#08200F")), "skin": Palette(accent: hex("#006B6B"), ink: hex("#062A2A")),
    "sleep": Palette(accent: hex("#2A3A6B"), ink: hex("#141C38")), "vitality": Palette(accent: hex("#8B3A1A"), ink: hex("#3A1A0A")),
    "general": Palette(accent: hex("#1A6B3A"), ink: hex("#08200F")), "thanks": Palette(accent: hex("#8E3B16"), ink: hex("#3B1607")),
]

// ── 繪圖小工具（座標原點在左上）
func fillRect(_ r: CGRect, _ c: NSColor, radius: CGFloat = 0) { c.setFill(); NSBezierPath(roundedRect: r, xRadius: radius, yRadius: radius).fill() }
func circle(_ c: CGPoint, _ rad: CGFloat, _ col: NSColor) { col.setFill(); NSBezierPath(ovalIn: CGRect(x: c.x - rad, y: c.y - rad, width: rad * 2, height: rad * 2)).fill() }
func withShadow(_ alpha: CGFloat = 0.2, blur: CGFloat = 28, dy: CGFloat = -12, _ body: () -> Void) {
    NSGraphicsContext.saveGraphicsState()
    let sh = NSShadow(); sh.shadowColor = NSColor(white: 0, alpha: alpha); sh.shadowBlurRadius = blur; sh.shadowOffset = NSSize(width: 0, height: dy); sh.set()
    body(); NSGraphicsContext.restoreGraphicsState()
}
@discardableResult
func text(_ s: String, _ f: NSFont, _ c: NSColor, _ r: CGRect, align: NSTextAlignment = .left, line: CGFloat = 1.18) -> CGFloat {
    let p = NSMutableParagraphStyle(); p.alignment = align; p.lineHeightMultiple = line; p.lineBreakMode = .byWordWrapping
    let a = NSAttributedString(string: s, attributes: [.font: f, .foregroundColor: c, .paragraphStyle: p])
    let h = a.boundingRect(with: CGSize(width: r.width, height: 2000), options: [.usesLineFragmentOrigin, .usesFontLeading]).height
    a.draw(with: CGRect(x: r.minX, y: r.minY, width: r.width, height: h + 4), options: [.usesLineFragmentOrigin, .usesFontLeading])
    return h
}
func textWidth(_ s: String, _ f: NSFont) -> CGFloat { NSAttributedString(string: s, attributes: [.font: f]).size().width }
func label(_ s: String, centerX: CGFloat, y: CGFloat, size: CGFloat = 22, color: NSColor) {
    let f = font(size); let w = textWidth(s, f)
    text(s, f, color, CGRect(x: centerX - w / 2 - 2, y: y, width: w + 6, height: size * 1.6))
}
func chip(_ s: String, centerX: CGFloat, y: CGFloat, _ pal: Palette, size: CGFloat = 19) {
    let f = font(size); let w = textWidth(s, f) + 28
    withShadow(0.12, blur: 12, dy: -4) { fillRect(CGRect(x: centerX - w / 2, y: y, width: w, height: size + 19), .white, radius: (size + 19) / 2) }
    text(s, f, pal.accent, CGRect(x: centerX - w / 2 + 14, y: y + 7, width: w, height: size + 10))
}
func panel(_ r: CGRect, alpha: CGFloat = 0.78) { withShadow(0.14, blur: 30, dy: -10) { fillRect(r, NSColor(white: 1, alpha: alpha), radius: 24) } }
func load(_ path: String) -> NSImage {
    guard let i = NSImage(contentsOfFile: path) else { fatalError("缺少素材 \(path)；請先執行 sh build-src/covers/fetch.sh") }
    return i
}
// 等比縮放放進框內（不裁切），底部對齊，可加陰影
@discardableResult
func imageFit(_ name: String, _ r: CGRect, shadow: Bool = true, anchorBottom: Bool = true) -> CGRect {
    let img = load("\(SRC)/\(name).png"); let s = min(r.width / img.size.width, r.height / img.size.height)
    let w = img.size.width * s, h = img.size.height * s
    let dst = CGRect(x: r.midX - w / 2, y: anchorBottom ? r.maxY - h : r.midY - h / 2, width: w, height: h)
    let draw = { img.draw(in: dst, from: .zero, operation: .sourceOver, fraction: 1, respectFlipped: true, hints: [.interpolation: NSImageInterpolation.high]) }
    if shadow { withShadow { draw() } } else { draw() }
    return dst
}
// 草本實拍是白底：放在白色卡片上，下方標名稱
func herbCard(_ name: String, _ title: String, _ r: CGRect, _ pal: Palette) {
    withShadow(0.16, blur: 26, dy: -10) { fillRect(r, .white, radius: 22) }
    imageFit(name, CGRect(x: r.minX + 14, y: r.minY + 14, width: r.width - 28, height: r.height - 64), shadow: false, anchorBottom: false)
    label(title, centerX: r.midX, y: r.maxY - 46, size: 24, color: pal.accent)
}

// ── 版型：背景照片＋左側文字
struct Cover { let slug, pal, bg, pillText, title, sub: String; let titleSize, textWidth: CGFloat; var dark = false; let draw: (Palette) -> Void }

func base(_ c: Cover) {
    let pal = PAL[c.pal]!
    load("\(BG)/\(c.bg).webp").draw(in: CGRect(x: 0, y: 0, width: W, height: H), from: .zero, operation: .copy, fraction: 1, respectFlipped: true, hints: [.interpolation: NSImageInterpolation.high])
    // 左側柔光（深色背景用暗色），讓標題清楚
    let wash = c.dark ? [NSColor(white: 0, alpha: 0.5), NSColor(white: 0, alpha: 0.25), NSColor(white: 0, alpha: 0)]
                      : [NSColor(white: 1, alpha: 0.82), NSColor(white: 1, alpha: 0.5), NSColor(white: 1, alpha: 0)]
    NSGradient(colors: wash, atLocations: [0, 0.42, 0.68], colorSpace: .sRGB)!.draw(in: CGRect(x: 0, y: 0, width: W, height: H), angle: 0)
    let ink = c.dark ? NSColor.white : pal.ink
    let f = font(20); let pw = textWidth(c.pillText, f) + 34
    fillRect(CGRect(x: 72, y: 74, width: pw, height: 40), c.dark ? hex("#C9A15A") : pal.accent, radius: 20)
    text(c.pillText, f, .white, CGRect(x: 89, y: 82, width: pw, height: 30))
    let th = text(c.title, font(c.titleSize), ink, CGRect(x: 72, y: 134, width: c.textWidth, height: 400), line: 1.08)
    fillRect(CGRect(x: 74, y: 134 + th + 18, width: 56, height: 5), c.dark ? hex("#C9A15A") : pal.accent, radius: 2.5)
    text(c.sub, font(25, "Regular"), ink.withAlphaComponent(c.dark ? 0.88 : 0.8), CGRect(x: 72, y: 134 + th + 40, width: c.textWidth, height: 200), line: 1.25)
    text("優健堂 UHealthFit × WiseQuest", font(19), c.dark ? hex("#E8C98A") : pal.accent, CGRect(x: 72, y: H - 70, width: 500, height: 30))
    c.draw(pal)
}

let covers: [Cover] = [
    Cover(slug: "eye-cream-buying-guide", pal: "eye", bg: "vanity-pink", pillText: "選購指南 · 護眼保健", title: "眼霜怎麼選？", sub: "白天的眼周保養：\n保濕、舒緩，擦了就能走", titleSize: 66, textWidth: 520) { pal in
        imageFit("products_herbal-soothing-repair-eye-cream_eye-cream-product-shot-wide", CGRect(x: 600, y: 95, width: 560, height: 470))
        for (i, s) in ["保濕", "舒緩", "米粒大小", "開封 6 個月內"].enumerated() { chip(s, centerX: CGFloat([672, 762, 872, 1028][i]), y: 590, pal) }
    },
    Cover(slug: "eye-patch-which-pack-to-buy", pal: "eye", bg: "eye-spa", pillText: "選購指南 · 護眼保健", title: "冷敷眼貼買哪一盒？", sub: "從兩晚體驗裝到 9 盒，每晚約 $2.6–$3", titleSize: 54, textWidth: 1000) { pal in
        panel(CGRect(x: 195, y: 318, width: 910, height: 270))
        let items: [(String, String, String, CGFloat)] = [("products_eye-patches_2-day-trial", "體驗裝", "2 晚", 100), ("products_eye-patches_eye-patches-box-front", "1 盒", "10 晚", 120),
                                                       ("products_eye-patches_3-boxes", "3 盒", "30 晚", 140), ("products_eye-patches_six-boxes", "6 盒", "60 晚", 155), ("products_eye-patches_9-boxes", "9 盒", "90 晚", 170)]
        for (i, it) in items.enumerated() {
            let cx = 300 + CGFloat(i) * 175
            imageFit(it.0, CGRect(x: cx - 80, y: 500 - it.3, width: 160, height: it.3))
            label(it.1, centerX: cx, y: 510, size: 22, color: pal.ink)
            label(it.2, centerX: cx, y: 542, size: 19, color: pal.accent)
        }
    },
    Cover(slug: "contact-lens-eye-drops-eye-patch-guide", pal: "eye", bg: "eye-spa", pillText: "使用教學 · 護眼保健", title: "隱形眼鏡、眼藥水、眼貼的睡前順序", sub: "五個步驟，一張圖看懂", titleSize: 50, textWidth: 1000) { pal in
        panel(CGRect(x: 60, y: 325, width: 1080, height: 262))
        let steps = [("👓", "洗手、\n取下鏡片"), ("🫧", "卸妝、\n洗臉"), ("💧", "需要的話\n點眼藥水"), ("⏱️", "等約\n30 分鐘"), ("🌙", "貼上\n冷敷眼貼")]
        for (i, s) in steps.enumerated() {
            let cx = 160 + CGFloat(i) * 220, cy: CGFloat = 410
            if i < 4 { fillRect(CGRect(x: cx + 62, y: cy - 2, width: 96, height: 4), pal.accent.withAlphaComponent(0.35), radius: 2) }
            withShadow(0.1, blur: 14, dy: -4) { circle(CGPoint(x: cx, y: cy), 62, .white) }
            text(s.0, NSFont(name: "Apple Color Emoji", size: 50) ?? font(50), .black, CGRect(x: cx - 34, y: cy - 36, width: 80, height: 70))
            circle(CGPoint(x: cx - 46, y: cy - 46), 18, pal.accent)
            label("\(i + 1)", centerX: cx - 46, y: cy - 60, size: 20, color: .white)
            text(s.1, font(21), pal.ink, CGRect(x: cx - 80, y: cy + 76, width: 160, height: 70), align: .center)
        }
    },
    Cover(slug: "herbal-skincare-which-cream-and-order", pal: "skin", bg: "vanity-pink", pillText: "選購指南 · 肌膚健康", title: "修護霜、淨顏霜、\n精華液怎麼選？", sub: "依膚況挑選，\n擦的順序也一次看懂", titleSize: 54, textWidth: 500) { pal in
        let items = [("products_herbal-soothing-repair-cream_herbal-soothing-repair-cream-jar-front", "乾燥・敏感"),
                     ("products_herbal-clarifying-cream_herbal-clarifying-cream-jar-front", "出油・易長痘"),
                     ("products_herbal-lifting-revitalizing-serum_herbal-lifting-revitalizing-serum-bottle-front", "疲倦・想要光澤")]
        for (i, it) in items.enumerated() {
            let cx = 680 + CGFloat(i) * 175
            imageFit(it.0, CGRect(x: cx - 82, y: 180, width: 164, height: 330))
            chip(it.1, centerX: cx, y: 532, pal)
        }
    },
    Cover(slug: "herbal-supplement-safety-checklist", pal: "general", bg: "green-desk", pillText: "安心清單 · 日常保健", title: "吃草本保健品前，\n先確認這 6 件事", sub: "服藥、孕期、手術前；\n看醫師時，帶上這張清單", titleSize: 54, textWidth: 520) { pal in
        let card = CGRect(x: 640, y: 70, width: 470, height: 535)
        withShadow(0.18, blur: 30, dy: -12) { fillRect(card, .white, radius: 22) }
        fillRect(CGRect(x: card.minX, y: card.minY, width: card.width, height: 76), pal.accent, radius: 22)
        fillRect(CGRect(x: card.minX, y: card.minY + 50, width: card.width, height: 26), pal.accent)
        text("服用前確認清單", font(26), .white, CGRect(x: card.minX + 30, y: card.minY + 20, width: 400, height: 40))
        for (i, r) in ["正在吃哪些藥", "懷孕、哺乳或準備懷孕", "近期要動手術", "年齡與用藥數量", "已在吃的其他保健品", "過敏史與體質"].enumerated() {
            let y = card.minY + 104 + CGFloat(i) * 70
            pal.accent.setStroke(); let b = NSBezierPath(roundedRect: CGRect(x: card.minX + 32, y: y, width: 30, height: 30), xRadius: 7, yRadius: 7); b.lineWidth = 3; b.stroke()
            text(r, font(23, "Regular"), pal.ink, CGRect(x: card.minX + 80, y: y - 2, width: 360, height: 40))
            if i < 5 { fillRect(CGRect(x: card.minX + 32, y: y + 50, width: card.width - 64, height: 1), hex("#E2E6D3")) }
        }
    },
    Cover(slug: "suanzaoren-calming-herbs-explained", pal: "sleep", bg: "bedroom-night", pillText: "成分百科 · 睡眠健康", title: "酸棗仁是什麼？", sub: "七味安神草本\n與「君臣佐使」一次看懂", titleSize: 62, textWidth: 520, dark: true) { pal in
        imageFit("products_calmoon_calmoon-ingredients-collage", CGRect(x: 560, y: 300, width: 360, height: 345))
        imageFit("products_calmoon_calmoon-bottle-front", CGRect(x: 880, y: 395, width: 230, height: 245))
    },
    Cover(slug: "cassia-chrysanthemum-goji-tea-or-capsule", pal: "eye", bg: "autumn-tea-window", pillText: "成分百科 · 護眼保健", title: "決明子、菊花、枸杞", sub: "泡茶和吃膠囊，怎麼選？", titleSize: 54, textWidth: 540) { pal in
        herbCard("ingredients_chrysanthemum", "菊花", CGRect(x: 600, y: 120, width: 200, height: 220), pal)
        herbCard("ingredients_goji", "枸杞", CGRect(x: 600, y: 360, width: 200, height: 220), pal)
        label("泡茶", centerX: 700, y: 590, size: 24, color: pal.ink)
        withShadow(0.18, blur: 14, dy: -4) { circle(CGPoint(x: 870, y: 350), 40, pal.accent) }
        label("VS", centerX: 870, y: 333, size: 24, color: .white)
        imageFit("products_lumiview_lumiview-bottle-front", CGRect(x: 925, y: 190, width: 240, height: 380))
        label("膠囊", centerX: 1045, y: 590, size: 24, color: pal.ink)
    },
    Cover(slug: "dendrobium-shihu-eye-cream-herb", pal: "eye", bg: "herbs-wood", pillText: "成分百科 · 護眼保健", title: "石斛是什麼？", sub: "眼霜裡的東方草本", titleSize: 66, textWidth: 520) { pal in
        herbCard("ingredients_dendrobium", "石斛", CGRect(x: 610, y: 90, width: 330, height: 380), pal)
        imageFit("products_herbal-soothing-repair-eye-cream_herbal-soothing-repair-eye-cream-jar-front", CGRect(x: 880, y: 350, width: 260, height: 270))
    },
    Cover(slug: "astragalus-huangqi-guide", pal: "vitality", bg: "herbs-wood", pillText: "成分百科 · 元氣活力", title: "黃芪是什麼？", sub: "日常調養常見草本入門", titleSize: 66, textWidth: 520) { pal in
        herbCard("ingredients_astragalus", "黃芪", CGRect(x: 610, y: 110, width: 340, height: 340), pal)
        imageFit("products_enerbalance_enerbalance-bottle-front", CGRect(x: 880, y: 300, width: 270, height: 330))
    },
    Cover(slug: "american-ginseng-cold-constitution", pal: "vitality", bg: "table-tea-notebook", pillText: "成分百科 · 元氣活力", title: "體質偏寒，可以吃西洋參嗎？", sub: "溫涼搭配的複方思路", titleSize: 54, textWidth: 1000) { pal in
        panel(CGRect(x: 110, y: 314, width: 980, height: 272), alpha: 1)
        let bar = CGRect(x: 150, y: 500, width: 900, height: 22)
        NSGradient(colors: [hex("#4F7FB8"), hex("#8FB7A0"), hex("#E0B060"), hex("#C2502A")])!.draw(in: NSBezierPath(roundedRect: bar, xRadius: 11, yRadius: 11), angle: 0)
        label("偏涼", centerX: bar.minX + 14, y: 530, size: 19, color: hex("#4F7FB8")); label("偏溫", centerX: bar.maxX - 14, y: 530, size: 19, color: hex("#C2502A"))
        for h in [("ingredients_panax-ginseng", "西洋參・偏涼", CGFloat(0.18)), ("ingredients_chinese-yam", "山藥・平", 0.5), ("ingredients_astragalus", "黃芪・溫", 0.82)] {
            let cx = bar.minX + bar.width * h.2
            imageFit(h.0, CGRect(x: cx - 95, y: 326, width: 190, height: 120), shadow: false, anchorBottom: false)
            circle(CGPoint(x: cx, y: bar.midY), 15, .white); circle(CGPoint(x: cx, y: bar.midY), 9, pal.accent)
            label(h.1, centerX: cx, y: 454, size: 22, color: pal.ink)
        }
    },
    Cover(slug: "poria-chinese-yam-everyday-herbs", pal: "vitality", bg: "autumn-tea-window", pillText: "成分百科 · 護眼＋元氣", title: "茯苓、山藥是什麼？", sub: "護眼和元氣配方裡\n都有的日常草本", titleSize: 56, textWidth: 520) { pal in
        herbCard("ingredients_poria", "茯苓", CGRect(x: 610, y: 150, width: 260, height: 300), pal)
        herbCard("ingredients_chinese-yam", "山藥", CGRect(x: 890, y: 150, width: 260, height: 300), pal)
    },
    Cover(slug: "thanksgiving-gift-for-parents-herbal", pal: "thanks", bg: "thanksgiving-table", pillText: "感恩節 · 送禮指南", title: "感恩節送爸媽什麼？", sub: "依日常需求，\n挑一份草本禮物", titleSize: 56, textWidth: 520) { pal in
        for it in [("products_eye-patches_eye-patches-box-front", CGRect(x: 735, y: 345, width: 100, height: 165)),
                   ("products_dentaforte_dentaforte-bottle-front", CGRect(x: 800, y: 362, width: 150, height: 150)),
                   ("products_enerbalance_enerbalance-bottle-front", CGRect(x: 875, y: 300, width: 205, height: 212)),
                   ("products_calmoon_calmoon-bottle-front", CGRect(x: 985, y: 362, width: 150, height: 150)),
                   ("products_herbal-soothing-repair-cream_herbal-soothing-repair-cream-jar-front", CGRect(x: 1110, y: 425, width: 88, height: 88))] { imageFit(it.0, it.1) }
    },
    Cover(slug: "thanksgiving-parents-supplement-schedule", pal: "thanks", bg: "table-tea-notebook", pillText: "感恩節 · 家庭保健", title: "幫爸媽排一張\n保健品時間表", sub: "回家這一趟，\n30 分鐘整理三步驟", titleSize: 56, textWidth: 480) { pal in
        let card = CGRect(x: 600, y: 64, width: 545, height: 545)
        withShadow(0.2, blur: 30, dy: -12) { fillRect(card, hex("#FFFDF8"), radius: 20) }
        text("爸媽的保健品時間表", font(26), pal.accent, CGRect(x: card.minX + 28, y: card.minY + 24, width: 480, height: 40))
        let colX: [CGFloat] = [258, 330, 402, 474]
        for (i, c) in ["早餐", "午餐", "晚餐", "睡前"].enumerated() { label(c, centerX: card.minX + colX[i], y: card.minY + 86, size: 19, color: pal.ink.withAlphaComponent(0.7)) }
        let rows: [(String, [Bool])] = [("明目膠囊", [true, false, true, false]), ("固齒膠囊", [true, false, true, false]), ("黑膏滋膠囊", [true, false, true, false]),
                                       ("潤暢膠囊", [true, false, true, false]), ("安睡膠囊", [false, true, false, true])]
        for (r, row) in rows.enumerated() {
            let y = card.minY + 140 + CGFloat(r) * 76
            fillRect(CGRect(x: card.minX + 24, y: y - 12, width: card.width - 48, height: 1), hex("#EAD9C2"))
            text(row.0, font(22, "Regular"), pal.ink, CGRect(x: card.minX + 28, y: y + 10, width: 200, height: 34))
            for (i, on) in row.1.enumerated() {
                let c = CGPoint(x: card.minX + colX[i], y: y + 26)
                if on { circle(c, 15, pal.accent); label("3", centerX: c.x, y: c.y - 14, size: 17, color: .white) } else { circle(c, 5, hex("#D9C4A6")) }
            }
        }
        text("每格 3 粒・隨餐", font(17, "Regular"), pal.ink.withAlphaComponent(0.6), CGRect(x: card.minX + 28, y: card.maxY - 40, width: 400, height: 28))
    },
    Cover(slug: "thanksgiving-feast-bloating-care", pal: "thanks", bg: "thanksgiving-table", pillText: "感恩節 · 腸胃舒暢", title: "感恩節大餐\n吃太飽？", sub: "節日飽脹感的日常照顧：\n慢慢吃、飯後走一走", titleSize: 60, textWidth: 520) { pal in
        imageFit("products_herbalflow_plan-dietary-fiber", CGRect(x: 690, y: 215, width: 310, height: 310))
        imageFit("products_herbalflow_herbalflow-bottle-front", CGRect(x: 920, y: 320, width: 230, height: 300))
    },
]

for c in covers where ONLY == nil || ONLY == c.slug {
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H), bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    let cg = NSGraphicsContext(bitmapImageRep: rep)!.cgContext
    cg.translateBy(x: 0, y: H); cg.scaleBy(x: 1, y: -1)
    NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: true)
    base(c)
    NSGraphicsContext.current = nil
    let jpg = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.84])!
    try! jpg.write(to: URL(fileURLWithPath: "\(OUT)/post-\(c.slug).jpg"))
    print("✓ post-\(c.slug).jpg \(jpg.count / 1024) KB")
}
