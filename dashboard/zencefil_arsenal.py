import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils import get_stats, search_files, mix_files

# Sayfa Ayarları
st.set_page_config(
    page_title="Zerdecalistops Arsenal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Zerdecalistops\n\n**Geliştirici:** Zencefil Efendi\n**İletişim:** zencefilefendi@gmail.com\n\n*ZERDECALISTOPS OPERATIONAL INTERFACE v2.1*"
    }
)

# Stil Özelleştirmeleri - Hyper-Cyber Tactical Interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;400&display=swap');

    /* Standart Streamlit Elemanlarını Gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stHeader"] {display:none;}
    
    /* Ana Arka Plan ve Grid */
    .stApp {
        background: #050505;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 80%),
            linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
            linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 100%, 100% 2px, 3px 100%;
    }

    /* Hareketli Tarama Çizgisi (Scanline) */
    .stApp::after {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: rgba(18, 16, 16, 0.1);
        opacity: 0;
        z-index: 2;
        pointer-events: none;
        animation: flicker 0.15s infinite;
    }

    @keyframes flicker {
        0% { opacity: 0.27861; }
        5% { opacity: 0.34769; }
        10% { opacity: 0.23604; }
        15% { opacity: 0.90626; }
        20% { opacity: 0.18128; }
        25% { opacity: 0.83891; }
        30% { opacity: 0.65583; }
        35% { opacity: 0.57807; }
        40% { opacity: 0.26559; }
        45% { opacity: 0.84693; }
        50% { opacity: 0.96019; }
        55% { opacity: 0.08594; }
        60% { opacity: 0.20313; }
        65% { opacity: 0.71988; }
        70% { opacity: 0.53455; }
        75% { opacity: 0.37288; }
        80% { opacity: 0.71428; }
        85% { opacity: 0.70419; }
        90% { opacity: 0.7003; }
        95% { opacity: 0.36108; }
        100% { opacity: 0.24387; }
    }

    /* Glitch Efekti Başlıklar */
    .glitch {
        font-family: 'Orbitron', sans-serif;
        color: #00ffff;
        position: relative;
        animation: glitch-anim 5s infinite linear alternate-reverse;
    }

    @keyframes glitch-anim {
        0% { text-shadow: -2px 0 red; }
        25% { text-shadow: 2px 0 blue; }
        50% { text-shadow: -1px 0 green; }
        75% { text-shadow: 1px 0 magenta; }
        100% { text-shadow: -2px 0 red; }
    }

    /* Global Sadeleştirme */
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace;
        color: #e0e0e0 !important;
    }
    
    h1, h2, h3 {
        color: #00ffff !important;
        background: linear-gradient(90deg, #00ffff, #008888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphism Refinement */
    div.stExpander, div.stMetric, .stAlert, div.stButton > button, .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid rgba(0, 255, 255, 0.3);
    }

    /* Buton Glow */
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        border-color: #00ffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Başlık (Sade ve Cool)
st.markdown('<h1 class="glitch">SYSTEM CORE / OPERATIONAL</h1>', unsafe_allow_html=True)
st.caption("TACTICAL DATA NODE ACCESSING...")

# Sidebar - Navigasyon (En Sade Hali)
page = st.sidebar.radio("DIRECTIVE", 
    ["MONITOR", "QUERY", "SYNTHESIS", "TACTICS", "FIELD-OPS", "INTEL", "SPECIAL-OPS", "UTILITIES"])

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if page == "MONITOR":
    st.header("📊 SYSTEM MONITOR")
    
    with st.spinner('Accessing node stats...'):
        stats = get_stats(root_dir)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Wordlist", stats['total_files'])
    col2.metric("Toplam Boyut (MB)", f"{stats['total_size'] / (1024*1024):.2f}")
    col3.metric("Kategori Sayısı", len(stats['categories']))
    
    st.markdown("---")
    
    # Grafik
    df = pd.DataFrame(list(stats['categories'].items()), columns=['Kategori', 'Dosya Sayısı'])
    fig = px.bar(df, x='Kategori', y='Dosya Sayısı', title="Data Distribution", color='Dosya Sayısı', color_continuous_scale='GnBu')
    st.plotly_chart(fig, use_container_width=True)

elif page == "QUERY":
    st.header("🔍 DATA QUERY")
    
    search_term = st.text_input("Arama Terimi (Dosya adı veya içerik)", "")
    search_content = st.checkbox("Dosya içeriklerinde de ara (Daha yavaş)")
    
    if search_term:
        with st.spinner('Mühimmat aranıyor...'):
            results = search_files(root_dir, search_term, search_content)
        
        if results:
            st.success(f"{len(results)} sonuç bulundu.")
            for res in results:
                with st.expander(f"{res['path']} ({res['type']})"):
                    try:
                        with open(os.path.join(root_dir, res['path']), 'r', errors='ignore') as f:
                            content = f.read(1000)
                            st.code(content)
                            if len(content) == 1000:
                                st.caption("...ilk 1000 karakter gösteriliyor.")
                    except Exception as e:
                        st.error(f"Dosya okunamadı: {e}")
        else:
            st.warning("Eşleşme bulunamadı.")

elif page == "SYNTHESIS":
    st.header("⚗️ Mühimmat Sentezleyici (Mixer)")
    st.info("Birden fazla wordlist'i birleştirip, tekrarları temizleyerek (deduplication) süper bir liste oluşturun.")
    
    # Dosya seçimi için tüm dosyaları listele
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        if 'dashboard' in root: continue
        if '.git' in root: continue
        for file in files:
            if not file.startswith('.'):
                rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                all_files.append(rel_path)
                
    selected_files = st.multiselect("Karıştırılacak Listeleri Seçin", all_files)
    
    output_name = st.text_input("Yeni Liste İsmi", "custom_wordlist.txt")
    
    if st.button("Sentezle ve Oluştur"):
        if not selected_files:
            st.warning("Lütfen en az bir dosya seçin.")
        else:
            with st.spinner('Sentezleniyor...'):
                full_paths = [os.path.join(root_dir, f) for f in selected_files]
                out_path, unique_count, total_count = mix_files(full_paths, output_name)
                
            st.success(f"✅ Sentez tamamlandı! '{output_name}' oluşturuldu.")
            col1, col2 = st.columns(2)
            col1.metric("Orijinal Satır Sayısı", total_count)
            col2.metric("Tekil (Unique) Satır Sayısı", unique_count)
            st.caption(f"Tekrarlanan {total_count - unique_count} satır temizlendi.")
            
            with open(out_path, "r") as f:
                st.download_button("Yeni Listeyi İndir", f, file_name=output_name)

elif page == "TACTICS":
    st.header("⚔️ Kullanım Taktikleri")
    tool = st.selectbox("Araç Seçin", ["Gobuster", "Hydra", "FFuF", "Nmap"])
    
    if tool == "Gobuster":
        st.code("gobuster dir -u http://hedef.com -w /path/to/wordlist.txt -t 50 --no-progres")
    elif tool == "Hydra":
        st.code("hydra -l admin -P /path/to/wordlist.txt ssh://hedef_ip -V")
    elif tool == "FFuF":
        st.code("ffuf -w /path/to/wordlist.txt -u http://hedef.com/FUZZ -mc 200,301")
    elif tool == "Nmap":
        st.code("nmap -p 80 --script http-enum --script-args http-enum.basepath='/',http-enum.displayall=1 -oN scan.txt hedef_ip")

elif page == "FIELD-OPS":
    from scanner import port_scan, directory_buster
    
    st.header("⚡ SAHA OPERASYONU (FIELD OPS)")
    st.warning("⚠️ DİKKAT: Bu modül gerçek hedeflere ağ trafiği gönderir. Sadece yetkili olduğunuz sistemlerde kullanın!")
    
    with st.expander("ℹ️ Test İçin Güvenli Hedefler"):
        st.markdown("""
        Eğer deneme yapmak istiyorsanız şu yasal test sitelerini kullanabilirsiniz:
        - **Port Tarama İçin:** `scanme.nmap.org` (Nmap projesinin izniyle)
        - **Dizin Tarama (DirBuster) İçin:** `http://testphp.vulnweb.com` (Acunetix tarafından test amaçlı kurulmuştur)
        """)
    
    mode = st.selectbox("Silah Seçimi", ["Zencefil Keşif (Port Scanner)", "Zencefil Bombardıman (Dir Buster)"])
    
    if mode == "Zencefil Keşif (Port Scanner)":
        target = st.text_input("Hedef IP / Domain", "scanme.nmap.org").strip()
        port_range = st.select_slider("Port Aralığı", options=["Hızlı (Top 100)", "Standart (1-1000)", "Tam (1-65535)"])
        
        if st.button("🔥 ATEŞLE (Taramayı Başlat)"):
            if port_range == "Hızlı (Top 100)":
                ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080] # Örnek
            elif port_range == "Standart (1-1000)":
                ports = range(1, 1001)
            else:
                ports = range(1, 65536)
                
            with st.spinner(f"Hedef {target} üzerinde zayıf noktalar taranıyor..."):
                open_ports = port_scan(target, ports)
                
            if open_ports:
                st.success(f"AÇIK PORTLAR TESPİT EDİLDİ: {len(open_ports)}")
                st.json(open_ports)
            else:
                st.info("Açık port bulunamadı veya hedef firewall arkasında.")
                
    elif mode == "Zencefil Bombardıman (Dir Buster)":
        target_url = st.text_input("Hedef URL", "http://testphp.vulnweb.com").strip()
        
        # Wordlist seçimi stratejisi
        st.subheader("Mühimmat Seçimi")
        list_type = st.radio("Liste Türü", ["⭐ Tavsiye Edilenler (Popüler)", "📂 Tüm Dosyalar"])
        
        selected_list = None
        
        if list_type == "⭐ Tavsiye Edilenler (Popüler)":
            # En popüler web wordlistleri
            popular_lists = {
                "Genel Tarama (common.txt)": "Discovery/Web-Content/common.txt",
                "Kapsamlı (raft-medium-directories.txt)": "Discovery/Web-Content/raft-medium-directories.txt",
                "Büyük Tarama (directory-list-2.3-medium.txt)": "Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt",
                "Hızlı (big.txt)": "Discovery/Web-Content/big.txt",
                "API Endpointleri (common-api.txt)": "Discovery/Web-Content/common-api-endpoints-mazen160.txt"
            }
            choice = st.selectbox("Seçiniz", list(popular_lists.keys()))
            selected_list = popular_lists[choice]
            
        else:
            # Tüm dosyaları listele (Yavaş olabilir)
            all_files = []
            for root, dirs, files in os.walk(root_dir):
                if 'dashboard' in root: continue
                if '.git' in root: continue
                for file in files:
                    if not file.startswith('.'):
                        rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                        all_files.append(rel_path)
            selected_list = st.selectbox("Dosya Seçin", all_files)
        
        if st.button("🚀 BOMBARDIMANI BAŞLAT"):
            if not selected_list:
                st.error("Wordlist seçilmedi!")
            else:
                full_path = os.path.join(root_dir, selected_list)
                
                # Dosya kontrolü
                if not os.path.exists(full_path):
                    st.error(f"Hata: Dosya bulunamadı: {full_path}")
                else:
                    st.info(f"Saldırı başlatıldı... Hedef: {target_url} | Mühimmat: {selected_list}")
                    
                    # İlerlemeyi göstermek zor, spinner kullanalım
                    with st.spinner("Hedef dövülüyor..."):
                         results = directory_buster(target_url, full_path, threads=20)
                    
                    if results:
                        st.success(f"{len(results)} Dizin/Dosya Keşfedildi!")
                        for res in results:
                            st.code(res)
                    else:
                        st.warning("Hiçbir şey bulunamadı.")

