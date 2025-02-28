document.getElementById('documentType').addEventListener('change', function() {
    const contentDiv = document.getElementById('content');
    const docDescription = document.getElementById('docDescription');
    const downloadBtn = document.getElementById('downloadBtn');

    let pdfFile = '';

    if (this.value) {
        contentDiv.classList.remove('hidden');
        switch (this.value) {
            case 'marriage':
                docDescription.textContent = 'Download the Marriage Certificate template.';
                pdfFile = 'PDFs/marriage.pdf';
                break;
            case 'divorce':
                docDescription.textContent = 'Download the Divorce Certificate template.';
                pdfFile = 'PDFs/divorce.pdf';
                break;
            case 'birth':
                docDescription.textContent = 'Download the Birth Certificate template.';
                pdfFile = 'PDFs/birth.pdf';
                break;
            case 'death':
                docDescription.textContent = 'Download the Death Certificate template.';
                pdfFile = 'PDFs/death.pdf';
                break;
            case 'domicile':
                docDescription.textContent = 'Download the Domicile Certificate template.';
                pdfFile = 'PDFs/domicile.pdf';
                break;
            case 'caste':
                docDescription.textContent = 'Download the Caste Certificate template.';
                pdfFile = 'PDFs/caste.pdf';
                break;
            case 'income':
                docDescription.textContent = 'Download the Income Certificate template.';
                pdfFile = 'PDFs/income.pdf';
                break;
            case 'disability':
                docDescription.textContent = 'Download the Disability Certificate template.';
                pdfFile = 'PDFs/disability.pdf';
                break;
            case 'migration':
                docDescription.textContent = 'Download the Migration Certificate template.';
                pdfFile = 'PDFs/migration.pdf';
                break;
            case 'trade':
                docDescription.textContent = 'Download the Trade License template.';
                pdfFile = 'PDFs/trade.pdf';
                break;
        }

        // Set the correct PDF file for download
        downloadBtn.setAttribute('data-file', pdfFile);
    } else {
        contentDiv.classList.add('hidden');
    }
});

// PDF Download Functionality
document.getElementById('downloadBtn').addEventListener('click', function() {
    const pdfFile = this.getAttribute('data-file');
    if (pdfFile) {
        const link = document.createElement('a');
        link.href = pdfFile;
        link.download = pdfFile;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});

// Dark/Light Mode Toggle
document.getElementById('toggleMode').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');

    const modeIcon = document.getElementById('modeIcon');
    if (document.body.classList.contains('dark-mode')) {
        modeIcon.classList.replace('fa-moon', 'fa-sun'); // Change to Sun icon for Light Mode
    } else {
        modeIcon.classList.replace('fa-sun', 'fa-moon'); // Change back to Moon icon for Dark Mode
    }
});
