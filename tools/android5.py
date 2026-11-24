# Past index.html aan voor het wandscherm (Android 5.1 / Chrome 39): emoji en weer-terugval
import sys
p=sys.argv[1]; t=open(p,encoding='utf-8').read()
R=[("'⏸ Stop'","'■ Stop'"),("⏹ Stop radio","■ Stop radio"),
   ("'🌤️'","'⛅'"),("'🌦️'","'☔'"),("'🌧️'","'☔'"),("'🌫️'","'🌁'"),("'⛈️'","'⚡'"),
   ("'🏘️ 3D-dorp'","'🏠 3D-dorp'"),
   ("['🥇', '🥈', '🥉', '4.', '5.']","['🏆', '2.', '3.', '4.', '5.']"),
   ("🥖","🍞"),("🥤","🍨"),
   ("['🙁', 'Chagrijnig']","['😞', 'Chagrijnig']"),("['🙂', 'Goed']","['😊', 'Goed']")]
for a,b in R:
    n=t.count(a); assert n>=1,(a,n); t=t.replace(a,b)
old="""        var x = new XMLHttpRequest();
        x.open('GET', 'https://api.open-meteo.com/v1/forecast?latitude=52.2333&longitude=6.1&current=temperature_2m,weather_code,is_day&hourly=temperature_2m,precipitation_probability,weather_code&forecast_days=2&timezone=Europe%2FAmsterdam');
        x.timeout = 15000;
        x.onload = function () { try { var d = JSON.parse(x.responseText); if (d && d.current && d.hourly) { LW = d; wx(); } } catch (e) { } };
        x.send();"""
new="""        /* Eerst rechtstreeks open-meteo; lukt dat niet (oude browsers vertrouwen het certificaat niet),
           dan weather.json dat GitHub elk uur ophaalt */
        var urls = ['https://api.open-meteo.com/v1/forecast?latitude=52.2333&longitude=6.1&current=temperature_2m,weather_code,is_day&hourly=temperature_2m,precipitation_probability,weather_code&forecast_days=2&timezone=Europe%2FAmsterdam', 'weather.json?t=' + new Date().getTime()];
        var tryUrl = function (i) {
            if (i >= urls.length) return;
            var x = new XMLHttpRequest(), done = false;
            var fail = function () { if (!done) { done = true; tryUrl(i + 1); } };
            x.open('GET', urls[i]);
            x.timeout = 15000;
            x.onload = function () { if (done) return; try { var d = JSON.parse(x.responseText); if (x.status === 200 && d && d.current && d.hourly) { done = true; LW = d; wx(); return; } } catch (e) { } fail(); };
            x.onerror = fail; x.ontimeout = fail;
            x.send();
        };
        tryUrl(0);"""
assert t.count(old)==1; t=t.replace(old,new)
open(p,'w',encoding='utf-8').write(t)

# --- Ronde 2: CSS-variabelen (Chrome 39 kent ze niet, pas vanaf 49) en nieuwere emoji ---
t=open(p,encoding='utf-8').read()
assert t.count('🧹')>=1; t=t.replace('🧹','💨')
POLY="""</style>
<script>
/* Terugval voor browsers zonder CSS-variabelen (o.a. het wandscherm, Chrome 39):
   vervang var(--x) door de kleur van het actieve thema, in de stylesheet en in style-attributen */
(function () {
    try { if (window.CSS && CSS.supports && CSS.supports('--a', '0')) return; } catch (e) { }
    if (!window.MutationObserver) return;
    var st = document.getElementsByTagName('style')[0]; if (!st) return;
    var src = st.textContent, D = document.documentElement;
    var grab = function (sel) { var m = src.match(new RegExp(sel + '\\\\{([^}]*)\\\\}')), o = {}; if (m) m[1].replace(/--([\\w-]+):([^;]+)/g, function (a, k, v) { o[k] = v; }); return o; };
    var base = grab(':root'), adst = grab('html\\\\.th-adst'), V = base;
    var sub = function (s) { return s.replace(/var\\(--([\\w-]+)\\)/g, function (a, k) { return V[k] || a; }); };
    var fixEl = function (el) { if (el.nodeType !== 1) return; var s = el.getAttribute('data-vs') || el.getAttribute('style'); if (s && s.indexOf('var(--') >= 0) { el.setAttribute('data-vs', s); el.setAttribute('style', sub(s)); } };
    var fixTree = function (n) { if (n.nodeType !== 1) return; fixEl(n); var a = n.querySelectorAll('[style*="var(--"],[data-vs]'); for (var i = 0; i < a.length; i++) fixEl(a[i]); };
    var apply = function () {
        var k = {}, x; for (x in base) k[x] = base[x];
        if (/(^|\\s)th-adst(\\s|$)/.test(D.className)) for (x in adst) k[x] = adst[x];
        V = k; st.textContent = sub(src); if (document.body) fixTree(document.body);
    };
    apply();
    new MutationObserver(apply).observe(D, { attributes: true, attributeFilter: ['class'] });
    new MutationObserver(function (ms) {
        for (var i = 0; i < ms.length; i++) { var m = ms[i]; if (m.type === 'attributes') { var s = m.target.getAttribute('style'); if (s && s.indexOf('var(--') >= 0) fixEl(m.target); } else for (var j = 0; j < m.addedNodes.length; j++) fixTree(m.addedNodes[j]); }
    }).observe(D, { childList: true, subtree: true, attributes: true, attributeFilter: ['style'] });
    document.addEventListener('DOMContentLoaded', function () { fixTree(document.body); });
})();
</script>"""
assert t.count('</style>')==1; t=t.replace('</style>',POLY,1)
open(p,'w',encoding='utf-8').write(t)
