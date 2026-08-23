document.addEventListener("DOMContentLoaded", function () {

    const addExerciseButton =
        document.getElementById("add-exercise");

    const exerciseList =
        document.getElementById("exercise-list");

    const totalFormsInput =
        document.querySelector('input[name$="-TOTAL_FORMS"]');


    if (!addExerciseButton || !exerciseList || !totalFormsInput) {
        console.error("Exercise formset elements not found.");
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