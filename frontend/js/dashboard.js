let chapterChartInstance = null;

function formatRelativeTime(isoString) {
    if (!isoString) {
        return "まだ学習履歴がありません";
    }

    const target = new Date(isoString);
    if (Number.isNaN(target.getTime())) {
        return isoString;
    }

    const diffMs = Date.now() - target.getTime();
    const diffMinutes = Math.floor(diffMs / 60000);

    if (diffMinutes < 1) {
        return "たった今";
    }

    if (diffMinutes < 60) {
        return `${diffMinutes}分前`;
    }

    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) {
        return `${diffHours}時間前`;
    }

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) {
        return `${diffDays}日前`;
    }

    return target.toLocaleDateString("ja-JP");
}

function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.innerText = value;
    }
}

function toPercent(correct, total) {
    if (!total) {
        return 0;
    }

    return Math.round((correct / total) * 100);
}

function renderSummary(summary) {
    setText(
        "summary",
        `総回答数 ${summary.total_answers} 件、正解 ${summary.total_correct} 件、現在の正答率 ${summary.accuracy}% です。復習対象は ${summary.review_count} 件で、継続日数は ${summary.current_streak} 日です。`
    );
    setText("totalAnswersValue", summary.total_answers);
    setText("accuracyValue", `${summary.accuracy}%`);
    setText("reviewCountValue", summary.review_count);
    setText("streakValue", `${summary.current_streak}日`);
    setText("recentAccuracyValue", `${summary.recent_accuracy || 0}%`);
    setText("recentWeekValue", summary.recent_week_answers || 0);
    setText("longestStreakValue", `${summary.longest_streak || 0}日`);
    setText("lastActivityValue", formatRelativeTime(summary.last_activity_at));
}

function renderChapterStats(chapter) {
    const chapterList = document.getElementById("chapter");
    chapterList.innerHTML = "";

    const entries = Object.entries(chapter).sort((a, b) => Number(a[0]) - Number(b[0]));
    setText("chapterCoverageValue", `${entries.length} chapter active`);

    if (entries.length === 0) {
        chapterList.innerHTML = '<li class="progress-item"><strong>学習データがまだありません</strong><p class="item-caption">最初の回答が記録されると chapter 別の可視化が始まります。</p></li>';
        return entries;
    }

    entries.forEach(([key, value]) => {
        const percentage = toPercent(value.correct, value.total);
        const item = document.createElement("li");
        item.className = "progress-item";
        item.innerHTML = `
            <div class="progress-item-head">
                <strong>chapter ${key}</strong>
                <span class="chip">${percentage}%</span>
            </div>
            <p class="item-caption">${value.correct} / ${value.total} correct</p>
            <div class="progress-bar"><span style="width: ${percentage}%;"></span></div>
        `;
        chapterList.appendChild(item);
    });

    return entries;
}

function renderDifficultyStats(difficulty) {
    const difficultyList = document.getElementById("difficulty");
    difficultyList.innerHTML = "";

    const entries = Object.entries(difficulty).sort((a, b) => Number(a[0]) - Number(b[0]));

    if (entries.length === 0) {
        difficultyList.innerHTML = '<li class="difficulty-item"><strong>difficulty データなし</strong><p class="item-caption">回答を始めると難易度別の傾向を確認できます。</p></li>';
        return entries;
    }

    entries.forEach(([key, value]) => {
        const percentage = toPercent(value.correct, value.total);
        const item = document.createElement("li");
        item.className = "difficulty-item";
        item.innerHTML = `
            <div class="difficulty-item-head">
                <strong>difficulty ${key}</strong>
                <span class="chip">${percentage}%</span>
            </div>
            <span class="item-meta">${value.correct} / ${value.total} correct</span>
            <p class="item-caption">現在の難易度帯での安定感を示しています。</p>
        `;
        difficultyList.appendChild(item);
    });

    return entries;
}

function renderRecentActivity(summary) {
    const activityList = document.getElementById("recentActivityList");
    activityList.innerHTML = "";

    if (!summary.recent_activity || summary.recent_activity.length === 0) {
        activityList.innerHTML = '<li class="activity-item"><strong>最近の学習はまだありません</strong><p class="item-caption">1問でも回答すると、ここに直近の記録が並びます。</p></li>';
        return;
    }

    summary.recent_activity.forEach((activity) => {
        const item = document.createElement("li");
        item.className = "activity-item";
        item.innerHTML = `
            <div class="activity-item-head">
                <strong>chapter ${activity.chapter} / difficulty ${activity.difficulty}</strong>
                <span class="activity-status ${activity.is_correct ? "is-correct" : "is-wrong"}">${activity.is_correct ? "Correct" : "Retry"}</span>
            </div>
            <span class="activity-meta">${formatRelativeTime(activity.answered_at)}</span>
            <p class="item-caption">question id: ${activity.question_id}</p>
        `;
        activityList.appendChild(item);
    });
}

