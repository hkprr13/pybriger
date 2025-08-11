import os

def save_directory_structure_with_sources(root_dir, output_file):
    output_file_abs = os.path.abspath(output_file)
    def walk(dir_path, prefix="", is_last=True, file_writer=None):
        basename = os.path.basename(dir_path)
        if basename == "__pycache__":
            return
        branch = "└── " if is_last else "├── "
        file_writer.write(f"{prefix}{branch}[{basename}]\n")
        new_prefix = prefix + ("    " if is_last else "│   ")

        entries = sorted(os.listdir(dir_path))
        dirs = [d for d in entries if os.path.isdir(os.path.join(dir_path, d)) and d != "__pycache__"]
        files = [f for f in entries if os.path.isfile(os.path.join(dir_path, f))]

        total = len(dirs) + len(files)
        for idx, entry in enumerate(dirs + files):
            path = os.path.join(dir_path, entry)
            is_last_entry = (idx == total - 1)
            if os.path.abspath(path) == output_file_abs:
                continue  # 出力ファイル自身はスキップ
            if os.path.isdir(path):
                walk(path, new_prefix, is_last_entry, file_writer)
            else:
                if entry == "dir.py":
                    continue
                if entry == "dir2.py":
                    continue
                if entry == "test.py":
                    continue
                if entry == "test2.py":
                    continue
                if entry == "test3.py":
                    continue
                branch = "└── " if is_last_entry else "├── "
                file_writer.write(f"{new_prefix}{branch}{entry}\n")

                # .pyファイルなどテキストファイルの中身を表示
                if entry.endswith((".py", ".txt", ".md")):
                    try:
                        with open(path, encoding="utf-8") as file:
                            lines = file.readlines()
                            file_writer.write(f"{new_prefix}    ↓ 内容（最大10000行）\n")
                            for i, line in enumerate(lines[:10000]):
                                clean_line = line.rstrip()
                                file_writer.write(f"{new_prefix}    {clean_line}\n")
                            if len(lines) > 10000:
                                file_writer.write(f"{new_prefix}    ...（以下省略）\n")
                    except Exception as e:
                        file_writer.write(f"{new_prefix}    ※ 読み込みエラー: {e}\n")

    with open(output_file, "w", encoding="utf-8") as f:
        walk(root_dir, "", True, f)

# 使用例
save_directory_structure_with_sources(
    "C:/Users/近藤和弘/Desktop/プロジェクト/pybriger/pybriger",
    "c:/Users/近藤和弘/Desktop/プロジェクト/pybriger/pybriger/全て.txt"
)
