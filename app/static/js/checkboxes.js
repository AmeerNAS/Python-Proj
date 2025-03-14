document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ checkboxes.js loaded!");

    document.querySelectorAll(".h_check").forEach((checkbox) => {
        console.log(`Found checkbox with ID: ${checkbox.value}`);  // Debugging line

        checkbox.addEventListener("change", async function () {
            console.log(`Clicked: Habit ID ${this.value}, Checked: ${this.checked}`);

            try {
                let response = await fetch(`/check/${this.value}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ checked: this.checked }),
                });

                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

                let result = await response.json();
                console.log("✅ Update successful:", result);

                // ✅ Refresh the page after successful update
                if (result.success) {
                    location.reload();
                }
            } catch (error) {
                console.error("❌ Error updating habit:", error);
            }
        });
    });
});