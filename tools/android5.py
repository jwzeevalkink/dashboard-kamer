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
import re
# Weer: eerst rechtstreeks open-meteo, anders weather.json (zelfde URL, elk uur door GitHub opgehaald)
WRE=re.compile(r"        var x = new XMLHttpRequest\(\);\n        x\.open\('GET', '(https://api\.open-meteo\.com/[^']*)'\);\n        x\.timeout = 15000;\n        x\.onload = function \(\) \{ try \{ var d = JSON\.parse\(x\.responseText\); if \((d && d\.current && d\.\w+)\) \{ LW = d; wx\(\); \} \} catch \(e\) \{ \} \};\n        x\.send\(\);")
m=WRE.search(t); assert m,'weer-blok niet gevonden'
new="""        /* Eerst rechtstreeks open-meteo; lukt dat niet (oude browsers vertrouwen het certificaat niet),
           dan weather.json dat GitHub elk uur ophaalt */
        var urls = ['%s', 'weather.json?t=' + new Date().getTime()];
        var tryUrl = function (i) {
            if (i >= urls.length) return;
            var x = new XMLHttpRequest(), done = false;
            var fail = function () { if (!done) { done = true; tryUrl(i + 1); } };
            x.open('GET', urls[i]);
            x.timeout = 15000;
            x.onload = function () { if (done) return; try { var d = JSON.parse(x.responseText); if (x.status === 200 && %s) { done = true; LW = d; wx(); return; } } catch (e) { } fail(); };
            x.onerror = fail; x.ontimeout = fail;
            x.send();
        };
        tryUrl(0);""" % (m.group(1), m.group(2))
t=t[:m.start()]+new+t[m.end():]
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

# --- Ronde 3: wandindeling ook op het wandscherm (viewport 980x515, onder het breekpunt van 1100px) ---
t=open(p,encoding='utf-8').read()
n=t.count('@media(min-width:1100px)'); assert n>=2,n
t=t.replace('@media(min-width:1100px)','@media(min-width:960px)')
small='@media(min-width:960px) and (min-aspect-ratio:4/3) and (max-height:649px){html{font-size:12px}}\n'
a='@media(min-width:960px) and (min-aspect-ratio:4/3) and (min-height:650px)'
assert t.count(a)==1; t=t.replace(a,small+a)
open(p,'w',encoding='utf-8').write(t)

# --- Ronde 4: plekken zonder CSS grid (Chrome 39) netjes 2 kolommen, plek 1-4 links en 5-8 rechts zoals in de grid-versie ---
t=open(p,encoding='utf-8').read()
old='@supports not (display:grid){.seats{display:flex;flex-wrap:wrap}.seats>.seat{width:48%;margin:0 2% 10px 0}}'
assert t.count(old)==1,'seats-fallback'
ordr=''.join('.seats>.seat:nth-child(%d){-webkit-order:%d;order:%d}'%(i,o,o) for i,o in zip(range(1,9),[1,3,5,7,2,4,6,8]))
new=('@supports not (display:grid){.seats{display:flex;flex-wrap:wrap;justify-content:space-between}.seats>.seat{width:48.5%;margin:0 0 10px}'+ordr+'}\n'
     '@media(min-width:960px) and (min-aspect-ratio:4/3){@supports not (display:grid){.k-room .seats{-webkit-align-content:space-between;align-content:space-between}.k-room .seats>.seat{height:calc(25% - .7vh);margin-bottom:0}}}')
t=t.replace(old,new)
open(p,'w',encoding='utf-8').write(t)
