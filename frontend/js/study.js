const RUNTIME_CACHE_KEY = "study_runtime_state_v4";
const LEGACY_RUNTIME_CACHE_KEYS = ["study_runtime_state_v3", "study_runtime_state_v2"];

const SNAPSHOT_FIELDS = [
    "id",
    "chapter",
    "category",
    "difficulty",
    "question",
    "starter_code",
    "ending_code",
    "judge_type",
    "expected_output",
    "required_keywords",
    "input_data",
    "explanation",
    "model_answers",
    "hints",
    "generated_values"
];

const state = {
    questions: [],
    currentQuestionIndex: 0,
    maxUnlockedIndex: 0,
    currentChapter: null,
    currentMode: "recommended",
    currentReviewMode: false,
    answeredQuestionIds: new Set(),
    questionStatuses: {},
    questionResults: {},
    currentStreak: 0,
    maxStreak: 0,
    isSubmitting: false,
    latestSession: null
};

function setSubmitButtonSubmittingState(submitting) {
    const submitButton = document.getElementById("submitButton");

    if (!submitButton) {
        return;
    }

    submitButton.disabled = submitting;
    submitButton.innerText = submitting ? "Submitting..." : "回答する";
}

function getAnsweredCount() {
    return state.answeredQuestionIds.size;
}

function getCorrectCount() {
    return Object.values(state.questionStatuses).filter((status) => status === "correct").length;
}

function getWrongCount() {
    return Object.values(state.questionStatuses).filter((status) => status === "wrong").length;
}

function getQuestionByIndex(index) {
    return state.questions[index] || null;
}

function getCurrentQuestion() {
    return getQuestionByIndex(state.currentQuestionIndex);
}

function getQuestionStatus(questionId) {
    return state.questionStatuses[questionId] || "unanswered";
}

function isCurrentQuestionAnswered() {
    const currentQuestion = getCurrentQuestion();

    if (!currentQuestion) {
        return false;
    }

    return getQuestionStatus(currentQuestion.id) !== "unanswered";
}

function calculateRank(accuracy, wrongCount) {
    if (accuracy >= 96 && wrongCount <= 1) {
        return "S";
    }
    if (accuracy >= 88) {
        return "A";
    }
    if (accuracy >= 75) {
        return "B";
    }
    if (accuracy >= 60) {
        return "C";
    }
    return "D";
}

function normalizeQuestionSnapshot(question) {
    const normalized = {};

    SNAPSHOT_FIELDS.forEach((field) => {
        const value = question?.[field];

        if (value === undefined) {
            return;
        }

        if (Array.isArray(value)) {
            normalized[field] = [...value];
            return;
        }

        if (value && typeof value === "object") {
            normalized[field] = { ...value };
            return;
        }

        normalized[field] = value;
    });

    return normalized;
}

function buildQuestionSnapshot() {
    return state.questions.map((question) => normalizeQuestionSnapshot(question));
}

function getSetupMessageElement() {
    let element = document.getElementById("setupMessage");

    if (element) {
        return element;
    }

    const settingArea = document.getElementById("settingArea");

    if (!settingArea) {
        return null;
    }

    element = document.createElement("p");
    element.id = "setupMessage";
    element.className = "inline-message";
    settingArea.appendChild(element);

    return element;
}

function setSetupMessage(text, type = "error") {
    const element = getSetupMessageElement();

    if (!element) {
        return;
    }

    element.innerText = text;
    element.classList.remove("is-success");

    if (text && type === "success") {
        element.classList.add("is-success");
    }
}

function persistRuntimeState() {
    if (!state.questions.length || state.currentChapter === null) {
        return;
    }

    const payload = {
        chapter: state.currentChapter,
        mode: state.currentMode,
        review_mode: state.currentReviewMode,
        question_ids: state.questions.map((question) => question.id),
        question_snapshot: buildQuestionSnapshot(),
        current_question_index: state.currentQuestionIndex,
        max_unlocked_index: state.maxUnlockedIndex,
        answered_question_ids: Array.from(state.answeredQuestionIds),
        question_statuses: state.questionStatuses,
        question_results: state.questionResults,
        current_streak: state.currentStreak,
        max_streak: state.maxStreak,
        updated_at: Date.now()
    };

    localStorage.setItem(RUNTIME_CACHE_KEY, JSON.stringify(payload));
}