elif page == "INTEL":
    from scanner import analyze_headers, get_robots_txt
    
    st.header("🕵️‍♂️ Zencefil İstihbarat ve Zafiyet Analizi")
    st.info("Bu modül, hedef sisteme zarar vermeden yapılandırma hatalarını ve bilgi ifşalarını (Information Disclosure) tespit eder.")
    
    target_url = st.text_input("Hedef URL (Örn: https://example.com)", "").strip()
    
    if st.button("🔍 İSTİHBARAT TOPLA"):
        if not target_url:
            st.warning("Lütfen bir hedef girin.")
        else:
            with st.spinner("Hedef analiz ediliyor..."):
                # Header Analizi
                report = analyze_headers(target_url)
                
                # Robots.txt
                robots_content = get_robots_txt(target_url)
            
            if report.get("status") == "error":
                st.error(f"Hata oluştu: {report.get('message')}")
            else:
                st.success("Analiz Tamamlandı!")
                
                # 1. Sunucu Bilgisi (Banner Grabbing)
                st.subheader("1. Sunucu Parmak İzi (Fingerprint)")
                col1, col2 = st.columns(2)
                col1.metric("Sunucu (Server)", report["server_info"]["Server"])
                col2.metric("Teknoloji (X-Powered-By)", report["server_info"]["X-Powered-By"])
                
                # 2. Güvenlik Headerları
                st.subheader("2. Güvenlik Kalkanları (Security Headers)")
                
                if report["missing"]:
                    st.error(f"🚨 EKSİK HEADERLAR ({len(report['missing'])})")
                    for miss in report["missing"]:
                        st.write(f"- ❌ **{miss}** (Bu headerın eksik olması zafiyet yaratabilir)")
                else:
                    st.success("✅ Tüm kritik güvenlik headerları mevcut.")
                    
                if report["present"]:
                    with st.expander("Mevcut Headerlar ve Değerleri"):
                        st.json(report["present"])
                        
                # 3. Robots.txt İfşası
                st.subheader("3. Robots.txt Casusu")
                if robots_content:
                    st.warning("⚠️ Robots.txt Bulundu! İşte gizlenen dizinler:")
                    st.code(robots_content)
                else:
                    st.info("Robots.txt bulunamadı.")

