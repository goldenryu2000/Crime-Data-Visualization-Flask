import enum
from flask import Flask, json,render_template,jsonify
import requests as rq
from random import sample

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/categories')
def categories():
    url = "https://crime-data-api.herokuapp.com/data"
    res = rq.get(url)
    data = res.json()
    cats = data["Categories"]
    id_l = ["collapseOne","collapseTwo","collapseThree","collapseFour","collapseFive","collapseSix"]
    hid  = ["headingOne","headingTwo","headingThree","headingFour","headingFive","headingSix"]
    l = {}
    d_url = {}
    for i,cat in enumerate(cats):
        url_1 = url + "/" + str(i+1)
        res2 = rq.get(url_1)
        d = res2.json()
        l[cat] = d["SubCategory List"]
    for i,s in enumerate(cats):
        size = len(l[s])
        l_url = []
        for j in range(size):
            url_2 = "https://crime-data-visualisation.herokuapp.com/data/" + str(i+1) + "/" + str(j+1)
            l_url.append(url_2)
        d_url[s] = l_url 
    fi = {}
    for i in cats:
        fi[i] = {}
        
    for k,v in fi.items():
        for (a,x) in zip(l[k],d_url[k]):
            v[a] = x
    
    return render_template("categories.html",cats_ids = zip(cats,id_l,hid),items=zip(d_url,l_url),fi = fi)

@app.route('/data/<int:category>/<int:subcategory>')
def data(category,subcategory):
    response = rq.get('https://crime-data-api.herokuapp.com/data/{}/{}'.format(category,subcategory))
    data = response.json()
    a = data["2017"]
    b = data["2018"]
    c = data["2019"]
    print(type(a))
    return render_template('chart.html',title=data['Category'].strip(),subtitle=data['Sub-Category'].strip(),A=a,B=b,C=c,max= max(a,b,c))

if __name__ == "__main__":
    app.run(debug=True)
