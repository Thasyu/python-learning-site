#ランダムな問題を出すため
import random

#コードの実行と正誤判定を行う関数のインポート
from backend.app.judge import judge

#ユーザーの入力を処理する関数のインポート
from backend.app.input_handler import (read_user_code, choose_chapter, choose_question_count, choose_random_mode)

#問題データのインポート
from backend.app.chapter_manager import get_chapters

#結果の記録と進捗管理の関数のインポート
from backend.app.progress_manager import create_result_record, append_progress, get_user_id

#復習データの管理関数のインポート
from backend.app.review import add_to_review_queue, remove_from_review_queue

#メインの関数
def ask_question(question_data, question_number, total_questions, wrong_questions, session_results, user_id):
    print(f"\n=== 問題 {question_number} / {total_questions} ===")
    print(f"カテゴリー: {question_data['category']}")
    print(question_data["question"])

    if question_data["starter_code"]:
        print("\n=== 最初からあるコード ===")
        print(question_data["starter_code"])

    if question_data["ending_code"]:
        print("\n=== 最後に続くコード ===")
        print(question_data["ending_code"])

    hint_index = 0

    while True:
        user_input = input("\n回答を入力（ヒントが欲しい場合は「hint」と入力）:")

        #ヒントの表示
        if user_input.lower() == "hint":
            if hint_index < len(question_data["hints"]):
                print(question_data["hints"][hint_index])
                hint_index += 1
            else:
                print("これ以上ヒントはありません。")
            continue

        user_code = read_user_code(user_input)
        is_correct, message, actual_output = judge(question_data, user_code)

        #回答の判定
        if is_correct:
            record = create_result_record(
                user_id=user_id,
                question_data=question_data,
                is_correct=True,
                submitted_code=user_code,
                actual_output=actual_output
            )
            append_progress(record)
            remove_from_review_queue(user_id, question_data["id"])

            print("\n 正解")
            print("\n=== 解説 ===")
            print(question_data["explanation"])

            session_results.append({
                "chapter": question_data["chapter"],
                "difficulty": question_data["difficulty"],
                "is_correct": True
            })

            return 1
        
        else:
            record = create_result_record(
                user_id=user_id,
                question_data=question_data,
                is_correct=False,
                submitted_code=user_code,
                actual_output=actual_output
            )
            append_progress(record)
            add_to_review_queue(user_id, question_data["id"])
            
            print("\n 不正解")
            print(message)

            session_results.append({
                "chapter": question_data["chapter"],
                "difficulty": question_data["difficulty"],
                "is_correct": False
            })

            if "model_answers" in question_data:
                print("=== 模範解答 ===")
                for ans in question_data["model_answers"]:
                    print(ans)
                    print("---")
            print("\n=== 解説 ===")
            print(question_data["explanation"])

            #間違えた問題を保存
            wrong_questions.append(question_data)

            return 0
        
#クイズを実行するメインの関数
def run_quiz():
    score = 0
    session_results = []

    print("===python学習アプリ===")

    username = input("ユーザー名を入力してください: ").strip()
    user_id = get_user_id(username)

    if not user_id:
        print("ユーザーが存在しません。先にWeb画面から登録してください。")
        return

    chapters = get_chapters()
    selected_chapter = choose_chapter(chapters)
    chapter_name = chapters[selected_chapter]["name"]
    quiz_questions = chapters[selected_chapter]["questions"].copy()

    print(f"\n選択したchapter: {chapter_name}")

    random_mode = choose_random_mode()
    if random_mode == "y":
        random.shuffle(quiz_questions)

    #間違えた問題を保存するリスト
    wrong_questions = []
    
    #ユーザーが出題する問題数を選択
    selected_count = choose_question_count(len(quiz_questions))
    quiz_questions = quiz_questions[:selected_count]

    #問題の総数を取得
    total_questions = len(quiz_questions)

    print(f"{total_questions}問出題します。")

    for i, question in enumerate(quiz_questions, start=1):
        score += ask_question(question, i, total_questions, wrong_questions, session_results, user_id)

    #最終スコアの表示
    print("\n======================")
    print(f"\n=== 結果 ===")
    print("\n====================")
    print(f"正解数: {score} / {total_questions}")

    print("\n=== 今回のchapter成績 ===")

    chapter_stats = {}

    for record in session_results:
        chapter = record["chapter"]

        if chapter not in chapter_stats:
            chapter_stats[chapter] = {"total": 0, "correct": 0}
        
        chapter_stats[chapter]["total"] += 1
        if record["is_correct"]:
            chapter_stats[chapter]["correct"] += 1
        
    for chapter, data in chapter_stats.items():
        total = data["total"]
        correct = data["correct"]
        rate = (correct / total) * 100 if total > 0 else 0
        print(f"chapter {chapter}: {correct} / {total} 正答率: ({rate:.1f}%)")

    print("\n=== 今回のdifficulty別成績 ===")

    difficulty_stats = {}

    for record in session_results:
        difficulty = record["difficulty"]

        if difficulty not in difficulty_stats:
            difficulty_stats[difficulty] = {"total": 0, "correct": 0}
        
        difficulty_stats[difficulty]["total"] += 1
        if record["is_correct"]:
            difficulty_stats[difficulty]["correct"] += 1

    for difficulty, data in difficulty_stats.items():
        total = data["total"]
        correct = data["correct"]
        rate = (correct / total) * 100 if total > 0 else 0
        print(f"difficulty {difficulty}: {correct} / {total} ({rate:.1f}%)")

    #復習するか確認
    if wrong_questions:
        review = input("\n間違えた問題を復習しますか？ (y/n): ")

        if review.lower() == "y":
            print("\n=== 復習モード ===")

            for i, question in enumerate(wrong_questions, start=1):
                ask_question(question, i, len(wrong_questions), [], session_results, user_id)
            
        else:
            print("\n学習を終了します。")

        #スコアに応じたメッセージの表示
        if score == total_questions:
            print("素晴らしい！全問正解です！")
        elif score >= total_questions / 2:
            print("お疲れ様！半分以上正解です！")
        else:
            print("もう少し頑張りましょう！")
    else:
        print("\n全問正解です！素晴らしい！")