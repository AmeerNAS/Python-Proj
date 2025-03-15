document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ checkboxes.js loaded!");

    let isProcessing = false; // Flag to prevent multiple requests

    document.querySelectorAll(".h_check").forEach((checkbox) => {
        console.log(`Found checkbox with ID: ${checkbox.value}`);

        checkbox.addEventListener("click", async function (event) {
            if (isProcessing) {
                console.warn("🚧 Request already in progress. Ignoring...");
                return;
            }

            isProcessing = true; // Lock new requests
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

                if (result.success) {
                    setTimeout(() => location.reload(), 300); // Slight delay before reload
                }
            } catch (error) {
                console.error("❌ Error updating habit:", error);
            } finally {
                setTimeout(() => { isProcessing = false; }, 500); // Reset flag with delay
            }
        });
    });
});