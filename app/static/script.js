function formatTimestamp(ts) {
    const date = new Date(ts);
    // Custom formatting to match: 1st April 2021 - 9:30 PM UTC
    const options = { day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'UTC' };
    let formatted = date.toLocaleDateString('en-GB', options).replace(',', '');
    return `${formatted} UTC`;
}

async function fetchEvents() {
    try {
        const response = await fetch('/events');
        const events = await response.json();
        const container = document.getElementById('events-container');
        
        if (events.length === 0) {
            container.innerHTML = '<p>No recent activity in the last 15 seconds.</p>';
            return;
        }

        container.innerHTML = ''; // Clear previous

        events.forEach(event => {
            const card = document.createElement('div');
            card.className = 'event-card';
            
            let message = "";
            const author = `<span class="author">${event.author}</span>`;
            const to = `<span class="branch">${event.to_branch}</span>`;
            const from = `<span class="branch">${event.from_branch}</span>`;

            // Formatting logic based on Action Type
            if (event.action === "PUSH") {
                message = `${author} pushed to ${to}`;
            } else if (event.action === "PULL_REQUEST") {
                message = `${author} submitted a pull request from ${from} to ${to}`;
            } else if (event.action === "MERGE") {
                message = `${author} merged branch ${from} to ${to}`;
            }

            card.innerHTML = `
                <div>${message} on ${formatTimestamp(event.timestamp)}</div>
                <div class="timestamp">ID: ${event.request_id}</div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching events:", error);
    }
}

// Initial call
fetchEvents();

// Poll every 15 seconds (15000 milliseconds)
let timeLeft = 15;
const timerElement = document.getElementById('timer');

function updateTimer() {
    timeLeft--;
    
    if (timeLeft <= 0) {
        // When timer hits 0, trigger the fetch and reset to 15
        fetchEvents();
        timeLeft = 15;
    }
    
    timerElement.innerText = timeLeft;
}

// Update the countdown display every 1 second
setInterval(updateTimer, 1000);

// Initial fetch when the page first loads
fetchEvents();