from datetime import datetime


# メニューを表示する関数
def show_menu():
    print("\n--- メモアプリ ---")
    print("1. メモを見る")
    print("2. メモを追加する")
    print("3. メモを削除する")
    print("4. メモを編集する")
    print("5. メモを検索する")
    print("6. 完了/未完了を切り替える")
    print("7. メモを並び替える")
    print("8. 終了する")


# memo.txt からメモを読み込む関数
# ファイルがまだ存在しないときは空のリストを返す
def read_memos():
    try:
        with open("memo.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        return []


# メモの内容を memo.txt に上書き保存する関数
def write_memos(lines):
    with open("memo.txt", "w", encoding="utf-8") as file:
        file.writelines(lines)


# 保存されているメモを一覧表示する関数
def show_memos():
    lines = read_memos()

    if lines:
        print("\n今までのメモ")
        print("---------------")
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")
    else:
        print("\nまだメモはありません。")


# 新しいメモを追加する関数
# 初期状態は [未完了] にして保存する
def add_memo():
    memo = input("新しいメモを入力してね：")

    if memo.strip() == "":
        print("空のメモは保存できません。")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_line = f"[未完了] [{now}] {memo}\n"

    with open("memo.txt", "a", encoding="utf-8") as file:
        file.write(new_line)

    print("保存したよ！")


# メモを削除する関数
def delete_memo():
    lines = read_memos()

    if not lines:
        print("削除するメモがありません。")
        return

    print("\n削除するメモを選んでね")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.strip()}")

    delete_num = input("削除する番号を入れてね：")

    if not delete_num.isdigit():
        print("数字で入力してね。")
        return

    delete_index = int(delete_num) - 1

    if not (0 <= delete_index < len(lines)):
        print("その番号はありません。")
        return

    confirm = input(
        f"本当に削除する？ {lines[delete_index].strip()} (y/n)："
    )

    if confirm.strip().lower() == "y":
        deleted_memo = lines.pop(delete_index)
        write_memos(lines)
        print(f"削除したよ：{deleted_memo.strip()}")
    else:
        print("削除をやめました。")


# メモを編集する関数
# 編集したときは日時も更新する
# 状態は今の [未完了] / [完了] をそのまま残す
def edit_memo():
    lines = read_memos()

    if not lines:
        print("編集するメモがありません。")
        return

    print("\n編集するメモを選んでね")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.strip()}")

    edit_num = input("編集する番号を入れてね：")

    if not edit_num.isdigit():
        print("数字で入力してね。")
        return

    edit_index = int(edit_num) - 1

    if not (0 <= edit_index < len(lines)):
        print("その番号はありません。")
        return

    print(f"今の内容：{lines[edit_index].strip()}")
    new_memo = input("新しい内容を入れてね：")

    if new_memo.strip() == "":
        print("空のメモにはできません。")
        return

    confirm = input("この内容で更新する？ (y/n)：")

    if confirm.strip().lower() == "y":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # もとの状態を引き継ぐ
        if lines[edit_index].startswith("[完了]"):
            status = "[完了]"
        else:
            status = "[未完了]"

        lines[edit_index] = f"{status} [{now}] {new_memo}\n"
        write_memos(lines)
        print("更新したよ！")
    else:
        print("編集をやめました。")


# キーワードでメモを検索する関数
def search_memos():
    lines = read_memos()

    if not lines:
        print("検索するメモがありません。")
        return

    keyword = input("検索したい言葉を入れてね：")

    if keyword.strip() == "":
        print("検索ワードを入れてね。")
        return

    print(f"\n「{keyword}」の検索結果")
    print("------------------")

    found = False

    for i, line in enumerate(lines, start=1):
        if keyword.lower() in line.lower():
            print(f"{i}. {line.strip()}")
            found = True

    if not found:
        print("見つかりませんでした。")


# 完了 / 未完了 を切り替える関数
def toggle_memo_status():
    lines = read_memos()

    if not lines:
        print("状態を変更するメモがありません。")
        return

    print("\n状態を変更するメモを選んでね")
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line.strip()}")

    toggle_num = input("番号を入れてね：")

    if not toggle_num.isdigit():
        print("数字で入力してね。")
        return

    toggle_index = int(toggle_num) - 1

    if not (0 <= toggle_index < len(lines)):
        print("その番号はありません。")
        return

    current_line = lines[toggle_index]

    if current_line.startswith("[完了]"):
        lines[toggle_index] = current_line.replace("[完了]", "[未完了]", 1)
        write_memos(lines)
        print("未完了に戻したよ！")
    elif current_line.startswith("[未完了]"):
        lines[toggle_index] = current_line.replace("[未完了]", "[完了]", 1)
        write_memos(lines)
        print("完了にしたよ！")
    else:
        print("状態の形式が正しくありません。")


# 並び替え用に日時を取り出す関数
# 例: [未完了] [2026-04-03 12:34:56] 買い物
def extract_datetime(line):
    parts = line.split("] [")
    if len(parts) > 1:
        date_str = parts[1].split("]")[0]
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.min
    return datetime.min


# 並び替えをする関数
def sort_memos():
    lines = read_memos()

    if not lines:
        print("並び替えるメモがありません。")
        return

    print("\n--- 並び替え ---")
    print("1. 新しい順")
    print("2. 古い順")
    print("3. 未完了を先にする")

    sort_choice = input("番号を選んでね：")

    if sort_choice == "1":
        lines.sort(key=extract_datetime, reverse=True)
        write_memos(lines)
        print("新しい順に並び替えたよ！")

    elif sort_choice == "2":
        lines.sort(key=extract_datetime)
        write_memos(lines)
        print("古い順に並び替えたよ！")

    elif sort_choice == "3":
        lines.sort(key=lambda line: line.startswith("[完了]"))
        write_memos(lines)
        print("未完了が上、完了が下になるように並び替えたよ！")

    else:
        print("1、2、3のどれかを入れてね。")


# アプリ全体を動かすメイン関数
def main():
    while True:
        show_menu()
        choice = input("番号を選んでね：")

        if choice == "1":
            show_memos()
        elif choice == "2":
            add_memo()
        elif choice == "3":
            delete_memo()
        elif choice == "4":
            edit_memo()
        elif choice == "5":
            search_memos()
        elif choice == "6":
            toggle_memo_status()
        elif choice == "7":
            sort_memos()
        elif choice == "8":
            print("アプリを終了します。")
            break
        else:
            print("1〜8のどれかを入れてね。")


# ここからアプリを開始する
main()