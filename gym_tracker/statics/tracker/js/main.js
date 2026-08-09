document.addEventListener("DOMContentLoaded", function () {

    const addExerciseButton =
        document.getElementById("add-exercise");

    const exerciseList =
        document.getElementById("exercise-list");


    if (addExerciseButton && exerciseList) {

        addExerciseButton.addEventListener("click", function () {

            const row = document.createElement("div");

            row.className = "exercise-row";

            row.innerHTML = `
                <div class="form-group">
                    <label>Exercise</label>
                    <input
                        type="text"
                        name="exercise[]"
                        placeholder="Bench Press"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Reps</label>
                    <input
                        type="number"
                        name="reps[]"
                        placeholder="10"
                        min="1"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Weight (kg)</label>
                    <input
                        type="number"
                        name="weight[]"
                        placeholder="60"
                        min="0"
                        step="0.5"
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

        });

    }

});


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