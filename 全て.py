import os

def merge_files_recursively(input_dir: str, output_file: str, encoding='utf-8'):
    with open(output_file, 'w', encoding=encoding) as outfile:
        for root, dirs, files in os.walk(input_dir):
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            for filename in sorted(files):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding=encoding) as infile:
                        content = infile.read()
                    outfile.write(content)
                    outfile.write("\n\n")
                except Exception as e:
                    print(f"ファイル読み込み失敗: {filepath} ({e})")

if __name__ == "__main__":
    merge_files_recursively(
        "C:/Users/近藤和弘/Desktop/プロジェクト/pybriger/pybriger",
        "c:/Users/近藤和弘/Desktop/プロジェクト/pybriger/全て.txt"
    )
