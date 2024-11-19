document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();

    const form = document.getElementById('scrapeForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsBody = document.getElementById('resultsBody');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const urlInput = document.getElementById('urlInput');
        const url = urlInput.value.trim();

        // Reset UI state
        loadingSpinner.classList.remove('d-none');
        errorMessage.classList.add('d-none');
        resultsContainer.classList.add('d-none');
        
        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `url=${encodeURIComponent(url)}`
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch results');
            }

            // Clear previous results
            resultsBody.innerHTML = '';

            // Populate results table
            data.forEach(runner => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${escapeHtml(runner.position)}</td>
                    <td>${escapeHtml(runner.name)}</td>
                    <td>${escapeHtml(runner.time)}</td>
                    <td>${escapeHtml(runner.category)}</td>
                `;
                resultsBody.appendChild(row);
            });

            resultsContainer.classList.remove('d-none');
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('d-none');
        } finally {
            loadingSpinner.classList.add('d-none');
        }
    });
});

// Helper function to escape HTML and prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
