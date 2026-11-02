// 2027 節氣養生月曆封面（深綠底＋四季圓環＋紅色「順時」印章）
// 用法：swift build-src/covers/calendar-cover.swift <輸出.jpg>   （2448×3168，Letter 比例）
import AppKit

let W: CGFloat = 612, H: CGFloat = 792, S: CGFloat = 4
func hex(_ s: String, _ a: CGFloat = 1) -> NSColor {
    var v: UInt64 = 0; Scanner(string: String(s.dropFirst())).scanHexInt64(&v)
    return NSColor(srgbRed: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: a)
}
let GOLD = hex("#D4B06A"), CREAM = hex("#F3EBD6"), WHITE = hex("#FFF8E6")
let serifB = { (s: CGFloat) in NSFont(name: "STSongti-TC-Bold", size: s)! }
let serifR = { (s: CGFloat) in NSFont(name: "STSongti-TC-Regular", size: s)! }
let sans = { (s: CGFloat, w: String) in NSFont(name: "PingFangTC-\(w)", size: s)! }

let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W * S), pixelsHigh: Int(H * S), bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
let base = NSGraphicsContext(bitmapImageRep: rep)!
let cg = base.cgContext
cg.translateBy(x: 0, y: H * S); cg.scaleBy(x: S, y: -S)   // 左上為原點、單位 = 1/72 吋
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: true)

// 置中文字；y 為基線；kern 為字距；heavy 為描邊加粗（宋體 Bold 偏細，用負值同時填色＋描邊）
func text(_ s: String, _ f: NSFont, _ c: NSColor, cx: CGFloat, y: CGFloat, kern: CGFloat = 0, heavy: CGFloat = 0) {
    var at: [NSAttributedString.Key: Any] = [.font: f, .foregroundColor: c, .kern: kern]
    if heavy > 0 { at[.strokeWidth] = -heavy; at[.strokeColor] = c }
    let a = NSAttributedString(string: s, attributes: at)
    let w = a.size().width - kern
    a.draw(at: CGPoint(x: cx - w / 2, y: y - f.ascender))
}
func pt(_ cx: CGFloat, _ cy: CGFloat, _ r: CGFloat, _ deg: CGFloat) -> CGPoint {
    let a = (deg - 90) * .pi / 180; return CGPoint(x: cx + r * cos(a), y: cy + r * sin(a))
}
func strokeRect(_ r: CGRect, _ c: NSColor, _ w: CGFloat, radius: CGFloat = 0) {
    cg.setStrokeColor(c.cgColor); cg.setLineWidth(w)
    cg.addPath(CGPath(roundedRect: r, cornerWidth: radius, cornerHeight: radius, transform: nil)); cg.strokePath()
}

// 背景：深綠放射漸層
let grad = CGGradient(colorsSpace: CGColorSpaceCreateDeviceRGB(), colors: [hex("#1F5E3C").cgColor, hex("#123F27").cgColor, hex("#0B2C1B").cgColor] as CFArray, locations: [0, 0.6, 1])!
cg.drawRadialGradient(grad, startCenter: CGPoint(x: W / 2, y: H * 0.28), startRadius: 0, endCenter: CGPoint(x: W / 2, y: H * 0.28), endRadius: 600, options: [.drawsAfterEndLocation])
strokeRect(CGRect(x: 26, y: 26, width: W - 52, height: H - 52), GOLD.withAlphaComponent(0.75), 1)
strokeRect(CGRect(x: 31, y: 31, width: W - 62, height: H - 62), GOLD.withAlphaComponent(0.5), 0.5)

