#!/bin/bash
echo "🛡️  Zencefil Arsenali Başlatılıyor..."
echo "📊 Dashboard hazırlanıyor..."

# Bağımlılıkları kontrol et ve yükle
echo "📦 Bağımlılıklar kontrol ediliyor..."
python3 -m pip install -q -r dashboard/requirements.txt

python3 -m streamlit run dashboard/zencefil_arsenal.py
