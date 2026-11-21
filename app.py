from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
# Tarayıcının (uygulamamızın) bu sunucuya istek atmasına izin veriyoruz
CORS(app) 

@app.route('/')
def ana_sayfa():
    return "Neural Rulet Sunucusu 7/24 Aktif!"

@app.route('/tahmin', methods=['POST'])
def tahmin_et():
    data = request.json
    gecmis = data.get('gecmis', [])
    
    if len(gecmis) < 5:
        return jsonify({"hata": "Yetersiz veri."})
        
    # --- GELİŞMİŞ PYTHON ANALİZİ (Markov + Frekans) ---
    
    # 1. Frekans Analizi: En çok çıkan sayıları bul
    frekanslar = {}
    for sayi in gecmis:
        frekanslar[sayi] = frekanslar.get(sayi, 0) + 1
    en_cok_cikanlar = sorted(frekanslar, key=frekanslar.get, reverse=True)
    
    # 2. Markov Zinciri: Son gelen sayıdan sonra ne gelmiş?
    son_sayi = gecmis[-1]
    markov_gecisleri = {}
    for i in range(len(gecmis)-1):
        if gecmis[i] == son_sayi:
            sonraki = gecmis[i+1]
            markov_gecisleri[sonraki] = markov_gecisleri.get(sonraki, 0) + 1
            
    markov_sirali = sorted(markov_gecisleri, key=markov_gecisleri.get, reverse=True)
    
    # 3. Harmanlama (Markov ve Frekansı Birleştir)
    tahminler = []
    # Önce Markov'un en güçlü olduğu sayıyı ekle
    if len(markov_sirali) > 0:
        tahminler.append(markov_sirali[0])
        
    # Sonra frekansı yüksek olanları ekle (aynı sayıyı ekleme)
    for s in en_cok_cikanlar:
        if s not in tahminler:
            tahminler.append(s)
        if len(tahminler) == 3:
            break
            
    # Eğer 3'e ulaşamadıysa rastgele doldur
    while len(tahminler) < 3:
        rast = random.randint(0, 36)
        if rast not in tahminler:
            tahminler.append(rast)

    return jsonify({
        "durum": "basarili",
        "tahminler": tahminler,
        "guven": "Bulut Zekası (Markov)",
        "model": "Python Backend v2.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