function readRuntimeState() {
    const raw = localStorage.getItem(RUNTIME_CACHE_KEY);

    if (!raw) {
        return null;
    }

    try {
        return JSON.parse(raw);
    } catch (error) {
        return null;
    }
}

function clearRuntimeState() {
    localStorage.removeItem(RUNTIME_CACHE_KEY);
}

function clearLegacyRuntimeState() {
    LEGACY_RUNTIME_CACHE_KEYS.forEach((key) => {
        localStorage.removeItem(key);
    });
}

function applyRuntimeState(runtimeState) {
    if (!runtimeState) {
        return;
    }

    const currentQuestionIds = state.questions.map((question) => question.id);
    const runtimeQuestionIds = Array.isArray(runtimeState.question_ids)
        ? runtimeState.question_ids
        : [];

    const isSameSet =
        currentQuestionIds.length === runtimeQuestionIds.length
        && currentQuestionIds.every((id, index) => id === runtimeQuestionIds[index]);

    if (!isSameSet) {
        return;
    }

    const statuses = runtimeState.question_statuses || {};
    const results = runtimeState.question_results || {};
    const answeredIds = Array.isArray(runtimeState.answered_question_ids)
        ? runtimeState.answered_question_ids
        : [];

    state.currentQuestionIndex = Number(runtimeState.current_question_index || 0);
    state.maxUnlockedIndex = Number(runtimeState.max_unlocked_index || 0);
    state.currentStreak = Number(runtimeState.current_streak || 0);
    state.maxStreak = Number(runtimeState.max_streak || 0);

    state.answeredQuestionIds = new Set(answeredIds);
    state.questionStatuses = {};
    state.questionResults = {};

    state.questions.forEach((question) => {
        state.questionStatuses[question.id] = statuses[question.id] || "unanswered";

        if (results[question.id]) {
            state.questionResults[question.id] = results[question.id];
        }
    });

    state.currentQuestionIndex = Math.max(0, Math.min(state.currentQuestionIndex, state.questions.length - 1));
    state.maxUnlockedIndex = Math.max(0, Math.min(state.maxUnlockedIndex, state.questions.length - 1));
}

async function inferStatusesFromReviewQueue() {
    try {
        const reviewResult = await fetchReviewQuestions();

        if (!reviewResult.ok) {
            return;
        }

        const reviewIds = new Set((reviewResult.data || []).map((question) => question.id));

        state.answeredQuestionIds.forEach((questionId) => {
            state.questionStatuses[questionId] = reviewIds.has(questionId) ? "wrong" : "correct";
        });
    } catch (error) {
        // Keep current state when review fetch fails.
    }
}

function syncModeCards() {
    const selectedMode = document.getElementById("modeSelect").value;

    document.querySelectorAll(".mode-card").forEach((card) => {
        card.classList.toggle("is-active", card.dataset.mode === selectedMode);
    });
}

function syncReviewCard() {
    const review = document.getElementById("reviewMode").checked;
    const reviewCard = document.querySelector(".review-card");

    if (!reviewCard) {
        return;
    }

    reviewCard.classList.toggle("is-on", review);
}

function updateEditorLineNumbers() {
    const textarea = document.getElementById("answerCode");
    const gutter = document.getElementById("editorLineNumbers");

    if (!textarea || !gutter) {
        return;
    }

    const lineCount = Math.max(1, textarea.value.split("\n").length);
    const lines = [];

    for (let line = 1; line <= lineCount; line += 1) {
        lines.push(String(line));
    }

    gutter.innerText = lines.join("\n");
    gutter.scrollTop = textarea.scrollTop;
}

function resetVerdictBanner() {
    const resultArea = document.getElementById("resultArea");

    resultArea.classList.remove("is-correct", "is-wrong", "flash-success", "flash-wrong");
    document.getElementById("verdictIcon").innerText = "\u25cf";
    document.getElementById("verdictText").innerText = "PENDING";
    document.getElementById("verdictSub").innerText = "Result appears after submit";
}