elif page == "UTILITIES":
    from scanner import (dns_map, geo_ip, ssl_check, detect_cms, spider, 
                         extract_emails, extract_comments, identify_hash, 
                         universal_decode, check_password_in_zerdecalistops)
    
    st.header("🛠️ Zencefil İsviçre Çakısı (Universal Tools)")
    st.info("Hızlı operasyonlar için tasarlanmış çok amaçlı araç seti.")
    
    tab1, tab2, tab3 = st.tabs(["🌐 Keşif (Recon)", "📧 Veri Sızdırma (Extraction)", "🔐 Kripto & Araçlar"])
    
    with tab1:
        st.subheader("Bölge Keşif Araçları")
        tool_choice = st.selectbox("Araç Seçin", ["DNS Haritası", "GeoIP Analizi", "SSL Röntgeni", "CMS Dedektifi", "Ağ Örümceği"])
        
        target = st.text_input("Hedef (Domain veya IP)", "").strip()
        
        if st.button("ÇALIŞTIR", key="recon_btn"):
            if not target: st.warning("Hedef giriniz.")
            else:
                with st.spinner("Analiz ediliyor..."):
                    if tool_choice == "DNS Haritası":
                        res = dns_map(target)
                        st.json(res)
                    elif tool_choice == "GeoIP Analizi":
                        res = geo_ip(target)
                        if res.get('status') == 'success':
                            col1, col2 = st.columns(2)
                            col1.write(f"**Ülke:** {res['country']}")
                            col1.write(f"**Şehir:** {res['city']}")
                            col2.write(f"**ISS:** {res['isp']}")
                            col2.write(f"**IP:** {res['query']}")
                            st.map(pd.DataFrame({'lat': [res['lat']], 'lon': [res['lon']]}))
                        else: st.error("Hata!")
                    elif tool_choice == "SSL Röntgeni":
                        res = ssl_check(target)
                        st.json(res)
                    elif tool_choice == "CMS Dedektifi":
                        res = detect_cms(target)
                        for r in res: st.write(f"- {r}")
                    elif tool_choice == "Ağ Örümceği":
                        res = spider(target)
                        st.write(f"Bulunan {len(res)} link:")
                        st.code("\n".join(res))
                        
    with tab2:
        st.subheader("İçerik Kazıma & Hunt")
        ext_choice = st.selectbox("Kazıma Türü", ["E-Posta Avcısı", "HTML Yorum Casusu", "Akıllı Desen Avcısı (Pattern Hunter)"])
        ext_url = st.text_input("URL", key="ext_url").strip()
        
        if st.button("OPERASYONU BAŞLAT"):
            if not ext_url: st.warning("URL giriniz.")
            else:
                with st.spinner("Mühimmatlarla hedef taranıyor..."):
                    if ext_choice == "E-Posta Avcısı":
                        res = extract_emails(ext_url)
                        if res: st.success(f"{len(res)} mail bulundu:"); st.write(res)
                        else: st.info("Mail bulunamadı.")
                    elif ext_choice == "HTML Yorum Casusu":
                        res = extract_comments(ext_url)
                        if res: st.success(f"{len(res)} yorum bulundu:"); st.write(res)
                        else: st.info("Yorum bulunamadı.")
                    else:
                        from scanner import smart_pattern_scan
                        res = smart_pattern_scan(ext_url, root_dir)
                        if res:
                            st.warning("⚠️ ÖNEMLİ BULGULAR (zerdecalistops Wordlist Eşleşmesi):")
                            for cat, findings in res.items():
                                with st.expander(cat):
                                    for f in findings: st.write(f"- {f}")
                        else:
                            st.success("✅ Temiz. Herhangi bir sızıntı veya hata dizgisi bulunamadı.")
                        
    with tab3:
        st.subheader("Şifreleme ve Yardımcı Araçlar")
        util_choice = st.selectbox("İşlem", ["Hash Teşhisi", "Şifre Sızıntı Kontrolü", "Universal Decoder"])
        
        if util_choice == "Hash Teşhisi":
            h_input = st.text_input("Hash Değeri")
            if h_input:
                st.write(f"**Tahmin Edilen Tür:** {identify_hash(h_input)}")
                
        elif util_choice == "Şifre Sızıntı Kontrolü":
            p_input = st.text_input("Şifre", type="password")
            if st.button("KONTROL ET"):
                res = check_password_in_zerdecalistops(p_input, root_dir)
                if res:
                    st.error(f"🚨 DİKKAT: Bu şifre şu sızıntı listelerinde bulundu: {', '.join(res)}")
                else: 
                    st.success("✅ Güvenli! Bu şifre zerdecalistops'in popüler listelerinde yok.")
                    
        elif util_choice == "Universal Decoder":
            d_input = st.text_area("Şifreli Veri")
            m_input = st.selectbox("Yöntem", ["Base64", "URL", "Hex"])
            if st.button("ÇÖZ"):
                st.code(universal_decode(d_input, m_input))