// 金色細枝葉
func branch(_ x: CGFloat, _ y: CGFloat, rot: CGFloat, flip: Bool) {
    cg.saveGState(); cg.translateBy(x: x, y: y); cg.rotate(by: rot * .pi / 180); if flip { cg.scaleBy(x: -1, y: 1) }
    cg.setStrokeColor(GOLD.withAlphaComponent(0.85).cgColor); cg.setLineWidth(1.1)
    let stem = CGMutablePath(); stem.move(to: .zero); stem.addCurve(to: CGPoint(x: -2, y: -120), control1: CGPoint(x: 2, y: -40), control2: CGPoint(x: 1, y: -80))
    cg.addPath(stem); cg.strokePath()
    cg.strokeEllipse(in: CGRect(x: -6, y: -128, width: 8, height: 8))
    for (yy, d) in [(-20.0, -1.0), (-45, 1), (-68, -1), (-92, 1)] as [(CGFloat, CGFloat)] {
        let p = CGMutablePath(); let o = CGPoint(x: 0.3 * yy / 40, y: yy)
        p.move(to: o)
        p.addQuadCurve(to: CGPoint(x: o.x + d * 38, y: o.y - 6), control: CGPoint(x: o.x + d * 16, y: o.y - 14))
        p.addQuadCurve(to: o, control: CGPoint(x: o.x + d * 20, y: o.y + 6))
        p.closeSubpath()
        cg.addPath(p); cg.setFillColor(GOLD.withAlphaComponent(0.12).cgColor); cg.fillPath()
        cg.addPath(p); cg.strokePath()
    }
    cg.restoreGState()
}
branch(70, 230, rot: -8, flip: false)
branch(548, 640, rot: 10, flip: true)

text("優健堂 UHealthFit × WiseQuest", sans(12.5, "Semibold"), CREAM, cx: W / 2, y: 76, kern: 2.2)

// 四季圓環：每季 6 個點 = 24 節氣
let cx = W / 2, cy: CGFloat = 268, R: CGFloat = 150
let offs: [CGFloat] = [-32, -22, -12, 12, 22, 32]
cg.setStrokeColor(GOLD.withAlphaComponent(0.8).cgColor); cg.setLineWidth(0.8)
cg.strokeEllipse(in: CGRect(x: cx - R - 20, y: cy - R - 20, width: 2 * (R + 20), height: 2 * (R + 20)))
for (name, c, col) in [("春", 0.0, "#A3C37A"), ("夏", 90, "#E0B65C"), ("秋", 180, "#CD8352"), ("冬", 270, "#86A6B4")] as [(String, CGFloat, String)] {
    cg.setStrokeColor(GOLD.cgColor); cg.setLineWidth(1)
    for o in offs { cg.move(to: pt(cx, cy, R + 20, c + o)); cg.addLine(to: pt(cx, cy, R + 27, c + o)) }
    cg.strokePath()
    let p = CGMutablePath(); p.move(to: pt(cx, cy, R, c - 40))
    for i in 1...80 { p.addLine(to: pt(cx, cy, R, c - 40 + CGFloat(i))) }
    cg.addPath(p); cg.setStrokeColor(hex(col, 0.95).cgColor); cg.setLineWidth(15); cg.setLineCap(.round); cg.strokePath()
    cg.setFillColor(WHITE.withAlphaComponent(0.9).cgColor)
    for o in offs { let q = pt(cx, cy, R, c + o); cg.fillEllipse(in: CGRect(x: q.x - 2.2, y: q.y - 2.2, width: 4.4, height: 4.4)) }
    let t = pt(cx, cy, R, c); text(name, serifB(22), WHITE, cx: t.x, y: t.y + 8, heavy: 4)
}
let inner = CGGradient(colorsSpace: CGColorSpaceCreateDeviceRGB(), colors: [hex("#1A5134").cgColor, hex("#103721").cgColor] as CFArray, locations: [0, 1])!
cg.saveGState(); cg.addEllipse(in: CGRect(x: cx - R + 22, y: cy - R + 22, width: 2 * (R - 22), height: 2 * (R - 22))); cg.clip()
cg.drawRadialGradient(inner, startCenter: CGPoint(x: cx, y: cy - 30), startRadius: 0, endCenter: CGPoint(x: cx, y: cy - 30), endRadius: 160, options: [.drawsAfterEndLocation])
cg.restoreGState()
cg.setStrokeColor(GOLD.cgColor); cg.setLineWidth(0.8); cg.strokeEllipse(in: CGRect(x: cx - R + 22, y: cy - R + 22, width: 2 * (R - 22), height: 2 * (R - 22)))
cg.setStrokeColor(GOLD.withAlphaComponent(0.6).cgColor); cg.setLineWidth(0.4); cg.strokeEllipse(in: CGRect(x: cx - R + 28, y: cy - R + 28, width: 2 * (R - 28), height: 2 * (R - 28)))
text("二十四節氣", sans(12, "Semibold"), GOLD, cx: cx, y: cy - 38, kern: 6)
text("2027", serifR(70), GOLD, cx: cx, y: cy + 26, kern: 3)
text("草本養生月曆", sans(12, "Medium"), CREAM, cx: cx, y: cy + 58, kern: 5)