function setVerdictBanner(result) {
    const resultArea = document.getElementById("resultArea");

    resultArea.classList.remove("is-correct", "is-wrong", "flash-success", "flash-wrong");

    if (result.is_correct) {
        resultArea.classList.add("is-correct", "flash-success");
        document.getElementById("verdictIcon").innerText = "\u2713";
        document.getElementById("verdictText").innerText = "CORRECT";
        document.getElementById("verdictSub").innerText = "Output matched expectation";
        return;
    }

    resultArea.classList.add("is-wrong", "flash-wrong");
    document.getElementById("verdictIcon").innerText = "\u2717";
    document.getElementById("verdictText").innerText = "WRONG";
    document.getElementById("verdictSub").innerText = result.result_message || "Fix and retry";
}

function triggerQuestionFeedback(isCorrect) {
    const card = document.getElementById("questionCard");

    if (!card) {
        return;
    }

    card.classList.remove(
        "flash-correct",
        "flash-wrong",
        "correct-pop",
        "wrong-shake",
        "success-glow",
        "error-glow"
    );

    if (isCorrect) {
        card.classList.add("flash-correct", "correct-pop", "success-glow");
        return;
    }

    card.classList.add("flash-wrong", "wrong-shake", "error-glow");
}

function resetQuestionFeedback() {
    const card = document.getElementById("questionCard");

    if (!card) {
        return;
    }

    card.classList.remove(
        "flash-correct",
        "flash-wrong",
        "correct-pop",
        "wrong-shake",
        "success-glow",
        "error-glow",
        "pulse"
    );

    card.style.animation = "";
    card.style.transform = "";
    card.style.opacity = "";
}

function resetResultAnimations() {
    const resultArea = document.getElementById("resultArea");
    const verdictBanner = document.getElementById("verdictBanner");

    if (!resultArea) {
        return;
    }

    resultArea.classList.remove(
        "is-correct",
        "is-wrong",
        "flash-success",
        "flash-wrong",
        "success-glow",
        "error-glow",
        "is-animating"
    );

    resultArea.style.animation = "";
    resultArea.style.transform = "";
    resultArea.style.opacity = "";

    if (verdictBanner) {
        verdictBanner.classList.remove("is-visible", "is-temporary", "success", "error");
        verdictBanner.style.animation = "";
        verdictBanner.style.transform = "";
        verdictBanner.style.opacity = "";
    }
}

function resetEditorTransientState() {
    const editorShell = document.getElementById("editorShell");
    const answerCode = document.getElementById("answerCode");

    if (editorShell) {
        editorShell.classList.remove("is-focus", "is-active-line", "is-glow");
        editorShell.style.animation = "";
        editorShell.style.transform = "";
        editorShell.style.opacity = "";
    }

    if (answerCode) {
        // 問題切替時に擬似フォーカス演出を残さない
        answerCode.blur();
    }
}

function resetNavTransientState() {
    const navButtons = document.querySelectorAll(".question-nav-btn");

    navButtons.forEach((button) => {
        button.classList.remove("is-hover", "is-pressed", "is-temporary", "is-animating");
        button.style.animation = "";
        button.style.transform = "";
        button.style.opacity = "";
    });
}

function resetControlTransientState() {
    const submitButton = document.getElementById("submitButton");
    const nextButton = document.getElementById("nextButton");
    const pauseButton = document.getElementById("pauseStudyButton");

    [submitButton, nextButton, pauseButton].forEach((button) => {
        if (!button) {
            return;
        }

        button.classList.remove("is-loading", "is-temporary", "is-pressed");
        button.style.animation = "";
        button.style.transform = "";
        button.style.opacity = "";
    });

    if (submitButton) {
        submitButton.dataset.loading = "false";
    }
}

function resetFinishTransientState() {
    const finishArea = document.getElementById("finishArea");

    if (!finishArea) {
        return;
    }

    finishArea.classList.remove("is-animating", "is-visible", "flash-success", "flash-wrong");
    finishArea.style.animation = "";
    finishArea.style.transform = "";
    finishArea.style.opacity = "";
}

function resetTransientUIState() {
    resetQuestionFeedback();
    resetResultAnimations();
    resetEditorTransientState();
    resetNavTransientState();
    resetControlTransientState();
    resetFinishTransientState();
}

