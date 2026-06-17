const CHAPTER_PAGE_DATA = {
	chapter1: {
		number: 1,
		title: "出力と基本",
		summary: "Pythonの最初の一歩として、printで内容を表示しながらコード実行の感覚をつかみます。",
		goals: [
			"printを使えるようになる",
			"Pythonの基本的な書き方を理解する",
			"コードを実行する感覚をつかむ"
		],
		explanation: [
			"Pythonでは、書いたコードを上から順に実行していきます。最初に慣れるべきなのが、文字や値を画面に表示する print です。",
			"print を使うと、自分が書いたコードがどう動いたかをすぐ確認できます。学習の初期段階では、まず表示結果を見ながら理解する流れが重要です。"
		],
		sampleCode: 'print("こんにちは")\nprint("Pythonへようこそ")',
		output: "こんにちは\nPythonへようこそ",
		calcOperators: [
			{ symbol: "+", meaning: "足し算", code: "print(5 + 3)", output: "8" },
			{ symbol: "-", meaning: "引き算", code: "print(10 - 4)", output: "6" },
			{ symbol: "*", meaning: "掛け算", code: "print(3 * 4)", output: "12" },
			{ symbol: "/", meaning: "割り算", code: "print(10 / 2)", output: "5.0" },
			{ symbol: "//", meaning: "切り捨て除算", code: "print(10 // 3)", output: "3" },
			{ symbol: "%", meaning: "余り", code: "print(10 % 3)", output: "1" },
			{ symbol: "**", meaning: "累乗（べき乗）", code: "print(2 ** 3)", output: "8" }
		],
		points: [
			"1行ずつ順番に実行されることを意識する",
			"文字列は、 ' ' または \" \" で囲んで表します。",
			"まずは出力して確かめる習慣をつける"
		],
		practice: {
			title: "試してみよう",
			instruction: "printを使って、好きな言葉を表示してみましょう。",
			starterCode: 'print("こんにちは")',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"まずはサンプルコードを少し変えて実行してみましょう。",
				"エラーが出た場合は、文字列のクォーテーションやインデントを確認しましょう。"
			]
		}
	},
	chapter2: {
		number: 2,
		title: "変数と型",
		summary: "変数への値の保存と、文字・数字・True/False などの型の基本を学びます。",
		goals: [
			"変数に値を代入できる",
			"値には型があることを理解する",
			"int や str を使った型変換を試せる"
		],
		explanation: [
			"変数は、データに名前を付けて保管するための仕組みです。値をそのまま何度も書くより、意味のある名前を付ける方が読みやすくなります。",
			"Pythonでは、文字・数字・True / False など、値の種類を『型』として区別しています。",
			"同じ『値』でも、文字なのか数字なのかによって扱い方が変わります。"
		],
		sampleCode: 'name = "Sakura"\nprint(name)',
		output: "Sakura",
		points: [
			"= は代入を表す",
			"値には型がある",
			"int() や str() で型変換できる"
		],
		typeBasics: {
			title: "型とは？",
			description: "Pythonでは、値の種類を「型」と呼びます。文字・数字・True / False などで扱い方が変わります。",
			examples: [
				{
					title: "int",
					description: "int() は文字列を整数に変換します。",
					code: 'age = "20"\n\nprint(int(age) + 5)',
					output: "25"
				},
				{
					title: "str",
					description: "str() は数字を文字列に変換します。",
					code: 'age = 20\n\nprint("年齢は" + str(age) + "歳です")',
					output: "年齢は20歳です"
				},
				{
					title: "len",
					description: "len() は文字数や要素数を取得します。",
					code: 'text = "Python"\n\nprint(len(text))',
					output: "6"
				},
				{
					title: "bool",
					description: "bool() は値を True / False に変換します。",
					code: 'print(bool(1))\nprint(bool(0))',
					output: "True\nFalse"
				},
				{
					title: "float",
					description: "float() は値を小数に変換します。",
					code: 'number = "1.5"\n\nprint(float(number))',
					output: "1.5"
				}
			]
		},
		practice: {
			title: "試してみよう",
			instruction: "変数へ文字や数字を入れて表示してみましょう。int() や str() を使った型変換も試せます。",
			starterCode: 'name = "Taro"\nage = "20"\n\nprint(name)\nprint(int(age) + 5)',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"変数名を変えて、表示される値の変化を確認してみましょう。",
				"文字列はクォーテーションで囲み、数字はそのまま代入できます。"
			]
		}
	},
	chapter3: {
		number: 3,
		title: "条件分岐",
		summary: "条件によって処理を切り替える if 文の基本を整理します。",
		goals: [
			"if文の書き方を理解する",
			"条件が真のときだけ処理が動くことを知る",
			"比較演算子を使って条件を書ける"
		],
		explanation: [
			"条件分岐では、『ある条件を満たしたときだけ実行する』処理を書きます。Pythonではインデントが構造を表すため、字下げも意味を持ちます。"
		],
		sampleCode: 'score = 80\nif score >= 70:\n    print("合格")',
		output: "合格",
		points: [
			"条件式は True / False で評価される",
			"比較演算子で値の大小や一致を比べる",
			"if / else / elif で処理を分ける"
		],
		conditionExamples: [
			{
				title: "if のみ",
				description: "条件を満たしたときだけ処理を実行します。",
				code: 'score = 80\n\nif score >= 70:\n    print("合格")',
				output: "合格"
			},
			{
				title: "if と else",
				description: "条件を満たす場合と、満たさない場合で処理を分けます。",
				code: 'score = 60\n\nif score >= 70:\n    print("合格")\nelse:\n    print("不合格")',
				output: "不合格"
			},
			{
				title: "if と elif と else",
				description: "複数の条件を上から順番に判定します。",
				code: 'score = 85\n\nif score >= 90:\n    print("とても良い")\nelif score >= 70:\n    print("合格")\nelse:\n    print("不合格")',
				output: "合格"
			}
		],
		comparisonOperators: [
			{ symbol: "==", label: "等しい" },
			{ symbol: "!=", label: "等しくない" },
			{ symbol: ">", label: "より大きい" },
			{ symbol: "<", label: "より小さい" },
			{ symbol: ">=", label: "以上" },
			{ symbol: "<=", label: "以下" }
		],
		practice: {
			title: "試してみよう",
			instruction: "scoreの値や比較演算子を変えて、表示される結果がどう変わるか試してみましょう。",
			starterCode: 'score = 80\n\nif score >= 70:\n    print("合格")\nelse:\n    print("不合格")',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"if と else の下の行は、半角スペース4つでインデントしましょう。",
				"score を 69 や 95 に変えて、分岐の結果を比べてみましょう。"
			]
		}
	},
	chapter4: {
		number: 4,
		title: "ループ",
		summary: "同じ処理を繰り返す for 文の基本を学習します。",
		goals: ["for文の役割を理解する", "rangeの基本を知る", "反復処理の流れをつかむ"],
		explanation: ["繰り返し処理は、同じ形の操作を何度も行いたいときに使います。for 文を使うと、回数を決めた処理を簡潔に書けます。", "for 文では、range() が作った数字を 1 つずつ取り出して繰り返します。i は、その数字を順番に受け取る変数です。"],
		rangeBasics: {
			title: "rangeとは？",
			eyebrow: "RANGE BASICS",
			description: "range() は、for 文で繰り返す回数を決めるために使います。range(3) は、0 から 2 までの数字を順番に作ります。",
			code: "for i in range(3):\n    print(i)",
			output: "0\n1\n2",
			note: "i は、繰り返すたびに変わる値です。range(3) の数字が、順番に i に入ります。"
		},
		rangeUsageExamples: [
			{
				title: "基本形",
				code: "for i in range(3):\n    print(i)",
				output: "0\n1\n2",
				description: "0から3未満まで繰り返します。"
			},
			{
				title: "開始値指定",
				code: "for i in range(1, 4):\n    print(i)",
				output: "1\n2\n3",
				description: "開始値と終了値を指定できます。"
			},
			{
				title: "ステップ指定",
				code: "for i in range(0, 10, 2):\n    print(i)",
				output: "0\n2\n4\n6\n8",
				description: "2ずつ増やしながら繰り返します。"
			},
			{
				title: "逆順ループ",
				code: "for i in range(5, 0, -1):\n    print(i)",
				output: "5\n4\n3\n2\n1",
				description: "1ずつ減らしながら繰り返します。"
			}
		],
		breakBasics: {
			title: "breakとは？",
			eyebrow: "LOOP CONTROL",
			description: "break を使うと、繰り返しを途中で止められます。",
			code: 'for i in range(5):\n    if i == 3:\n        break\n\n    print(i)',
			output: "0\n1\n2",
			note: "i が 3 になったタイミングで break が実行され、ループが終了します。"
		},
		sampleCode: "for i in range(3):\n    print(i)",
		output: "0\n1\n2",
		points: ["range(3) は 0, 1, 2 を順に返す", "range(終了値)", "range(開始値, 終了値)", "range(開始値, 終了値, 増加量)", "同じ構造を短く書ける", "インデントでループ本体を表す"],
		practice: {
			title: "試してみよう",
			instruction: "range の数字を変えて、i の値がどう変わるか試してみましょう。",
			starterCode: "for i in range(5):\n    print(i)",
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"range(3) や range(10) に変えて、回数の違いを確認してみましょう。",
				"print(i) を print(i * 2) に変えると、繰り返しの中の処理を変えられます。"
			]
		}
	},
	chapter5: {
		number: 5,
		title: "リスト",
		summary: "複数の値をまとめて扱うリストの基礎を確認します。",
		goals: ["リストを作成できる", "添字で要素を取り出せる", "複数データをまとめる意味を理解する"],
		explanation: ["リストは複数のデータを順番つきでまとめるための型です。同じ種類の情報を扱うときに便利です。"],
		indexBasics: {
			eyebrow: "INDEX BASICS",
			title: "番号について",
			description: "リストは 0 番目から始まります。番号を使って、リストの中の値を取り出します。",
			rows: [
				{ index: "0", value: "apple" },
				{ index: "1", value: "banana" },
				{ index: "2", value: "orange" }
			]
		},
		listExamples: [
			{
				title: "取り出し",
				description: "番号を使って、リストから値を取り出します。",
				code: 'fruits = ["apple", "banana"]\n\nprint(fruits[0])',
				output: "apple"
			},
			{
				title: "追加",
				description: "append() を使うと、リストの最後に値を追加できます。",
				code: 'fruits = ["apple", "banana"]\n\nfruits.append("orange")\n\nprint(fruits)',
				output: "['apple', 'banana', 'orange']"
			},
			{
				title: "変更",
				description: "番号を指定すると、リストの値を変更できます。",
				code: 'fruits = ["apple", "banana"]\n\nfruits[1] = "orange"\n\nprint(fruits)',
				output: "['apple', 'orange']"
			},
			{
				title: "削除",
				description: "remove() を使うと、指定した値を削除できます。",
				code: 'fruits = ["apple", "banana", "orange"]\n\nfruits.remove("banana")\n\nprint(fruits)',
				output: "['apple', 'orange']"
			}
		],
		sampleCode: 'fruits = ["apple", "banana"]\nprint(fruits[0])',
		output: "apple",
		points: ["最初の要素は 0 番目", "[] で要素へアクセスする", "複数の値をひとまとめにできる"],
		practice: {
			title: "試してみよう",
			instruction: "リストの番号や append()、remove() を変えて、表示される結果を確認してみましょう。",
			starterCode: 'fruits = ["apple", "banana", "orange"]\n\nprint(fruits)\nprint(fruits[0])',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"インデックスは 0 から始まります。2番目の要素は fruits[1] です。",
				"存在しない番号を指定するとエラーになるので、長さも確認してみましょう。"
			]
		}
	},
	chapter6: {
		number: 6,
		title: "デバッグ",
		summary: "エラーを読み取り、原因を切り分けるための見方を学びます。",
		goals: ["エラーメッセージを見る習慣を付ける", "値を出力して確認できる", "原因を一つずつ切り分ける"],
		explanation: [
			"デバッグは、動かないコードを直すための作業です。すぐ直そうとするより、何が起きているかを確認する姿勢が重要です。",
			"エラーメッセージには、どこで何が起きたかのヒントがあります。まずはエラー文を読んで原因を探してみましょう。",
			"エラーを怖がらず、原因を切り分けながら一つずつ直していくことが、デバッグの基本です。"
		],
		sampleCode: "numbers = [10, 20, 30]\n\nprint(numbers[5])",
		output: "IndexError: list index out of range",
		points: ["まず再現する", "値を print して確認する", "1か所ずつ直す"],
		practice: {
			title: "試してみよう",
			instruction: "左のサンプルコードを参考に、エラーが出ないように修正してみましょう。",
			starterCode: "numbers = [10, 20, 30]\n\nprint(numbers[5])",
			placeholder: "ここにPythonコードを書いてください",
			prefillStarterCode: true,
			errorDisplayMap: {
				"list index out of range": "IndexError: list index out of range"
			},
			hints: [
				"エラー文の最後にある行番号を見て、どの行で失敗したか確認してみましょう。",
				"numbers[5] を numbers[2] に変えると成功する理由を考えてみましょう。"
			]
		},
		debugReference: [
			{
				title: "SyntaxError",
				description: "コードの書き方が間違っています。() や : や quotes の閉じ忘れが多いです。",
				causes: ["() の閉じ忘れ", ": の付け忘れ", "quotes の閉じ忘れ"],
				example: 'print("hello"'
			},
			{
				title: "NameError",
				description: "存在しない変数を使っています。スペルミスや、変数を作る前に使っていないか確認しましょう。",
				causes: ["変数名のスペルミス", "定義する前に使っている", "大文字小文字が違う"],
				example: "print(message)"
			},
			{
				title: "TypeError",
				description: "文字列と数字など、違う種類の値を混ぜています。int() や str() を確認しましょう。",
				causes: ["文字列と数字をそのまま足している", "関数に違う型を渡している", "input の値を変換していない"],
				example: '"5" + 3'
			},
			{
				title: "IndexError",
				description: "存在しない番号を取り出そうとしています。リストの長さを確認しましょう。",
				causes: ["要素数より大きい番号を指定している", "0番目から始まることを忘れている", "空のリストを参照している"],
				example: "numbers = [1, 2, 3]\nprint(numbers[5])"
			},
			{
				title: "ValueError",
				description: "変換できない値を int() などに渡しています。",
				causes: ["数字以外を int() に渡している", "空文字を変換している", "形式が想定と違う"],
				example: 'int("hello")'
			},
			{
				title: "ZeroDivisionError",
				description: "0で割ることはできません。割る数が0になっていないか確認しましょう。",
				causes: ["計算途中で割る数が0になった", "入力値のチェックがない", "変数の初期値が0のまま"],
				example: "10 / 0"
			},
			{
				title: "IndentationError",
				description: "インデント（字下げ）が正しくありません。Pythonではインデントが重要です。",
				causes: ["if や for の次の行が下がっていない", "スペース数が揃っていない", "タブとスペースが混ざっている"],
				example: 'if True:\nprint("hello")'
			}
		]
	},
	chapter7: {
		number: 7,
		title: "input",
		summary: "ユーザー入力を受け取り、処理へ使う流れを学びます。",
		goals: ["inputの使い方を理解する", "受け取った値を表示できる", "入力値が文字列であることを知る"],
		explanation: ["input を使うと、実行中にユーザーから値を受け取れます。最初は『受け取って表示する』ところから始めると理解しやすいです。"],
		sampleCode: 'name = input("名前を入力: ")\nprint("こんにちは", name)',
		output: "こんにちは Taro",
		points: ["input の戻り値は文字列", "必要に応じて変換する", "入出力の流れを意識する"],
		practice: {
			title: "試してみよう",
			instruction: "inputで受け取った値を表示してみましょう。数値を受け取る場合は int(input())、文字列を受け取る場合は input() を試せます。",
			starterCode: 'name = input("名前を入力: ")\nprint("こんにちは", name)',
			placeholder: "ここにPythonコードを書いてください",
			allowInput: true,
			inputLabel: "[input]",
			inputPlaceholder: "例：\n10\n\nまたは：\nTaro\n\n複数のinputを使う場合は1行ずつ入力\n例：\nTaro\n20"
		}
	},
	chapter8: {
		number: 8,
		title: "関数",
		summary: "処理をまとめて再利用する関数の基本を押さえます。",
		goals: ["関数を定義できる", "引数の役割を理解する", "return の意味を知る"],
		explanation: [
			"関数は、何度も使う処理をひとまとまりにする仕組みです。名前を付けて呼び出すことで、コードが整理しやすくなります。",
			"同じコードを何度も書く代わりに、関数へまとめると短く分かりやすくできます。引数を変えるだけで同じ処理を再利用できるのが大きな利点です。",
			"return は、関数の結果を外へ返すために使います。print(greet(\"Taro\")) は、関数が返した値を print で表示している形です。"
		],
		sampleCode: 'def greet(name):\n    return "こんにちは " + name\n\nprint(greet("Taro"))\nprint(greet("Hanako"))\nprint(greet("Aoi"))',
		output: "こんにちは Taro\nこんにちは Hanako\nこんにちは Aoi",
		points: ["def で関数を作る", "引数を変えて同じ処理を再利用する", "return で返した値を外側の print で表示できる"],
		functionComparison: {
			title: "関数なしと関数ありの比較",
			withoutLabel: "関数なし",
			withoutCode: 'print("こんにちは", "Taro")\nprint("こんにちは", "Hanako")\nprint("こんにちは", "Aoi")',
			withLabel: "関数あり",
			withCode: 'def greet(name):\n    return "こんにちは " + name\n\nprint(greet("Taro"))\nprint(greet("Hanako"))\nprint(greet("Aoi"))'
		},
		practice: {
			title: "試してみよう",
			instruction: "print(greet(\"Sakura\")) のように引数を変えて、return した値を表示してみましょう。",
			starterCode: 'def greet(name):\n    return "こんにちは " + name\n\nprint(greet("Taro"))\nprint(greet("Hanako"))',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"def の次の行はインデントが必要です。",
				"return で返した値を、外側の print で表示している流れを確認してみましょう。"
			]
		}
	},
	chapter9: {
		number: 9,
		title: "文字列",
		summary: "文字列の変換や検索など、実用的な操作を整理します。",
		goals: ["文字列メソッドを使える", "大小文字変換を理解する", "文字列操作の用途を知る"],
		explanation: ["文字列には便利なメソッドが多くあり、整形や検索に役立ちます。入力データを扱うときにも頻繁に使います。"],
		sampleCode: 'text = "python study"\nprint(text.upper())',
		output: "PYTHON STUDY",
		stringExamples: [
			{
				title: "upper()",
				description: ".upper() は文字列を大文字へ変換します。",
				code: 'text = "python study"\n\nprint(text.upper())',
				output: "PYTHON STUDY"
			},
			{
				title: "lower()",
				description: ".lower() は文字列を小文字へ変換します。",
				code: 'text = "PYTHON STUDY"\n\nprint(text.lower())',
				output: "python study"
			},
			{
				title: "replace()",
				description: ".replace() は文字列の一部を別の文字へ置き換えます。",
				code: 'text = "I like JAVA"\n\nprint(text.replace("JAVA", "Python"))',
				output: "I like Python"
			},
			{
				title: "split()",
				description: ".split() は文字列を区切ってリストへ変換します。",
				code: 'text = "apple,banana,orange"\n\nprint(text.split(","))',
				output: "['apple', 'banana', 'orange']"
			},
			{
				title: "strip()",
				description: ".strip() は文字列の前後の空白を削除します。",
				code: 'text = "  hello  "\n\nprint(text.strip())',
				output: "hello"
			},
			{
				title: "len()",
				description: "len() は文字列の長さを数えます。",
				code: 'text = "Python"\n\nprint(len(text))',
				output: "6"
			},
			{
				title: "文字列連結",
				description: "+ を使うと文字列同士をつなげられます。",
				code: 'first = "Python"\nsecond = "Study"\n\nprint(first + " " + second)',
				output: "Python Study"
			}
		],
		points: ["文字列はメソッドで加工できる", "元の値が変わるかは都度確認する", "表示前の整形に便利"],
		practice: {
			title: "試してみよう",
			instruction: "文字列の中身を変えて、upper、replace、lenの結果を確認してみましょう。",
			starterCode: 'text = "python study"\n\nprint(text.upper())\nprint(text.replace("python", "Python"))\nprint(len(text))',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"replace の1つ目が置換前、2つ目が置換後です。",
				"len は文字数を返します。スペースも1文字として数えられます。"
			]
		}
	},
	chapter10: {
		number: 10,
		title: "辞書",
		summary: "キーと値の組み合わせでデータを管理する辞書を学びます。",
		goals: ["辞書を作成できる", "キーから値を取り出せる", "リストとの違いを理解する"],
		explanation: ["辞書は『名前で値を取り出す』データ構造です。属性がはっきりした情報を持つときに便利です。"],
		sampleCode: 'user = {"name": "Aoi", "score": 95}\nprint(user["score"])',
		output: "95",
		dictionaryExamples: [
			{
				title: "値を取り出す",
				description: "[\"key\"] を使うと、辞書から値を取り出せます。",
				code: 'user = {"name": "Aoi", "score": 95}\n\nprint(user["name"])\nprint(user["score"])',
				output: "Aoi\n95"
			},
			{
				title: "値を追加する",
				description: "新しい key を追加すると、辞書へ新しいデータを保存できます。",
				code: 'user = {"name": "Aoi", "score": 95}\n\nuser["level"] = "Beginner"\n\nprint(user)',
				output: "{'name': 'Aoi', 'score': 95, 'level': 'Beginner'}"
			},
			{
				title: "値を変更する",
				description: "すでに存在する key に代入すると、値を変更できます。",
				code: 'user = {"name": "Aoi", "score": 95}\n\nuser["score"] = 100\n\nprint(user)',
				output: "{'name': 'Aoi', 'score': 100}"
			}
		],
		points: ["キーで値を参照する", "順番より対応関係を重視する", "データの意味を表しやすい"],
		practice: {
			title: "試してみよう",
			instruction: "辞書のキーや値を変えて、データの取り出し方を試してみましょう。",
			starterCode: 'user = {\n    "name": "Aoi",\n    "score": 95\n}\n\nprint(user["name"])\nprint(user["score"])',
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"キー名を変えるときは、取り出す側のキーも同じ名前に揃えましょう。",
				"存在しないキーを参照するとエラーになるので注意しましょう。"
			]
		}
	},
	chapter11: {
		number: 11,
		title: "while",
		summary: "条件に応じて繰り返す while 文の基本を学びます。",
		goals: ["while文の書き方を理解する", "終了条件を考えられる", "無限ループを避ける意識を持つ"],
		explanation: [
			"while は『条件が真の間だけ繰り返す』処理です。いつ終わるかを必ず意識して書く必要があります。",
			"for は『回数が決まっている繰り返し』に向いています。while は『条件を満たしている間だけ繰り返す』ときに向いています。"
		],
		sampleCode: "count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
		output: "1\n2\n3",
		points: ["for は回数ベース、while は条件ベース", "while は条件が変わるよう更新処理を入れる", "無限ループを避けるため終了条件を確認する"],
		loopComparisonExamples: [
			{
				title: "for と while の比較",
				description: "for は『回数が決まっている繰り返し』に向いています。while は『条件を満たしている間だけ繰り返す』ときに使います。",
				codeBlocks: [
					{
						label: "for",
						code: "for i in range(3):\n    print(i)",
						output: "0\n1\n2"
					},
					{
						label: "while",
						code: "count = 0\n\nwhile count < 3:\n    print(count)\n    count += 1",
						output: "0\n1\n2"
					}
				]
			},
			{
				title: "count += 1 の大切さ",
				description: "count += 1 があるかないかで、while が終了するかどうかが変わります。更新処理の有無を左右で比較して確認しましょう。",
				codeBlocks: [
					{
						label: "count += 1 がない",
						code: "count = 1\n\nwhile count <= 3:\n    print(count)",
						description: "count の値が変わらないため、条件がずっと True のままになります。",
						output: "1\n1\n1\n...",
						note: "このコードは無限ループになります。"
					},
					{
						label: "count += 1 がある",
						code: "count = 1\n\nwhile count <= 3:\n    print(count)\n    count += 1",
						description: "count += 1 によって count が増えます。条件が False になるため while が終了します。",
						output: "1\n2\n3"
					}
				]
			},
			{
				title: "while と break",
				description: "while でも break を使うと、条件の途中でループを終了できます。",
				codeBlocks: [
					{
						label: "while + break",
						code: "count = 0\n\nwhile True:\n    print(count)\n\n    if count == 2:\n        break\n\n    count += 1",
						output: "0\n1\n2",
						description: "count が 2 になったタイミングで break が実行され、while が終了します。"
					}
				]
			}
		],
		practice: {
			title: "試してみよう",
			instruction: "終了条件やcountの増え方を変えて、繰り返しの動きを確認してみましょう。",
			starterCode: "count = 1\n\nwhile count <= 5:\n    print(count)\n    count += 1",
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"count += 1 を消すと無限ループに近い状態になり、タイムアウトすることを確認できます。",
				"count <= 3 や count += 2 に変えて、ループ回数の違いを見てみましょう。"
			]
		}
	},
	chapter12: {
		number: 12,
		title: "import",
		summary: "標準ライブラリやモジュールを読み込む基本を理解します。",
		goals: ["import の意味を理解する", "標準ライブラリを使える", "機能を分けて使う発想を知る"],
		explanation: ["import を使うと、Pythonに用意された機能や別ファイルの機能を利用できます。自分で全部書かずに済むのが利点です。"],
		sampleCode: "import math\nprint(math.sqrt(16))",
		output: "4.0",
		points: ["必要な機能を読み込む", "モジュール名.関数名 で使う", "再利用の考え方につながる"],
		importExamples: [
			{
				title: "math",
				description: "math は、平方根や円周率などの数学機能を使うためのモジュールです。",
				code: "import math\n\nprint(math.sqrt(16))\nprint(math.pi)",
				output: "4.0\n3.141592653589793",
				featureBlocks: [
					{
						name: "sqrt()",
						description: "sqrt() は平方根を求める関数です。",
						code: "import math\n\nprint(math.sqrt(16))",
						output: "4.0"
					},
					{
						name: "pi",
						description: "pi は円周率を表します。",
						code: "import math\n\nprint(math.pi)",
						output: "3.141592653589793"
					},
					{
						name: "ceil()",
						description: "ceil() は小数を切り上げます。",
						code: "import math\n\nprint(math.ceil(3.2))",
						output: "4"
					},
					{
						name: "floor()",
						description: "floor() は小数を切り下げます。",
						code: "import math\n\nprint(math.floor(3.8))",
						output: "3"
					}
				]
			},
			{
				title: "random",
				description: "random は、ランダムな数を作るためのモジュールです。サイコロやガチャのような処理に使えます。",
				code: "import random\n\nprint(random.randint(1, 6))",
				output: "例：4",
				featureBlocks: [
					{
						name: "randint()",
						description: "randint() は指定した範囲のランダムな整数を作ります。",
						code: "import random\n\nprint(random.randint(1, 6))",
						output: "例：4"
					},
					{
						name: "shuffle()",
						description: "shuffle() はリストの順番をランダムに並び替えます。",
						code: "import random\n\ncards = [1, 2, 3, 4, 5]\n\nrandom.shuffle(cards)\n\nprint(cards)",
						output: "例：[3, 1, 5, 2, 4]"
					}
				]
			},
			{
				title: "time",
				description: "time は、処理を少し待たせるときなどに使うモジュールです。なお、この実行環境のPracticeでは time モジュールが制限されるため、この例は教科書での紹介用です。",
				code: "import time\n\nprint(\"スタート\")\ntime.sleep(1)\nprint(\"1秒後\")",
				output: "スタート\n1秒後",
				featureBlocks: [
					{
						name: "sleep()",
						description: "sleep() は処理を一定時間止めます。1秒待ってから次の処理が実行されます。",
						code: "import time\n\nprint(\"スタート\")\n\ntime.sleep(1)\n\nprint(\"1秒後\")",
						output: "スタート\n1秒後"
					},
					{
						name: "time()",
						description: "time() は現在時刻を秒で取得します。",
						code: "import time\n\nprint(time.time())",
						output: "例：1749033000.12345"
					}
				]
			},
			{
				title: "datetime",
				description: "datetime は、日付や時刻を扱うためのモジュールです。",
				code: "import datetime\n\nprint(datetime.date.today())",
				output: "例：2026-06-04",
				featureBlocks: [
					{
						name: "date.today()",
						description: "date.today() は今日の日付を取得します。",
						code: "import datetime\n\nprint(datetime.date.today())",
						output: "例：2026-06-04"
					},
					{
						name: "datetime.datetime.now()",
						description: "datetime.datetime.now() は現在の日時を取得します。",
						code: "import datetime\n\nprint(datetime.datetime.now())",
						output: "例：2026-06-04 19:30:45"
					}
				]
			}
		],
		practice: {
			title: "試してみよう",
			instruction: "math・random・datetime などを使って、標準ライブラリの機能を試してみましょう（time はこのPractice環境では制限があります）。",
			starterCode: "import math\n\nprint(math.sqrt(16))\nprint(math.pi)",
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"この実行環境では import できるモジュールが制限されています。",
				"危険なモジュールは許可されていないため、許可済みの範囲で試しましょう。"
			]
		}
	},
	chapter13: {
		number: 13,
		title: "例外処理",
		summary: "エラーが起きても安全に処理を続ける例外処理の入口です。",
		goals: ["try / except の役割を理解する", "エラー時の分岐を書ける", "安全にプログラムを止めない考え方を知る"],
		explanation: [
			"例外処理は、エラーが発生しそうな箇所を安全に扱うための仕組みです。失敗を前提にした設計を学ぶ入口になります。",
			"try / except を使うと、エラーが起きてもプログラムを完全停止させずに処理を続けられます。",
			"エラーが発生した場合は except の処理が実行され、その後のコードも続行されます。",
			"finally は、エラーが起きても起きなくても最後に必ず実行される処理です。"
		],
		sampleCode: "try:\n    value = 10 / 0\nexcept ZeroDivisionError:\n    print(\"エラー\")",
		output: "エラー",
		points: ["危険な処理を try に入れる", "except でエラー時の対応を書く", "finally は最後に必ず実行される"],
		exceptionExamples: [
			{
				title: "try / except",
				description: "エラーが起きたとき、except の処理が実行されます。",
				code: "try:\n    value = 10 / 0\nexcept ZeroDivisionError:\n    print(\"エラー\")",
				output: "エラー"
			},
			{
				title: "finally",
				description: "finally は、エラーが起きても起きなくても最後に必ず実行される処理です。",
				code: "try:\n    value = 10 / 0\nexcept ZeroDivisionError:\n    print(\"エラー\")\nfinally:\n    print(\"終了処理\")",
				output: "エラー\n終了処理"
			}
		],
		practice: {
			title: "試してみよう",
			instruction: "エラーが起きる処理をtry/exceptで安全に扱う流れを確認してみましょう。",
			starterCode: "try:\n    value = 10 / 0\n    print(value)\nexcept ZeroDivisionError:\n    print(\"0で割ることはできません\")",
			placeholder: "ここにPythonコードを書いてください",
			hints: [
				"try の中でエラーが起きると、対応する except が実行されます。",
				"except の種類を ValueError に変えて、動きの違いも確認してみましょう。"
			]
		}
	}
};

