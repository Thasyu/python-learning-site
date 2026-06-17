async function loadQuestions() {
    const tbody = document.querySelector("#questionTable tbody");

    tbody.innerHTML = "";
    setMessage("message", "");

    try {
        const chapterNumbers = Array.from({ length: 15 }, (_, index) => index + 1);
        const responses = await Promise.all(
            chapterNumbers.map(chapter => fetchQuestionsByChapter(chapter))
        );

        if (responses.some(response => !response.ok)) {
            setMessage("message", "問題一覧の取得に失敗しました。");
            return;
        }

        const questions = responses.flatMap(response => response.data);

        for (const q of questions) {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${q.id}</td>
                <td>${q.chapter}</td>
                <td>${q.category}</td>
                <td>${q.difficulty}</td>
                <td>${q.judge_type}</td>
                <td>${q.question}</td>
            `;

            tbody.appendChild(tr);
        }
    } catch (error) {
        setMessage("message", "通信エラーが発生しました。");
    }
}

loadQuestions();