function syncProgressUI() {
    const answeredCount = getAnsweredCount();
    const total = state.questions.length;
    const correctCount = getCorrectCount();
    const wrongCount = getWrongCount();
    const accuracy = answeredCount > 0
        ? Math.round((correctCount / answeredCount) * 100)
        : 0;

    document.getElementById("progressText").innerText = `${state.currentQuestionIndex + 1} / ${total} 問`;
    document.getElementById("statProgress").innerText = `${answeredCount} / ${total}`;
    document.getElementById("statAccuracy").innerText = `${accuracy}%`;
    document.getElementById("statStreak").innerText = String(state.currentStreak);
    document.getElementById("statReview").innerText = String(wrongCount);

    const navProgress = total > 0 ? Math.round((answeredCount / total) * 100) : 0;
    document.getElementById("navProgressBar").style.width = `${navProgress}%`;
}

function getNavState(index) {
    const question = getQuestionByIndex(index);

    if (!question) {
        return "locked";
    }

    if (index === state.currentQuestionIndex) {
        return "current";
    }

    if (index > state.maxUnlockedIndex) {
        return "locked";
    }

    const status = getQuestionStatus(question.id);

    if (status === "correct") {
        return "correct";
    }
    if (status === "wrong") {
        return "wrong";
    }
    return "unlocked";
}

function renderQuestionNav() {
    const nav = document.getElementById("questionNav");

    nav.innerHTML = "";

    state.questions.forEach((question, index) => {
        const navState = getNavState(index);
        const button = document.createElement("button");

        button.className = `question-nav-btn is-${navState}`;
        button.innerText = String(index + 1);
        button.dataset.index = String(index);
        button.type = "button";

        if (navState === "locked") {
            button.disabled = true;
        }

        const statusLabelMap = {
            current: "current",
            correct: "correct",
            wrong: "wrong",
            unlocked: "unlocked",
            locked: "locked"
        };
        button.title = `Q${index + 1}: ${statusLabelMap[navState]}`;

        button.addEventListener("click", async () => {
            await moveToQuestionByIndex(index);
        });

        nav.appendChild(button);
    });

    const nextLocked = state.currentQuestionIndex + 1 > state.maxUnlockedIndex;
    document.getElementById("navHelpText").innerText = nextLocked
        ? "Answer to unlock next question"
        : "You can revisit answered questions";
}

function renderResultPanel(questionId) {
    const resultArea = document.getElementById("resultArea");
    const result = state.questionResults[questionId];

    if (!result) {
        resultArea.style.display = "none";
        document.getElementById("inputData").innerText = "";
        document.getElementById("actualOutput").innerText = "";
        document.getElementById("expectedOutput").innerText = "";
        document.getElementById("explanation").innerText = "";
        document.getElementById("modelAnswers").innerText = "";
        document.getElementById("inputDataBlock").style.display = "none";
        resetVerdictBanner();
        return;
    }

    resultArea.style.display = "block";

    // Display input_data if available
    const inputDataBlock = document.getElementById("inputDataBlock");
    if (result.input_data && result.input_data.trim()) {
        inputDataBlock.style.display = "block";
        document.getElementById("inputData").innerText = result.input_data;
    } else {
        inputDataBlock.style.display = "none";
        document.getElementById("inputData").innerText = "";
    }

    document.getElementById("actualOutput").innerText = result.actual_output || "(no output)";
    document.getElementById("expectedOutput").innerText = result.expected_output || "(no fixed expected output)";
    document.getElementById("explanation").innerText = result.explanation || "(no explanation)";
    document.getElementById("modelAnswers").innerText = (result.model_answers || []).join("\n\n") || "(no model answer)";
    setVerdictBanner(result);
}

function refreshQuestionView() {
    resetTransientUIState();

    const question = getCurrentQuestion();

    if (!question) {
        return;
    }

    const starterCodeArea = document.getElementById("starterCodeArea");
    const starterCode = document.getElementById("starterCode");
    const endingCodeArea = document.getElementById("endingCodeArea");
    const endingCode = document.getElementById("endingCode");
    const answerCode = document.getElementById("answerCode");

    document.getElementById("questionInfo").innerText =
        `chapter ${question.chapter} / ${question.category} / difficulty ${question.difficulty}`;
    document.getElementById("questionText").innerText = question.question;

    if (question.starter_code) {
        starterCodeArea.style.display = "block";
        starterCode.innerText = question.starter_code;
    } else {
        starterCodeArea.style.display = "none";
        starterCode.innerText = "";
    }

    if (question.ending_code) {
        endingCodeArea.style.display = "block";
        endingCode.innerText = question.ending_code;
    } else {
        endingCodeArea.style.display = "none";
        endingCode.innerText = "";
    }

    const savedResult = state.questionResults[question.id];
    const initialCode = question.starter_code || "";

    answerCode.value = savedResult?.submitted_code ?? initialCode;

    const answered = getQuestionStatus(question.id) !== "unanswered";
    answerCode.disabled = answered;
    setSubmitButtonSubmittingState(false);
    document.getElementById("submitButton").disabled = answered;

    const nextButton = document.getElementById("nextButton");
    if (answered) {
        nextButton.style.display = "inline-flex";
        nextButton.disabled = false;
    } else {
        nextButton.style.display = "none";
    }

    setMessage("message", "");
    renderResultPanel(question.id);
    updateEditorLineNumbers();
    syncProgressUI();
    renderQuestionNav();
}

