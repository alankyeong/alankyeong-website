from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
STAGING_OUTPUT = ROOT / "preview_dist"
OUTPUT = ROOT / "production_dist"
SITE_URL = "https://alankyeong.com/"


subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_preview.py")], check=True)

if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
shutil.copytree(STAGING_OUTPUT, OUTPUT)

privacy_shell = (OUTPUT / "privacy-policy" / "index.html").read_text(encoding="utf-8")
privacy_main = '''<main><header class="page-hero"><div class="wrap narrow"><p class="eyebrow">Effective 24 August 2026</p><h1>Privacy policy</h1><p class="lead">How personal information submitted through alankyeong.com is handled.</p></div></header><div class="page-body wrap narrow prose">
<p>This notice applies to alankyeong.com and professional enquiries made through this website. Alan Yeong is responsible for the personal data described below. It is intended to support the principles of Malaysia's Personal Data Protection Act 2010.</p>
<h2>Information collected</h2><p>When you submit an enquiry, the website collects your name, work email address, organisation (if provided), area of interest, relevant market or region, message and consent confirmation. Hosting and security systems may also process technical information such as IP address, browser type, timestamps and server logs.</p>
<h2>Why the information is used</h2><p>Information is used to receive, assess and respond to professional enquiries; communicate about a requested service, collaboration or opportunity; maintain security and prevent abuse; keep appropriate business records; and comply with legal obligations. Enquiry information is not added to a marketing list without separate consent.</p>
<h2>Disclosure and service providers</h2><p>Information may be processed by service providers needed to operate the website and email, including Hostinger. It may also be disclosed where required by law or reasonably necessary to protect legal rights and website security. Personal data is not sold.</p>
<h2>International processing</h2><p>Website hosting, email delivery or professional communications may involve processing in countries other than the country from which you submitted the enquiry. Reasonable steps are taken to use providers and safeguards appropriate to the nature of the information.</p>
<h2>Retention</h2><p>Unsuccessful or one-off enquiries are normally retained for no longer than 24 months after the last meaningful communication. Information connected to an ongoing business relationship may be retained for the relationship and any additional period required for legitimate business, accounting, dispute-resolution or legal purposes. Information is deleted or anonymised when it is no longer reasonably required.</p>
<h2>Security</h2><p>Reasonable administrative and technical measures are used to protect personal data. No internet transmission or storage system can be guaranteed to be completely secure.</p>
<h2>Your choices and rights</h2><p>You may request access to or correction of your personal data, withdraw consent where processing depends on consent, or ask that information no longer required be deleted. Some information may need to be retained where required by law or for legitimate legal and business purposes.</p>
<h2>Third-party websites</h2><p>Links to LinkedIn, Stripe and ai.alankyeong.com take you to separate services or properties with their own privacy practices. Stripe processes payment information on its own systems; alankyeong.com does not receive or store complete payment-card details.</p>
<h2>Contact</h2><p>For a privacy request or question, email <a href="mailto:hello@alankyeong.com">hello@alankyeong.com</a>. Identity may need to be reasonably verified before fulfilling a request.</p>
<h2>Changes to this notice</h2><p>This notice may be updated when the website's services, providers or legal obligations change. The effective date above will be revised when material changes are made.</p>
<hr><p class="eyebrow">Bahasa Malaysia</p><h2>Notis privasi</h2><p>Notis ini terpakai kepada alankyeong.com dan pertanyaan profesional yang dihantar melalui laman web ini. Alan Yeong bertanggungjawab terhadap data peribadi yang diterangkan di bawah.</p>
<h3>Data yang dikumpulkan dan tujuannya</h3><p>Apabila anda menghantar pertanyaan, laman web mengumpulkan nama, alamat e-mel kerja, organisasi (jika diberikan), bidang minat, pasaran atau rantau berkaitan, mesej dan pengesahan persetujuan. Sistem pengehosan dan keselamatan juga mungkin memproses alamat IP, jenis pelayar, masa akses dan log pelayan. Maklumat digunakan untuk menjawab pertanyaan, berkomunikasi mengenai perkhidmatan atau peluang yang diminta, menjaga keselamatan, mencegah penyalahgunaan, menyimpan rekod perniagaan yang wajar dan mematuhi undang-undang.</p>
<h3>Penzahiran, pemindahan dan penyimpanan</h3><p>Maklumat mungkin diproses oleh penyedia yang diperlukan untuk mengendalikan laman web dan e-mel, termasuk Hostinger, atau dizahirkan apabila diwajibkan oleh undang-undang. Data peribadi tidak dijual. Pemprosesan mungkin berlaku di luar negara anda dengan perlindungan yang munasabah. Pertanyaan sekali sahaja biasanya disimpan tidak melebihi 24 bulan selepas komunikasi bermakna terakhir; rekod hubungan perniagaan mungkin disimpan lebih lama jika diperlukan untuk tujuan perniagaan, perakaunan atau undang-undang.</p>
<h3>Hak dan hubungan</h3><p>Anda boleh meminta akses atau pembetulan data, menarik balik persetujuan apabila pemprosesan bergantung pada persetujuan, atau meminta pemadaman maklumat yang tidak lagi diperlukan. Untuk pertanyaan privasi, e-mel <a href="mailto:hello@alankyeong.com">hello@alankyeong.com</a>. Pengesahan identiti yang munasabah mungkin diperlukan.</p>
</div></main>'''
privacy_page = re.sub(r"<main>.*?</main>", privacy_main, privacy_shell, count=1, flags=re.S)
privacy_page = re.sub(r"<title>.*?</title>", "<title>Privacy Policy | Alan Yeong</title>", privacy_page, count=1)
privacy_page = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="How alankyeong.com collects, uses, protects and retains personal data.">', privacy_page, count=1)
(OUTPUT / "privacy-policy" / "index.html").write_text(privacy_page, encoding="utf-8")

