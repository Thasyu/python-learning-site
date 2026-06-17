from backend.app.judge import judge


def show(label, res):
    print(label, '=>', res)

q_random = {
    'judge_type': 'random_output_and_keywords',
    'starter_code': '',
    'ending_code': '',
    'required_keywords': ['random', 'print'],
    'expected_output': '',
    'output_validator': 'int_range_1_10_lines3',
}

show('ok_case', judge(q_random, 'import random\nfor _ in range(3):\n    print(random.randint(1,10))'))
show('kw_missing_case', judge(q_random, 'for _ in range(3):\n    print(5)'))
show('error_case', judge(q_random, 'import random\nprint(10/0)'))