const CHAPTER_ROUTES = {
	textbook: "../textbook.html",
	study: "../../pages/study.html",
	settings: "../../pages/settings.html",
	home: "../../pages/index.html",
	dashboard: "../../pages/dashboard.html"
};

function getChapterIdsInOrder() {
	return Object.keys(CHAPTER_PAGE_DATA).sort((left, right) => CHAPTER_PAGE_DATA[left].number - CHAPTER_PAGE_DATA[right].number);
}

function getAdjacentChapterId(chapterId, offset) {
	const chapterIds = getChapterIdsInOrder();
	const currentIndex = chapterIds.indexOf(chapterId);

	if (currentIndex === -1) {
		return null;
	}

	return chapterIds[currentIndex + offset] || null;
}

function createListItems(items) {
	return items.map((item) => `<li>${item}</li>`).join("");
}

function createParagraphs(items) {
	return items.map((item) => `<p>${item}</p>`).join("");
}

function createDebugReferenceCards(items) {
	return items
		.map((item) => {
			const causes = (item.causes || []).map((cause) => `<li>${escapeHtml(cause)}</li>`).join("");

			return `
				<article class="debug-card glass-outline">
					<div class="debug-card-header">
						<p class="debug-card-title">${escapeHtml(item.title)}</p>
					</div>
					<p class="debug-card-description">${escapeHtml(item.description)}</p>
					<div class="debug-card-group">
						<p class="debug-card-label">よくある原因</p>
						<ul class="debug-card-list">${causes}</ul>
					</div>
					<div class="debug-card-group">
						<p class="debug-card-label">例</p>
						<pre class="debug-card-example"><code>${escapeHtml(item.example)}</code></pre>
					</div>
				</article>
			`;
		})
		.join("");
}