function renderInsights(summary, chapterEntries, difficultyEntries) {
    if (chapterEntries.length > 0) {
        const weakestChapter = [...chapterEntries].sort((a, b) => {
            const aRate = toPercent(a[1].correct, a[1].total);
            const bRate = toPercent(b[1].correct, b[1].total);
            return aRate - bRate;
        })[0];

        setText(
            "focusInsight",
            `chapter ${weakestChapter[0]} を優先すると改善余地が大きいです。現在 ${weakestChapter[1].correct} / ${weakestChapter[1].total} correct です。`
        );
    } else {
        setText("focusInsight", "まずは1問回答して、弱点分析の基準を作ってください。");
    }

    if (summary.review_count > 0) {
        setText("reviewInsight", `復習キューが ${summary.review_count} 件あります。新規学習の前に復習を混ぜると定着しやすいです。`);
    } else {
        setText("reviewInsight", "復習キューは空です。新しい chapter に進む準備ができています。");
    }

    if (difficultyEntries.length > 0) {
        const highestDifficulty = difficultyEntries[difficultyEntries.length - 1];
        setText(
            "rhythmInsight",
            `直近7日で ${summary.recent_week_answers || 0} 回回答しています。difficulty ${highestDifficulty[0]} に触れる頻度も徐々に増やせます。`
        );
    } else {
        setText("rhythmInsight", "学習リズムはまだ計測前です。まずは短い演習から始めてください。");
    }
}

function renderChart(chapterEntries) {
    const ctx = document.getElementById("chapterChart");

    if (chapterChartInstance) {
        chapterChartInstance.destroy();
    }

    chapterChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: chapterEntries.map(([chapter]) => `chapter ${chapter}`),
            datasets: [
                {
                    label: "正解数",
                    data: chapterEntries.map(([, value]) => value.correct),
                    borderRadius: 999,
                    backgroundColor: [
                        "rgba(76, 201, 255, 0.86)",
                        "rgba(123, 97, 255, 0.8)",
                        "rgba(38, 208, 168, 0.82)",
                        "rgba(255, 179, 71, 0.8)"
                    ]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "#dbe6ff"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#a8b5d5"
                    },
                    grid: {
                        color: "rgba(168, 181, 213, 0.08)"
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#a8b5d5",
                        precision: 0
                    },
                    grid: {
                        color: "rgba(168, 181, 213, 0.08)"
                    }
                }
            }
        }
    });
}

async function loadData() {
    if (!requireLogin()) {
        return;
    }

    setText("usernameDisplay", "ログイン情報を取得中...");

    try {
        const meResult = await fetchMe();

        if (meResult.ok) {
            setText("usernameDisplay", `${meResult.data.display_name || meResult.data.username} としてログイン中`);
        } else {
            setText("usernameDisplay", "ログイン中");
        }

        const summaryResult = await fetchProgressSummary();
        const chapterResult = await fetchChapterStats();
        const difficultyResult = await fetchDifficultyStats();

        if (!summaryResult.ok || !chapterResult.ok || !difficultyResult.ok) {
            setMessage("dashboardMessage", "進捗データの取得に失敗しました。");
            setMessage("summary", "進捗データの取得に失敗しました。");
            return;
        }

        const summary = summaryResult.data;
        const chapterEntries = renderChapterStats(chapterResult.data);
        const difficultyEntries = renderDifficultyStats(difficultyResult.data);

        renderSummary(summary);
        renderRecentActivity(summary);
        renderInsights(summary, chapterEntries, difficultyEntries);
        renderChart(chapterEntries);
    } catch (error) {
        setMessage("dashboardMessage", "通信エラーが発生しました。");
        setMessage("summary", "通信エラーが発生しました。");
    }
}


document.getElementById("homeButton").addEventListener("click", () => {
        window.location.href = "index.html";
});

document.getElementById("startStudyButton").addEventListener("click", () => {
        window.location.href = "study.html";
});

loadData();