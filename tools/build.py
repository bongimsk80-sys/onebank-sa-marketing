#!/usr/bin/env python3
"""
Builds the OneView marketing site into the repository root as plain HTML.

Every page shares one header, footer and stylesheet. Edit the content here,
then run:  python3 tools/build.py
Netlify serves the generated files directly (no build step on Netlify).
"""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://onebank-sa.netlify.app"          # current Netlify address; change when the custom domain is live
APP_URL = "https://onebank-sa-iota.vercel.app"         # the OneView app (rename the Vercel domain to match the brand)
CONTACT = "hello@oneview.co.za"
SECURITY = "security@oneview.co.za"
PRIVACY = "privacy@oneview.co.za"
TODAY = date.today().isoformat()

MARK = """<svg class="brand-mark" viewBox="0 0 26 26" aria-hidden="true"><rect x="1" y="1" width="24" height="24" rx="6" fill="#2B54A6"/><circle cx="13" cy="13" r="6.2" fill="none" stroke="#fff" stroke-width="2.4"/><path d="M4.5 13h17" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>"""

NAV = [("/product/", "Product"), ("/security/", "Security"), ("/pricing/", "Pricing"), ("/about/", "About"), ("/faq/", "FAQ")]


def page(path, title, description, body, current=None):
    nav = "\n".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in NAV
    )
    canonical = SITE_URL + ("/" if path == "index.html" else "/" + path.replace("index.html", ""))
    html = f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OneView">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="beta-note"><div class="wrap">OneView is in beta. Payments are simulated and no money moves. <a href="/faq/#simulation">What this means</a></div></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{MARK}OneView</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {nav}
      <a href="{APP_URL}/login">Sign in</a>
      <a class="btn btn-primary" href="/demo/">Book a demo</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <a class="brand" href="/">{MARK}OneView</a>
      <p class="small mt-12">Payment approval and cash visibility across South African banks.</p>
      <p class="small">OneView is not a bank and does not hold client funds. Company registration in progress. Johannesburg, South Africa.</p>
    </div>
    <div>
      <h2>Product</h2>
      <ul>
        <li><a href="/product/">Features</a></li>
        <li><a href="/security/">Security</a></li>
        <li><a href="/pricing/">Pricing</a></li>
        <li><a href="{APP_URL}/login">Sign in</a></li>
      </ul>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/demo/">Book a demo</a></li>
        <li><a href="/legal/privacy/">Privacy notice</a></li>
        <li><a href="/legal/terms/">Website terms</a></li>
      </ul>
    </div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return canonical


SLIP = """
<figure class="slip" aria-label="Example payment instruction with its approval trail">
  <div class="slip-top">
    <div>
      <div class="slip-payee">Karoo Building Supplies</div>
      <div class="slip-ref">Invoice INV-20417 · batch of 3 supplier payments</div>
    </div>
    <div class="slip-amount">R&nbsp;248&nbsp;600,00</div>
  </div>
  <div class="slip-route">From <strong>Nedbank Business Current ••4417</strong> to <strong>FNB ••0293</strong></div>
  <ol class="trail">
    <li><span class="dot"></span><span class="who">Lerato M.<span class="what">Initiated from the ERP invoice</span></span><time>08:42</time></li>
    <li><span class="dot"></span><span class="who">Pieter v.d. W.<span class="what">Reviewed: beneficiary details match</span></span><time>09:15</time></li>
    <li><span class="dot"></span><span class="who">Ayesha K., Financial Controller<span class="what">Approved with authenticator code</span></span><time>10:03</time></li>
    <li><span class="dot wait"></span><span class="who">Second approver<span class="what">Required above R&nbsp;200&nbsp;000</span></span><time>waiting</time></li>
  </ol>
  <div class="slip-foot"><span class="policy">Policy: two approvers above R&nbsp;200&nbsp;000</span><span>Initiator cannot approve</span></div>
</figure>
<p class="slip-caption">Illustration with example data.</p>
"""

