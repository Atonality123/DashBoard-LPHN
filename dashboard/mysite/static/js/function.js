function toggleTheme() {
    const lightThemeLink = document.getElementById('light-theme');
    const darkThemeLink = document.getElementById('dark-theme');
    const modal = document.getElementById('financeModal');
    
    modal.classList.toggle('dark-active');

    lightThemeLink.toggleAttribute('disabled');
    darkThemeLink.toggleAttribute('disabled');

    closeFinanceModal();
}


function redirectToAdmin() {
    var adminUrl = '/admin/';
    window.open(adminUrl, '_blank');
}

function openFinanceModal(id) {
    const modal = document.getElementById('financeModal');
    const projectName = document.getElementById('projectValue');
    const canvas = document.getElementById('pieChart');

    if (canvas.chart) {
        canvas.chart.destroy();
    }

    const cacheBuster = new Date().getTime();
    const url = `/finance_data/${id}/?cache=${cacheBuster}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            projectName.textContent = data.total;

            const ctx = canvas.getContext('2d');
            canvas.chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['เหลือ (บาท)', 'เบิก (บาท)'],
                    datasets: [{
                        data: [data.remain, data.withdraw],
                        backgroundColor: ['#FF6384', '#36A2EB'],
                    }]
                },
                options: {
                    animation: {
                        animateRotate: true,
                        animateScale: true,
                    },
                },
            });

            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching finance data:', error);
        });
}

function closeFinanceModal(){
    const modal = document.getElementById('financeModal');
    modal.style.display = 'none';
}