cookie_main = '''<main><header class="page-hero"><div class="wrap narrow"><p class="eyebrow">Effective 24 August 2026</p><h1>Cookie policy</h1><p class="lead">How alankyeong.com currently uses cookies and similar technologies.</p></div></header><div class="page-body wrap narrow prose">
<h2>Current use</h2><p>At the effective date above, alankyeong.com does not intentionally set non-essential advertising, profiling or analytics cookies. The public pages are delivered as a static website.</p>
<h2>Strictly necessary technology</h2><p>The hosting and security infrastructure may use technically necessary identifiers or short-lived storage to deliver the website, maintain security, balance traffic or prevent abuse. These technologies are used only where required for the requested service and cannot always be disabled through the website.</p>
<h2>Analytics</h2><p>Analytics is not currently activated on this production website. If optional analytics is enabled later, it will not be loaded until an appropriate consent mechanism is available where required. This policy and the consent controls will be updated at that time.</p>
<h2>Third-party links</h2><p>Following a link to LinkedIn, Stripe or ai.alankyeong.com takes you to a separate service or property. Those destinations may use their own cookies under their own policies. Their cookies are not placed merely because a normal text link appears on this website.</p>
<h2>Browser controls</h2><p>You can use your browser settings to inspect, block or delete cookies. Blocking strictly necessary technology may affect website availability or security.</p>
<h2>Contact</h2><p>For questions about cookies or privacy, email <a href="mailto:hello@alankyeong.com">hello@alankyeong.com</a>.</p>
</div></main>'''
cookie_page = re.sub(r"<main>.*?</main>", cookie_main, privacy_shell, count=1, flags=re.S)
cookie_page = cookie_page.replace("https://alankyeong.com/privacy-policy/", "https://alankyeong.com/cookie-policy/")
cookie_page = re.sub(r"<title>.*?</title>", "<title>Cookie Policy | Alan Yeong</title>", cookie_page, count=1)
cookie_page = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Information about cookies and similar technologies on alankyeong.com.">', cookie_page, count=1)
(OUTPUT / "cookie-policy").mkdir(exist_ok=True)
(OUTPUT / "cookie-policy" / "index.html").write_text(cookie_page, encoding="utf-8")


def public_url(path: Path) -> str:
    relative = path.relative_to(OUTPUT).as_posix()
    if relative == "index.html":
        return SITE_URL
    if relative.endswith("/index.html"):
        relative = relative[: -len("index.html")]
    return urljoin(SITE_URL, relative)


urls = []
for html_file in sorted(OUTPUT.rglob("*.html")):
    html = html_file.read_text(encoding="utf-8")
    html = html.replace('<a href="/privacy-policy/">Privacy policy</a>', '<a href="/privacy-policy/">Privacy policy</a><a href="/cookie-policy/">Cookie policy</a>')
    html = re.sub(
        r'<meta name="robots" content="noindex,nofollow,noarchive">',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        html,
    )
    html_file.write_text(html, encoding="utf-8")
    if html_file.name == "index.html" and "thank-you" not in html_file.parts:
        urls.append(public_url(html_file))

(OUTPUT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nSitemap: https://alankyeong.com/sitemap.xml\n",
    encoding="utf-8",
)

sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
sitemap.extend(f"  <url><loc>{url}</loc></url>" for url in urls)
sitemap.append("</urlset>")
(OUTPUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

print(f"Generated production website with {len(urls)} indexable routes in {OUTPUT}")