elif page == "SPECIAL-OPS":
    from scanner import passive_subdomain_enum, detect_waf
    
    st.header("👻 Zencefil Özel Kuvvetler (Genius Ops)")
    st.info("Bu modüller **GÖRÜNMEZDİR**. Hedef sistem sizin IP adresinizi loglayamaz (Passive Recon).")
    
    op_mode = st.radio("Operasyon Modu", ["Hayalet Keşif (Subdomain Enum)", "Kalkan Avcısı (WAF Detector)"])
    
    if op_mode == "Hayalet Keşif (Subdomain Enum)":
        st.subheader("☁️ Pasif Alt Alan Adı Keşfi")
        st.write("`crt.sh` veritabanını kullanarak hedefin SSL sertifikalarından alt alan adlarını (subdomain) çıkarır.")
        
        target_domain = st.text_input("Hedef Domain (Örn: google.com)", "").strip()
        
        if st.button("👻 HAYALETİ GÖNDER"):
            if not target_domain:
                st.warning("Domain giriniz.")
            else:
                with st.spinner("Sertifika okyanusu taranıyor..."):
                    subs = passive_subdomain_enum(target_domain)
                    
                if subs:
                    st.success(f"{len(subs)} adet Subdomain bulundu!")
                    st.json(subs)
                else:
                    st.warning("Sonuç bulunamadı veya bağlantı hatası.")
                    
    elif op_mode == "Kalkan Avcısı (WAF Detector)":
        st.subheader("🛡️ Web Güvenlik Duvarı (WAF) Tespiti")
        st.write("Hedefin önünde bir koruma kalkanı (Cloudflare, Akamai vb.) olup olmadığını analiz eder.")
        
        waf_target = st.text_input("Hedef URL", "").strip()
        
        if st.button("🛡️ KALKANI ANALİZ ET"):
            if not waf_target:
                st.warning("URL giriniz.")
            else:
                with st.spinner("Kalkan frekansları dinleniyor..."):
                    wafs = detect_waf(waf_target)
                    
                if wafs:
                    st.error(f"🚨 KALKAN TESPİT EDİLDİ: {', '.join(wafs)}")
                    st.info("Saldırı yaparken bu kalkanları atlatacak (WAF Bypass) listeleri kullanmalısın.")
                else:
                    st.success("✅ Doğrudan Bağlantı! (Herhangi bir WAF imzası görülmedi)")
                    st.caption("Not: Gizli veya özel bir WAF olabilir, ama bilinen majör kalkanlar yok.")
