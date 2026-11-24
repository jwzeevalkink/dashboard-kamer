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
