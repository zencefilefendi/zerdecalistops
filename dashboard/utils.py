import os

def get_stats(root_dir):
    stats = {
        'total_files': 0,
        'categories': {},
        'total_size': 0
    }
    
    exclude_dirs = {'.git', '.github', '.bin', 'dashboard', '__pycache__'}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.startswith('.'): continue
            
            stats['total_files'] += 1
            file_path = os.path.join(root, file)
            stats['total_size'] += os.path.getsize(file_path)
            
            # Kategori belirleme (kök dizindeki ilk klasör)
            rel_path = os.path.relpath(root, root_dir)
            category = rel_path.split(os.sep)[0]
            if category == '.': category = 'Uncategorized'
            
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
    return stats

def search_files(root_dir, search_term, search_content=False, limit=50):
    results = []
    exclude_dirs = {'.git', '.github', '.bin', 'dashboard', '__pycache__'}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.startswith('.'): continue
            if len(results) >= limit: break
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            
            if search_term.lower() in file.lower():
                results.append({'path': rel_path, 'type': 'Filename Match'})
                continue
            
            if search_content:
                try:
                    with open(full_path, 'r', errors='ignore') as f:
                        for i, line in enumerate(f):
                            if search_term.lower() in line.lower():
                                results.append({'path': rel_path, 'type': f'Content Match (Line {i+1})'})
                                break
                except:
                    pass
    return results

def mix_files(file_paths, output_filename):
    unique_lines = set()
    total_lines = 0
    
    for path in file_paths:
        try:
            with open(path, 'r', errors='ignore') as f:
                for line in f:
                    clean_line = line.strip()
                    if clean_line:
                        unique_lines.add(clean_line)
                        total_lines += 1
        except Exception as e:
            print(f"Hata: {path} okunamadı - {e}")
            
    # Kaydet
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in sorted(unique_lines):
            f.write(line + '\n')
            
    return output_path, len(unique_lines), total_lines