async function moveToQuestionByIndex(nextIndex) {
    if (nextIndex === state.currentQuestionIndex) {
        return;
    }

    if (!isCurrentQuestionAnswered()) {
        setMessage("message", "Current question must be submitted first");
        return;
    }

    if (nextIndex > state.maxUnlockedIndex) {
        setMessage("message", "Future questions are locked");
        return;
    }

    state.currentQuestionIndex = nextIndex;
    refreshQuestionView();
    await saveCurrentStudySession();
}

async function handleSubmitAnswer() {
    if (state.isSubmitting) {
        return;
    }

    const question = getCurrentQuestion();

    if (!question) {
        return;
    }

    if (getQuestionStatus(question.id) !== "unanswered") {
        setMessage("message", "Already judged", "success");
        return;
    }

    const userCode = document.getElementById("answerCode").value;
    const isEmptyAnswer = !userCode.trim();

    setMessage("message", "");
    state.isSubmitting = true;
    setSubmitButtonSubmittingState(true);

    try {
        const result = await submitAnswer(question.id, userCode);

        if (!result.ok) {
            setMessage("message", result.data.message || "Submit failed");
            return;
        }

        const isCorrect = !!result.data.is_correct;

        state.questionStatuses[question.id] = isCorrect ? "correct" : "wrong";
        state.answeredQuestionIds.add(question.id);

        state.questionResults[question.id] = {
            is_correct: isCorrect,
            result_message: result.data.message || "",
            submitted_code: userCode,
            input_data: String(result.data.input_data || ""),
            actual_output: result.data.actual_output || "",
            explanation: result.data.explanation || "",
            model_answers: result.data.model_answers || [],
            expected_output: String(result.data.expected_output || "")
        };

        if (isCorrect) {
            state.currentStreak += 1;
            state.maxStreak = Math.max(state.maxStreak, state.currentStreak);
            setMessage("message", "Correct", "success");
        } else {
            state.currentStreak = 0;
            if (isEmptyAnswer) {
                setMessage("message", "Empty answer is treated as wrong");
            } else {
                setMessage("message", `Wrong: ${result.data.message || ""}`.trim());
            }
        }

        if (state.currentQuestionIndex + 1 > state.maxUnlockedIndex) {
            state.maxUnlockedIndex = Math.min(state.currentQuestionIndex + 1, state.questions.length - 1);
        }

        document.getElementById("answerCode").disabled = true;
        document.getElementById("submitButton").disabled = true;
        document.getElementById("nextButton").style.display = "inline-flex";

        triggerQuestionFeedback(isCorrect);
        renderResultPanel(question.id);
        syncProgressUI();
        renderQuestionNav();
        persistRuntimeState();
    } catch (error) {
        setMessage("message", "Network error");
    } finally {
        state.isSubmitting = false;
        const submitButton = document.getElementById("submitButton");
        submitButton.innerText = "回答する";
        submitButton.disabled = getQuestionStatus(question.id) !== "unanswered";
    }

    await saveCurrentStudySession();
}

async function nextQuestion() {
    if (!isCurrentQuestionAnswered()) {
        setMessage("message", "Submit first");
        return;
    }

    const nextIndex = state.currentQuestionIndex + 1;

    if (nextIndex >= state.questions.length) {
        showFinishView();
        await clearCurrentStudySession();
        clearRuntimeState();
        return;
    }

    state.currentQuestionIndex = nextIndex;
    refreshQuestionView();
    persistRuntimeState();
    await saveCurrentStudySession();
}

