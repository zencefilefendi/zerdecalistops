#!/usr/bin/env python3
import os
import sys
import argparse

# Renk kodları
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def banner():
    print(f"""{GREEN}
    ZENCEFİL EFENDİ ARAMA ARACI
    ---------------------------
    Bu araç, wordlistler içinde hızlı arama yapmanızı sağlar.
    {RESET}""")

def search_files(search_term, search_contents=False):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    matches = []
    
    print(f"{YELLOW}[*] '{search_term}' aranıyor...{RESET}")
    
    for root, dirs, files in os.walk(root_dir):
        # .git ve benzeri gizli klasörleri atla
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file == "zencefil_arama.py":
                continue
                
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, root_dir)
            
            # Dosya isminde arama
            if search_term.lower() in file.lower():
                print(f"{GREEN}[DOSYA BULUNDU] {relative_path}{RESET}")
                matches.append(relative_path)
            
            # Dosya içeriğinde arama (eğer istenirse)
            if search_contents:
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if search_term.lower() in line.lower():
                                print(f"{BOLD}[İÇERİK] {relative_path}:{i} -> {line.strip()[:100]}{RESET}")
                                matches.append(f"{relative_path}:{i}")
                                # Bir dosyada çok fazla eşleşme varsa boğulmamak için break atabiliriz
                                # ama şimdilik bırakalım.
                except Exception as e:
                    pass

    if not matches:
        print(f"{RED}[-] Hiçbir eşleşme bulunamadı.{RESET}")
    else:
        print(f"\n{GREEN}[+] Toplam {len(matches)} eşleşme bulundu.{RESET}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Zencefil Efendi Wordlist Arama Aracı")
    parser.add_argument("terim", help="Aranacak kelime veya dosya ismi")
    parser.add_argument("-c", "--content", action="store_true", help="Dosya içeriklerinde de ara (Yavaş olabilir!)")
    
    args = parser.parse_args()
    
    try:
        search_files(args.terim, args.content)
    except KeyboardInterrupt:
        print(f"\n{RED}[!] İşlem iptal edildi.{RESET}")

if __name__ == "__main__":
    main()