home = f"""
<section class="hero">
  <div class="wrap split">
    <div>
      <h1>Every payment approved the same way, at every bank.</h1>
      <p class="lead">OneView puts your company's accounts at FNB, Standard Bank, Absa, Nedbank, Capitec and Investec on one screen, and sends every payment through your approval policy before it reaches the bank.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/demo/">Book a demo</a>
        <a class="btn btn-quiet" href="/product/">See what it does</a>
      </div>
      <p class="small mt-20">For finance teams at South African companies that bank with more than one institution.</p>
    </div>
    <div>{SLIP}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Several banks means several sets of rules</h2>
    <p class="lead">Most mid-sized companies run accounts at two to five banks. Each portal has its own login, its own approval settings and its own reports.</p>
    <div class="cols mt-32">
      <div><h3>The cash position is a spreadsheet</h3><p>Someone logs into each portal every morning and adds up the balances by hand.</p></div>
      <div><h3>Approvals depend on the bank</h3><p>A payment that needs two signatures at one bank may need one at another, and sign-offs happen in email or WhatsApp.</p></div>
      <div><h3>The audit trail is scattered</h3><p>When the auditors ask who approved a payment, the answer is split across portals, inboxes and chat threads.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>How OneView works</h2>
    <ol class="steps">
      <li><h3>Connect your banks</h3><p>An authorised person links each account with read-only consent. OneView never sees your banking passwords.</p></li>
      <li><h3>Set your approval policy</h3><p>Choose who can initiate, review and approve, with amount bands and transfer limits per role.</p></li>
      <li><h3>Approve in one place</h3><p>Every payment, from every account, follows the same policy and needs an authenticator code to approve.</p></li>
      <li><h3>Keep the record</h3><p>Each step is written to a tamper-evident audit log you can export for your auditors.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Built for South African banking</h2>
    <ul class="banks"><li>FNB</li><li>Standard Bank</li><li>Absa</li><li>Nedbank</li><li>Capitec</li><li>Investec</li></ul>
    <p>Live bank data connects through <a href="https://stitch.money">Stitch</a>, a South African bank-data provider, once our integration is approved. Until then, the beta runs on realistic demo data and accounts you enter yourself. Amounts are in rand and dates follow South African conventions.</p>
    <p class="small">OneView is independent and not affiliated with any bank. Bank names identify the institutions you can connect.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>See it with your own banks and approvers</h2>
    <p class="lead">A 30-minute walkthrough, set up around how your team approves payments today.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/demo/">Book a demo</a><a class="btn btn-quiet" href="/pricing/">View pricing</a></div>
  </div>
</section>
"""

FEATURES = [
    ("Consolidated dashboard", "Balances and recent activity for every connected account, with a combined rand total and the time each figure was last updated.", "live", "Live in beta"),
    ("Approval workflows", "Multi-step approval chains set by amount band. The person who initiates a payment cannot approve it.", "live", "Live in beta"),
    ("Roles and permissions", "Admin, Initiator, Reviewer, Approver, Executor and Viewer, enforced on every request.", "live", "Live in beta"),
    ("Transfer limits", "Per-transaction, daily and monthly limits for each role.", "live", "Live in beta"),
    ("Two-factor authentication", "Authenticator-app codes at sign-in; required for admins, approvers and executors.", "live", "Live in beta"),
    ("Tamper-evident audit trail", "Every action is chained to the one before it, so edits or deletions can be detected.", "live", "Live in beta"),
    ("Beneficiaries", "Supplier, vendor and employee details with tags and payment history.", "live", "Live in beta"),
    ("Analytics and exports", "Money in and out, spend by category and bank, with PDF and Excel export.", "live", "Live in beta"),
    ("Live bank data via Stitch", "Consent-based connection to South African banks, with up to three months of history.", "pilot", "In integration"),
    ("ERP connections", "Import invoices from Sage, Xero and other accounting systems into payment batches.", "planned", "In development"),
    ("Payment execution", "Sending approved payments to the bank from OneView. Requires regulatory authorisation or a licensed partner.", "planned", "Planned"),
    ("Letters of guarantee", "Apply for bid, performance and rental guarantees with a partner bank.", "planned", "Planned"),
]

rows = "\n".join(
    f"<tr><td><strong>{n}</strong></td><td>{d}</td><td><span class=\"status status-{k}\">{s}</span></td></tr>" for n, d, k, s in FEATURES
)

product = f"""
<section class="page-head">
  <div class="wrap">
    <h1>One approval policy across all your banks</h1>
    <p class="lead">OneView is a control layer on top of your existing bank accounts. Your banks keep your money and execute payments; OneView gives you one view and one set of rules.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>What is available today</h2>
    <p>We label every feature by where it really is, so you know what you can use in the beta.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Feature</th><th scope="col">What it does</th><th scope="col">Status</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>
<section>
  <div class="wrap split">
    <div>
      <h2>How bank connections work</h2>
      <p>An authorised user chooses <em>Connect a bank</em>, confirms they may share read-only data for 90 days, and authorises access at their bank through Stitch. OneView receives balances and transactions, not your login details.</p>
      <p>You can see each connection's status and last update, refresh it, or revoke consent at any time. Revoking stops all syncing; past transactions stay in your audit trail.</p>
    </div>
    <div>
      <h2>Who it is for</h2>
      <p>Finance teams of two to twenty people at companies that bank with more than one institution: CFOs, financial controllers, treasury and accounts-payable staff.</p>
      <p>Single-bank companies use OneView for the approval workflow and audit trail alone.</p>
    </div>
  </div>
</section>
"""

security = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Security and data protection</h1>
    <p class="lead">What we do to protect your financial data today, and what is still on the way. We would rather be precise than impressive.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Controls in place</h2>
    <div class="table-wrap"><table>
      <thead><tr><th scope="col">Area</th><th scope="col">What we do</th></tr></thead>
      <tbody>
        <tr><td><strong>Sign-in</strong></td><td>Passwords hashed with bcrypt; authenticator-app codes required for admins, approvers and executors; sessions invalidated after a password reset; rate limits on sign-in.</td></tr>
        <tr><td><strong>Separation of companies</strong></td><td>Every request is checked against your organisation; users without an organisation cannot read any data.</td></tr>
        <tr><td><strong>Approvals</strong></td><td>Initiators cannot approve their own payments; limits and roles are enforced on the server, not only in the screen.</td></tr>
        <tr><td><strong>Bank access</strong></td><td>Read-only, consent-based access through Stitch. Bank access tokens are encrypted with AES-256-GCM. We never ask for or store online-banking passwords.</td></tr>
        <tr><td><strong>Audit trail</strong></td><td>Append-only and hash-chained per organisation; admins can check that it has not been altered.</td></tr>
        <tr><td><strong>Transport</strong></td><td>HTTPS everywhere with HSTS; database connections require TLS.</td></tr>
      </tbody>
    </table></div>
  </div>
</section>
<section>
  <div class="wrap split">
    <div>
      <h2>Where your data is held</h2>
      <p>The application runs on Vercel and its database is a managed PostgreSQL service (Neon) in the European Union. Transfers outside South Africa rely on binding operator agreements under section 72 of POPIA. We plan to move the database to a South African region before onboarding live customer bank data.</p>
      <p>Bank data retrieved through Stitch is processed by Stitch in South Africa.</p>
    </div>
    <div>
      <h2>Still to come</h2>
      <ul>
        <li>Independent penetration test before the first live-data pilot</li>
        <li>South African database region</li>
        <li>ISO 27001 readiness programme</li>
      </ul>
      <h2 class="mt-32">Report a vulnerability</h2>
      <p>Email <a href="mailto:{SECURITY}">{SECURITY}</a>. We acknowledge reports within two working days and will not take action against good-faith research that avoids customer data and service disruption.</p>
    </div>
  </div>
</section>
"""

PLANS = [
    ("Beta", "R0", "Invite only, while the beta runs", ["All live features", "Up to 10 bank accounts", "Demo data and manual accounts", "Email support"], "Ask to join", "/demo/", False),
    ("Starter", "R799", "per organisation a month", ["Up to 5 bank accounts", "Approval workflows and limits", "Audit trail and exports", "Email support"], "Book a demo", "/demo/", False),
    ("Growth", "R2,499", "per organisation a month", ["Up to 25 bank accounts", "Everything in Starter", "Advanced analytics", "Priority support"], "Book a demo", "/demo/", True),
    ("Enterprise", "Custom", "quoted per organisation", ["Unlimited bank accounts", "Custom approval policies", "Named account manager and SLA", "Onboarding and training"], "Contact us", "/demo/", False),
]
plans = "\n".join(
    f"""<div class="plan{' featured' if f else ''}"><h3>{n}</h3><div class="price">{p}</div><div class="small">{u}</div><ul>{''.join(f'<li>{i}</li>' for i in items)}</ul><a class="btn {'btn-primary' if f else 'btn-quiet'}" href="{href}">{cta}</a></div>"""
    for n, p, u, items, cta, href, f in PLANS
)
pricing = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Pricing</h1>
    <p class="lead">One price per organisation, month to month. Annual billing gives two months free. Prices exclude VAT.</p>
    <div class="plans">{plans}</div>
    <p class="small mt-20">Live bank connections through Stitch are included on paid plans once available. Bank charges for payments stay with your bank.</p>
  </div>
</section>
"""

