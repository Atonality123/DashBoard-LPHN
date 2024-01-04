function dowloadForm(form){
    var link1 = "https://drive.google.com/drive/folders/1Zj5OZuio9MrPvoB2w0TxT4IfUgyW1xUS?usp=sharing";
    var link2 = "https://drive.google.com/drive/folders/1lD-fY3vVGeDiFq1-V16cSkwgj4doEv9R?usp=sharing";
    var link3 = "https://drive.google.com/drive/folders/1K6l9LikPZw1K61bVGaboQNQvCwzfxoOv?usp=sharing";

    if(form == 'form1')
        window.open(link1, '_blank'); 
    else if(form == 'form2')
        window.open(link2, '_blank'); 
    else if(form == 'form3')
        window.open(link3, '_blank'); 
}

function loadExel(nameFile){
    var downloadLink = document.createElement('a');
    downloadLink.href = '/download-excel/';
    downloadLink.download = nameFile;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
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