function showFinishView() {
    resetTransientUIState();

    const total = state.questions.length;
    const correctCount = getCorrectCount();
    const wrongCount = getWrongCount();
    const answeredCount = getAnsweredCount();
    const accuracy = answeredCount > 0
        ? Math.round((correctCount / answeredCount) * 100)
        : 0;

    document.getElementById("studyArea").style.display = "none";
    document.getElementById("finishArea").style.display = "grid";
    document.getElementById("finishResult").innerText = `${total} questions / ${correctCount} correct`;
    document.getElementById("finishAccuracy").innerText = `${accuracy}%`;
    document.getElementById("finishCorrect").innerText = String(correctCount);
    document.getElementById("finishWrong").innerText = String(wrongCount);
    document.getElementById("finishStreak").innerText = String(state.maxStreak);
    document.getElementById("finishReview").innerText = String(wrongCount);
    document.getElementById("finishRank").innerText = calculateRank(accuracy, wrongCount);
}

function resetStateWithQuestions(questions) {
    state.questions = questions;
    state.currentQuestionIndex = 0;
    state.maxUnlockedIndex = 0;
    state.answeredQuestionIds = new Set();
    state.questionResults = {};
    state.questionStatuses = {};
    state.currentStreak = 0;
    state.maxStreak = 0;

    state.questions.forEach((question) => {
        state.questionStatuses[question.id] = "unanswered";
    });
}

async function loadStudyQuestion() {
    if (!requireLogin()) {
        return;
    }

    clearLegacyRuntimeState();

    document.getElementById("settingArea").style.display = "block";
    document.getElementById("studyArea").style.display = "none";
    document.getElementById("finishArea").style.display = "none";
    setSetupMessage("");

    initializeSetupUI();
    await loadLatestSessionOption();
}

async function loadLatestSessionOption() {
    const resumeArea = document.getElementById("resumeArea");
    const resumeSummary = document.getElementById("resumeSummary");

    resumeArea.style.display = "none";
    resumeSummary.innerText = "";
    state.latestSession = null;

    try {
        const result = await fetchLatestStudySession();

        if (!result.ok || !result.data.session) {
            return;
        }

        const latestSession = result.data.session;
        const hasSnapshot = Array.isArray(latestSession.question_snapshot) && latestSession.question_snapshot.length > 0;

        if (!hasSnapshot) {
            await clearCurrentStudySession();
            setSetupMessage("前回の学習データが古いため再開できません。新しく開始してください。");
            return;
        }

        state.latestSession = latestSession;
        resumeArea.style.display = "block";

        const totalQuestions = Array.isArray(state.latestSession.question_ids)
            ? state.latestSession.question_ids.length
            : 0;

        const currentProgress = Math.min(Number(state.latestSession.current_question_index || 0) + 1, totalQuestions);

        resumeSummary.innerText =
            `Saved: chapter ${state.latestSession.chapter} / ${state.latestSession.mode} / ` +
            `${currentProgress} / ${totalQuestions} / correct ${state.latestSession.correct_count}`;
    } catch (error) {
        // Keep normal start.
    }
}

function initializeSetupUI() {
    syncModeCards();
    syncReviewCard();
}

async function startStudy() {
    document.getElementById("settingArea").style.display = "none";
    document.getElementById("studyArea").style.display = "block";
    document.getElementById("finishArea").style.display = "none";

    const initialized = await initializeQuestionsBySelection();

    if (!initialized) {
        document.getElementById("settingArea").style.display = "block";
        document.getElementById("studyArea").style.display = "none";
        return;
    }

    refreshQuestionView();
    persistRuntimeState();
    await saveCurrentStudySession();
}