about = f"""
<section class="page-head">
  <div class="wrap">
    <h1>About OneView</h1>
    <p class="lead">We are building the control layer South African finance teams need when their money sits at more than one bank.</p>
  </div>
</section>
<section>
  <div class="wrap founder">
    <img src="/founder-v2.jpg" width="560" height="497" alt="Bonginkosi Masuku, founder of OneView">
    <div>
      <h2>Bonginkosi Masuku, Founder and CEO</h2>
      <p>Bonginkosi has spent more than 16 years in enterprise risk, governance and business continuity, working alongside CFOs and audit committees at large organisations in South Africa and abroad.</p>
      <p>He kept seeing the same problem: treasury teams juggling several bank portals, approvals that depended on the person rather than the policy, and no single record an auditor could rely on. OneView is his answer to it.</p>
      <ul class="creds">
        <li>MBA, Gordon Institute of Business Science, University of Pretoria</li>
        <li>IRMP, Institute of Risk Management South Africa</li>
        <li>GRCP and GRCA, OCEG</li>
        <li>ISO 22301 Lead Implementer; ISO 31000 Practitioner</li>
        <li>AI Business Strategy, Johns Hopkins University</li>
      </ul>
      <p><a href="https://www.linkedin.com/in/bonginkosi-masuku-mba-6802315a">LinkedIn profile</a></p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>Advisers</h2>
    <p>We are looking for a technology adviser with experience of South African banking or payments infrastructure, and a finance adviser who has run treasury at a mid-sized or listed company. If that is you, email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  </div>
</section>
"""

FAQ = [
    ("simulation", "Does OneView move money?", "Not during the beta. Payments go through the full approval workflow, but execution is simulated and no funds leave any account. Sending payments to banks from OneView will need regulatory authorisation or a licensed partner, and we will switch it on only when that is in place."),
    ("banks", "Which banks can I connect?", "FNB, Standard Bank, Absa, Nedbank, Capitec and Investec. Live data will come through Stitch once our integration is approved; until then you can use demo data or enter accounts yourself."),
    ("passwords", "Do you need our online-banking passwords?", "No. You authorise access at your bank through Stitch and OneView receives read-only data. We never ask for or store banking passwords."),
    ("regulated", "Is OneView regulated?", "OneView is software. It does not hold client funds or execute payments, so it does not currently need payment authorisation from the South African Reserve Bank. We are tracking the Reserve Bank's new activity-based payments framework and will obtain the authorisation, or work through a licensed partner, before offering payment execution."),
    ("popia", "How do you handle POPIA?", "We process personal and financial information as a responsible party under POPIA. Our privacy notice explains what we collect, why, where it is held and your rights. We are registering our Information Officer with the Information Regulator."),
    ("data", "Where is our data stored?", "In a managed PostgreSQL database in the European Union, under operator agreements that meet section 72 of POPIA. We plan to move to a South African region before onboarding live bank data."),
    ("onebank", "Is this the product previously called OneBank TMS?", "Yes. We renamed the product OneView. South African law reserves the word “bank” for registered banks, and OneView is not a bank."),
    ("cancel", "Can we cancel or export our data?", f"Plans are month to month. You can request a full export at any time by emailing {CONTACT}. Financial audit records are kept for the period the law requires, then deleted."),
]
faq_html = "\n".join(f'<details id="{i}"><summary>{q}</summary><p>{a}</p></details>' for i, q, a in FAQ)
faq = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Questions finance teams ask us</h1>
    <div class="mt-28">{faq_html}</div>
    <p class="mt-28">Something else? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  </div>
</section>
"""

demo = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Book a demo</h1>
    <p class="lead">Tell us a little about your finance team. We will email you within two working days to set up a 30-minute walkthrough.</p>
    <form class="demo" id="demo-form" data-endpoint="{APP_URL}/api/enquiries" novalidate>
      <div class="field"><label for="firstName">First name</label><input id="firstName" name="firstName" autocomplete="given-name" required maxlength="80"></div>
      <div class="field"><label for="lastName">Last name</label><input id="lastName" name="lastName" autocomplete="family-name" required maxlength="80"></div>
      <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required maxlength="200"></div>
      <div class="field"><label for="phone">Phone <span class="hint">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" maxlength="30"></div>
      <div class="field"><label for="company">Company</label><input id="company" name="company" autocomplete="organization" required maxlength="160"></div>
      <div class="field"><label for="role">Your role <span class="hint">(optional)</span></label>
        <select id="role" name="role"><option value="">Choose one</option><option>CFO or finance director</option><option>Financial controller</option><option>Treasury or AP</option><option>CEO or managing director</option><option>IT or systems</option><option>Other</option></select></div>
      <div class="field"><label for="banks">How many banks does your company use? <span class="hint">(optional)</span></label>
        <select id="banks" name="banks"><option value="">Choose one</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5 or more</option></select></div>
      <div class="field full"><label for="message">What would you like to see? <span class="hint">(optional)</span></label><textarea id="message" name="message" maxlength="2000"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
      <label class="field full check"><input type="checkbox" name="consentProcessing" required><span>I agree that OneView may use these details to respond to my request, as described in the <a href="/legal/privacy/">privacy notice</a>.</span></label>
      <label class="field full check"><input type="checkbox" name="consentMarketing"><span>Send me occasional product updates. You can unsubscribe at any time.</span></label>
      <div class="form-status" id="form-status" role="status" tabindex="-1"></div>
      <div class="field full"><button class="btn btn-primary" type="submit">Request a demo</button></div>
    </form>
  </div>
</section>
"""

