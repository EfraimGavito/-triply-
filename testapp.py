from flask import Flask, request, render_template_string
import random, math, datetime

app = Flask(__name__)

BASE='''<!doctype html><html><head><title>Triply</title><style>body{font-family:Arial;margin:40px;background:#f5f7fb} .card{background:white;padding:20px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08);margin:15px 0} table{width:100%;border-collapse:collapse} td,th{padding:8px;border-bottom:1px solid #ddd} a{color:#2563eb;text-decoration:none} .btn{background:#2563eb;color:white;padding:10px 14px;border-radius:8px}</style></head><body><h1>✈️ Triply</h1>{{content|safe}}</body></html>'''

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        q=request.form
        return flights_page(q)
    c='''<div class=card><h2>Plan Your Trip</h2><form method=post>
    From <input name=origin required> To <input name=dest required><br><br>
    Depart <input type=date name=date required>
    Budget <input name=budget value=500>
    Preferences <input name=pref placeholder="food, museums, nightlife"><br><br>
    <button class=btn>Search Trip</button></form></div>'''
    return render_template_string(BASE, content=c)

def sample_flights(origin,dest,budget,sort_by='value',max_price=None,nonstop=False):
    airlines=['Delta','United','American','Southwest','JetBlue','Alaska']
    rows=[]
    for a in airlines:
        price=random.randint(120,650)
        lay=random.randint(0,2)
        hrs=random.randint(2,12)
        co2=random.randint(90,420)
        score=price+lay*40+hrs*8+co2*.2
        rows.append(dict(airline=a,price=price,lay=lay,hrs=hrs,co2=co2,score=score))
    if max_price:
        rows=[r for r in rows if r['price']<=int(max_price)]
    if nonstop:
        rows=[r for r in rows if r['lay']==0]
    keymap={'value':'score','price':'price','time':'hrs','layovers':'lay','co2':'co2'}
    key=keymap.get(sort_by,'score')
    rows.sort(key=lambda x:x[key])
    return rows

def flights_page(q):
    sort_by=q.get('sort','value')
    nonstop=True if q.get('nonstop') else False
    rows=sample_flights(q['origin'],q['dest'],q['budget'],sort_by,q.get('max_price'),nonstop)
    best=rows[0]
    html='<div class=card><h2>Flight Results</h2><form method=post><input type=hidden name=origin value="'+q['origin']+'"><input type=hidden name=dest value="'+q['dest']+'"><input type=hidden name=budget value="'+q['budget']+'">Sort <select name=sort><option value=value>Best Value</option><option value=price>Cheapest</option><option value=time>Fastest</option><option value=layovers>Fewest Layovers</option><option value=co2>Lowest CO2</option></select> Max Price <input name=max_price size=6> Nonstop <input type=checkbox name=nonstop> <button class=btn>Apply</button></form><br><table><tr><th>Airline</th><th>Price</th><th>Layovers</th><th>Hours</th><th>CO2</th></tr>'
    for r in rows:
        badge=' ⭐ Best Value' if r==best else ''
        html+=f"<tr><td>{r['airline']}{badge}</td><td>${r['price']}</td><td>{r['lay']}</td><td>{r['hrs']}</td><td>{r['co2']}kg</td></tr>"
    html+='</table></div>'
    html+=rides_html(q['dest'])
    html+=recs_html(q['dest'], q.get('pref',''))
    return render_template_string(BASE, content=html)

def rides_html(dest):
    providers=['Uber','Lyft','Bolt','Waymo']
    dist=random.randint(3,18)
    html='<div class=card><h2>Ride Comparison</h2><table><tr><th>Provider</th><th>ETA</th><th>Price</th></tr>'
    prices=[]
    for p in providers:
        surge=random.uniform(1,2)
        price=round(2+dist*1.8*surge,2)
        eta=random.randint(3,12)
        prices.append((price,p,eta))
    prices.sort()
    cheapest=prices[0][1]
    for price,p,eta in prices:
        badge=' 💸 Cheapest' if p==cheapest else ''
        html+=f'<tr><td>{p}{badge}</td><td>{eta} min</td><td>${price}</td></tr>'
    html+='</table></div>'
    return html

def recs_html(dest,pref):
    ideas=['Hidden taco stand','Local jazz bar','Neighborhood walking tour','Street art district','Budget museum pass','Sunset park viewpoint','Family-owned cafe']
    random.shuffle(ideas)
    html=f'<div class=card><h2>Local Recommendations for {dest}</h2><p>Based on your interests: {pref}</p><ul>'
    for i in ideas[:5]: html+=f'<li>{i}</li>'
    html+='</ul></div>'
    return html

if __name__=='__main__':
    app.run(debug=True)
