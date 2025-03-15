document.addEventListener("DOMContentLoaded", function() {
    fetchHabits(); // Load habits when the page loads
});

function fetchHabits() {
    const searchQuery = document.getElementById("search").value.trim();
    const intervalFilter = document.getElementById("interval").value;
    console.log(intervalFilter)
    if (intervalFilter === "all") {
        var url = `/api/habits?search=${encodeURIComponent(searchQuery)}`;
    }
    else {
        var url = `/api/habits?search=${encodeURIComponent(searchQuery)}&interval=${encodeURIComponent(intervalFilter)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(habits => displayHabits(habits))
        .catch(error => console.error("Error fetching habits:", error));
}

function displayHabits(habits) {
    const tableBody = document.getElementById("habitTableBody");
    tableBody.innerHTML = ""; // Clear previous results

    if (habits.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No habits found</td></tr>";
        return;
    }

    habits.forEach(habit => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${habit.id}</td>
            <td>${habit.name}</td>
            <td>${habit.desc ? habit.desc : "No description"}</td>
            <td>${habit.interval}</td>
            <td>${habit.streak}</td>
        `;
        row.onclick = () => window.location.href = `/habit/${habit.id}`;
        tableBody.appendChild(row);
    });
}