privacy = f"""
<section class="page-head">
  <div class="wrap legal">
    <h1>Privacy notice</h1>
    <p class="small">Last updated {TODAY}. This notice covers this website. The OneView application has its own privacy notice, shown at sign-up.</p>
    <h2>Who we are</h2>
    <p>OneView (company registration in progress) is the responsible party for personal information collected on this website. Information Officer: <a href="mailto:{PRIVACY}">{PRIVACY}</a>.</p>
    <h2>What we collect and why</h2>
    <p>When you request a demo we collect your name, work email, company and, if you choose, your phone number, role, number of banks and message. We use them to respond to your request and, only if you tick the box, to send product updates. We also record the IP address of the request to prevent abuse.</p>
    <p>This website sets no tracking or advertising cookies.</p>
    <h2>Where it is held</h2>
    <p>Demo requests are stored in the OneView application database (Neon PostgreSQL, European Union), hosted on Vercel. These operators are bound by agreements that give protection substantially similar to POPIA, as section 72 requires. The website itself is hosted by Netlify. Fonts load from Google Fonts.</p>
    <h2>How long we keep it</h2>
    <p>Demo requests are kept for 24 months after our last contact with you, then deleted, unless you become a customer.</p>
    <h2>Your rights</h2>
    <p>You may ask to see, correct or delete your information, object to its use, or withdraw consent for updates, by emailing <a href="mailto:{PRIVACY}">{PRIVACY}</a>. You may also complain to the Information Regulator at <a href="https://inforegulator.org.za">inforegulator.org.za</a>.</p>
  </div>
</section>
"""

terms = f"""
<section class="page-head">
  <div class="wrap legal">
    <h1>Website terms</h1>
    <p class="small">Last updated {TODAY}.</p>
    <p>This website gives general information about OneView. It is not financial, legal or tax advice. Features marked as in integration, in development or planned are not yet available and may change.</p>
    <p>Bank names are used only to identify the institutions customers can connect. OneView is not affiliated with or endorsed by any bank, and is not itself a bank.</p>
    <p>Use of the OneView application is governed by the terms you accept when you sign up.</p>
    <p>These terms are governed by the law of the Republic of South Africa. Questions: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  </div>
</section>
"""

notfound = """
<section class="page-head"><div class="wrap">
<h1>This page does not exist</h1>
<p class="lead">The link may be out of date. Go to the <a href="/">home page</a> or <a href="/demo/">book a demo</a>.</p>
</div></section>
"""

urls = [
    page("index.html", "OneView: payment approvals across South African banks", "One view of your company's accounts at FNB, Standard Bank, Absa, Nedbank, Capitec and Investec, with one approval policy for every payment.", home, "/"),
    page("product/index.html", "Product: OneView", "Consolidated balances, approval workflows, transfer limits, two-factor authentication and a tamper-evident audit trail, with each feature's status.", product, "/product/"),
    page("security/index.html", "Security: OneView", "How OneView protects financial data: two-factor sign-in, read-only bank access, encryption and a tamper-evident audit trail.", security, "/security/"),
    page("pricing/index.html", "Pricing: OneView", "Month-to-month pricing per organisation for South African finance teams.", pricing, "/pricing/"),
    page("about/index.html", "About: OneView", "Why OneView exists and who is building it.", about, "/about/"),
    page("faq/index.html", "FAQ: OneView", "Answers on payments, bank connections, regulation, POPIA and data storage.", faq, "/faq/"),
    page("demo/index.html", "Book a demo: OneView", "Request a 30-minute OneView walkthrough for your finance team.", demo),
    page("legal/privacy/index.html", "Privacy notice: OneView", "How OneView handles personal information collected on this website.", privacy),
    page("legal/terms/index.html", "Website terms: OneView", "Terms for using the OneView website.", terms),
]
page("404.html", "Page not found: OneView", "This page does not exist.", notfound)

(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls)
    + "</urlset>\n",
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
(ROOT / "assets" / "favicon.svg").write_text(MARK.replace(' class="brand-mark"', ' xmlns="http://www.w3.org/2000/svg"'), encoding="utf-8")
print(f"Built {len(urls) + 1} pages")
