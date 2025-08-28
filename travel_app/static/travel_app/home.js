document.addEventListener('DOMContentLoaded', function() {
    const filters = document.querySelectorAll('.filter');

    filters.forEach(f => {
        f.addEventListener('change', function() {
            const params = new URLSearchParams({
                type: document.getElementById('type').value,
                source: document.getElementById('source').value,
                destination: document.getElementById('destination').value,
                date: document.getElementById('date').value
            });

            fetch(`?${params.toString()}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').innerHTML = data.html;
            });
        });
    });
});