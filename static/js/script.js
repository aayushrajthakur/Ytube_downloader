async function convertVideo() {
    const url = document.getElementById('youtubeUrl').value;
    const format = document.querySelector('input[name="format"]:checked').value;
    const resultDiv = document.getElementById('result');
    
    if (!isValidYoutubeUrl(url)) {
        showError("Please enter a valid YouTube URL");
        return;
    }

    showSuccess("Processing your request...");
    
    try {
        const response = await fetch('/process-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, format })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        // Create download link
        const downloadUrl = `/download-file/${data.filename}`;
        showSuccess(`
            <p>Title: ${data.title}</p>
            <a href="${downloadUrl}" class="download-btn">Download ${format.toUpperCase()}</a>
        `);

    } catch (error) {
        showError("An error occurred during conversion");
    }
}

function isValidYoutubeUrl(url) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return youtubeRegex.test(url);
}

function showSuccess(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result success';
    resultDiv.innerHTML = message;
}

function showError(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result error';
    resultDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
}

// Contact Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            // Here you would typically send this data to your backend
            console.log('Form submitted:', { name, email, subject, message });
            
            // Show success message (you can customize this)
            alert('Thank you for your message! We will get back to you soon.');
            
            // Reset form
            contactForm.reset();
        });
    }
}); 