// 標題＋印章
let ty: CGFloat = 520
text("跟著節氣，", serifB(44), .white, cx: cx, y: ty, heavy: 3.5)
text("過好每一天", serifB(44), .white, cx: cx, y: ty + 56, heavy: 3.5)
cg.saveGState(); cg.translateBy(x: 452, y: 505); cg.rotate(by: -6 * .pi / 180)
cg.setFillColor(hex("#B5402F").cgColor); cg.addPath(CGPath(roundedRect: CGRect(x: -19, y: -19, width: 38, height: 38), cornerWidth: 4, cornerHeight: 4, transform: nil)); cg.fillPath()
strokeRect(CGRect(x: -16, y: -16, width: 32, height: 32), hex("#F7D9CF"), 0.8, radius: 2)
text("順", serifB(13), hex("#FFF1EA"), cx: 0, y: -2, heavy: 4); text("時", serifB(13), hex("#FFF1EA"), cx: 0, y: 13, heavy: 4)
cg.restoreGState()

// 分隔飾線
let dy = ty + 92
cg.setStrokeColor(GOLD.cgColor); cg.setLineWidth(0.8)
cg.move(to: CGPoint(x: cx - 120, y: dy)); cg.addLine(to: CGPoint(x: cx - 22, y: dy))
cg.move(to: CGPoint(x: cx + 22, y: dy)); cg.addLine(to: CGPoint(x: cx + 120, y: dy)); cg.strokePath()
cg.setLineWidth(0.9); cg.strokeEllipse(in: CGRect(x: cx - 4.5, y: dy - 8, width: 9, height: 16))
cg.setLineWidth(0.8)
cg.strokeEllipse(in: CGRect(x: cx - 14, y: dy - 5.5, width: 6, height: 11)); cg.strokeEllipse(in: CGRect(x: cx + 8, y: dy - 5.5, width: 6, height: 11))

// 24 節氣格子
let terms = "小寒 大寒 立春 雨水 驚蟄 春分 清明 穀雨 立夏 小滿 芒種 夏至 小暑 大暑 立秋 處暑 白露 秋分 寒露 霜降 立冬 小雪 大雪 冬至".split(separator: " ").map(String.init)
let bw: CGFloat = 52, bh: CGFloat = 26, gx: CGFloat = 7, gy: CGFloat = 7, x0 = cx - (8 * bw + 7 * gx) / 2, y0: CGFloat = 648
for (i, t) in terms.enumerated() {
    let x = x0 + CGFloat(i % 8) * (bw + gx), y = y0 + CGFloat(i / 8) * (bh + gy)
    let r = CGRect(x: x, y: y, width: bw, height: bh)
    cg.setFillColor(NSColor(white: 1, alpha: 0.04).cgColor); cg.addPath(CGPath(roundedRect: r, cornerWidth: 3, cornerHeight: 3, transform: nil)); cg.fillPath()
    strokeRect(r, GOLD.withAlphaComponent(0.95), 0.8, radius: 3)
    text(t, sans(12.5, "Regular"), CREAM, cx: x + bw / 2 + 0.5, y: y + 17.5, kern: 1)
}

NSGraphicsContext.current = nil
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "calendar-cover.jpg"
try! rep.representation(using: .jpeg, properties: [.compressionFactor: 0.9])!.write(to: URL(fileURLWithPath: out))
print("→ \(out)")
