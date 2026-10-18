/**
 * app.js - NPTEL PrepMaster AI Interactive Client Logic & Exam Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // ================= APPLICATION STATE =================
  const state = {
    apiKey: localStorage.getItem('nptel_gemini_api_key') || '',
    currentPdfText: '',
    currentFilename: '',
    studyKit: null,
    selectedMcqCount: 10,
    quiz: {
      currentQuestionIndex: 0,
      userAnswers: {}, // { [qId]: [optionIndex, ...] }
      questionStatuses: {}, // { [qId]: 'not_visited' | 'not_answered' | 'answered' | 'marked' | 'answered_marked' }
      isSubmitted: false,
      timerSeconds: 15 * 60,
      timerInterval: null,
      timeTakenSeconds: 0,
      filterMode: 'all', // 'all' | 'mistakes'
      score: 0,
      totalPossibleMarks: 0,
      accuracy: 0
    },
    flashcards: {
      currentIndex: 0,
      isFlipped: false,
      cards: [],
      masteredCount: 0
    },
    chat: {
      messages: []
    }
  };

  // ================= DOM ELEMENTS =================
  // Header & Modals
  const btnThemeToggle = document.getElementById('btnThemeToggle');
  const btnOpenApiKeyModal = document.getElementById('btnOpenApiKeyModal');
  const btnCloseApiKeyModal = document.getElementById('btnCloseApiKeyModal');
  const apiKeyModal = document.getElementById('apiKeyModal');
  const inputApiKey = document.getElementById('inputApiKey');
  const btnSaveApiKey = document.getElementById('btnSaveApiKey');
  const btnClearApiKey = document.getElementById('btnClearApiKey');
  const apiKeyStatusText = document.getElementById('apiKeyStatusText');
  const btnQuickSample = document.getElementById('btnQuickSample');
  const noticeBanner = document.getElementById('noticeBanner');
  const toastContainer = document.getElementById('toastContainer');

  // Upload & Customization
  const dropzone = document.getElementById('dropzone');
  const pdfFileInput = document.getElementById('pdfFileInput');
  const dropzoneContentDefault = document.getElementById('dropzoneContentDefault');
  const dropzoneContentSelected = document.getElementById('dropzoneContentSelected');
  const selectedFileName = document.getElementById('selectedFileName');
  const selectedFileSize = document.getElementById('selectedFileSize');
  const selectedPageCount = document.getElementById('selectedPageCount');
  const selectedWordCount = document.getElementById('selectedWordCount');
  const btnChangeFile = document.getElementById('btnChangeFile');
  const btnGenerateKit = document.getElementById('btnGenerateKit');
  const selectDifficulty = document.getElementById('selectDifficulty');
  const selectFocusMode = document.getElementById('selectFocusMode');
  const mcqCountButtons = document.querySelectorAll('.mcq-count-btn');
  const mcqCountSummaryLabel = document.getElementById('mcqCountSummaryLabel');
  const sampleCourseChips = document.querySelectorAll('.btn-sample-chip');
  const btnLoadLocalSamplePdf = document.getElementById('btnLoadLocalSamplePdf');

  // Progress Stepper
  const generationProgressContainer = document.getElementById('generationProgressContainer');
  const progressStepTitle = document.getElementById('progressStepTitle');
  const progressPercent = document.getElementById('progressPercent');
  const progressBar = document.getElementById('progressBar');
  const progressDetail = document.getElementById('progressDetail');

  // Dashboard & Study Kit
  const studyKitSection = document.getElementById('studyKitSection');
  const studyKitTitle = document.getElementById('studyKitTitle');
  const studyKitOverview = document.getElementById('studyKitOverview');
  const badgeWeekTopic = document.getElementById('badgeWeekTopic');
  const badgeAiMode = document.getElementById('badgeAiMode');
  const statMcqCount = document.getElementById('statMcqCount');
  const statFlashcardCount = document.getElementById('statFlashcardCount');
  const statReadTime = document.getElementById('statReadTime');
  const tabBadgeMcq = document.getElementById('tabBadgeMcq');
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  // Quiz Elements
  const qNumberDisplay = document.getElementById('qNumberDisplay');
  const qTypeBadge = document.getElementById('qTypeBadge');
  const qDiffBadge = document.getElementById('qDiffBadge');
  const qMarksDisplay = document.getElementById('qMarksDisplay');
  const qTextDisplay = document.getElementById('qTextDisplay');
  const qOptionsContainer = document.getElementById('qOptionsContainer');
  const qHintContainer = document.getElementById('qHintContainer');
  const qHintText = document.getElementById('qHintText');
  const btnSaveAndNext = document.getElementById('btnSaveAndNext');
  const btnMarkForReview = document.getElementById('btnMarkForReview');
  const btnClearResponse = document.getElementById('btnClearResponse');
  const btnPrevQuestion = document.getElementById('btnPrevQuestion');
  const btnSubmitExam = document.getElementById('btnSubmitExam');
  const quizTimerDisplay = document.getElementById('quizTimerDisplay');
  const quizModeBadge = document.getElementById('quizModeBadge');
  const paletteButtonsContainer = document.getElementById('paletteButtonsContainer');
  const paletteTotalSummary = document.getElementById('paletteTotalSummary');
  const quizReviewOptions = document.getElementById('quizReviewOptions');
  const filterAllQuestions = document.getElementById('filterAllQuestions');
  const filterWrongQuestions = document.getElementById('filterWrongQuestions');
  const btnRetakeExam = document.getElementById('btnRetakeExam');

  // Results Modal
  const resultsModal = document.getElementById('resultsModal');
  const btnCloseResultsModal = document.getElementById('btnCloseResultsModal');
  const resultTitle = document.getElementById('resultTitle');
  const resultTierText = document.getElementById('resultTierText');
  const resTotalScore = document.getElementById('resTotalScore');
  const resAccuracy = document.getElementById('resAccuracy');
  const resTimeTaken = document.getElementById('resTimeTaken');
  const resultFeedback = document.getElementById('resultFeedback');
  const resultBadgeIcon = document.getElementById('resultBadgeIcon');
  const btnReviewAnswersFromModal = document.getElementById('btnReviewAnswersFromModal');
  const btnRetakeFromModal = document.getElementById('btnRetakeFromModal');

  // Key Points
  const keyPointsList = document.getElementById('keyPointsList');
  const btnCopyKeyPoints = document.getElementById('btnCopyKeyPoints');

  // Explanations
  const explanationsList = document.getElementById('explanationsList');

  // Flashcards
  const flashcardScene = document.getElementById('flashcardScene');
  const flashcardInner = document.getElementById('flashcardInner');
  const fcFrontText = document.getElementById('fcFrontText');
  const fcBackText = document.getElementById('fcBackText');
  const fcFrontTag = document.getElementById('fcFrontTag');
  const fcBackTag = document.getElementById('fcBackTag');
  const currentCardIndex = document.getElementById('currentCardIndex');
  const totalCardsCount = document.getElementById('totalCardsCount');
  const btnFcPrev = document.getElementById('btnFcPrev');
  const btnFcNext = document.getElementById('btnFcNext');
  const btnFcShuffle = document.getElementById('btnFcShuffle');

  // Doubts Chat
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const suggestedDoubtsList = document.getElementById('suggestedDoubtsList');
  const btnClearChat = document.getElementById('btnClearChat');

  // Export
  const btnExportMarkdown = document.getElementById('btnExportMarkdown');
  const btnExportJson = document.getElementById('btnExportJson');

  // ================= TOAST NOTIFICATION SYSTEM =================
  function showToast(msg, type = "info") {
    const toast = document.createElement('div');
    toast.className = 'toast-enter pointer-events-auto flex items-center gap-3 p-4 rounded-2xl glass-card border shadow-xl text-xs sm:text-sm font-semibold max-w-sm transition-all duration-300';
    
    let icon = "fa-circle-info text-blue-500";
    if (type === "success") icon = "fa-circle-check text-emerald-500";
    if (type === "warning") icon = "fa-triangle-exclamation text-amber-500";
    if (type === "error") icon = "fa-circle-exclamation text-rose-500";

    toast.innerHTML = `
      <i class="fa-solid ${icon} text-base shrink-0"></i>
      <span class="flex-1 leading-snug">${msg}</span>
      <button class="text-slate-400 hover:text-slate-600 dark:hover:text-white transition ml-2">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;

    toast.querySelector('button').addEventListener('click', () => {
      toast.classList.replace('toast-enter', 'toast-exit');
      setTimeout(() => toast.remove(), 200);
    });

    toastContainer.appendChild(toast);

    setTimeout(() => {
      if (toast.parentElement) {
        toast.classList.replace('toast-enter', 'toast-exit');
        setTimeout(() => toast.remove(), 200);
      }
    }, 4000);
  }

  // ================= INITIALIZATION =================
  initTheme();
  updateApiKeyUI();

  btnQuickSample.addEventListener('click', () => {
    loadSampleCourse('cloud_computing');
  });

  fetch('/api/health')
    .then(r => r.json())
    .then(data => {
      if (data.has_env_gemini_key && !state.apiKey) {
        apiKeyStatusText.innerHTML = '<span class="text-emerald-500 font-bold">Gemini Active ✓</span>';
      }
    })
    .catch(() => {});

  // ================= THEME TOGGLE =================
  function initTheme() {
    const savedTheme = localStorage.getItem('nptel_theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  btnThemeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('nptel_theme', isDark ? 'dark' : 'light');
    showToast(isDark ? "Switched to Dark Mode" : "Switched to Light Mode", "info");
  });

  // ================= API KEY MANAGEMENT =================
  function updateApiKeyUI() {
    if (state.apiKey) {
      apiKeyStatusText.innerHTML = '<span class="text-emerald-600 dark:text-emerald-400 font-bold">Gemini Key ✓</span>';
      inputApiKey.value = state.apiKey;
    } else {
      apiKeyStatusText.innerText = 'Gemini Key';
      inputApiKey.value = '';
    }
  }

  btnOpenApiKeyModal.addEventListener('click', () => {
    inputApiKey.value = state.apiKey;
    apiKeyModal.classList.remove('hidden');
  });

  btnCloseApiKeyModal.addEventListener('click', () => {
    apiKeyModal.classList.add('hidden');
  });

  apiKeyModal.addEventListener('click', (e) => {
    if (e.target === apiKeyModal) apiKeyModal.classList.add('hidden');
  });

  btnSaveApiKey.addEventListener('click', () => {
    const key = inputApiKey.value.trim();
    if (key) {
      state.apiKey = key;
      localStorage.setItem('nptel_gemini_api_key', key);
      showToast("Gemini API Key saved! Live AI analysis is now active.", "success");
    }
    updateApiKeyUI();
    apiKeyModal.classList.add('hidden');
  });

  btnClearApiKey.addEventListener('click', () => {
    state.apiKey = '';
    localStorage.removeItem('nptel_gemini_api_key');
    updateApiKeyUI();
    apiKeyModal.classList.add('hidden');
    showToast("API Key removed. Switched to smart offline engine.", "info");
  });

  // Dynamic Notice Banner
  function showNotice(msg, type = "info") {
    noticeBanner.classList.remove('hidden', 'bg-emerald-50', 'bg-blue-50', 'bg-amber-50', 'border-emerald-200', 'border-blue-200', 'border-amber-200', 'text-emerald-800', 'text-blue-800', 'text-amber-800', 'dark:bg-emerald-950/60', 'dark:bg-blue-950/60', 'dark:bg-amber-950/60');
    
    let colorClasses = "bg-blue-50/90 border border-blue-200 text-blue-900 dark:bg-blue-950/60 dark:border-blue-800 dark:text-blue-200";
    let icon = "fa-circle-info text-blue-600";
    
    if (type === "success") {
      colorClasses = "bg-emerald-50/90 border border-emerald-200 text-emerald-900 dark:bg-emerald-950/60 dark:border-emerald-800 dark:text-emerald-200";
      icon = "fa-circle-check text-emerald-600";
    } else if (type === "warning") {
      colorClasses = "bg-amber-50/90 border border-amber-200 text-amber-900 dark:bg-amber-950/60 dark:border-amber-800 dark:text-amber-200";
      icon = "fa-triangle-exclamation text-amber-600";
    }

    noticeBanner.className = `p-4 rounded-2xl text-xs sm:text-sm font-semibold flex items-center justify-between gap-3 shadow-sm ${colorClasses}`;
    noticeBanner.innerHTML = `
      <div class="flex items-center gap-3">
        <i class="fa-solid ${icon} text-base"></i>
        <span>${msg}</span>
      </div>
      <button onclick="document.getElementById('noticeBanner').classList.add('hidden')" class="text-xs opacity-60 hover:opacity-100 p-1">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;
  }

  // ================= MCQ COUNT SELECTOR =================
  mcqCountButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      mcqCountButtons.forEach(b => {
        b.classList.remove('border-2', 'border-blue-600', 'bg-blue-50', 'dark:bg-blue-950/80', 'text-blue-600', 'dark:text-blue-300');
        b.classList.add('border', 'border-slate-200', 'dark:border-slate-700', 'bg-white', 'dark:bg-slate-800');
      });
      btn.classList.remove('border', 'border-slate-200', 'dark:border-slate-700', 'bg-white', 'dark:bg-slate-800');
      btn.classList.add('border-2', 'border-blue-600', 'bg-blue-50', 'dark:bg-blue-950/80', 'text-blue-600', 'dark:text-blue-300');
      
      const count = parseInt(btn.getAttribute('data-mcq-count'), 10);
      state.selectedMcqCount = count;
      if (mcqCountSummaryLabel) mcqCountSummaryLabel.innerText = `${count} Questions`;
    });
  });

  // ================= DRAG & DROP PDF UPLOAD =================
  dropzone.addEventListener('click', () => pdfFileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dropzone-active');
  });

  ['dragleave', 'dragend'].forEach(type => {
    dropzone.addEventListener(type, () => {
      dropzone.classList.remove('dropzone-active');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dropzone-active');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  pdfFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  btnChangeFile.addEventListener('click', (e) => {
    e.stopPropagation();
    pdfFileInput.value = '';
    dropzoneContentSelected.classList.add('hidden');
    dropzoneContentDefault.classList.remove('hidden');
    state.currentPdfText = '';
    state.currentFilename = '';
    showToast("File cleared. Select or drop a new PDF.", "info");
  });

  async function handleFileSelected(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      showToast('Please upload a valid PDF document.', 'warning');
      return;
    }

    selectedFileName.innerText = file.name;
    selectedFileSize.innerText = formatFileSize(file.size);
    selectedPageCount.innerText = 'Extracting pages...';
    selectedWordCount.innerText = 'Analyzing...';

    dropzoneContentDefault.classList.add('hidden');
    dropzoneContentSelected.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to extract text from PDF.');
      }

      state.currentPdfText = data.full_text;
      state.currentFilename = data.filename;
      selectedPageCount.innerText = `${data.total_pages} Pages`;
      selectedWordCount.innerText = `${data.total_words} Words`;

      showToast(`Extracted ${data.total_pages} pages successfully!`, "success");
      showNotice(`"${data.filename}" is loaded and ready. Configure your preferences and click "Generate NPTEL Study Kit".`, "success");
    } catch (err) {
      showToast(`Error: ${err.message}`, "error");
      dropzoneContentSelected.classList.add('hidden');
      dropzoneContentDefault.classList.remove('hidden');
    }
  }

  function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  // ================= LOAD PRELOADED SAMPLE COURSES =================
  sampleCourseChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const courseId = chip.getAttribute('data-course');
      loadSampleCourse(courseId);
    });
  });

  btnLoadLocalSamplePdf.addEventListener('click', async () => {
    showToast("Loading pre-generated sample NPTEL lecture PDF...", "info");
    loadSampleCourse('cloud_computing');
  });

  async function loadSampleCourse(courseId) {
    try {
      showProgressBar(true);
      updateProgressStep(1, "Loading NPTEL Module Courseware...", 35);

      const res = await fetch(`/api/sample-courses/${courseId}`);
      const json = await res.json();

      setTimeout(() => {
        updateProgressStep(3, "Synthesizing TCS iON Quiz & Flashcards...", 80);
        setTimeout(() => {
          hideProgressBar();
          renderStudyKit(json.data);
          showToast(`Loaded ${json.data.title}!`, "success");
          studyKitSection.scrollIntoView({ behavior: 'smooth' });
        }, 350);
      }, 350);

    } catch (err) {
      hideProgressBar();
      showToast("Failed to load sample course: " + err.message, "error");
    }
  }

  // ================= GENERATE STUDY KIT PIPELINE =================
  btnGenerateKit.addEventListener('click', async () => {
    if (!state.currentPdfText || state.currentPdfText.length < 10) {
      showToast("Please upload a lecture PDF or choose one of the preloaded courses below!", "warning");
      return;
    }

    try {
      showProgressBar(true);
      updateProgressStep(1, "Parsing pages, formulas, and structural headings...", 25);

      const payload = {
        text: state.currentPdfText,
        filename: state.currentFilename || "lecture.pdf",
        num_mcqs: state.selectedMcqCount,
        difficulty: selectDifficulty.value,
        focus_mode: selectFocusMode.value,
        api_key: state.apiKey || undefined
      };

      const stepTimer1 = setTimeout(() => {
        updateProgressStep(2, "Formulating NPTEL assignment-style MCQs & MSQs...", 50);
      }, 1400);

      const stepTimer2 = setTimeout(() => {
        updateProgressStep(3, "Synthesizing deep conceptual breakdowns & analogies...", 75);
      }, 3000);

      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Generation failed.');
      }

      updateProgressStep(4, "Finalizing TCS iON exam simulation...", 100);
      setTimeout(() => {
        hideProgressBar();
        renderStudyKit(data.data);
        if (data.data.fallback_notice) {
          showNotice(data.data.fallback_notice, data.data.ai_mode === 'live_gemini' ? "success" : "warning");
        }
        showToast("NPTEL Study Kit generated successfully!", "success");
        studyKitSection.scrollIntoView({ behavior: 'smooth' });
      }, 350);

    } catch (err) {
      hideProgressBar();
      showToast(`Generation failed: ${err.message}`, "error");
    }
  });

  function showProgressBar(show) {
    if (show) {
      generationProgressContainer.classList.remove('hidden');
      btnGenerateKit.disabled = true;
      btnGenerateKit.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
      generationProgressContainer.classList.add('hidden');
      btnGenerateKit.disabled = false;
      btnGenerateKit.classList.remove('opacity-50', 'cursor-not-allowed');
    }
  }

  function hideProgressBar() {
    showProgressBar(false);
  }

  function updateProgressStep(step, text, percent) {
    progressStepTitle.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i> <span>${text}</span>`;
    progressPercent.innerText = `${percent}%`;
    progressBar.style.width = `${percent}%`;
  }

  // ================= RENDER COMPLETE STUDY KIT =================
  function renderStudyKit(data) {
    state.studyKit = data;
    studyKitSection.classList.remove('hidden');

    studyKitTitle.innerText = data.title || "NPTEL Lecture Module";
    studyKitOverview.innerText = data.overview || "Comprehensive NPTEL study kit.";
    badgeWeekTopic.innerText = data.week_or_topic || data.week || "NPTEL Certified";
    
    if (data.ai_mode === 'live_gemini') {
      badgeAiMode.innerText = `Gemini 2.5 Flash (${data.model_used || 'Live AI'})`;
      badgeAiMode.className = "px-3 py-1 text-xs font-bold rounded-lg bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800";
    } else {
      badgeAiMode.innerText = "Smart NPTEL Engine (Offline Mode)";
      badgeAiMode.className = "px-3 py-1 text-xs font-bold rounded-lg bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800";
    }

    const mcqs = data.mcqs || [];
    statMcqCount.innerText = mcqs.length;
    tabBadgeMcq.innerText = mcqs.length;
    
    const flashcards = data.flashcards || [];
    statFlashcardCount.innerText = flashcards.length;
    statReadTime.innerText = `${Math.max(10, Math.round(mcqs.length * 1.5))}m`;

    initQuiz(mcqs);
    renderKeyPoints(data.key_points || []);
    renderExplanations(data.conceptual_explanations || []);
    initFlashcards(flashcards);
    initDoubts(data.sample_doubts || []);

    setTimeout(renderMath, 150);
  }

  function renderMath() {
    if (window.renderMathInElement) {
      renderMathInElement(studyKitSection, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false
      });
    }
  }

  // ================= TABS SWITCHING =================
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabButtons.forEach(b => {
        b.classList.remove('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400', 'font-bold');
        b.classList.add('border-transparent', 'text-slate-600', 'dark:text-slate-400', 'font-semibold');
      });
      btn.classList.add('active', 'border-blue-600', 'text-blue-600', 'dark:text-blue-400', 'font-bold');
      btn.classList.remove('border-transparent', 'text-slate-600', 'dark:text-slate-400', 'font-semibold');

      tabContents.forEach(c => c.classList.add('hidden'));
      const activeContent = document.getElementById(`tabContent_${targetTab}`);
      if (activeContent) {
        activeContent.classList.remove('hidden');
        renderMath();
      }
    });
  });

  // ================= QUIZ & NPTEL EXAM SIMULATOR =================
  function initQuiz(mcqs) {
    state.quiz.currentQuestionIndex = 0;
    state.quiz.userAnswers = {};
    state.quiz.questionStatuses = {};
    state.quiz.isSubmitted = false;
    state.quiz.filterMode = 'all';
    state.quiz.timeTakenSeconds = 0;

    mcqs.forEach((q, idx) => {
      state.quiz.questionStatuses[q.id] = idx === 0 ? 'not_answered' : 'not_visited';
      state.quiz.userAnswers[q.id] = [];
    });

    quizModeBadge.innerText = "Timed Proctored Exam Active";
    quizModeBadge.className = "text-[11px] font-semibold text-amber-600 dark:text-amber-400";
    btnSubmitExam.classList.remove('hidden');
    quizReviewOptions.classList.add('hidden');
    qHintContainer.classList.add('hidden');

    clearInterval(state.quiz.timerInterval);
    state.quiz.timerSeconds = Math.max(5, mcqs.length) * 90;
    startTimer();

    renderPalette();
    renderCurrentQuestion();
  }

  function startTimer() {
    updateTimerDisplay();
    state.quiz.timerInterval = setInterval(() => {
      state.quiz.timerSeconds--;
      state.quiz.timeTakenSeconds++;
      updateTimerDisplay();

      if (state.quiz.timerSeconds === 120) {
        showToast("⚠️ 2 minutes remaining! Review your answers.", "warning");
      }

      if (state.quiz.timerSeconds <= 0) {
        clearInterval(state.quiz.timerInterval);
        showToast("Time's up! Automatically submitting your exam...", "info");
        submitExam();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(state.quiz.timerSeconds / 60);
    const secs = state.quiz.timerSeconds % 60;
    quizTimerDisplay.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function renderPalette() {
    paletteButtonsContainer.innerHTML = '';
    const mcqs = state.studyKit.mcqs || [];
    let answeredCount = 0;

    mcqs.forEach((q, idx) => {
      const status = state.quiz.questionStatuses[q.id] || 'not_visited';
      const isCurrent = idx === state.quiz.currentQuestionIndex;

      // Filter in review mode
      if (state.quiz.isSubmitted && state.quiz.filterMode === 'mistakes') {
        const userAns = (state.quiz.userAnswers[q.id] || []).slice().sort();
        const trueAns = (q.correct_answers || []).slice().sort();
        const isCorrect = userAns.length === trueAns.length && userAns.every((val, i) => val === trueAns[i]);
        if (isCorrect) return; // skip correct questions when filtering mistakes
      }

      const btn = document.createElement('button');
      btn.className = `palette-btn w-9 h-9 sm:w-10 sm:h-10 rounded-xl font-heading font-black text-xs sm:text-sm flex items-center justify-center border transition-all ${isCurrent ? 'palette-current ring-2 ring-blue-500 scale-105' : ''}`;
      btn.innerText = idx + 1;

      if (status === 'answered') {
        btn.classList.add('palette-answered');
        answeredCount++;
      } else if (status === 'marked') {
        btn.classList.add('palette-marked');
      } else if (status === 'answered_marked') {
        btn.classList.add('palette-answered-marked');
        answeredCount++;
      } else if (status === 'not_answered') {
        btn.classList.add('palette-not-answered');
      } else {
        btn.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300', 'border-slate-300', 'dark:border-slate-700');
      }

      btn.addEventListener('click', () => {
        saveCurrentQuestionStatus(false);
        state.quiz.currentQuestionIndex = idx;
        if (state.quiz.questionStatuses[q.id] === 'not_visited') {
          state.quiz.questionStatuses[q.id] = 'not_answered';
        }
        renderCurrentQuestion();
        renderPalette();
      });

      paletteButtonsContainer.appendChild(btn);
    });

    paletteTotalSummary.innerText = `${answeredCount} of ${mcqs.length} Answered`;
  }

  function renderCurrentQuestion() {
    const mcqs = state.studyKit.mcqs || [];
    if (mcqs.length === 0) return;

    const q = mcqs[state.quiz.currentQuestionIndex];
    if (!q) return;

    qNumberDisplay.innerText = `Question ${state.quiz.currentQuestionIndex + 1} of ${mcqs.length}`;
    qTypeBadge.innerText = q.type === 'multiple' ? 'Multiple Correct (MSQ)' : 'Single Choice (MCQ)';
    qDiffBadge.innerText = q.difficulty || 'Medium';
    qMarksDisplay.innerText = q.type === 'multiple' ? '+2.0 / -0.0 Marks' : '+1.0 / -0.0 Marks';
    qTextDisplay.innerHTML = q.question;

    if (q.hint && (state.quiz.isSubmitted || selectFocusMode.value === "Rapid Revision")) {
      qHintContainer.classList.remove('hidden');
      qHintText.innerHTML = q.hint;
    } else {
      qHintContainer.classList.add('hidden');
    }

    qOptionsContainer.innerHTML = '';
    const selectedAnswers = state.quiz.userAnswers[q.id] || [];
    const optionLetters = ['A', 'B', 'C', 'D', 'E', 'F'];

    q.options.forEach((optText, optIdx) => {
      const isSelected = selectedAnswers.includes(optIdx);
      const isCorrect = (q.correct_answers || []).includes(optIdx);
      const letter = optionLetters[optIdx] || `${optIdx + 1}`;

      const optDiv = document.createElement('div');
      optDiv.className = `option-card p-4 rounded-2xl border text-xs sm:text-sm font-medium transition-all cursor-pointer flex items-center gap-3 select-none`;

      if (state.quiz.isSubmitted) {
        if (isCorrect) {
          optDiv.className += ' bg-emerald-50 dark:bg-emerald-950/70 border-emerald-500 text-emerald-900 dark:text-emerald-100 shadow-sm';
        } else if (isSelected && !isCorrect) {
          optDiv.className += ' bg-rose-50 dark:bg-rose-950/70 border-rose-500 text-rose-900 dark:text-rose-100 shadow-sm';
        } else {
          optDiv.className += ' bg-white/40 dark:bg-slate-900/40 border-slate-200 dark:border-slate-800 text-slate-400 opacity-60';
        }
      } else {
        if (isSelected) {
          optDiv.className += ' option-selected';
        } else {
          optDiv.className += ' bg-white/80 dark:bg-slate-850/80 border-slate-200 dark:border-slate-700/80 text-slate-800 dark:text-slate-200 hover:border-blue-400 dark:hover:border-blue-500 shadow-sm';
        }
      }

      let badgeHtml = '';
      if (state.quiz.isSubmitted) {
        if (isCorrect) {
          badgeHtml = '<span class="w-7 h-7 rounded-xl bg-emerald-500 text-white font-bold flex items-center justify-center shrink-0 shadow-sm"><i class="fa-solid fa-check"></i></span>';
        } else if (isSelected) {
          badgeHtml = '<span class="w-7 h-7 rounded-xl bg-rose-500 text-white font-bold flex items-center justify-center shrink-0 shadow-sm"><i class="fa-solid fa-xmark"></i></span>';
        } else {
          badgeHtml = `<span class="w-7 h-7 rounded-xl border border-slate-300 dark:border-slate-600 text-slate-400 font-bold flex items-center justify-center shrink-0 text-xs">${letter}</span>`;
        }
      } else {
        if (isSelected) {
          badgeHtml = `<span class="w-7 h-7 rounded-xl bg-blue-600 text-white font-bold flex items-center justify-center shrink-0 shadow-sm text-xs">${letter}</span>`;
        } else {
          badgeHtml = `<span class="w-7 h-7 rounded-xl border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400 font-bold flex items-center justify-center shrink-0 text-xs">${letter}</span>`;
        }
      }

      optDiv.innerHTML = `
        ${badgeHtml}
        <div class="flex-1 leading-relaxed">${optText}</div>
      `;

      if (!state.quiz.isSubmitted) {
        optDiv.addEventListener('click', () => {
          if (q.type === 'multiple') {
            const foundIdx = selectedAnswers.indexOf(optIdx);
            if (foundIdx > -1) {
              selectedAnswers.splice(foundIdx, 1);
            } else {
              selectedAnswers.push(optIdx);
            }
          } else {
            state.quiz.userAnswers[q.id] = [optIdx];
          }
          renderCurrentQuestion();
        });
      }

      qOptionsContainer.appendChild(optDiv);
    });

    if (state.quiz.isSubmitted) {
      const expDiv = document.createElement('div');
      expDiv.className = 'mt-5 p-5 rounded-2xl bg-blue-50/90 dark:bg-blue-950/50 border border-blue-200 dark:border-blue-900 text-xs sm:text-sm text-slate-800 dark:text-slate-200 space-y-2 shadow-sm';
      expDiv.innerHTML = `
        <div class="font-heading font-black text-blue-700 dark:text-blue-300 flex items-center gap-2">
          <i class="fa-solid fa-graduation-cap text-base"></i>
          <span>Official Solution & Explanation:</span>
        </div>
        <p class="leading-relaxed font-normal">${q.explanation || 'Detailed solution.'}</p>
        <div class="text-[11px] text-slate-500 font-semibold pt-1">
          Topic: <span class="text-blue-600 dark:text-blue-400 font-bold">${q.topic_tag || 'Core Concept'}</span>
        </div>
      `;
      qOptionsContainer.appendChild(expDiv);
    }

    btnPrevQuestion.disabled = state.quiz.currentQuestionIndex === 0;
    btnPrevQuestion.classList.toggle('opacity-40', state.quiz.currentQuestionIndex === 0);

    if (state.quiz.currentQuestionIndex === mcqs.length - 1) {
      btnSaveAndNext.innerHTML = state.quiz.isSubmitted ? 'Finish Review' : 'Save & Submit Exam <i class="fa-solid fa-check ml-1.5"></i>';
    } else {
      btnSaveAndNext.innerHTML = 'Save & Next <i class="fa-solid fa-arrow-right ml-1.5"></i>';
    }

    renderMath();
  }

  function saveCurrentQuestionStatus(markForReview = false) {
    const mcqs = state.studyKit.mcqs || [];
    const q = mcqs[state.quiz.currentQuestionIndex];
    if (!q) return;

    const answers = state.quiz.userAnswers[q.id] || [];
    const hasAnswered = answers.length > 0;

    if (markForReview) {
      state.quiz.questionStatuses[q.id] = hasAnswered ? 'answered_marked' : 'marked';
    } else {
      if (hasAnswered) {
        state.quiz.questionStatuses[q.id] = 'answered';
      } else {
        state.quiz.questionStatuses[q.id] = 'not_answered';
      }
    }
  }

  btnSaveAndNext.addEventListener('click', () => {
    saveCurrentQuestionStatus(false);
    const mcqs = state.studyKit.mcqs || [];

    if (state.quiz.currentQuestionIndex < mcqs.length - 1) {
      state.quiz.currentQuestionIndex++;
      const nextQ = mcqs[state.quiz.currentQuestionIndex];
      if (state.quiz.questionStatuses[nextQ.id] === 'not_visited') {
        state.quiz.questionStatuses[nextQ.id] = 'not_answered';
      }
      renderPalette();
      renderCurrentQuestion();
    } else {
      if (!state.quiz.isSubmitted) {
        submitExam();
      }
    }
  });

  btnMarkForReview.addEventListener('click', () => {
    saveCurrentQuestionStatus(true);
    const mcqs = state.studyKit.mcqs || [];

    if (state.quiz.currentQuestionIndex < mcqs.length - 1) {
      state.quiz.currentQuestionIndex++;
      const nextQ = mcqs[state.quiz.currentQuestionIndex];
      if (state.quiz.questionStatuses[nextQ.id] === 'not_visited') {
        state.quiz.questionStatuses[nextQ.id] = 'not_answered';
      }
    }
    showToast("Question marked for review!", "info");
    renderPalette();
    renderCurrentQuestion();
  });

  btnClearResponse.addEventListener('click', () => {
    const mcqs = state.studyKit.mcqs || [];
    const q = mcqs[state.quiz.currentQuestionIndex];
    if (!q) return;

    state.quiz.userAnswers[q.id] = [];
    state.quiz.questionStatuses[q.id] = 'not_answered';
    showToast("Response cleared.", "info");
    renderPalette();
    renderCurrentQuestion();
  });

  btnPrevQuestion.addEventListener('click', () => {
    if (state.quiz.currentQuestionIndex > 0) {
      saveCurrentQuestionStatus(false);
      state.quiz.currentQuestionIndex--;
      renderPalette();
      renderCurrentQuestion();
    }
  });

  btnSubmitExam.addEventListener('click', () => {
    submitExam();
  });

  function submitExam() {
    clearInterval(state.quiz.timerInterval);
    state.quiz.isSubmitted = true;

    const mcqs = state.studyKit.mcqs || [];
    let earnedMarks = 0;
    let totalMarks = 0;

    mcqs.forEach(q => {
      const qMarks = q.type === 'multiple' ? 2 : 1;
      totalMarks += qMarks;

      const userAns = (state.quiz.userAnswers[q.id] || []).slice().sort();
      const trueAns = (q.correct_answers || []).slice().sort();

      const isExact = userAns.length === trueAns.length && userAns.every((val, i) => val === trueAns[i]);
      if (isExact) {
        earnedMarks += qMarks;
      }
    });

    state.quiz.score = earnedMarks;
    state.quiz.totalPossibleMarks = totalMarks;
    const accuracy = Math.round((earnedMarks / (totalMarks || 1)) * 100);
    state.quiz.accuracy = accuracy;

    let tierText = "";
    let feedback = "";
    let badgeColor = "bg-amber-100 text-amber-500";

    if (accuracy >= 90) {
      tierText = "🥇 Elite + Gold Certificate Tier (Top 1-2%)";
      feedback = "Outstanding! You scored in the top tier (>=90%) of NPTEL candidates. You are in prime shape to top the exam!";
      badgeColor = "bg-amber-100 text-amber-500 shadow-amber-500/30";
      triggerConfetti();
    } else if (accuracy >= 75) {
      tierText = "🥈 Elite + Silver Certificate Tier";
      feedback = "Excellent mastery! Scoring >=75% qualifies you for the prestigious Elite + Silver certification badge.";
      badgeColor = "bg-slate-200 text-slate-700 shadow-slate-500/30";
      triggerConfetti();
    } else if (accuracy >= 60) {
      tierText = "🎖️ Elite Certificate Tier";
      feedback = "Good job! You have comfortably crossed the 60% mark to secure the Elite Certificate.";
      badgeColor = "bg-blue-100 text-blue-600";
    } else if (accuracy >= 40) {
      tierText = "📜 Qualified / Successfully Completed Tier";
      feedback = "You passed the NPTEL minimum cutoff (>=40%). Review your mistakes to reach the Elite bracket!";
      badgeColor = "bg-emerald-100 text-emerald-600";
    } else {
      tierText = "⚠️ Needs Focused Revision (<40% Cutoff)";
      feedback = "NPTEL passing criteria requires >=40% in the proctored exam. Review the Key Points and Deep Explanations tabs to reinforce weak topics.";
      badgeColor = "bg-rose-100 text-rose-500";
    }

    resultBadgeIcon.className = `w-20 h-20 mx-auto rounded-3xl flex items-center justify-center text-4xl shadow-lg ${badgeColor}`;
    resultTitle.innerText = `NPTEL Exam Scorecard`;
    resultTierText.innerText = tierText;
    resTotalScore.innerText = `${earnedMarks} / ${totalMarks}`;
    resAccuracy.innerText = `${accuracy}%`;

    const mins = Math.floor(state.quiz.timeTakenSeconds / 60);
    const secs = state.quiz.timeTakenSeconds % 60;
    resTimeTaken.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    resultFeedback.innerText = feedback;

    resultsModal.classList.remove('hidden');

    quizModeBadge.innerText = "Review & Solutions Mode";
    quizModeBadge.className = "text-[11px] font-bold text-emerald-600 dark:text-emerald-400";
    btnSubmitExam.classList.add('hidden');
    quizReviewOptions.classList.remove('hidden');

    renderPalette();
    renderCurrentQuestion();
  }

  function triggerConfetti() {
    if (window.confetti) {
      confetti({
        particleCount: 90,
        spread: 80,
        origin: { y: 0.6 }
      });
    }
  }

  btnCloseResultsModal.addEventListener('click', () => resultsModal.classList.add('hidden'));
  btnReviewAnswersFromModal.addEventListener('click', () => {
    resultsModal.classList.add('hidden');
    state.quiz.currentQuestionIndex = 0;
    renderCurrentQuestion();
    renderPalette();
  });
  btnRetakeFromModal.addEventListener('click', () => {
    resultsModal.classList.add('hidden');
    initQuiz(state.studyKit.mcqs || []);
  });
  btnRetakeExam.addEventListener('click', () => {
    initQuiz(state.studyKit.mcqs || []);
  });

  filterAllQuestions.addEventListener('click', () => {
    state.quiz.filterMode = 'all';
    filterAllQuestions.className = "px-3 py-1.5 text-xs rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 font-bold transition";
    filterWrongQuestions.className = "px-3 py-1.5 text-xs rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-200 transition";
    renderPalette();
  });

  filterWrongQuestions.addEventListener('click', () => {
    state.quiz.filterMode = 'mistakes';
    filterWrongQuestions.className = "px-3 py-1.5 text-xs rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 font-bold transition";
    filterAllQuestions.className = "px-3 py-1.5 text-xs rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-200 transition";
    renderPalette();
  });

  // ================= TAB 2: KEY POINTS & FORMULAS =================
  function renderKeyPoints(points) {
    keyPointsList.innerHTML = '';
    if (points.length === 0) {
      keyPointsList.innerHTML = '<p class="text-xs text-slate-500 italic">No key points generated.</p>';
      return;
    }

    points.forEach((kp, idx) => {
      const card = document.createElement('div');
      card.className = 'glass-card glow-border rounded-2xl p-5 shadow-sm space-y-3 flex flex-col justify-between';

      let categoryColor = 'bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300 border-blue-200 dark:border-blue-800';
      if (kp.category && kp.category.toLowerCase().includes('pitfall')) {
        categoryColor = 'bg-rose-50 text-rose-700 dark:bg-rose-950 dark:text-rose-300 border-rose-200 dark:border-rose-800';
      } else if (kp.category && (kp.category.toLowerCase().includes('formula') || kp.category.toLowerCase().includes('metric'))) {
        categoryColor = 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';
      }

      card.innerHTML = `
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 text-[10px] font-black uppercase rounded-lg border ${categoryColor}">
              ${kp.category || 'Core Concept'}
            </span>
            <label class="flex items-center gap-1.5 text-xs font-semibold text-slate-500 dark:text-slate-400 cursor-pointer select-none">
              <input type="checkbox" class="rounded-md border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500 w-4 h-4 cursor-pointer" id="kpCheck_${idx}">
              <span>Mastered</span>
            </label>
          </div>
          <h4 class="font-heading font-black text-sm text-slate-900 dark:text-white" id="kpTitle_${idx}">${kp.title}</h4>
          <div class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-normal" id="kpContent_${idx}">
            ${kp.content}
          </div>
        </div>
        <div class="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-end">
          <button class="btn-copy-point text-[11px] font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1" data-point-idx="${idx}">
            <i class="fa-regular fa-copy"></i> Copy Formula/Point
          </button>
        </div>
      `;

      const checkbox = card.querySelector(`#kpCheck_${idx}`);
      const titleEl = card.querySelector(`#kpTitle_${idx}`);
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          titleEl.classList.add('line-through', 'text-slate-400');
          showToast(`Mastered "${kp.title.slice(0, 30)}..." 🎯`, "success");
        } else {
          titleEl.classList.remove('line-through', 'text-slate-400');
        }
      });

      card.querySelector('.btn-copy-point').addEventListener('click', () => {
        navigator.clipboard.writeText(`${kp.title}\n${kp.content}`).then(() => {
          showToast("Copied formula to clipboard!", "success");
        });
      });

      keyPointsList.appendChild(card);
    });
  }

  btnCopyKeyPoints.addEventListener('click', () => {
    if (!state.studyKit || !state.studyKit.key_points) return;
    const text = state.studyKit.key_points.map((k, i) => `${i + 1}. [${k.category}] ${k.title}\n   ${k.content}`).join('\n\n');
    navigator.clipboard.writeText(text).then(() => {
      showToast("All formulas & key points copied to clipboard!", "success");
    });
  });

  // ================= TAB 3: DEEP CONCEPT EXPLANATIONS =================
  function renderExplanations(explanations) {
    explanationsList.innerHTML = '';
    if (explanations.length === 0) {
      explanationsList.innerHTML = '<p class="text-xs text-slate-500 italic">No conceptual explanations generated.</p>';
      return;
    }

    explanations.forEach((exp, idx) => {
      const card = document.createElement('div');
      card.className = 'glass-card rounded-3xl p-6 sm:p-7 shadow-sm space-y-4 glow-border';

      card.innerHTML = `
        <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="w-9 h-9 rounded-xl bg-indigo-100 dark:bg-indigo-950 text-indigo-600 flex items-center justify-center font-heading font-black text-sm shadow-sm">
            ${idx + 1}
          </div>
          <h4 class="font-heading font-black text-base text-slate-900 dark:text-white">${exp.topic}</h4>
        </div>

        <div class="p-4 rounded-2xl bg-amber-50/90 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/60 text-xs sm:text-sm text-amber-950 dark:text-amber-200 flex items-start gap-3 shadow-sm">
          <i class="fa-solid fa-lightbulb text-amber-500 text-base mt-0.5 shrink-0"></i>
          <div>
            <span class="font-bold block mb-1">Intuitive Mental Model / Analogy:</span>
            <p class="leading-relaxed font-normal">${exp.analogy || 'Conceptual model'}</p>
          </div>
        </div>

        <div class="space-y-1.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
          <span class="font-bold text-slate-900 dark:text-white block">Technical Breakdown & Equations:</span>
          <div class="prose-nptel">${marked.parse(exp.deep_dive || '')}</div>
        </div>

        <div class="p-3.5 rounded-2xl bg-blue-50/90 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900 text-xs text-blue-950 dark:text-blue-200 flex items-center gap-3">
          <i class="fa-solid fa-triangle-exclamation text-blue-600 dark:text-blue-400 text-base shrink-0"></i>
          <div>
            <span class="font-bold">NPTEL Professor's Exam Warning: </span>
            <span class="font-normal">${exp.key_takeaway || 'Pay attention to units and indices.'}</span>
          </div>
        </div>
      `;

      explanationsList.appendChild(card);
    });
  }

  // ================= TAB 4: FLASHCARDS ENGINE =================
  function initFlashcards(cards) {
    state.flashcards.cards = cards;
    state.flashcards.currentIndex = 0;
    state.flashcards.isFlipped = false;

    totalCardsCount.innerText = cards.length;
    renderCurrentFlashcard();
  }

  function renderCurrentFlashcard() {
    const cards = state.flashcards.cards;
    if (cards.length === 0) {
      fcFrontText.innerText = "No flashcards generated.";
      fcBackText.innerText = "";
      return;
    }

    const card = cards[state.flashcards.currentIndex];
    state.flashcards.isFlipped = false;
    flashcardInner.classList.remove('rotate-y-180');

    currentCardIndex.innerText = state.flashcards.currentIndex + 1;
    fcFrontText.innerText = card.front;
    fcBackText.innerText = card.back;
    fcFrontTag.innerText = card.tag || "NPTEL Concept";
    fcBackTag.innerText = card.tag || "NPTEL Definition";

    renderMath();
  }

  function flipFlashcard() {
    state.flashcards.isFlipped = !state.flashcards.isFlipped;
    flashcardInner.classList.toggle('rotate-y-180', state.flashcards.isFlipped);
  }

  flashcardScene.addEventListener('click', flipFlashcard);

  btnFcNext.addEventListener('click', () => {
    if (state.flashcards.cards.length === 0) return;
    state.flashcards.currentIndex = (state.flashcards.currentIndex + 1) % state.flashcards.cards.length;
    renderCurrentFlashcard();
  });

  btnFcPrev.addEventListener('click', () => {
    if (state.flashcards.cards.length === 0) return;
    state.flashcards.currentIndex = (state.flashcards.currentIndex - 1 + state.flashcards.cards.length) % state.flashcards.cards.length;
    renderCurrentFlashcard();
  });

  btnFcShuffle.addEventListener('click', () => {
    state.flashcards.cards.sort(() => Math.random() - 0.5);
    state.flashcards.currentIndex = 0;
    renderCurrentFlashcard();
    showToast("Flashcards shuffled!", "info");
  });

  window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
      const flashcardTabActive = !document.getElementById('tabContent_flashcards').classList.contains('hidden');
      if (flashcardTabActive) {
        e.preventDefault();
        flipFlashcard();
      }
    }
  });

  // ================= TAB 5: ASK AI DOUBTS (TUTOR) =================
  function initDoubts(sampleDoubts) {
    suggestedDoubtsList.innerHTML = '';
    sampleDoubts.forEach(doubtText => {
      const chip = document.createElement('button');
      chip.className = 'px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-blue-50 dark:hover:bg-blue-950 text-slate-700 dark:text-slate-300 hover:text-blue-600 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition text-left flex items-center gap-2 shadow-sm active:scale-95';
      chip.innerHTML = `<i class="fa-regular fa-comment-dots text-blue-500"></i> <span>${doubtText}</span>`;
      chip.addEventListener('click', () => {
        chatInput.value = doubtText;
        chatForm.dispatchEvent(new Event('submit'));
      });
      suggestedDoubtsList.appendChild(chip);
    });
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const doubt = chatInput.value.trim();
    if (!doubt) return;

    chatInput.value = '';
    appendChatMessage('user', doubt);

    const loadingId = 'aiTyping_' + Date.now();
    appendLoadingMessage(loadingId);

    try {
      const res = await fetch('/api/chat-doubt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          doubt: doubt,
          context_text: state.currentPdfText || state.studyKit.overview || '',
          api_key: state.apiKey || undefined
        })
      });

      const data = await res.json();
      removeLoadingMessage(loadingId);

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to get answer.');
      }

      appendChatMessage('ai', data.answer);
    } catch (err) {
      removeLoadingMessage(loadingId);
      appendChatMessage('ai', `Sorry, an error occurred: ${err.message}. Please check your connection or API key.`);
    }
  });

  function appendChatMessage(sender, text) {
    const isUser = sender === 'user';
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`;

    const icon = isUser 
      ? '<div class="w-8 h-8 rounded-xl bg-slate-700 text-white shrink-0 flex items-center justify-center text-xs shadow-sm"><i class="fa-solid fa-user"></i></div>'
      : '<div class="w-8 h-8 rounded-xl bg-blue-600 text-white shrink-0 flex items-center justify-center text-xs shadow-sm"><i class="fa-solid fa-robot"></i></div>';

    const bubbleColor = isUser
      ? 'bg-blue-600 text-white rounded-tr-none shadow-md shadow-blue-500/25'
      : 'glass-card text-slate-800 dark:text-slate-200 rounded-tl-none';

    msgDiv.innerHTML = `
      ${icon}
      <div class="${bubbleColor} p-4 rounded-2xl text-xs sm:text-sm max-w-2xl leading-relaxed shadow-sm">
        ${isUser ? text : marked.parse(text)}
      </div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    renderMath();
  }

  function appendLoadingMessage(id) {
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = 'flex gap-3';
    msgDiv.innerHTML = `
      <div class="w-8 h-8 rounded-xl bg-blue-600 text-white shrink-0 flex items-center justify-center text-xs shadow-sm">
        <i class="fa-solid fa-robot"></i>
      </div>
      <div class="glass-card p-4 rounded-2xl rounded-tl-none text-xs text-slate-500 flex items-center gap-2">
        <i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i>
        <span>Formulating TA explanation...</span>
      </div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  btnClearChat.addEventListener('click', () => {
    chatMessages.innerHTML = '';
    appendChatMessage('ai', 'Chat history cleared. What topic or derivation can I help you with?');
    showToast("Chat cleared.", "info");
  });

  // ================= TAB 6: EXPORT & DOWNLOAD =================
  btnExportMarkdown.addEventListener('click', () => {
    if (!state.studyKit) return;
    const kit = state.studyKit;

    let md = `# ${kit.title || 'NPTEL Study Kit'}\n\n`;
    md += `*${kit.week_or_topic || 'NPTEL Certification'}*\n\n`;
    md += `## Overview\n${kit.overview || ''}\n\n`;

    md += `## Key Points & Formulas\n`;
    (kit.key_points || []).forEach((kp, i) => {
      md += `### ${i + 1}. [${kp.category}] ${kp.title}\n${kp.content}\n\n`;
    });

    md += `## Conceptual Explanations\n`;
    (kit.conceptual_explanations || []).forEach((exp, i) => {
      md += `### ${i + 1}. ${exp.topic}\n`;
      md += `> **Analogy:** ${exp.analogy}\n\n`;
      md += `${exp.deep_dive}\n\n`;
      md += `**Exam Warning:** ${exp.key_takeaway}\n\n`;
    });

    md += `## NPTEL Practice Question Bank\n`;
    (kit.mcqs || []).forEach((q, i) => {
      md += `### Q${i + 1} (${q.type === 'multiple' ? 'MSQ' : 'MCQ'} - ${q.difficulty})\n`;
      md += `${q.question}\n\n`;
      q.options.forEach(opt => {
        md += `- ${opt}\n`;
      });
      const correctStr = (q.correct_answers || []).map(idx => q.options[idx]).join(', ');
      md += `\n**Correct Answer:** ${correctStr}\n`;
      md += `**Explanation:** ${q.explanation}\n\n`;
    });

    downloadFile(md, `${(kit.title || 'nptel_study_kit').replace(/\s+/g, '_')}.md`, 'text/markdown');
    showToast("Markdown notes downloaded!", "success");
  });

  btnExportJson.addEventListener('click', () => {
    if (!state.studyKit) return;
    const jsonStr = JSON.stringify(state.studyKit, null, 2);
    downloadFile(jsonStr, `${(state.studyKit.title || 'nptel_study_kit').replace(/\s+/g, '_')}.json`, 'application/json');
    showToast("JSON question bank downloaded!", "success");
  });

  function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type: type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

});