function createCalcOperatorCards(items) {
	return items
		.map((item) => `
			<div class="calc-operator-row" role="listitem">
				<div class="calc-operator-header">
					<code class="calc-operator-badge">${escapeHtml(item.symbol)}</code>
					<span class="calc-operator-meaning">${escapeHtml(item.meaning)}</span>
				</div>
				<div class="calc-operator-example">
					<p class="calc-operator-label">コード例</p>
					<pre class="code-block calc-operator-code-block"><code>${escapeHtml(item.code || "")}</code></pre>
				</div>
				<div class="calc-operator-example">
					<p class="calc-operator-label">実行結果</p>
					<pre class="output-block calc-operator-output-block"><code>${escapeHtml(item.output || "")}</code></pre>
				</div>
			</div>
		`)
		.join("");
}

const DEBUG_CARDS_PER_PAGE = 3;
const CALC_OPERATOR_CARDS_PER_PAGE = 2;

function chunkArray(items, chunkSize) {
	if (!Array.isArray(items) || chunkSize <= 0) {
		return [];
	}

	const chunks = [];
	for (let index = 0; index < items.length; index += chunkSize) {
		chunks.push(items.slice(index, index + chunkSize));
	}

	return chunks;
}

function bindDebugReferenceCarousel(root, items) {
	const carousel = root.querySelector("[data-debug-carousel]");
	if (!carousel || !Array.isArray(items) || !items.length) {
		return;
	}

	const bodyNode = carousel.querySelector("[data-debug-body]");
	const pageNode = carousel.querySelector("[data-debug-page]");
	const prevButton = carousel.querySelector("[data-debug-prev]");
	const nextButton = carousel.querySelector("[data-debug-next]");
	const dotsNode = carousel.querySelector("[data-debug-dots]");

	if (!bodyNode || !pageNode || !prevButton || !nextButton || !dotsNode) {
		return;
	}

	let currentPage = 0;
	let pages = [];
	let cardsPerPage = DEBUG_CARDS_PER_PAGE;

	const getCardsPerPage = () => {
		if (window.matchMedia && window.matchMedia("(max-width: 768px)").matches) {
			return 1;
		}

		return DEBUG_CARDS_PER_PAGE;
	};

	const renderDots = () => {
		dotsNode.innerHTML = pages
			.map((_, index) => `
				<button
					type="button"
					class="debug-reference-dot ${index === currentPage ? "is-active" : ""}"
					data-debug-dot="${index}"
					aria-label="${index + 1}ページ目へ"
				></button>
			`)
			.join("");

		Array.from(dotsNode.querySelectorAll("[data-debug-dot]")).forEach((dotButton) => {
			dotButton.addEventListener("click", () => {
				const nextPage = Number(dotButton.dataset.debugDot);
				if (Number.isNaN(nextPage)) {
					return;
				}

				goToPage(nextPage);
			});
		});
	};

	const syncView = () => {
		const safePage = pages[currentPage] || [];
		pageNode.innerHTML = createDebugReferenceCards(safePage);
		renderDots();

		const hasMultiplePages = pages.length > 1;
		prevButton.hidden = !hasMultiplePages;
		nextButton.hidden = !hasMultiplePages;
		dotsNode.hidden = !hasMultiplePages;
	};

	const goToPage = (nextPage) => {
		const totalPages = pages.length;
		if (!totalPages) {
			return;
		}

		currentPage = (nextPage + totalPages) % totalPages;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	const refreshPages = () => {
		const nextCardsPerPage = getCardsPerPage();
		if (!pages.length) {
			cardsPerPage = nextCardsPerPage;
			pages = chunkArray(items, cardsPerPage);
			currentPage = 0;
			syncView();
			return;
		}

		const firstVisibleIndex = currentPage * cardsPerPage;
		cardsPerPage = nextCardsPerPage;
		pages = chunkArray(items, cardsPerPage);
		currentPage = Math.floor(firstVisibleIndex / cardsPerPage);
		if (currentPage >= pages.length) {
			currentPage = Math.max(pages.length - 1, 0);
		}
		syncView();
	};

	prevButton.addEventListener("click", () => goToPage(currentPage - 1));
	nextButton.addEventListener("click", () => goToPage(currentPage + 1));
	window.addEventListener("resize", refreshPages);

	refreshPages();
}

function bindCalcOperatorsCarousel(root, items) {
	const carousel = root.querySelector("[data-calc-carousel]");
	if (!carousel || !Array.isArray(items) || !items.length) {
		return;
	}

	const bodyNode = carousel.querySelector("[data-calc-body]");
	const pageNode = carousel.querySelector("[data-calc-page]");
	const prevButton = carousel.querySelector("[data-calc-prev]");
	const nextButton = carousel.querySelector("[data-calc-next]");
	const dotsNode = carousel.querySelector("[data-calc-dots]");

	if (!bodyNode || !pageNode || !prevButton || !nextButton || !dotsNode) {
		return;
	}

	let currentPage = 0;
	let pages = [];
	let cardsPerPage = CALC_OPERATOR_CARDS_PER_PAGE;

	const getCardsPerPage = () => {
		if (window.matchMedia && window.matchMedia("(max-width: 768px)").matches) {
			return 1;
		}

		return CALC_OPERATOR_CARDS_PER_PAGE;
	};

	const renderDots = () => {
		dotsNode.innerHTML = pages
			.map((_, index) => `
				<button
					type="button"
					class="calc-operators-dot ${index === currentPage ? "is-active" : ""}"
					data-calc-dot="${index}"
					aria-label="${index + 1}ページ目へ"
				></button>
			`)
			.join("");

		Array.from(dotsNode.querySelectorAll("[data-calc-dot]")).forEach((dotButton) => {
			dotButton.addEventListener("click", () => {
				const nextPage = Number(dotButton.dataset.calcDot);
				if (Number.isNaN(nextPage)) {
					return;
				}

				goToPage(nextPage);
			});
		});
	};

	const syncView = () => {
		const safePage = pages[currentPage] || [];
		pageNode.innerHTML = createCalcOperatorCards(safePage);
		renderDots();

		const hasMultiplePages = pages.length > 1;
		prevButton.hidden = !hasMultiplePages;
		nextButton.hidden = !hasMultiplePages;
		dotsNode.hidden = !hasMultiplePages;
	};

	const goToPage = (nextPage) => {
		const totalPages = pages.length;
		if (!totalPages) {
			return;
		}

		currentPage = (nextPage + totalPages) % totalPages;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	const refreshPages = () => {
		const nextCardsPerPage = getCardsPerPage();
		if (!pages.length) {
			cardsPerPage = nextCardsPerPage;
			pages = chunkArray(items, cardsPerPage);
			currentPage = 0;
			syncView();
			return;
		}

		const firstVisibleIndex = currentPage * cardsPerPage;
		cardsPerPage = nextCardsPerPage;
		pages = chunkArray(items, cardsPerPage);
		currentPage = Math.floor(firstVisibleIndex / cardsPerPage);
		if (currentPage >= pages.length) {
			currentPage = Math.max(pages.length - 1, 0);
		}
		syncView();
	};

	prevButton.addEventListener("click", () => goToPage(currentPage - 1));
	nextButton.addEventListener("click", () => goToPage(currentPage + 1));
	window.addEventListener("resize", refreshPages);

	refreshPages();
}

function bindStringExampleCarousel(root, examples) {
	const carousel = root.querySelector("[data-string-carousel]");
	if (!carousel || !Array.isArray(examples) || !examples.length) {
		return;
	}

	const titleNode = carousel.querySelector("[data-string-title]");
	const codeNode = carousel.querySelector("[data-string-code]");
	const outputNode = carousel.querySelector("[data-string-output]");
	const descriptionNode = carousel.querySelector("[data-string-description]");
	const featureSectionNode = carousel.querySelector("[data-string-feature-section]");
	const featureListNode = carousel.querySelector("[data-string-feature-list]");
	const bodyNode = carousel.querySelector("[data-string-body]");
	const prevButton = carousel.querySelector("[data-string-prev]");
	const nextButton = carousel.querySelector("[data-string-next]");
	const tabButtons = Array.from(carousel.querySelectorAll("[data-string-tab]"));

	if (!titleNode || !descriptionNode || !bodyNode || !prevButton || !nextButton || !featureSectionNode || !featureListNode) {
		return;
	}

	let currentIndex = 0;

	const syncView = () => {
		const currentExample = examples[currentIndex];
		titleNode.textContent = currentExample.title || "文字列操作";
		if (codeNode) {
			codeNode.textContent = currentExample.code || "";
		}

		if (outputNode) {
			outputNode.textContent = currentExample.output || "";
		}

		descriptionNode.textContent = currentExample.description || "";

		const featureBlocks = Array.isArray(currentExample.featureBlocks) ? currentExample.featureBlocks : [];
		featureSectionNode.hidden = !featureBlocks.length;
		featureListNode.innerHTML = featureBlocks
			.map((feature) => {
				return `
					<article class="string-feature-card">
						<p class="string-feature-name">${escapeHtml(feature.name || "機能")}</p>
						<p class="string-feature-description">${escapeHtml(feature.description || "")}</p>
						<p class="string-feature-label">コード例</p>
						<pre class="function-comparison-code"><code>${escapeHtml(feature.code || "")}</code></pre>
						<p class="string-feature-label">実行結果</p>
						<pre class="output-block"><code>${escapeHtml(feature.output || "")}</code></pre>
					</article>
				`;
			})
			.join("");

		tabButtons.forEach((button, index) => {
			button.classList.toggle("is-active", index === currentIndex);
		});
	};

	const goToIndex = (nextIndex) => {
		const total = examples.length;
		currentIndex = (nextIndex + total) % total;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	prevButton.addEventListener("click", () => goToIndex(currentIndex - 1));
	nextButton.addEventListener("click", () => goToIndex(currentIndex + 1));

	tabButtons.forEach((button) => {
		button.addEventListener("click", () => {
			const targetIndex = Number(button.dataset.stringTab);
			if (Number.isNaN(targetIndex)) {
				return;
			}

			goToIndex(targetIndex);
		});
	});

	syncView();
}

function bindTypeBasicsCarousel(root, examples) {
	const carousel = root.querySelector("[data-type-carousel]");
	if (!carousel || !Array.isArray(examples) || !examples.length) {
		return;
	}

	const titleNode = carousel.querySelector("[data-type-title]");
	const codeNode = carousel.querySelector("[data-type-code]");
	const outputNode = carousel.querySelector("[data-type-output]");
	const descriptionNode = carousel.querySelector("[data-type-description]");
	const bodyNode = carousel.querySelector("[data-type-body]");
	const prevButton = carousel.querySelector("[data-type-prev]");
	const nextButton = carousel.querySelector("[data-type-next]");
	const tabButtons = Array.from(carousel.querySelectorAll("[data-type-tab]"));

	if (!titleNode || !codeNode || !outputNode || !descriptionNode || !bodyNode || !prevButton || !nextButton) {
		return;
	}

	let currentIndex = 0;

	const syncView = () => {
		const currentExample = examples[currentIndex];
		titleNode.textContent = currentExample.title || "type";
		codeNode.textContent = currentExample.code || "";
		outputNode.textContent = currentExample.output || "";
		descriptionNode.textContent = currentExample.description || "";

		tabButtons.forEach((button, index) => {
			button.classList.toggle("is-active", index === currentIndex);
		});
	};

	const goToIndex = (nextIndex) => {
		const total = examples.length;
		currentIndex = (nextIndex + total) % total;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	prevButton.addEventListener("click", () => goToIndex(currentIndex - 1));
	nextButton.addEventListener("click", () => goToIndex(currentIndex + 1));

	tabButtons.forEach((button) => {
		button.addEventListener("click", () => {
			const targetIndex = Number(button.dataset.typeTab);
			if (Number.isNaN(targetIndex)) {
				return;
			}

			goToIndex(targetIndex);
		});
	});

	syncView();
}

function bindRangeUsageCarousel(root, examples) {
	const carousel = root.querySelector("[data-range-carousel]");
	if (!carousel || !Array.isArray(examples) || !examples.length) {
		return;
	}

	const titleNode = carousel.querySelector("[data-range-title]");
	const codeNode = carousel.querySelector("[data-range-code]");
	const outputNode = carousel.querySelector("[data-range-output]");
	const descriptionNode = carousel.querySelector("[data-range-description]");
	const bodyNode = carousel.querySelector("[data-range-body]");
	const prevButton = carousel.querySelector("[data-range-prev]");
	const nextButton = carousel.querySelector("[data-range-next]");
	const tabButtons = Array.from(carousel.querySelectorAll("[data-range-tab]"));

	if (!titleNode || !codeNode || !outputNode || !descriptionNode || !bodyNode || !prevButton || !nextButton) {
		return;
	}

	let currentIndex = 0;

	const syncView = () => {
		const currentExample = examples[currentIndex];
		titleNode.textContent = currentExample.title || "range";
		codeNode.textContent = currentExample.code || "";
		outputNode.textContent = currentExample.output || "";
		descriptionNode.textContent = currentExample.description || "";

		tabButtons.forEach((button, index) => {
			button.classList.toggle("is-active", index === currentIndex);
		});
	};

	const goToIndex = (nextIndex) => {
		const total = examples.length;
		currentIndex = (nextIndex + total) % total;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	prevButton.addEventListener("click", () => goToIndex(currentIndex - 1));
	nextButton.addEventListener("click", () => goToIndex(currentIndex + 1));

	tabButtons.forEach((button) => {
		button.addEventListener("click", () => {
			const targetIndex = Number(button.dataset.rangeTab);
			if (Number.isNaN(targetIndex)) {
				return;
			}

			goToIndex(targetIndex);
		});
	});

	syncView();
}

function bindLoopComparisonCarousel(root, examples) {
	const carousel = root.querySelector("[data-loop-carousel]");
	if (!carousel || !Array.isArray(examples) || !examples.length) {
		return;
	}

	const titleNode = carousel.querySelector("[data-loop-title]");
	const descriptionNode = carousel.querySelector("[data-loop-description]");
	const bodyNode = carousel.querySelector("[data-loop-body]");
	const splitNode = carousel.querySelector("[data-loop-split]");
	const singleNode = carousel.querySelector("[data-loop-single]");
	const singleCodeNode = carousel.querySelector("[data-loop-code]");
	const singleOutputWrapNode = carousel.querySelector("[data-loop-output-wrap]");
	const singleOutputNode = carousel.querySelector("[data-loop-output]");
	const noteNode = carousel.querySelector("[data-loop-note]");
	const prevButton = carousel.querySelector("[data-loop-prev]");
	const nextButton = carousel.querySelector("[data-loop-next]");
	const tabButtons = Array.from(carousel.querySelectorAll("[data-loop-tab]"));

	if (
		!titleNode ||
		!descriptionNode ||
		!bodyNode ||
		!splitNode ||
		!noteNode ||
		!prevButton ||
		!nextButton
	) {
		return;
	}

	let currentIndex = 0;

	const renderSplitBlocks = (codeBlocks) => {
		splitNode.innerHTML = codeBlocks
			.map((block) => {
				const blockDescription = block.description
					? `<p class="loop-comparison-block-description">${escapeHtml(block.description)}</p>`
					: "";
				const blockOutput = block.output
					? `
						<p class="loop-comparison-label">出力</p>
						<pre class="output-block"><code>${escapeHtml(block.output)}</code></pre>
					`
					: "";
				const blockNote = block.note
					? `<p class="loop-comparison-block-note">${escapeHtml(block.note)}</p>`
					: "";

				return `
					<section class="loop-comparison-block">
						<p class="loop-comparison-label">${escapeHtml(block.label || "サンプル")}</p>
						<pre class="function-comparison-code"><code>${escapeHtml(block.code || "")}</code></pre>
						${blockDescription}
						${blockOutput}
						${blockNote}
					</section>
				`;
			})
			.join("");
	};

	const syncView = () => {
		const currentExample = examples[currentIndex];
		titleNode.textContent = currentExample.title || "Loop Comparison";
		descriptionNode.textContent = currentExample.description || "";

		if (Array.isArray(currentExample.codeBlocks) && currentExample.codeBlocks.length) {
			splitNode.hidden = false;
			if (singleNode) {
				singleNode.hidden = true;
			}
			renderSplitBlocks(currentExample.codeBlocks);
		} else if (singleNode && singleCodeNode && singleOutputWrapNode && singleOutputNode) {
			splitNode.hidden = true;
			singleNode.hidden = false;
			singleCodeNode.textContent = currentExample.code || "";
			singleOutputNode.textContent = currentExample.output || "";
			singleOutputWrapNode.hidden = !currentExample.output;
		} else {
			splitNode.hidden = false;
			renderSplitBlocks([
				{
					label: currentExample.title || "サンプル",
					code: currentExample.code || "",
					description: currentExample.description || "",
					output: currentExample.output || "",
					note: currentExample.note || ""
				}
			]);
		}

		noteNode.hidden = !currentExample.note;
		noteNode.textContent = currentExample.note || "";

		tabButtons.forEach((button, index) => {
			button.classList.toggle("is-active", index === currentIndex);
		});
	};

	const goToIndex = (nextIndex) => {
		const total = examples.length;
		currentIndex = (nextIndex + total) % total;
		bodyNode.classList.add("is-switching");
		window.setTimeout(() => {
			syncView();
			bodyNode.classList.remove("is-switching");
		}, 120);
	};

	prevButton.addEventListener("click", () => goToIndex(currentIndex - 1));
	nextButton.addEventListener("click", () => goToIndex(currentIndex + 1));

	tabButtons.forEach((button) => {
		button.addEventListener("click", () => {
			const targetIndex = Number(button.dataset.loopTab);
			if (Number.isNaN(targetIndex)) {
				return;
			}

			goToIndex(targetIndex);
		});
	});

	syncView();
}

function escapeHtml(text) {
	return String(text)
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/\"/g, "&quot;")
		.replace(/'/g, "&#39;");
}

function codeUsesInput(sourceCode) {
	return /\binput\s*\(/.test(sourceCode || "");
}

function normalizePractice(practice) {
	if (typeof practice === "string") {
		return {
			title: "試してみよう",
			instruction: practice,
			starterCode: "",
			placeholder: "ここにPythonコードを書いてください",
			prefillStarterCode: false,
			allowInput: false,
			inputLabel: "[input]",
			inputPlaceholder: "例：Taro",
			errorDisplayMap: {}
		};
	}

	return {
		title: practice?.title || "試してみよう",
		instruction: practice?.instruction || "課題は準備中です。",
		starterCode: practice?.starterCode || "",
		placeholder: practice?.placeholder || "ここにPythonコードを書いてください",
		prefillStarterCode: Boolean(practice?.prefillStarterCode),
		allowInput: Boolean(practice?.allowInput),
		inputLabel: practice?.inputLabel || "[input]",
		inputPlaceholder: practice?.inputPlaceholder || "例：Taro",
		errorDisplayMap: practice?.errorDisplayMap && typeof practice.errorDisplayMap === "object" ? practice.errorDisplayMap : {}
	};
}

const PYTHON_ERROR_NAMES = [
	"SyntaxError",
	"NameError",
	"TypeError",
	"ValueError",
	"ZeroDivisionError",
	"IndentationError",
	"IndexError"
];

function startsWithPythonErrorName(message) {
	return PYTHON_ERROR_NAMES.some((name) => message.startsWith(`${name}:`));
}

function normalizeIndentationMessageBody(message) {
	const lower = message.toLowerCase();

	if (lower.includes("expected an indented block")) {
		return "expected an indented block";
	}

	if (lower.includes("unexpected indent")) {
		return "unexpected indent";
	}

	if (lower.includes("unindent does not match any outer indentation level")) {
		return "unindent does not match any outer indentation level";
	}

	return null;
}

function inferPythonErrorName(message) {
	const lower = message.toLowerCase();

	if (normalizeIndentationMessageBody(message)) {
		return "IndentationError";
	}

	if (
		message.includes("構文エラー")
		|| message.includes("was never closed")
		|| lower.includes("invalid syntax")
	) {
		return "SyntaxError";
	}

	if (lower.includes("is not defined")) {
		return "NameError";
	}

	if (
		lower.includes("unsupported operand type")
		|| lower.includes("can only concatenate")
		|| lower.includes("is not subscriptable")
		|| lower.includes("has no len")
	) {
		return "TypeError";
	}

	if (lower.includes("invalid literal") || lower.includes("could not convert string to float")) {
		return "ValueError";
	}

	if (lower.includes("division by zero")) {
		return "ZeroDivisionError";
	}

	if (lower.includes("index out of range")) {
		return "IndexError";
	}

	return null;
}

function normalizePracticeErrorDisplay(text) {
	const message = (text || "").trim();
	if (!message) {
		return "実行時にエラーが発生しました。";
	}

	const indentationBody = normalizeIndentationMessageBody(message);
	if (indentationBody) {
		return `IndentationError: ${indentationBody}`;
	}

	if (startsWithPythonErrorName(message)) {
		return message;
	}

	if (message.startsWith("構文エラー:")) {
		return `SyntaxError:${message.slice("構文エラー:".length)}`;
	}

	const inferredName = inferPythonErrorName(message);
	if (inferredName) {
		return `${inferredName}: ${message}`;
	}

	return message;
}

function formatPracticeErrorMessage(practice, text) {
	const fallbackMessage = normalizePracticeErrorDisplay(text || "実行時にエラーが発生しました。");
	const errorDisplayMap = practice?.errorDisplayMap || {};

	return errorDisplayMap[fallbackMessage] || fallbackMessage;
}

async function requestPracticeExecution(sourceCode, inputData = null) {
	const headers = {
		"Content-Type": "application/json"
	};

	const token = typeof getToken === "function" ? getToken() : null;
	if (token) {
		headers.Authorization = `Bearer ${token}`;
	}

	const practiceApiBaseUrl = typeof BASE_URL === "string" ? BASE_URL : "http://127.0.0.1:5000";
	const payload = {
		code: sourceCode
	};

	if (typeof inputData === "string") {
		payload.input_data = inputData;
	}

	const response = await fetch(`${practiceApiBaseUrl}/practice/run`, {
		method: "POST",
		headers: headers,
		body: JSON.stringify(payload)
	});

	let data = {};
	try {
		data = await response.json();
	} catch (error) {
		data = {
			message: "レスポンスの解析に失敗しました。"
		};
	}

	return {
		ok: response.ok,
		status: response.status,
		data: data
	};
}

function setPracticeLoading(button, isLoading) {
	if (typeof setButtonLoading === "function") {
		setButtonLoading(button, isLoading, "実行中...");
		return;
	}

	if (!button) {
		return;
	}

	if (!button.dataset.originalText) {
		button.dataset.originalText = button.textContent;
	}

	button.disabled = isLoading;
	button.textContent = isLoading ? "実行中..." : button.dataset.originalText;
}

function bindPracticeCardActions(root, practice) {
	const runButton = root.querySelector("[data-practice-action='run']");
	const resetButton = root.querySelector("[data-practice-action='reset']");
	const editor = root.querySelector("[data-practice-editor]");
	const inputEditor = root.querySelector("[data-practice-input]");
	const consoleCode = root.querySelector("[data-practice-console]");
	const terminalWrap = root.querySelector("[data-practice-terminal]");
	const statusText = root.querySelector("[data-practice-status]");

	if (!runButton || !resetButton || !editor || !consoleCode || !terminalWrap || !statusText) {
		return;
	}

	if (practice.prefillStarterCode) {
		editor.value = practice.starterCode;
	}

	const setTerminalState = (state) => {
		terminalWrap.classList.remove("is-idle", "is-success", "is-error");
		terminalWrap.classList.add(state);
	};

	const resetConsole = () => {
		consoleCode.textContent = "";
		setTerminalState("is-idle");
	};

	const showConsoleSuccess = (text) => {
		consoleCode.textContent = text && text.trim() ? text : "(出力なし)";
		setTerminalState("is-success");
		statusText.textContent = "実行が完了しました。";
	};

	const showConsoleError = (text) => {
		consoleCode.textContent = formatPracticeErrorMessage(practice, text);
		setTerminalState("is-error");
		statusText.textContent = "エラーが発生しました。コードを見直して再実行してください。";
	};

	runButton.addEventListener("click", async () => {
		resetConsole();

		const sourceCode = editor.value;
		const inputData = practice.allowInput ? (inputEditor?.value || "") : null;
		const usesInput = codeUsesInput(sourceCode);

		if (practice.allowInput && usesInput && !inputData.trim()) {
			showConsoleError("[input] に値を入力してください。\n数値inputなら 10、文字列inputなら Taro のように入力できます。\n複数のinputを使う場合は、1行ずつ入力してください。\n例：\nTaro\n20");
			return;
		}

		statusText.textContent = "実行中です...";
		setPracticeLoading(runButton, true);

		try {
			const response = await requestPracticeExecution(sourceCode, inputData);

			if (!response.ok) {
				showConsoleError(response.data?.message || "APIリクエストに失敗しました。");
				return;
			}

			if (response.data?.success) {
				showConsoleSuccess(response.data?.output || "");
				return;
			}

			showConsoleError(response.data?.error || "実行時にエラーが発生しました。");
		} catch (error) {
			showConsoleError(error?.message || "通信エラーが発生しました。");
		} finally {
			setPracticeLoading(runButton, false);
		}
	});

	resetButton.addEventListener("click", () => {
		editor.value = practice.prefillStarterCode ? practice.starterCode : "";
		if (inputEditor) {
			inputEditor.value = "";
		}
		statusText.textContent = "自由にコードを書いて実行してみましょう。";
		resetConsole();
	});
}

function createChapterNavigation(chapterId) {
	const previousChapterId = getAdjacentChapterId(chapterId, -1);
	const nextChapterId = getAdjacentChapterId(chapterId, 1);
	const actions = [];

	if (previousChapterId) {
		actions.push(`<a class="btn-ghost" href="${previousChapterId}.html">前のchapter</a>`);
	}

	if (nextChapterId) {
		actions.push(`<a class="btn-primary" href="${nextChapterId}.html">次のchapter</a>`);
	}

	actions.push(`<a class="btn-secondary" href="${CHAPTER_ROUTES.textbook}">chapter一覧へ戻る</a>`);

	return actions.join("");
}

function renderChapterPage() {
	const root = document.getElementById("chapterPageRoot");

	if (!root) {
		return;
	}

	const chapterId = root.dataset.chapterId;
	const chapter = CHAPTER_PAGE_DATA[chapterId];
	const practice = normalizePractice(chapter?.practice);
	const functionComparison = chapter?.functionComparison;
	const loopComparisonExamples = Array.isArray(chapter?.loopComparisonExamples) ? chapter.loopComparisonExamples : [];
	const debugReference = Array.isArray(chapter?.debugReference) ? chapter.debugReference : [];
	const conditionExamples = Array.isArray(chapter?.conditionExamples) ? chapter.conditionExamples : [];
	const comparisonOperators = Array.isArray(chapter?.comparisonOperators) ? chapter.comparisonOperators : [];
	const calcOperators = Array.isArray(chapter?.calcOperators) ? chapter.calcOperators : [];
	const rangeBasics = chapter?.rangeBasics;
	const rangeUsageExamples = Array.isArray(chapter?.rangeUsageExamples) ? chapter.rangeUsageExamples : [];
	const breakBasics = chapter?.breakBasics;
	const indexBasics = chapter?.indexBasics;
	const importExamples = Array.isArray(chapter?.importExamples) ? chapter.importExamples : [];
	const typeBasics = chapter?.typeBasics;
	const typeBasicsExamples = Array.isArray(typeBasics?.examples) ? typeBasics.examples : [];
	const listExamples = Array.isArray(chapter?.listExamples) ? chapter.listExamples : [];
	const stringExamples = Array.isArray(chapter?.stringExamples) ? chapter.stringExamples : [];
	const dictionaryExamples = Array.isArray(chapter?.dictionaryExamples) ? chapter.dictionaryExamples : [];
	const exceptionExamples = Array.isArray(chapter?.exceptionExamples) ? chapter.exceptionExamples : [];
	let carouselExamples = [];
	if (conditionExamples.length) {
		carouselExamples = conditionExamples;
	} else if (exceptionExamples.length) {
		carouselExamples = exceptionExamples;
	} else if (importExamples.length) {
		carouselExamples = importExamples;
	} else if (listExamples.length) {
		carouselExamples = listExamples;
	} else if (stringExamples.length) {
		carouselExamples = stringExamples;
	} else {
		carouselExamples = dictionaryExamples;
	}
	const isConditionExamplesCarousel = conditionExamples.length > 0;
	const isExceptionExamplesCarousel = exceptionExamples.length > 0;
	const isImportExamplesCarousel = importExamples.length > 0;
	const isListExamplesCarousel = listExamples.length > 0;
	const navigationSection = `
		<section class="chapter-nav-card glass-outline">
			<span class="eyebrow">Navigation</span>
			<h2>chapter移動ボタン</h2>
			<div class="chapter-nav-actions">
				${createChapterNavigation(chapterId)}
			</div>
		</section>
	`;
	const debugReferenceSection = debugReference.length
		? `
			<section class="debug-reference-section glass-outline">
				<div class="debug-reference-header">
					<span class="eyebrow">Debug Reference</span>
					<h2>よくあるエラー</h2>
					<p>最初に出会いやすいエラーだけを並べた、初心者向けのデバッグガイドです。エラー文を見たら、まずはここで原因の当たりを付けてみましょう。</p>
				</div>
				<div class="debug-reference-carousel" data-debug-carousel>
					<div class="debug-reference-toolbar">
						<button type="button" class="btn-ghost debug-reference-nav" data-debug-prev aria-label="前のエラーへ">◀</button>
						<p class="debug-reference-toolbar-title">よくあるエラー</p>
						<button type="button" class="btn-ghost debug-reference-nav" data-debug-next aria-label="次のエラーへ">▶</button>
					</div>
					<div class="debug-reference-body" data-debug-body>
						<div class="debug-reference-grid" data-debug-page></div>
					</div>
					<div class="debug-reference-dots" data-debug-dots role="tablist" aria-label="Debug Reference ページ切り替え"></div>
				</div>
			</section>
		`
		: "";
	const comparisonOperatorsSection = comparisonOperators.length
		? `
			<article class="chapter-content-card glass-outline comparison-operators-card">
				<span class="eyebrow">COMPARISON OPERATORS</span>
				<h2>比較演算子</h2>
				<p class="comparison-operators-description">条件式では、値を比べるために比較演算子を使います。比較した結果は True または False になります。</p>
				<div class="comparison-operators-grid">
					${comparisonOperators.map((item) => `
						<div class="comparison-operator-card">
							<code class="comparison-operator-symbol">${escapeHtml(item.symbol)}</code>
							<span class="comparison-operator-label">${escapeHtml(item.label)}</span>
						</div>
					`).join("")}
				</div>
			</article>
		`
		: "";
	const calcOperatorsSection = calcOperators.length
		? `
			<article class="chapter-content-card glass-outline calc-operators-card">
				<span class="eyebrow">CALC OPERATORS</span>
				<h2>計算演算子</h2>
				<p class="calc-operators-description">Pythonでよく使う基本的な計算演算子です。記号の意味だけでなく、実際の書き方と実行結果も合わせて確認できます。</p>
				<div class="calc-operators-carousel" data-calc-carousel>
					<div class="calc-operators-toolbar">
						<button type="button" class="btn-ghost calc-operators-nav" data-calc-prev aria-label="前の演算子へ">◀</button>
						<p class="calc-operators-toolbar-title">計算演算子</p>
						<button type="button" class="btn-ghost calc-operators-nav" data-calc-next aria-label="次の演算子へ">▶</button>
					</div>
					<div class="calc-operators-body" data-calc-body>
						<div class="calc-operators-table" data-calc-page role="list" aria-label="計算演算子の一覧"></div>
					</div>
					<div class="calc-operators-dots" data-calc-dots role="tablist" aria-label="計算演算子ページ切り替え"></div>
				</div>
			</article>
		`
		: "";
	const rangeBasicsSection = rangeBasics
		? `
			<article class="chapter-code-card glass-outline range-basics-card">
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">${escapeHtml(rangeBasics.eyebrow || "RANGE BASICS")}</span>
						<h2>${escapeHtml(rangeBasics.title || "rangeとは？")}</h2>
					</div>
				</div>
				<p class="range-basics-description">${escapeHtml(rangeBasics.description || "")}</p>
				<p class="range-basics-note">${escapeHtml(rangeBasics.note || "")}</p>
			</article>
		`
		: "";
	const rangeUsageTabs = rangeUsageExamples
		.map((example, index) => `<button type="button" class="string-carousel-tab" data-range-tab="${index}">${escapeHtml(example.title || `range${index + 1}`)}</button>`)
		.join("");
	const rangeUsageSection = rangeUsageExamples.length
		? `
			<article class="chapter-code-card glass-outline string-carousel-card range-usage-carousel-card" data-range-carousel>
				<div class="string-carousel-toolbar">
					<button type="button" class="btn-ghost string-carousel-nav" data-range-prev aria-label="前のrange例へ">◀</button>
					<p class="string-carousel-title" data-range-title>${escapeHtml(rangeUsageExamples[0]?.title || "range")}</p>
					<button type="button" class="btn-ghost string-carousel-nav" data-range-next aria-label="次のrange例へ">▶</button>
				</div>
				<div class="string-carousel-tabs" role="tablist" aria-label="rangeの使い方切り替え">
					${rangeUsageTabs}
				</div>
				<div class="string-carousel-body" data-range-body>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">RANGE PATTERNS</span>
							<h2>rangeの使い方</h2>
						</div>
						<span class="chip">Loop</span>
					</div>
					<pre class="code-block"><code data-range-code></code></pre>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">Output</span>
							<h2>実行結果</h2>
						</div>
						<span class="chip">Console</span>
					</div>
					<pre class="output-block"><code data-range-output></code></pre>
					<p class="string-carousel-description" data-range-description></p>
				</div>
			</article>
		`
		: "";
	const breakBasicsSection = breakBasics
		? `
			<article class="chapter-code-card glass-outline break-basics-card">
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">${escapeHtml(breakBasics.eyebrow || "LOOP CONTROL")}</span>
						<h2>${escapeHtml(breakBasics.title || "breakとは？")}</h2>
					</div>
				</div>
				<p class="break-basics-description">${escapeHtml(breakBasics.description || "")}</p>
				<pre class="code-block"><code>${escapeHtml(breakBasics.code || "")}</code></pre>
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">Output</span>
						<h2>実行結果</h2>
					</div>
					<span class="chip">Console</span>
				</div>
				<pre class="output-block"><code>${escapeHtml(breakBasics.output || "")}</code></pre>
				<p class="break-basics-note">${escapeHtml(breakBasics.note || "")}</p>
			</article>
		`
		: "";
	const indexBasicsRows = Array.isArray(indexBasics?.rows) ? indexBasics.rows : [];
	const indexBasicsSection = indexBasics
		? `
			<article class="chapter-content-card glass-outline index-basics-card">
				<span class="eyebrow">${escapeHtml(indexBasics.eyebrow || "INDEX BASICS")}</span>
				<h2>${escapeHtml(indexBasics.title || "番号について")}</h2>
				<p class="index-basics-description">${escapeHtml(indexBasics.description || "")}</p>
				<div class="index-basics-table-wrap" role="region" aria-label="リストの番号と値の対応表">
					<table class="index-basics-table">
						<thead>
							<tr>
								<th scope="col">番号</th>
								<th scope="col">値</th>
							</tr>
						</thead>
						<tbody>
							${indexBasicsRows.map((item) => `
								<tr>
									<td>${escapeHtml(item.index ?? "")}</td>
									<td>${escapeHtml(item.value ?? "")}</td>
								</tr>
							`).join("")}
						</tbody>
					</table>
				</div>
			</article>
		`
		: "";
	const functionComparisonSection = functionComparison
		? `
			<article class="chapter-code-card glass-outline function-comparison-card">
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">${escapeHtml(functionComparison.eyebrow || "Function Comparison")}</span>
						<h2>${escapeHtml(functionComparison.title || "関数なしと関数ありの比較")}</h2>
					</div>
					<span class="chip">${escapeHtml(functionComparison.chip || "Reuse")}</span>
				</div>
				<div class="function-comparison-grid">
					<section class="function-comparison-block">
						<p class="function-comparison-label">${escapeHtml(functionComparison.withoutLabel || "関数なし")}</p>
						<pre class="function-comparison-code"><code>${escapeHtml(functionComparison.withoutCode || "")}</code></pre>
					</section>
					<section class="function-comparison-block">
						<p class="function-comparison-label">${escapeHtml(functionComparison.withLabel || "関数あり")}</p>
						<pre class="function-comparison-code"><code>${escapeHtml(functionComparison.withCode || "")}</code></pre>
					</section>
				</div>
			</article>
		`
		: "";
	const loopComparisonTabs = loopComparisonExamples
		.map((example, index) => `<button type="button" class="string-carousel-tab" data-loop-tab="${index}">${escapeHtml(example.title || `比較${index + 1}`)}</button>`)
		.join("");
	const loopComparisonSection = loopComparisonExamples.length
		? `
			<article class="chapter-code-card glass-outline loop-comparison-carousel-card" data-loop-carousel>
				<div class="string-carousel-toolbar">
					<button type="button" class="btn-ghost string-carousel-nav" data-loop-prev aria-label="前の比較へ">◀</button>
					<p class="string-carousel-title" data-loop-title>${escapeHtml(loopComparisonExamples[0]?.title || "Loop Comparison")}</p>
					<button type="button" class="btn-ghost string-carousel-nav" data-loop-next aria-label="次の比較へ">▶</button>
				</div>
				<div class="string-carousel-tabs" role="tablist" aria-label="Loop Comparison 切り替え">
					${loopComparisonTabs}
				</div>
				<div class="string-carousel-body" data-loop-body>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">Loop Comparison</span>
							<h2>while の理解ポイント</h2>
						</div>
						<span class="chip">Loop</span>
					</div>
					<p class="string-carousel-description" data-loop-description></p>
					<div class="loop-comparison-split" data-loop-split></div>
					<p class="loop-comparison-note" data-loop-note hidden></p>
				</div>
			</article>
		`
		: "";
	const stringCarouselTabs = carouselExamples
		.map((example, index) => `<button type="button" class="string-carousel-tab" data-string-tab="${index}">${escapeHtml(example.title || `例${index + 1}`)}</button>`)
		.join("");
	const sampleOutputSection = carouselExamples.length
		? `
			<article class="chapter-code-card glass-outline string-carousel-card" data-string-carousel>
				<div class="string-carousel-toolbar">
					<button type="button" class="btn-ghost string-carousel-nav" data-string-prev aria-label="前のサンプルへ">◀</button>
					<p class="string-carousel-title" data-string-title>${escapeHtml(carouselExamples[0]?.title || (isExceptionExamplesCarousel ? "例外処理" : "サンプル"))}</p>
					<button type="button" class="btn-ghost string-carousel-nav" data-string-next aria-label="次のサンプルへ">▶</button>
				</div>
				<div class="string-carousel-tabs" role="tablist" aria-label="${isExceptionExamplesCarousel ? "例外処理の切り替え" : (isImportExamplesCarousel ? "標準ライブラリ切り替え" : (isListExamplesCarousel ? "リスト例の切り替え" : "サンプル切り替え"))}">
					${stringCarouselTabs}
				</div>
				<div class="string-carousel-body" data-string-body>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">${isConditionExamplesCarousel ? "Condition Examples" : (isExceptionExamplesCarousel ? "Exception Examples" : (isImportExamplesCarousel ? "Import Examples" : (isListExamplesCarousel ? "List Examples" : "Sample Code")))}</span>
							<h2>${isConditionExamplesCarousel ? "条件分岐の例" : (isExceptionExamplesCarousel ? "例外処理の例" : (isImportExamplesCarousel ? "標準ライブラリの例" : (isListExamplesCarousel ? "リストの例" : "サンプルコード")))}</h2>
						</div>
						<span class="chip">${isConditionExamplesCarousel ? "If" : (isExceptionExamplesCarousel ? "Try" : (isImportExamplesCarousel ? "Library" : (isListExamplesCarousel ? "List" : "Python")))}</span>
					</div>
					<section class="string-feature-section" data-string-feature-section hidden>
						<div class="chapter-code-header string-feature-header">
							<div>
								<span class="eyebrow">Features</span>
								<h3>よく使う機能</h3>
							</div>
						</div>
						<div class="string-feature-list" data-string-feature-list></div>
					</section>
					${
						isImportExamplesCarousel
							? ""
							: `
								<pre class="code-block"><code data-string-code></code></pre>
								<div class="chapter-code-header">
									<div>
										<span class="eyebrow">Output</span>
										<h2>実行結果</h2>
									</div>
									<span class="chip">Console</span>
								</div>
								<pre class="output-block"><code data-string-output></code></pre>
							`
					}
					<p class="string-carousel-description" data-string-description></p>
				</div>
			</article>
		`
		: `
			<article class="chapter-code-card glass-outline">
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">Sample Code</span>
						<h2>サンプルコード</h2>
					</div>
					<span class="chip">Python</span>
				</div>
				<pre class="code-block"><code>${escapeHtml(chapter.sampleCode || "")}</code></pre>
			</article>

			<article class="chapter-code-card glass-outline">
				<div class="chapter-code-header">
					<div>
						<span class="eyebrow">Output</span>
						<h2>実行結果</h2>
					</div>
					<span class="chip">Console</span>
				</div>
				<pre class="output-block"><code>${escapeHtml(chapter.output || "")}</code></pre>
			</article>
		`;
	const typeBasicsTabs = typeBasicsExamples
		.map((example, index) => `<button type="button" class="string-carousel-tab" data-type-tab="${index}">${escapeHtml(example.title || `型${index + 1}`)}</button>`)
		.join("");
	const typeBasicsSection = typeBasicsExamples.length
		? `
			<article class="chapter-code-card glass-outline string-carousel-card type-basics-card" data-type-carousel>
				<div class="string-carousel-toolbar">
					<button type="button" class="btn-ghost string-carousel-nav" data-type-prev aria-label="前の型へ">◀</button>
					<p class="string-carousel-title" data-type-title>${escapeHtml(typeBasicsExamples[0]?.title || "type")}</p>
					<button type="button" class="btn-ghost string-carousel-nav" data-type-next aria-label="次の型へ">▶</button>
				</div>
				<div class="string-carousel-tabs" role="tablist" aria-label="型の切り替え">
					${typeBasicsTabs}
				</div>
				<div class="string-carousel-body" data-type-body>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">Type Basics</span>
							<h2>${escapeHtml(typeBasics?.title || "型とは？")}</h2>
						</div>
						<span class="chip">Type</span>
					</div>
					<p class="string-carousel-description">${escapeHtml(typeBasics?.description || "")}</p>
					<pre class="code-block"><code data-type-code></code></pre>
					<div class="chapter-code-header">
						<div>
							<span class="eyebrow">Output</span>
							<h2>実行結果</h2>
						</div>
						<span class="chip">Console</span>
					</div>
					<pre class="output-block"><code data-type-output></code></pre>
					<p class="string-carousel-description" data-type-description></p>
				</div>
			</article>
		`
		: "";
	const practiceTerminalInput = practice.allowInput
		? `
			<div class="practice-terminal-block">
				<p class="practice-terminal-label">${escapeHtml(practice.inputLabel)}</p>
				<textarea id="practiceInputEditor" class="practice-terminal-input" data-practice-input placeholder="${escapeHtml(practice.inputPlaceholder)}" spellcheck="false"></textarea>
			</div>
		`
		: "";

	if (!chapter) {
		root.innerHTML = `
			<section class="card glass-outline chapter-content-card">
				<h1>chapterが見つかりません</h1>
				<p>指定されたchapterの定義が存在しません。</p>
				<div class="chapter-nav-actions">
					<a class="btn-secondary" href="${CHAPTER_ROUTES.textbook}">chapter一覧へ戻る</a>
				</div>
			</section>
		`;
		return;
	}

	document.title = `Chapter ${chapter.number} | ${chapter.title} | Python Learning Cloud`;

	root.innerHTML = `
		<header class="topbar chapter-page-topbar">
			<div class="brand-wrap">
				<a class="brand" href="${CHAPTER_ROUTES.textbook}" aria-label="教科書一覧へ戻る">
					<img src="../../image/main_bg_transparent.png" alt="Python Learning Cloud" class="brand-logo">
					<span class="brand-name">Python Learning Cloud</span>
				</a>
				<span class="eyebrow">Textbook Chapter</span>
			</div>
			<div class="topbar-actions">
				<a class="btn-ghost" href="${CHAPTER_ROUTES.textbook}">教科書一覧へ戻る</a>
				<a class="btn-primary" href="${CHAPTER_ROUTES.study}">学習画面へ</a>
				<a class="btn-ghost" href="${CHAPTER_ROUTES.settings}">設定</a>
			</div>
		</header>

		<main class="chapter-page-main">
			<section class="card glass-outline chapter-hero">
				<div class="chapter-hero-copy">
					<span class="chapter-kicker">Chapter ${chapter.number}</span>
					<h1>${chapter.title}</h1>
					<p>${chapter.summary}</p>
				</div>
				<aside class="chapter-hero-panel">
					<h2>学習目標</h2>
					<ul class="chapter-objectives">${createListItems(chapter.goals)}</ul>
				</aside>
			</section>

			<section class="chapter-content-grid">
				<div class="chapter-content-stack">
					<article class="chapter-content-card glass-outline">
						<span class="eyebrow">Explanation</span>
						<h2>解説セクション</h2>
						${createParagraphs(chapter.explanation)}
					</article>

					${indexBasicsSection}

					${comparisonOperatorsSection}

					${rangeBasicsSection}

					${rangeUsageSection}

					${breakBasicsSection}

					${sampleOutputSection}

					${calcOperatorsSection}

					${typeBasicsSection}

					${loopComparisonSection}

					${functionComparisonSection}
				</div>

				<aside class="chapter-side-stack">
					<article class="chapter-summary-card glass-outline">
						<span class="eyebrow">Key Points</span>
						<h2>ポイントまとめ</h2>
						<ul class="chapter-points-list">${createListItems(chapter.points)}</ul>
					</article>

					<article class="chapter-practice-card glass-outline">
						<span class="eyebrow">Practice</span>
						<h2>${practice.title}</h2>
						<p class="chapter-practice-text">${practice.instruction}</p>
						<div class="practice-editor-wrap">
							<label class="field-label" for="practiceEditor">コード入力欄</label>
							<textarea id="practiceEditor" class="practice-editor" data-practice-editor placeholder="${escapeHtml(practice.placeholder || "ここにPythonコードを書いて試してみましょう")}" spellcheck="false"></textarea>
						</div>
						<div class="practice-actions">
							<button type="button" class="btn-primary" data-practice-action="run">実行</button>
							<button type="button" class="btn-ghost" data-practice-action="reset">初期化</button>
						</div>
						<p class="practice-status" data-practice-status>自由にコードを書いて実行してみましょう。</p>
						<div class="practice-terminal-wrap is-idle" data-practice-terminal>
							<p class="practice-section-label">Terminal</p>
							<div class="practice-terminal-box">
								${practiceTerminalInput}
								<div class="practice-terminal-block">
									<p class="practice-terminal-label">[output]</p>
									<pre class="practice-terminal-output"><code data-practice-console></code></pre>
								</div>
							</div>
						</div>
					</article>
				</aside>
			</section>

			${debugReferenceSection}
			${navigationSection}
		</main>
	`;

	bindPracticeCardActions(root, practice);
	bindStringExampleCarousel(root, carouselExamples);
	bindTypeBasicsCarousel(root, typeBasicsExamples);
	bindRangeUsageCarousel(root, rangeUsageExamples);
	bindLoopComparisonCarousel(root, loopComparisonExamples);
	bindCalcOperatorsCarousel(root, calcOperators);
	bindDebugReferenceCarousel(root, debugReference);
}

document.addEventListener("DOMContentLoaded", () => {
	if (!requireLogin()) {
		window.location.href = "../../pages/login.html";
		return;
	}

	renderChapterPage();
});