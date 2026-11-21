from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def ana_sayfa():
    return "Neural Rulet Sunucusu Calisiyor!"

@app.route('/tahmin', methods=['POST'])
def tahmin_et():
    data = request.json
    gecmis = data.get('gecmis', [])
    
    if len(gecmis) < 5:
        return jsonify({"hata": "Yetersiz veri. En az 5 spin lazım."})
        
    frekanslar = {}
    for sayi in gecmis:
        frekanslar[sayi] = frekanslar.get(sayi, 0) + 1
        
    en_cok_cikanlar = sorted(frekanslar, key=frekanslar.get, reverse=True)[:3]
    
    while len(en_cok_cikanlar) < 3:
        rast = random.randint(0, 36)
        if rast not in en_cok_cikanlar:
            en_cok_cikanlar.append(rast)

    return jsonify({
        "durum": "basarili",
        "tahminler": en_cok_cikanlar,
        "guven": "Yüksek (Bulut Sunucu)",
        "model": "Python Backend v1.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
