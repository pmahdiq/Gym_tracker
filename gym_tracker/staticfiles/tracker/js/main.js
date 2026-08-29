document.addEventListener("DOMContentLoaded", function () {
    initExerciseFormset();
    initSessionTimer();
});


/* =========================
   EXERCISE FORMSET
   (only present on add/update program page)
========================= */

function initExerciseFormset() {
    const addExerciseButton = document.getElementById("add-exercise");
    const exerciseList = document.getElementById("exercise-list");
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');

    if (!addExerciseButton || !exerciseList || !totalFormsInput) {
        return;
    }

    addExerciseButton.addEventListener("click", function () {
        const formIndex = parseInt(totalFormsInput.value, 10);
        
        // Dynamically extract the prefix (e.g., "exercise_set") from the total forms input name
        const prefix = totalFormsInput.name.replace("-TOTAL_FORMS", "");

        const row = document.createElement("div");
        row.className = "exercise-row";

        row.innerHTML = `
            <!-- Hidden ID field required by Django's formset processor -->
            <input 
                type="hidden" 
                name="${prefix}-${formIndex}-id" 
                id="id_${prefix}-${formIndex}-id"
            >

            <div class="form-group">
                <label for="id_${prefix}-${formIndex}-title">
                    Exercise
                </label>
                <input
                    type="text"
                    name="${prefix}-${formIndex}-title"
                    id="id_${prefix}-${formIndex}-title"
                    placeholder="Bench Press"
                    required
                >
            </div>

            <button
                type="button"
                class="remove-exercise"
                onclick="removeExercise(this)"
            >
                ×
            </button>
        `;

        exerciseList.appendChild(row);

        // Update the TOTAL_FORMS count
        totalFormsInput.value = formIndex + 1;
    });
}


function initSessionTimer() {
    const timerEl = document.getElementById("session-timer");
    const timerButton = document.getElementById("timer-button");

    if (!timerEl || !timerButton) {
        return;
    }

    const startedAt = new Date(timerEl.dataset.startedAt);
    let paused = false;
    let pausedElapsed = 0; // seconds accumulated while paused

    function formatTime(totalSeconds) {
        const h = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
        const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
        const s = String(Math.floor(totalSeconds % 60)).padStart(2, "0");
        return `${h}:${m}:${s}`;
    }

    function tick() {
        if (paused) return;
        const now = new Date();
        const elapsedSeconds = Math.floor((now - startedAt) / 1000) - pausedElapsed;
        timerEl.textContent = formatTime(elapsedSeconds);
    }

    let pauseStartedAt = null;

    timerButton.addEventListener("click", function () {
        paused = !paused;

        if (paused) {
            pauseStartedAt = new Date();
            timerButton.textContent = "Resume";
        } else {
            if (pauseStartedAt) {
                pausedElapsed += Math.floor((new Date() - pauseStartedAt) / 1000);
            }
            timerButton.textContent = "Pause";
        }
    });

    tick();
    setInterval(tick, 1000);
}


function removeExercise(button) {

    const row = button.closest(".exercise-row");

    if (row) {
        row.remove();
    }

}


function confirmDelete(button) {

    const confirmed =
        confirm("Are you sure you want to delete this session?");

    if (confirmed) {
        button.closest("form").submit();
    }

}