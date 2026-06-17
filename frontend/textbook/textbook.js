const TEXTBOOK_CHAPTERS = [
	{
		id: "chapter1",
		number: 1,
		title: "出力と基本",
		description: "printを使った出力と、Python学習の最初の考え方を学びます。",
		level: "Beginner",
		estimatedMinutes: 10,
		pageUrl: "textbookpages/chapter1.html",
		status: "available"
	},
	{
		id: "chapter2",
		number: 2,
		title: "変数",
		description: "変数への代入と、値の扱い方の基礎を身につけます。",
		level: "Beginner",
		estimatedMinutes: 12,
		pageUrl: "textbookpages/chapter2.html",
		status: "available"
	},
	{
		id: "chapter3",
		number: 3,
		title: "条件分岐",
		description: "if文を使って、条件に応じた処理の分岐を学びます。",
		level: "Beginner",
		estimatedMinutes: 15,
		pageUrl: "textbookpages/chapter3.html",
		status: "available"
	},
	{
		id: "chapter4",
		number: 4,
		title: "ループ",
		description: "for文で繰り返し処理を作り、反復の感覚をつかみます。",
		level: "Beginner",
		estimatedMinutes: 14,
		pageUrl: "textbookpages/chapter4.html",
		status: "available"
	},
	{
		id: "chapter5",
		number: 5,
		title: "リスト",
		description: "複数の値をまとめるリストと基本操作を学習します。",
		level: "Beginner",
		estimatedMinutes: 16,
		pageUrl: "textbookpages/chapter5.html",
		status: "available"
	},
	{
		id: "chapter6",
		number: 6,
		title: "デバッグ",
		description: "エラーの読み取りと、原因切り分けの基礎を学びます。",
		level: "Intermediate",
		estimatedMinutes: 15,
		pageUrl: "textbookpages/chapter6.html",
		status: "available"
	},
	{
		id: "chapter7",
		number: 7,
		title: "input",
		description: "inputで値を受け取り、文字列として処理する流れを理解します。",
		level: "Beginner",
		estimatedMinutes: 12,
		pageUrl: "textbookpages/chapter7.html",
		status: "available"
	},
	{
		id: "chapter8",
		number: 8,
		title: "関数",
		description: "関数定義と呼び出しを通して、処理の再利用を学びます。",
		level: "Intermediate",
		estimatedMinutes: 18,
		pageUrl: "textbookpages/chapter8.html",
		status: "available"
	},
	{
		id: "chapter9",
		number: 9,
		title: "文字列",
		description: "文字列の連結、分割、検索など実用的な操作を学びます。",
		level: "Intermediate",
		estimatedMinutes: 17,
		pageUrl: "textbookpages/chapter9.html",
		status: "available"
	},
	{
		id: "chapter10",
		number: 10,
		title: "辞書",
		description: "キーと値の対応でデータを管理する辞書を学びます。",
		level: "Intermediate",
		estimatedMinutes: 17,
		pageUrl: "textbookpages/chapter10.html",
		status: "available"
	},
	{
		id: "chapter11",
		number: 11,
		title: "while",
		description: "条件で反復を制御するwhile文の基礎を身につけます。",
		level: "Intermediate",
		estimatedMinutes: 14,
		pageUrl: "textbookpages/chapter11.html",
		status: "available"
	},
	{
		id: "chapter12",
		number: 12,
		title: "import",
		description: "モジュールを読み込み、機能を拡張する方法を学びます。",
		level: "Intermediate",
		estimatedMinutes: 13,
		pageUrl: "textbookpages/chapter12.html",
		status: "available"
	},
	{
		id: "chapter13",
		number: 13,
		title: "例外処理",
		description: "try/exceptでエラー時の挙動を安全に扱う方法を学びます。",
		level: "Intermediate",
		estimatedMinutes: 16,
		pageUrl: "textbookpages/chapter13.html",
		status: "available"
	}
];

const TOPBAR_ROUTES = {
	home: "../pages/index.html",
	dashboard: "../pages/dashboard.html",
	study: "../pages/study.html",
	settings: "../pages/settings.html"
};

function getChapterById(chapterId) {
	return TEXTBOOK_CHAPTERS.find((chapter) => chapter.id === chapterId) || null;
}

function toStatusLabel(status) {
	return status === "available" ? "Available" : "Coming Soon";
}

function createChapterCard(chapter) {
	const article = document.createElement("article");
	article.className = "chapter-card";
	article.setAttribute("role", "listitem");

	if (chapter.status === "coming soon") {
		article.classList.add("is-coming-soon");
	}

	const statusClass = chapter.status === "available" ? "is-available" : "is-coming-soon";
	const actionMarkup = chapter.status === "available"
		? `
			<div class="chapter-actions">
				<button class="btn-primary" type="button" data-open-chapter="${chapter.id}">読む</button>
			</div>
		`
		: `
			<div class="chapter-actions">
				<span class="chapter-coming-soon-text">準備中です</span>
				<button class="btn-ghost" type="button" disabled aria-disabled="true">準備中</button>
			</div>
		`;

	article.innerHTML = `
		<div class="chapter-card-head">
			<span class="chapter-number">Chapter ${chapter.number}</span>
			<span class="chapter-status ${statusClass}">${toStatusLabel(chapter.status)}</span>
		</div>
		<h3 class="chapter-title">${chapter.title}</h3>
		<p class="chapter-description">${chapter.description}</p>
		${actionMarkup}
	`;

	return article;
}

function renderChapterCards() {
	const chapterGrid = document.getElementById("chapterGrid");
	const chapterCountBadge = document.getElementById("chapterCountBadge");

	chapterGrid.innerHTML = "";

	TEXTBOOK_CHAPTERS.forEach((chapter) => {
		chapterGrid.appendChild(createChapterCard(chapter));
	});

	chapterCountBadge.innerText = `${TEXTBOOK_CHAPTERS.length} chapter`;
}

function openChapter(chapterId) {
	const chapter = getChapterById(chapterId);

	if (!chapter || chapter.status !== "available") {
		return;
	}

	window.location.href = chapter.pageUrl;
}

function bindChapterActions() {
	const chapterGrid = document.getElementById("chapterGrid");

	chapterGrid.addEventListener("click", (event) => {
		const openButton = event.target.closest("[data-open-chapter]");

		if (openButton) {
			openChapter(openButton.dataset.openChapter);
			return;
		}
	});

	document.getElementById("startChapter1Button").addEventListener("click", () => {
		openChapter("chapter1");
	});
}

function bindTextbookTopbarActions() {
	document.getElementById("homeButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.home;
	});

	document.getElementById("dashboardButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.dashboard;
	});

	document.getElementById("studyButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.study;
	});

	document.getElementById("settingsButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.settings;
	});

	document.getElementById("goStudyFromHeroButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.study;
	});

	document.getElementById("footerHomeButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.home;
	});

	document.getElementById("footerDashboardButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.dashboard;
	});

	document.getElementById("footerStudyButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.study;
	});

	document.getElementById("footerSettingsButton").addEventListener("click", () => {
		window.location.href = TOPBAR_ROUTES.settings;
	});
}

document.addEventListener("DOMContentLoaded", () => {
	if (!requireLogin()) {
		// textbook 配下では requireLogin の相対遷移先がずれるため補正する。
		window.location.href = "../pages/login.html";
		return;
	}

	bindTextbookTopbarActions();
	renderChapterCards();
	bindChapterActions();
});
