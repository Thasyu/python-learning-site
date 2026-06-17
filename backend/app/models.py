#モデル定義を行うモジュール
from dataclasses import dataclass

#問題データの構造を定義するクラス
from typing import List

@dataclass
class Question:
    id: str
    chapter_id: int
    category: str
    difficulty: int
    question: str
    starter_code: str
    ending_code: str
    judge_code: str
    expected_output: str
    required_keywords: List[str]
    model_answers: List[str]
    hints: List[str]
    explanation: str

@dataclass
class ResultRecord:
    question_id: str
    chapter:int
    is_correct: bool
    submitted_code: str
    actual_output: str
    answer_at: str