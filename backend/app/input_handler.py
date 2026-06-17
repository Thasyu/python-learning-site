#ユーザーからコードを複数行入力してもらう関数  
def read_user_code(first_line=""):
    print("\nコードを入力してください。入力が終わったら END を入力してください。")
    lines = []

    if first_line.strip():
        lines.append(first_line)

    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    return "\n".join(lines)

#ユーザーにchapterを選んでもらう関数
def choose_chapter(chapters):
    while True:
        print("\n学習するchapterを選んでください。")

        for chapter_id, chapter_info in chapters.items():
            print(f"{chapter_id}: {chapter_info['name']}")

        user_input = input("chapter番号を入力してください: ")

        if not user_input.isdigit():
            print("数字を入力してください。")
            continue

        chapter_id = int(user_input)

        if chapter_id in chapters:
            return chapter_id
        else:
            print("存在するchapter番号を入力してください。")

#出題する問題数をユーザーが選択        
def choose_question_count(max_questions):
    while True:
        user_input = input(f"\n何問出題しますか？ (1～{max_questions}): ")

        if not user_input.isdigit():
            print("数字を入力してください。")
            continue

        count = int(user_input)

        if 1 <= count <= max_questions:
            return count
        else:
            print(f"1～{max_questions}の数字を入力してください。")

#ランダムに問題を出すかどうかをユーザーが選択
def choose_random_mode():
    while True:
        user_input = input("\n問題をランダムに出題しますか？ (y/n): ")

        if user_input in ["y", "n"]:
            return user_input
        else:
            print("y または n を入力してください。")