async function initializeQuestionsBySelection() {
    const selectedChapter = document.getElementById("chapterSelect").value;
    const selectedMode = document.getElementById("modeSelect").value;
    const isReviewMode = document.getElementById("reviewMode").checked;

    state.currentChapter = Number(selectedChapter);
    state.currentMode = selectedMode;
    state.currentReviewMode = isReviewMode;

    let chapterQuestions = [];

    try {
        if (isReviewMode) {
            const result = await fetchReviewQuestions();

            if (!result.ok) {
                setMessage("message", "Review fetch failed");
                return false;
            }

            chapterQuestions = (result.data || []).filter((question) => question.chapter === state.currentChapter);
        } else {
            const result = await fetchQuestionsByChapter(selectedChapter, selectedMode);

            if (!result.ok) {
                setMessage("message", "Question fetch failed");
                return false;
            }

            chapterQuestions = result.data || [];
        }
    } catch (error) {
        setMessage("message", "Network error");
        return false;
    }

    const selectedQuestions = selectQuestionsByMode(chapterQuestions, selectedMode);

    if (!selectedQuestions.length) {
        setMessage("message", "No questions for current condition");
        return false;
    }

    resetStateWithQuestions(selectedQuestions);
    return true;
}

function buildStudySessionPayload() {
    return {
        chapter: state.currentChapter,
        mode: state.currentMode,
        review_mode: state.currentReviewMode,
        question_ids: state.questions.map((question) => question.id),
        question_snapshot: buildQuestionSnapshot(),
        current_question_index: state.currentQuestionIndex,
        correct_count: getCorrectCount(),
        answered_question_ids: Array.from(state.answeredQuestionIds)
    };
}

async function saveCurrentStudySession(options = {}) {
    const { silent = true } = options;

    if (!state.questions.length || state.currentChapter === null) {
        return {
            ok: false,
            message: "学習データがないため保存できません。"
        };
    }

    try {
        const result = await saveStudySession(buildStudySessionPayload());

        if (!result.ok) {
            const message = result.data?.message || "学習状態の保存に失敗しました。";

            if (!silent) {
                setMessage("message", message);
            }

            return {
                ok: false,
                message: message
            };
        }

        persistRuntimeState();

        return {
            ok: true,
            message: ""
        };
    } catch (error) {
        const message = "学習状態の保存中に通信エラーが発生しました。";

        if (!silent) {
            setMessage("message", message);
        }

        return {
            ok: false,
            message: message
        };
    }
}

async function clearCurrentStudySession() {
    try {
        await deleteStudySession();
    } catch (error) {
        // Ignore delete failure.
    }

    state.latestSession = null;
}

function pauseStudy() {
    document.getElementById("pauseConfirmModal").style.display = "flex";
}

function closePauseModal() {
    document.getElementById("pauseConfirmModal").style.display = "none";
}

async function saveAndExit() {
    closePauseModal();
    const saveResult = await saveCurrentStudySession({ silent: false });

    if (!saveResult.ok) {
        setMessage("message", saveResult.message || "保存に失敗しました。再試行してください。");
        return;
    }

    window.location.href = "index.html";
}

async function exitWithoutSave() {
    clearRuntimeState();
    await clearCurrentStudySession();
    window.location.href = "index.html";
}

async function resumeStudyFromSession() {
    if (!state.latestSession) {
        return;
    }

    const questionSnapshot = Array.isArray(state.latestSession.question_snapshot)
        ? state.latestSession.question_snapshot.map((question) => normalizeQuestionSnapshot(question))
        : [];

    try {
        if (!questionSnapshot.length) {
            await clearCurrentStudySession();
            state.latestSession = null;
            setSetupMessage("前回の学習データが古いため再開できません。新しく開始してください。");
            await loadLatestSessionOption();
            return;
        }

        state.currentChapter = Number(state.latestSession.chapter);
        state.currentMode = state.latestSession.mode || "recommended";
        state.currentReviewMode = !!state.latestSession.review_mode;

        resetStateWithQuestions(questionSnapshot);

        state.currentQuestionIndex = Number(state.latestSession.current_question_index || 0);
        state.maxUnlockedIndex = Math.max(
            Number(state.latestSession.current_question_index || 0),
            Number((state.latestSession.answered_question_ids || []).length || 0) - 1
        );

        state.answeredQuestionIds = new Set(state.latestSession.answered_question_ids || []);

        state.answeredQuestionIds.forEach((questionId) => {
            state.questionStatuses[questionId] = "unanswered";
        });

        state.currentQuestionIndex = Math.max(0, Math.min(state.currentQuestionIndex, state.questions.length - 1));
        state.maxUnlockedIndex = Math.max(state.currentQuestionIndex, Math.min(state.maxUnlockedIndex, state.questions.length - 1));

        await inferStatusesFromReviewQueue();

        const runtimeState = readRuntimeState();

        if (
            runtimeState
            && runtimeState.chapter === state.currentChapter
            && runtimeState.mode === state.currentMode
            && runtimeState.review_mode === state.currentReviewMode
        ) {
            applyRuntimeState(runtimeState);
        }

        setSetupMessage("");

        document.getElementById("settingArea").style.display = "none";
        document.getElementById("studyArea").style.display = "block";
        document.getElementById("finishArea").style.display = "none";

        document.getElementById("modeSelect").value = state.currentMode;
        document.getElementById("reviewMode").checked = state.currentReviewMode;
        syncModeCards();
        syncReviewCard();

        refreshQuestionView();
        persistRuntimeState();
        await saveCurrentStudySession();
    } catch (error) {
        setSetupMessage("再開処理に失敗しました。新しく開始してください。");
    }
}

