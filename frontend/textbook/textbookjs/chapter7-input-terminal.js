(function () {
	"use strict";

	function escapeHtml(text) {
		return String(text)
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/\"/g, "&quot;")
			.replace(/'/g, "&#39;");
	}

	function decodeSimplePythonString(rawText) {
		return rawText
			.replace(/\\n/g, "\n")
			.replace(/\\t/g, "\t")
			.replace(/\\r/g, "\r")
			.replace(/\\\"/g, "\"")
			.replace(/\\'/g, "'")
			.replace(/\\\\/g, "\\");
	}

	function extractInputPrompts(sourceCode) {
		const prompts = [];
		const inputPattern = /\binput\s*\(([^)]*)\)/g;
		let match = null;

		while ((match = inputPattern.exec(sourceCode)) !== null) {
			const argumentText = (match[1] || "").trim();
			if (!argumentText) {
				prompts.push("input:");
				continue;
			}

			const quotedPrompt = argumentText.match(/^([\"'])([\s\S]*?)\1$/);
			if (!quotedPrompt) {
				prompts.push("input:");
				continue;
			}

			const decodedPrompt = decodeSimplePythonString(quotedPrompt[2]);
			prompts.push(decodedPrompt || "input:");
		}

		return prompts;
	}

	function setLoading(button, isLoading) {
		if (typeof window.setPracticeLoading === "function") {
			window.setPracticeLoading(button, isLoading);
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

	function setupChapter7InteractivePractice() {
		const chapterRoot = document.getElementById("chapterPageRoot");
		if (!chapterRoot || chapterRoot.dataset.chapterId !== "chapter7") {
			return;
		}

		const runButton = chapterRoot.querySelector("[data-practice-action='run']");
		const resetButton = chapterRoot.querySelector("[data-practice-action='reset']");
		const editor = chapterRoot.querySelector("[data-practice-editor]");
		const statusText = chapterRoot.querySelector("[data-practice-status]");
		const terminalWrap = chapterRoot.querySelector("[data-practice-terminal]");
		if (!runButton || !resetButton || !editor || !statusText || !terminalWrap) {
			return;
		}

		terminalWrap.classList.add("chapter7-interactive-terminal");
		terminalWrap.innerHTML = `
			<p class="practice-section-label">Terminal</p>
			<div class="practice-terminal-box chapter7-terminal-box">
				<div class="chapter7-terminal-prompt-row" data-ch7-prompt-row hidden>
					<span class="chapter7-terminal-prompt" data-ch7-prompt-label>input:</span>
					<div class="chapter7-terminal-input-line">
						<span class="chapter7-terminal-cursor">&gt;</span>
						<input type="text" class="chapter7-terminal-live-input" data-ch7-prompt-input autocomplete="off" spellcheck="false">
					</div>
					<button type="button" class="btn-secondary chapter7-terminal-submit" data-ch7-prompt-submit>送信</button>
				</div>
				<div class="practice-terminal-block">
					<p class="practice-terminal-label">[output]</p>
					<pre class="practice-terminal-output"><code data-practice-console></code></pre>
				</div>
			</div>
		`;

		const promptRow = terminalWrap.querySelector("[data-ch7-prompt-row]");
		const promptLabel = terminalWrap.querySelector("[data-ch7-prompt-label]");
		const promptInput = terminalWrap.querySelector("[data-ch7-prompt-input]");
		const promptSubmit = terminalWrap.querySelector("[data-ch7-prompt-submit]");
		const consoleCode = terminalWrap.querySelector("[data-practice-console]");

		const state = {
			sourceCode: "",
			prompts: [],
			answers: [],
			index: 0
		};

		const setTerminalState = (stateClass) => {
			terminalWrap.classList.remove("is-idle", "is-success", "is-error", "is-waiting");
			terminalWrap.classList.add(stateClass);
		};

		const resetTerminal = () => {
			state.sourceCode = "";
			state.prompts = [];
			state.answers = [];
			state.index = 0;
			promptLabel.textContent = "input:";
			promptInput.value = "";
			promptRow.hidden = true;
			consoleCode.textContent = "";
			setTerminalState("is-idle");
		};

		const showOutput = (text) => {
			consoleCode.textContent = text && text.trim() ? text : "(出力なし)";
			setTerminalState("is-success");
			statusText.textContent = "実行が完了しました。";
		};

		const showError = (message) => {
			consoleCode.textContent = `[error]\n${message || "実行時にエラーが発生しました。"}`;
			setTerminalState("is-error");
			statusText.textContent = "エラーが発生しました。コードを見直して再実行してください。";
		};

		const executeWithInputData = async (sourceCode, inputData) => {
			statusText.textContent = "実行中です...";
			setLoading(runButton, true);

			try {
				if (typeof window.requestPracticeExecution !== "function") {
					showError("実行関数が見つかりません。ページを再読み込みしてください。");
					return;
				}

				const response = await window.requestPracticeExecution(sourceCode, inputData);
				if (!response.ok) {
					showError(response.data?.message || "APIリクエストに失敗しました。");
					return;
				}

				if (response.data?.success) {
					showOutput(response.data?.output || "");
					return;
				}

				showError(response.data?.error || "実行時にエラーが発生しました。");
			} catch (error) {
				showError(error?.message || "通信エラーが発生しました。");
			} finally {
				setLoading(runButton, false);
			}
		};

		const moveToNextPrompt = () => {
			if (state.index >= state.prompts.length) {
				promptRow.hidden = true;
				const inputData = state.answers.join("\n");
				executeWithInputData(state.sourceCode, inputData);
				return;
			}

			const currentPrompt = state.prompts[state.index] || "input:";
			promptLabel.textContent = currentPrompt;
			promptInput.value = "";
			promptRow.hidden = false;
			setTerminalState("is-waiting");
			statusText.textContent = "input待ちです。Terminalに値を入力してください。";
			promptInput.focus();
		};

		const submitPromptValue = () => {
			const value = promptInput.value;
			const currentPrompt = state.prompts[state.index] || "input:";
			state.answers.push(value);
			state.index += 1;
			moveToNextPrompt();
		};

		runButton.addEventListener("click", (event) => {
			event.preventDefault();
			event.stopImmediatePropagation();

			resetTerminal();
			const sourceCode = editor.value || "";
			if (!sourceCode.trim()) {
				showError("実行するコードを入力してください。");
				return;
			}

			const prompts = extractInputPrompts(sourceCode);
			if (!prompts.length) {
				executeWithInputData(sourceCode, "");
				return;
			}

			state.sourceCode = sourceCode;
			state.prompts = prompts;
			state.answers = [];
			state.index = 0;
			moveToNextPrompt();
		}, true);

		resetButton.addEventListener("click", (event) => {
			event.preventDefault();
			event.stopImmediatePropagation();

			editor.value = "";
			statusText.textContent = "自由にコードを書いて実行してみましょう。";
			resetTerminal();
		}, true);

		promptSubmit.addEventListener("click", submitPromptValue);
		promptInput.addEventListener("keydown", (event) => {
			if (event.key === "Enter" && !event.shiftKey) {
				event.preventDefault();
				submitPromptValue();
			}
		});
	};

	document.addEventListener("DOMContentLoaded", setupChapter7InteractivePractice);
})();
