import socket
import requests
import concurrent.futures

def port_scan(target, ports):
    open_ports = []
    
    # Hedef çözümleme
    try:
        ip = socket.gethostbyname(target)
    except:
        return []

    def check_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return port
            sock.close()
        except:
            pass
        return None

    # Threading ile hızlandırılmış tarama
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(check_port, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
                
    return sorted(open_ports)

def directory_buster(url, wordlist_path, threads=10):
    found_dirs = []
    
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
    except:
        return []

    def check_dir(word):
        target_url = f"{url.rstrip('/')}/{word}"
        try:
            # Sadece header alarak hız kazan (HEAD request)
            res = requests.head(target_url, timeout=3, allow_redirects=True)
            if res.status_code == 200:
                return f"[200] {target_url}"
            elif res.status_code == 301 or res.status_code == 302:
                return f"[{res.status_code}] {target_url} -> {res.headers.get('Location')}"
            elif res.status_code == 403:
                return f"[403] {target_url}"
        except:
            pass
        return None

    # Threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check_dir, word): word for word in words}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found_dirs.append(result)
                
    return found_dirs

def analyze_headers(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
            
        res = requests.get(url, timeout=5)
        headers = res.headers
        
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-XSS-Protection",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]
        
        missing = []
        present = {}
        
        for h in security_headers:
            if h in headers:
                present[h] = headers[h]
            else:
                missing.append(h)
                
        server = headers.get("Server", "Gizli/Belirtilmemiş")
        powered_by = headers.get("X-Powered-By", "Gizli/Belirtilmemiş")
        
        return {
            "status": "success",
            "missing": missing,
            "present": present,
            "server_info": {"Server": server, "X-Powered-By": powered_by}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_robots_txt(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
            
        robots_url = f"{url.rstrip('/')}/robots.txt"
        res = requests.get(robots_url, timeout=5)
        if res.status_code == 200:
            return res.text
        return None
    except:
        return None

def passive_subdomain_enum(domain):
    """crt.sh üzerinden pasif subdomain keşfi"""
    subdomains = set()
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        pkgs = requests.get(url, headers=headers, timeout=10).json()
        
        for p in pkgs:
            name = p['name_value']
            if "\n" in name:
                for sub in name.split("\n"):
                    if domain in sub and "*" not in sub:
                        subdomains.add(sub.lower())
            else:
                if domain in name and "*" not in name:
                    subdomains.add(name.lower())
                    
        return sorted(list(subdomains))
    except Exception as e:
        return [f"Hata: {str(e)}"]

def detect_waf(url):
    """Basit WAF Tespiti (Header ve Cookie Analizi)"""
    waf_signatures = {
        "Cloudflare": ["cf-ray", "__cfduid", "cf-cache-status", "server: cloudflare"],
        "Imperva Incapsula": ["incap_ses", "visid_incap", "x-cdn: incap"],
        "Akamai": ["akamai-ghost", "x-akamai", "akamai-x-get-cache-key"],
        "AWS WAF": ["x-amzn-requestid", "x-amz-cf-id", "awselb/2.0"],
        "F5 BIG-IP": ["bigipserver", "x-cnection: close"],
        "Sucuri": ["sucuri_cloudproxyid", "x-sucuri"]
    }
    
    detected = []
    try:
        if not url.startswith("http"):
            url = "http://" + url
            
        res = requests.get(url, timeout=5)
        headers = str(res.headers).lower()
        cookies = str(res.cookies.get_dict()).lower()
        
        combined_data = headers + cookies
        
        for waf, sigs in waf_signatures.items():
            for sig in sigs:
                if sig.lower() in combined_data:
                    detected.append(waf)
                    break
                    
        return list(set(detected))
    except:
        return []

# --- ULTIMATE ARSENAL: RECON ---
import dns.resolver
import socket
import ssl
from bs4 import BeautifulSoup, Comment
import re
import base64
import urllib.parse
from datetime import datetime

def dns_map(domain):
    """DNS Kayıtlarını Çeker"""
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    for r in record_types:
        try:
            answers = dns.resolver.resolve(domain, r)
            records[r] = [str(data) for data in answers]
        except:
            continue
    return records

def geo_ip(target):
    """IP Coğrafi Konum (GeoIP)"""
    try:
        # IP'ye çevir (eğer domain ise)
        ip = socket.gethostbyname(target)
        url = f"http://ip-api.com/json/{ip}"
        res = requests.get(url, timeout=5).json()
        return res
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def ssl_check(domain):
    """SSL Sertifika Analizi"""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            
        subject = dict(x[0] for x in cert['subject'])
        issuer = dict(x[0] for x in cert['issuer'])
        not_after = cert['notAfter']
        
        return {
            "Subject": subject.get('common_name') if 'common_name' in subject else subject.get('commonName'),
            "Issuer": issuer.get('common_name') if 'common_name' in issuer else issuer.get('commonName'),
            "Expires": not_after,
            "Version": cert.get('version')
        }
    except Exception as e:
        return {"error": str(e)}

def detect_cms(url):
    """CMS Tespiti (WordPress, Joomla, Drupal)"""
    try:
        if not url.startswith("http"): url = "http://" + url
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        meta_gen = soup.find("meta", attrs={"name": "generator"})
        
        detected = []
        if meta_gen and meta_gen.get("content"):
            detected.append(f"Meta Generator: {meta_gen['content']}")
            
        if "/wp-content/" in res.text: detected.append("WordPress (Dosya Yapısı)")
        if "/components/com_" in res.text: detected.append("Joomla (Dosya Yapısı)")
        if "/sites/default/files/" in res.text: detected.append("Drupal (Dosya Yapısı)")
        
        return detected if detected else ["Bilinmiyor / Özel Yazılım"]
    except:
        return ["Hata"]

def spider(url, max_links=50):
    """Basit Ağ Örümceği"""
    links = set()
    try:
        if not url.startswith("http"): url = "http://" + url
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith(('http', 'https', '/')):
                links.add(href)
                if len(links) >= max_links: break
        return list(links)
    except:
        return []

# --- ULTIMATE ARSENAL: DATA EXTRACTION ---
def extract_emails(url):
    """E-Posta Avcısı"""
    try:
        if not url.startswith("http"): url = "http://" + url
        res = requests.get(url, timeout=5)
        emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", res.text, re.I))
        return list(emails)
    except:
        return []

def extract_comments(url):
    """HTML Yorumlarını Okur"""
    try:
        if not url.startswith("http"): url = "http://" + url
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        return [c.strip() for c in comments if c.strip()]
    except:
        return []

# --- ULTIMATE ARSENAL: CRYPTO & TOOLS ---
def identify_hash(hash_str):
    """Hash Türü Tahmini"""
    l = len(hash_str)
    if l == 32: return "MD5 / NTLM"
    if l == 40: return "SHA-1 / MySQL5"
    if l == 64: return "SHA-256"
    if l == 96: return "SHA-384"
    if l == 128: return "SHA-512 / Whirlpool"
    return "Bilinmiyor"

def universal_decode(data, method):
    """Universal Decoder"""
    try:
        if method == "Base64": return base64.b64decode(data).decode()
        if method == "URL": return urllib.parse.unquote(data)
        if method == "Hex": return bytes.fromhex(data).decode()
        return "Geçersiz Yöntem"
    except Exception as e:
        return f"Hata: {str(e)}"

def smart_pattern_scan(url, root_dir):
    """Zerdecalistops Pattern-Matching wordlistlerini kullanarak hedebi tarar"""
    patterns = {
        "Hata Mesajları (Information Disclosure)": "Pattern-Matching/errors.txt",
        "Zararlı / Şüpheli Dizgiler": "Pattern-Matching/malicious.txt",
        "Potansiyel Sızıntı Kaynakları": "Pattern-Matching/repo-scan.txt"
    }
    
    findings = {}
    try:
        if not url.startswith("http"): url = "http://" + url
        res = requests.get(url, timeout=5)
        content = res.text
        
        for cat, rel_path in patterns.items():
            full_path = os.path.join(root_dir, rel_path)
            cat_findings = []
            if os.path.exists(full_path):
                with open(full_path, 'r', errors='ignore') as f:
                    for line in f:
                        pattern = line.strip()
                        if pattern and pattern in content:
                            cat_findings.append(pattern)
            if cat_findings:
                findings[cat] = cat_findings
        return findings
    except Exception as e:
        return {"error": str(e)}

def check_password_in_zerdecalistops(password, root_dir):
    """Zerdecalistops içinde şifre araması yapar"""
    # En popüler şifre listelerini tara
    target_lists = [
        "Passwords/Common-Credentials/xato-net-10-million-passwords-1000.txt",
        "Passwords/Common-Credentials/10k-most-common.txt",
        "Passwords/Common-Credentials/best110.txt",
        "Passwords/Common-Credentials/top-20-common-passwords.txt"
    ]
    
    found_in = []
    for rel_path in target_lists:
        full_path = os.path.join(root_dir, rel_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', errors='ignore') as f:
                    if password in f.read():
                        found_in.append(rel_path)
            except:
                continue
    return found_in
