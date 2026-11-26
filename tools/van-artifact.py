# Zet een versie van het claude.ai-artifact om naar de publieke GitHub-versie:
#   python3 tools/van-artifact.py artifact.html index.html
# 1) Rad van Fortuin-mp3 eruit, CC0-draaimuziek (spin-tune.m4a) erin
# 2) Aanpassingen voor het wandscherm (Android 5.1 / Chrome 39): emoji en weer-terugval
import sys, os
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
L = t.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("var RADSRC = 'data:audio/mpeg")]
if idx:
    L[idx[0]] = "var RADSRC = 'spin-tune.m4a'; /* 'Party and Gameover loop' (happy theme) door gilzoide, CC0 - opengameart.org/content/party-and-gameover-loop */"
t = '\n'.join(L)
import re
t = re.sub(r"/\* Audio: draaimuziek = [^\n]*?\(mp3, ingesloten\); synth-tune als terugval \*/", "/* Audio: draaimuziek = spin-tune.m4a (CC0); synth-tune als terugval */", t)
old = "    tuneStop(true);\n    try {\n        if (!RADSND)"
if "if (!RADSRC) { synthStart(); return; }" not in t:
    t = t.replace(old, "    tuneStop(true);\n    if (!RADSRC) { synthStart(); return; }\n    try {\n        if (!RADSND)")

# Web Audio-draaimuziek: RADSRC is hier een los bestand (spin-tune.m4a), geen data:-URL; dan ophalen via XHR
WOLD = "    try { var r = a.decodeAudioData(b64buf(src), function (b) { done(b); }, function () { done(null); }); if (r && r.then) r.then(function (b) { done(b); }, function () { done(null); }); } catch (e) { done(null); }"
WNEW = """    var dec = function (buf) { try { var r = a.decodeAudioData(buf, function (b) { done(b); }, function () { done(null); }); if (r && r.then) r.then(function (b) { done(b); }, function () { done(null); }); } catch (e) { done(null); } };
    if (/^data:/.test(src)) { try { dec(b64buf(src)); } catch (e) { done(null); } }
    else { try { var x = new XMLHttpRequest(); x.open('GET', src); x.responseType = 'arraybuffer'; x.onload = function () { if ((x.status === 200 || x.status === 0) && x.response) dec(x.response); else done(null); }; x.onerror = function () { done(null); }; x.send(); } catch (e) { done(null); } }"""
if WOLD in t: t = t.replace(WOLD, WNEW)
open(dst, 'w', encoding='utf-8').write(t)
exec(compile(open(os.path.join(os.path.dirname(__file__), 'android5.py'), encoding='utf-8').read().replace("p=sys.argv[1]", "p=dst"), 'android5.py', 'exec'))