function shuffleQuestions(array) {
    const copiedArray = [...array];

    for (let i = copiedArray.length - 1; i > 0; i -= 1) {
        const randomIndex = Math.floor(Math.random() * (i + 1));
        [copiedArray[i], copiedArray[randomIndex]] = [copiedArray[randomIndex], copiedArray[i]];
    }

    return copiedArray;
}

function selectQuestionsByMode(chapterQuestions, mode) {
    const d1 = chapterQuestions.filter((question) => question.difficulty === 1);
    const d2 = chapterQuestions.filter((question) => question.difficulty === 2);
    const d3 = chapterQuestions.filter((question) => question.difficulty === 3);

    if (mode === "recommended") {
        return [
            ...shuffleQuestions(d1).slice(0, 4),
            ...shuffleQuestions(d2).slice(0, 3),
            ...shuffleQuestions(d3).slice(0, 3)
        ];
    }
    if (mode === "easy") {
        return shuffleQuestions(d1).slice(0, 10);
    }
    if (mode === "normal") {
        return shuffleQuestions(d2).slice(0, 10);
    }
    if (mode === "hard") {
        return shuffleQuestions(d3).slice(0, 10);
    }

    return chapterQuestions;
}

function bindSetupEvents() {
    document.querySelectorAll(".mode-card").forEach((card) => {
        card.addEventListener("click", () => {
            document.getElementById("modeSelect").value = card.dataset.mode;
            syncModeCards();
        });
    });

    document.getElementById("modeSelect").addEventListener("change", syncModeCards);
    document.getElementById("reviewMode").addEventListener("change", syncReviewCard);
}

function bindEditorEvents() {
    const textarea = document.getElementById("answerCode");
    const editorShell = document.getElementById("editorShell");

    textarea.addEventListener("input", updateEditorLineNumbers);
    textarea.addEventListener("scroll", updateEditorLineNumbers);
    textarea.addEventListener("focus", () => {
        editorShell.classList.add("is-focus");
    });
    textarea.addEventListener("blur", () => {
        editorShell.classList.remove("is-focus");
    });
}

document.getElementById("homeButton").addEventListener("click", () => {
    window.location.href = "index.html";
});

document.getElementById("dashboardButton").addEventListener("click", () => {
    window.location.href = "dashboard.html";
});

document.getElementById("startStudyButton").addEventListener("click", startStudy);
document.getElementById("resumeStudyButton").addEventListener("click", resumeStudyFromSession);

document.getElementById("startNewStudyButton").addEventListener("click", async () => {
    await clearCurrentStudySession();
    clearRuntimeState();
    await startStudy();
});

document.getElementById("submitButton").addEventListener("click", handleSubmitAnswer);
document.getElementById("nextButton").addEventListener("click", nextQuestion);

document.getElementById("pauseStudyButton").addEventListener("click", pauseStudy);
document.getElementById("saveAndExitButton").addEventListener("click", saveAndExit);
document.getElementById("exitWithoutSaveButton").addEventListener("click", exitWithoutSave);
document.getElementById("cancelPauseButton").addEventListener("click", closePauseModal);

document.getElementById("goDashboardButton").addEventListener("click", () => {
    window.location.href = "dashboard.html";
});

document.getElementById("goHomeButton").addEventListener("click", () => {
    window.location.href = "index.html";
});

document.getElementById("restartButton").addEventListener("click", async () => {
    clearRuntimeState();
    await startStudy();
});

bindSetupEvents();
bindEditorEvents();
loadStudyQuestion();
