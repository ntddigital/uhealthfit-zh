// Cloudflare Pages Function — runs only for /en/* (the English pages).
// Sets the same geo cookie uhealthfit.com's edge sets (uh-ip-country = "US-WA", "FR", ...), so the
// English pages can apply uhealthfit.com's consent rules: GTM (GA4 + Meta Pixel) loads right away where
// consent isn't required, and waits for the visitor's choice in the EU/UK and in WA, NV and CT
// (consumer-health-data laws). If this function doesn't run, the pages fail safe: the consent
// banner is shown and nothing loads until the visitor chooses.
export async function onRequest(context) {
  const res = await context.next();
  try {
    const cf = context.request.cf || {};
    const type = res.headers.get('content-type') || '';
    if (!cf.country || !type.includes('text/html')) return res;
    const value = cf.regionCode ? `${cf.country}-${cf.regionCode}` : cf.country;
    const out = new Response(res.body, res);
    out.headers.append('Set-Cookie', `uh-ip-country=${encodeURIComponent(value)}; Path=/; Max-Age=86400; SameSite=Lax; Secure`);
    return out;
  } catch (e) {
    return res;
  }
}
