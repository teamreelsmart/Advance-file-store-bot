from aiohttp import web
from html import escape
from datetime import datetime, timedelta, timezone

routes = web.RouteTableDef()
BOT_CLIENT = None


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OrvixNetworks • Premium File Hub</title>
        <style>
            :root {
                --bg:#07111d;
                --bg2:#0b1726;
                --card:#0f1c2d;
                --card2:#122131;
                --muted:#9fb0c6;
                --text:#f8fafc;
                --accent:#facc15;
                --accent2:#fde68a;
                --line:rgba(255,255,255,.08);
                --shadow:0 20px 50px rgba(0,0,0,.35);
            }
            * { box-sizing: border-box; }
            html { scroll-behavior:smooth; }
            body {
                margin:0;
                font-family: Inter, Arial, sans-serif;
                background:
                    radial-gradient(circle at top right, rgba(250,204,21,.15), transparent 30%),
                    radial-gradient(circle at bottom left, rgba(56,189,248,.10), transparent 28%),
                    linear-gradient(180deg, #06101a 0%, #08111d 100%);
                color:var(--text);
            }
            a { color:inherit; }
            .container { width:min(1120px, 92vw); margin:0 auto; }
            .nav {
                position: sticky; top:0; z-index:15;
                background: rgba(7,17,29,.78);
                backdrop-filter: blur(14px);
                border-bottom:1px solid var(--line);
            }
            .nav-inner { display:flex; align-items:center; justify-content:space-between; padding:14px 0; gap:14px; }
            .brand { display:flex; align-items:center; gap:12px; font-weight:900; letter-spacing:.2px; }
            .brand-mark {
                width:38px; height:38px; border-radius:12px;
                display:grid; place-items:center;
                background: linear-gradient(145deg, #facc15, #fde68a);
                color:#111827; font-weight:900;
                box-shadow: 0 10px 30px rgba(250,204,21,.2);
            }
            .brand-text { line-height:1.05; }
            .brand-text small { display:block; color:var(--muted); font-weight:600; margin-top:3px; }
            .btn {
                display:inline-flex; align-items:center; justify-content:center; gap:8px;
                text-decoration:none; color:#111827;
                background: linear-gradient(90deg, var(--accent), var(--accent2));
                padding:11px 18px; border-radius:14px; font-weight:800;
                box-shadow: 0 14px 35px rgba(250,204,21,.18);
                transition: transform .2s ease, box-shadow .2s ease;
                border:0;
                white-space:nowrap;
            }
            .btn:hover { transform: translateY(-1px); box-shadow: 0 18px 40px rgba(250,204,21,.26); }
            .btn.secondary {
                background: transparent;
                color: var(--text);
                border:1px solid rgba(255,255,255,.10);
                box-shadow:none;
            }
            .hero {
                padding:74px 0 48px;
                display:grid;
                grid-template-columns: 1.2fr .8fr;
                gap:24px;
                align-items:stretch;
            }
            .card {
                background: linear-gradient(180deg, rgba(15,28,45,.96), rgba(10,20,34,.92));
                border:1px solid var(--line);
                border-radius:24px;
                padding:22px;
                box-shadow: var(--shadow);
            }
            .hero-copy {
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                gap:18px;
            }
            .eyebrow {
                display:inline-flex;
                align-items:center;
                gap:8px;
                font-size:12px;
                letter-spacing:.12em;
                text-transform:uppercase;
                color:#fde68a;
                margin-bottom:14px;
                font-weight:800;
            }
            .headline {
                font-size: clamp(34px, 5vw, 60px);
                margin:0 0 14px;
                line-height:1.03;
            }
            .sub {
                color:var(--muted);
                font-size:16px;
                line-height:1.75;
                margin:0 0 22px;
                max-width: 62ch;
            }
            .chips { display:flex; flex-wrap:wrap; gap:10px; }
            .chip {
                font-size:12px;
                border:1px solid rgba(255,255,255,.12);
                padding:8px 12px;
                border-radius:999px;
                color:#dbeafe;
                background: rgba(255,255,255,.03);
            }
            .actions { display:flex; flex-wrap:wrap; gap:12px; margin-top:4px; }
            .stats { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-top:14px; }
            .stat {
                background: linear-gradient(180deg, rgba(18,33,49,.95), rgba(12,22,35,.95));
                border:1px solid rgba(255,255,255,.08);
                border-radius:16px;
                padding:14px;
            }
            .stat div { color:var(--muted); font-size:12px; margin-bottom:6px; }
            .stat b { font-size:20px; letter-spacing:.2px; }
            .sidebar-top {
                display:flex;
                align-items:center;
                justify-content:space-between;
                margin-bottom:16px;
            }
            .mini-pill {
                font-size:12px;
                padding:7px 10px;
                border-radius:999px;
                background: rgba(250,204,21,.13);
                color:#fde68a;
                border:1px solid rgba(250,204,21,.22);
                font-weight:800;
            }
            .list {
                display:grid;
                gap:12px;
            }
            .list-item {
                display:flex;
                align-items:flex-start;
                gap:12px;
                padding:14px;
                border-radius:16px;
                background: rgba(255,255,255,.03);
                border:1px solid rgba(255,255,255,.06);
            }
            .icon {
                width:36px; height:36px; flex:0 0 36px;
                border-radius:12px;
                display:grid; place-items:center;
                background: linear-gradient(145deg, rgba(250,204,21,.22), rgba(56,189,248,.15));
                color:#fde68a;
                font-weight:900;
            }
            .list-item h4 { margin:0 0 4px; font-size:15px; }
            .list-item p { margin:0; color:var(--muted); line-height:1.55; font-size:14px; }
            .section-title { margin:0 0 16px; font-size:24px; }
            .grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
            .feature {
                padding:18px;
                border-radius:18px;
                background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
                border:1px solid rgba(255,255,255,.06);
            }
            .feature p { color:var(--muted); margin:8px 0 0; line-height:1.6; }
            .faq details {
                border:1px solid rgba(255,255,255,.08);
                border-radius:16px;
                padding:14px 16px;
                margin-bottom:10px;
                background: rgba(255,255,255,.025);
            }
            .faq summary { cursor:pointer; font-weight:800; }
            .faq p { color:var(--muted); margin:10px 0 0; line-height:1.6; }
            footer {
                color:#94a3b8;
                border-top:1px solid var(--line);
                margin-top:36px;
                padding:18px 0 28px;
                text-align:center;
            }
            @media (max-width: 900px){
                .hero { grid-template-columns:1fr; padding-top:42px; }
                .grid-3 { grid-template-columns:1fr; }
                .nav-inner { flex-direction:column; align-items:flex-start; }
            }
        </style>
    </head>
    <body>
        <div class="nav">
            <div class="container nav-inner">
                <div class="brand">
                    <div class="brand-mark">OX</div>
                    <div class="brand-text">
                        OrvixNetworks
                        <small>Premium file hub & verified access</small>
                    </div>
                </div>
                <div class="actions" style="margin:0;">
                    <a class="btn secondary" href="https://t.me/TheOrviX">TheOrviX</a>
                    <a class="btn" href="https://t.me/OrvixAdminBot">Open Bot</a>
                </div>
            </div>
        </div>

        <main class="container">
            <section class="hero">
                <div class="card hero-copy">
                    <div>
                        <div class="eyebrow">Secure access • faster flow • cleaner UI</div>
                        <h1 class="headline">OrvixNetworks made for quick links, smart verification, and smooth access.</h1>
                        <p class="sub">Welcome to the official OrvixNetworks page. Generate secure links, verify quickly, and access content through a modern, protected workflow built for real users.</p>
                        <div class="chips">
                            <span class="chip">Secure Verify Flow</span>
                            <span class="chip">One-Time Links</span>
                            <span class="chip">Auto-Expiring Invites</span>
                            <span class="chip">Admin Controls</span>
                        </div>
                    </div>
                    <div class="actions">
                        <a class="btn" href="https://t.me/OrvixAdminBot">Open OrvixAdminBot</a>
                        <a class="btn secondary" href="https://t.me/OrvixNetworks">Join OrvixNetworks</a>
                    </div>
                </div>

                <div class="card">
                    <div class="sidebar-top">
                        <h2 style="margin:0;">Official Channels</h2>
                        <span class="mini-pill">Live</span>
                    </div>
                    <p class="sub" style="margin-bottom:14px;">Join updates, support, and latest drops.</p>
                    <div class="list">
                        <a class="list-item" style="text-decoration:none;" href="https://t.me/TheOrviX">
                            <div class="icon">T</div>
                            <div>
                                <h4>TheOrviX</h4>
                                <p>Updates, announcements, and official info.</p>
                            </div>
                        </a>
                        <a class="list-item" style="text-decoration:none;" href="https://t.me/OrvixNetworks">
                            <div class="icon">N</div>
                            <div>
                                <h4>OrvixNetworks</h4>
                                <p>Main community channel and service hub.</p>
                            </div>
                        </a>
                    </div>
                    <div class="stats">
                        <div class="stat"><div>Uptime</div><b>24x7</b></div>
                        <div class="stat"><div>Invite TTL</div><b>15m</b></div>
                        <div class="stat"><div>Verify Delay</div><b>5s</b></div>
                        <div class="stat"><div>Mode</div><b>Protected</b></div>
                    </div>
                </div>
            </section>

            <section class="card" style="margin-bottom:18px;">
                <h2 class="section-title">Why OrvixNetworks?</h2>
                <div class="grid-3">
                    <article class="feature">
                        <h3 style="margin:0">🔒 Safer Links</h3>
                        <p>Verification tokens are controlled and validated before redirect, preventing direct abuse and improving trust.</p>
                    </article>
                    <article class="feature">
                        <h3 style="margin:0">⚙️ Admin Friendly</h3>
                        <p>Admins can generate channel join links from forwarded posts and share them instantly with users.</p>
                    </article>
                    <article class="feature">
                        <h3 style="margin:0">🚀 Smooth Experience</h3>
                        <p>Clean pages with a clear timer and redirect flow keep onboarding fast and simple.</p>
                    </article>
                </div>
            </section>

            <section class="card faq">
                <h2 class="section-title">Quick FAQ</h2>
                <details>
                    <summary>How do I get files?</summary>
                    <p>Start the bot, open your generated link, complete verification, and access your content directly.</p>
                </details>
                <details>
                    <summary>Why verification is required?</summary>
                    <p>Verification protects links from bypassing and helps keep the system stable for genuine users.</p>
                </details>
                <details>
                    <summary>Need support?</summary>
                    <p>Use the channels above or contact the bot admin team from official Telegram pages.</p>
                </details>
            </section>
        </main>

        <footer>
            © <span id="year"></span> OrvixNetworks • Powered by TheOrviX
        </footer>

        <script>
            document.getElementById('year').textContent = new Date().getFullYear();
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_page, content_type="text/html")


@routes.get("/mini", allow_head=True)
@routes.get("/mini/", allow_head=True)
async def mini_entry_handler(request):
    user_id = (request.query.get("user_id") or "").strip()
    if user_id and user_id.lstrip('-').isdigit():
        raise web.HTTPFound(f"/mini/{user_id}")

    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini App Loader</title>
        <style>
            body {
                margin:0;
                min-height:100vh;
                display:flex;
                align-items:center;
                justify-content:center;
                background:
                    radial-gradient(circle at top, rgba(250,204,21,.10), transparent 35%),
                    linear-gradient(180deg, #08111d 0%, #0a1524 100%);
                color:#e5e7eb;
                font-family:Arial,sans-serif;
            }
            .card {
                width:min(92vw,560px);
                background:#111827;
                border:1px solid #1f2937;
                border-radius:18px;
                padding:22px;
                text-align:center;
                box-shadow: 0 20px 50px rgba(0,0,0,.35);
            }
            .btn {
                display:inline-block;
                margin-top:14px;
                text-decoration:none;
                color:#111827;
                background:linear-gradient(90deg,#facc15,#fde68a);
                padding:10px 14px;
                border-radius:12px;
                font-weight:800;
            }
            .muted { color:#9ca3af; font-size:14px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="margin:0 0 10px;">Opening Mini App...</h2>
            <p class="muted">If this page doesn't auto-open your profile, tap the button below.</p>
            <a id="open" class="btn" href="#">Open My Profile</a>
        </div>

        <script>
            const q = new URLSearchParams(window.location.search);
            let uid = q.get('user_id');

            if (!uid && window.Telegram && Telegram.WebApp && Telegram.WebApp.initDataUnsafe && Telegram.WebApp.initDataUnsafe.user) {
                uid = Telegram.WebApp.initDataUnsafe.user.id;
            }

            const openBtn = document.getElementById('open');
            if (uid) {
                const target = `/mini/${uid}`;
                openBtn.href = target;
                window.location.replace(target);
            } else {
                openBtn.textContent = 'Open Mini with user_id';
                openBtn.href = '/mini/123456?user_id=123456';
            }
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_page, content_type="text/html")


@routes.get("/mini/{user_id}", allow_head=True)
async def mini_profile_handler(request):
    user_id_raw = request.match_info.get("user_id", "").strip()
    if not user_id_raw.lstrip('-').isdigit():
        return web.Response(text="Invalid user id", status=400)

    user_id = int(user_id_raw)
    if BOT_CLIENT is None:
        return web.Response(text="Bot is not ready. Please try again.", status=503)

    try:
        user = await BOT_CLIENT.get_users(user_id)
    except Exception:
        return web.Response(text="User not found", status=404)

    username = f"@{user.username}" if getattr(user, 'username', None) else "N/A"
    full_name = (f"{user.first_name or ''} {user.last_name or ''}").strip() or "Unknown"

    created_at = await BOT_CLIENT.mongodb.get_user_created_at(user_id)
    ist = timezone(timedelta(hours=5, minutes=30))
    if created_at is None:
        started_ist = "Not Available"
    else:
        started_ist = created_at.replace(tzinfo=timezone.utc).astimezone(ist).strftime("%d-%m-%Y %I:%M:%S %p IST")

    links_generated = await BOT_CLIENT.mongodb.get_links_generated(user_id)

    default_dp = BOT_CLIENT.messages.get("DEFAULT_PROFILE_PIC", "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg")
    if getattr(user, 'username', None):
        profile_pic = f"https://t.me/i/userpic/320/{user.username}.jpg"
    else:
        profile_pic = default_dp

    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini App • User Profile</title>
        <style>
            body {{
                margin:0;
                font-family:Arial,sans-serif;
                background:
                    radial-gradient(circle at top, rgba(250,204,21,.12), transparent 35%),
                    linear-gradient(180deg, #08111d 0%, #0a1524 100%);
                color:#e5e7eb;
            }}
            .wrap {{ width:min(900px,92vw); margin:24px auto; }}
            .card {{
                background:#111827;
                border:1px solid #1f2937;
                border-radius:18px;
                padding:20px;
                box-shadow: 0 20px 50px rgba(0,0,0,.3);
            }}
            .head {{ display:flex; gap:18px; align-items:center; flex-wrap:wrap; }}
            .avatar {{ width:110px; height:110px; border-radius:50%; object-fit:cover; border:3px solid #facc15; }}
            .grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-top:16px; }}
            .item {{ background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:12px; }}
            .label {{ color:#9ca3af; font-size:12px; }}
            .value {{ font-weight:700; margin-top:4px; }}
            .btns {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:18px; }}
            .btn {{
                text-decoration:none;
                color:#111827;
                background:linear-gradient(90deg,#facc15,#fde68a);
                padding:10px 14px;
                border-radius:12px;
                font-weight:800;
            }}
            @media(max-width:700px){{ .grid{{grid-template-columns:1fr;}} }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="card">
                <div class="head">
                    <img src="{escape(profile_pic)}" class="avatar" alt="profile" onerror="this.src='{escape(default_dp)}'" />
                    <div>
                        <h2 style="margin:0 0 8px;">Mini App Profile</h2>
                        <div style="color:#fcd34d;">Welcome to TheOrviX x OrvixNetworks</div>
                    </div>
                </div>

                <div class="grid">
                    <div class="item"><div class="label">User ID</div><div class="value">{user_id}</div></div>
                    <div class="item"><div class="label">Username</div><div class="value">{escape(username)}</div></div>
                    <div class="item"><div class="label">Name</div><div class="value">{escape(full_name)}</div></div>
                    <div class="item"><div class="label">First Start (IST)</div><div class="value">{escape(started_ist)}</div></div>
                    <div class="item"><div class="label">Links Generated</div><div class="value">{links_generated}</div></div>
                    <div class="item"><div class="label">Status</div><div class="value">Active</div></div>
                </div>

                <div class="btns">
                    <a class="btn" href="https://t.me/TheOrviX">Join TheOrviX</a>
                    <a class="btn" href="https://t.me/OrvixNetworks">Join OrvixNetworks</a>
                    <a class="btn" href="https://t.me/OrvixAdminBot?start=premium">Buy Premium</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_page, content_type="text/html")


@routes.get("/verify/{token}", allow_head=True)
async def verify_route_handler(request):
    token = request.match_info.get("token", "").strip()
    if not token:
        return web.Response(text="Invalid verify link.", status=400)

    if BOT_CLIENT is None:
        return web.Response(text="Bot is not ready. Please try again.", status=503)

    data = await BOT_CLIENT.mongodb.get_verify_link_by_service_token(token)
    if not data:
        return web.Response(text="This verify link is invalid or expired.", status=404)

    if data.get("used"):
        return web.Response(text="This verify link has already been used.", status=410)

    if data.get("expires_at") and data["expires_at"] <= datetime.now():
        await BOT_CLIENT.mongodb.remove_verify_link(token)
        return web.Response(text="This verify link has expired.", status=410)

    delay = max(int(getattr(BOT_CLIENT, "verify_redirect_delay", 5)), 1)
    short_link = escape(data.get("short_link", ""))

    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verification Link Generator</title>
        <style>
            :root {{
                --bg:#f8d44a;
                --text:#111827;
                --shadow:rgba(0,0,0,.25);
            }}
            * {{ box-sizing:border-box; }}
            body {{
                margin:0;
                min-height:100vh;
                display:flex;
                align-items:center;
                justify-content:center;
                background: var(--bg);
                color: var(--text);
                font-family: Arial, sans-serif;
                overflow:hidden;
            }}
            .card {{
                width:min(92vw, 560px);
                text-align:center;
                padding:28px 18px 30px;
            }}
            .stage {{
                position:relative;
                width:100%;
                height:260px;
                display:flex;
                align-items:center;
                justify-content:center;
                margin-bottom: 10px;
            }}
            .ball-wrap {{
                position:relative;
                width:160px;
                height:200px;
            }}
            .ball {{
                position:absolute;
                left:50%;
                top:0;
                width:124px;
                height:124px;
                margin-left:-62px;
                border-radius:50%;
                background:#212121;
                box-shadow: inset -8px -10px 0 rgba(255,255,255,.04);
                transform-origin:center center;
            }}
            .ball::before {{
                content:'';
                position:absolute;
                top:16px;
                left:22px;
                width:30px;
                height:18px;
                border-radius:50%;
                background:rgba(255,255,255,.92);
                transform: rotate(-28deg);
                filter: blur(.1px);
            }}
            .ball.fall {{
                animation: fallToHole 1s ease-in forwards;
            }}
            @keyframes fallToHole {{
                0%   {{ transform: translateY(0) scale(1); opacity:1; }}
                72%  {{ transform: translateY(104px) scale(1); opacity:1; }}
                100% {{ transform: translateY(124px) scale(.55); opacity:0; }}
            }}
            .hole {{
                position:absolute;
                left:50%;
                top:120px;
                width:128px;
                height:34px;
                margin-left:-64px;
                border-radius:50%;
                background: rgba(0,0,0,.18);
                box-shadow: 0 8px 0 rgba(0,0,0,.18);
                overflow:hidden;
            }}
            .hole::before {{
                content:'';
                position:absolute;
                inset:5px 10px 4px 10px;
                border-radius:50%;
                background:#111111;
            }}
            .hole::after {{
                content:'';
                position:absolute;
                left:50%;
                top:-8px;
                width:96px;
                height:18px;
                margin-left:-48px;
                border-radius:50%;
                background: rgba(255,255,255,.13);
                filter: blur(1px);
            }}
            .progress {{
                width:min(420px, 86vw);
                height:30px;
                margin:0 auto 20px;
                border-radius:999px;
                border:2px solid rgba(0,0,0,.65);
                background: rgba(255,255,255,.12);
                overflow:hidden;
                box-shadow: inset 0 2px 0 rgba(255,255,255,.14);
            }}
            .progress > span {{
                display:block;
                height:100%;
                width:0%;
                background:#111111;
                border-radius:999px;
                transition: width 1s linear;
            }}
            .title {{
                font-size:24px;
                font-weight:800;
                margin:0 0 2px;
            }}
            .muted {{
                margin:0;
                font-size:15px;
                opacity:.8;
            }}
            .timer {{
                margin-top:14px;
                font-size:16px;
                font-weight:700;
            }}
            .channels {{
                display:flex;
                gap:10px;
                flex-wrap:wrap;
                justify-content:center;
                margin-top:18px;
            }}
            .pill {{
                text-decoration:none;
                color:#111827;
                background: rgba(255,255,255,.32);
                border:1px solid rgba(0,0,0,.20);
                padding:9px 14px;
                border-radius:999px;
                font-weight:800;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="stage">
                <div class="ball-wrap">
                    <div id="ball" class="ball fall"></div>
                    <div class="hole"></div>
                </div>
            </div>

            <div class="progress"><span id="progress"></span></div>

            <p class="title">Loading...</p>
            <p class="muted">Please wait while your link is being prepared.</p>
            <div class="timer"><span id="seconds">{delay}</span>s</div>

            <div class="channels">
                <a href="https://t.me/TheOrviX" class="pill">TheOrviX</a>
                <a href="https://t.me/OrvixNetworks" class="pill">OrvixNetworks</a>
            </div>
        </div>

        <script>
            let seconds = {delay};
            const total = seconds;
            const secEl = document.getElementById('seconds');
            const progressEl = document.getElementById('progress');
            const ball = document.getElementById('ball');

            function restartBall() {{
                ball.classList.remove('fall');
                void ball.offsetWidth;
                ball.classList.add('fall');
            }}

            function tick() {{
                seconds -= 1;
                secEl.innerText = Math.max(seconds, 0);
                const done = ((total - Math.max(seconds, 0)) / total) * 100;
                progressEl.style.width = done + '%';
                restartBall();

                if (seconds <= 0) {{
                    clearInterval(timer);
                    window.location.href = "{short_link}";
                }}
            }}

            progressEl.style.width = '0%';
            const timer = setInterval(tick, 1000);
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_page, content_type="text/html")


@routes.get("/health", allow_head=True)
async def health_route_handler(request):
    return web.Response(text="ok", status=200)


app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=8080)
