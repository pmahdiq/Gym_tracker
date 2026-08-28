document.addEventListener("DOMContentLoaded", function () {
    initExerciseFormset();
    initSessionTimer();
});


/* =========================
   EXERCISE FORMSET
   (only present on add/update program page)
========================= */

function initExerciseFormset() {

    const addExerciseButton =
        document.getElementById("add-exercise");

    const exerciseList =
        document.getElementById("exercise-list");

    const totalFormsInput =
        document.querySelector('input[name$="-TOTAL_FORMS"]');


    if (!addExerciseButton || !exerciseList || !totalFormsInput) {
        // Not on the add/update program page — nothing to do here.
        return;
    }


    addExerciseButton.addEventListener("click", function () {

        const formIndex = parseInt(totalFormsInput.value, 10);

        const row = document.createElement("div");

        row.className = "exercise-row";

        row.innerHTML = `
            <div class="form-group">

                <label for="id_form-${formIndex}-title">
                    Exercise
                </label>

                <input
                    type="text"
                    name="form-${formIndex}-title"
                    id="id_form-${formIndex}-title"
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

        totalFormsInput.value = formIndex + 1;

    });

}


/* =========================
   SESSION TIMER
   (only present on the start_session page)
========================= */

function initSessionTimer() {

    const timer = document.getElementById("session-timer");
    const timerButton = document.getElementById("timer-button");

    if (!timer || !timerButton || !timer.dataset.startedAt) {
        // Not on the start_session page — nothing to do here.
        return;
    }

    const startedAt = new Date(timer.dataset.startedAt);

    let running = true;
    let pausedAccumulated = 0;   // milliseconds banked while paused
    let pauseStartedAt = null;

    function formatDuration(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return [hours, minutes, seconds]
            .map(function (n) { return String(n).padStart(2, "0"); })
            .join(":");
    }

    function updateTimer() {
        if (!running) {
            return;
        }

        const elapsedMs = Date.now() - startedAt.getTime() - pausedAccumulated;
        timer.textContent = formatDuration(Math.floor(elapsedMs / 1000));
    }

    setInterval(updateTimer, 1000);
    updateTimer();

    timerButton.addEventListener("click", function () {

        running = !running;

        if (!running) {
            pauseStartedAt = Date.now();
        } else if (pauseStartedAt) {
            pausedAccumulated += Date.now() - pauseStartedAt;
        }

        timerButton.textContent = running ? "Pause" : "Resume";

    });

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