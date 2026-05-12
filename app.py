from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from rag import RAGBot

app = FastAPI()
bot = RAGBot()
bot.read_and_embed_data("data/")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>RAGBot - AI Assistant</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* Custom overrides while maintaining Tailwind */
        body {
            background-color: #000000;
            color: #ffffff;
        }
        
        /* Custom button styling - Green buttons */
        .btn-custom-green {
            background-color: #28a745;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        
        .btn-custom-green:hover {
            background-color: #218838;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .btn-custom-green:active {
            transform: translateY(0);
        }
        
        /* Modal styling for dark theme */
        .modal-content {
            background-color: #1a1a1a;
            color: white;
        }
        
        .modal-header {
            border-bottom-color: #28a745;
        }
        
        .modal-footer {
            border-top-color: #28a745;
        }
        
        .btn-close {
            filter: invert(1);
        }
        
        /* Input field styling */
        .form-control {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #28a745;
        }
        
        .form-control:focus {
            background-color: #2a2a2a;
            color: white;
            border-color: #28a745;
            box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
        }
        
        .form-control::placeholder {
            color: #888888;
        }
        
        /* Responsive container */
        .rag-container {
            min-height: calc(100vh - 160px);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Footer styling */
        footer {
            background-color: #000000;
            border-top: 1px solid #28a745;
        }
        
        .footer-link {
            color: #28a745;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-link:hover {
            color: #ffffff;
            text-decoration: underline;
        }
        
        /* Responsive adjustments */
        @media (max-width: 640px) {
            h1 {
                font-size: 2rem;
            }
            
            .rag-card {
                margin: 1rem;
                padding: 1.5rem;
            }
        }
        
        /* Custom scrollbar for modal */
        .modal-body::-webkit-scrollbar {
            width: 8px;
        }
        
        .modal-body::-webkit-scrollbar-track {
            background: #2a2a2a;
        }
        
        .modal-body::-webkit-scrollbar-thumb {
            background: #28a745;
            border-radius: 4px;
        }
        
        .modal-body::-webkit-scrollbar-thumb:hover {
            background: #218838;
        }
        
        /* Loading animation */
        .loading {
            display: none;
            margin-top: 1rem;
        }
        
        .loading.show {
            display: block;
        }
        
        /* Response container */
        .response-container {
            margin-top: 2rem;
            padding: 1rem;
            background-color: #1a1a1a;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }
    </style>
</head>
<body class="bg-black text-white">
    <!-- Header with Contact Modal Trigger -->
    <nav class="bg-black border-b border-green-700 px-4 py-3">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <i class="fas fa-robot text-green-500 text-2xl"></i>
                <span class="text-xl font-bold">RAGBot</span>
            </div>
            <div>
                <button type="button" class="btn-custom-green px-4 py-2 rounded-lg flex items-center gap-2" data-bs-toggle="modal" data-bs-target="#contactModal">
                    <i class="fas fa-envelope"></i>
                    <span>Contact</span>
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="rag-container container mx-auto px-4 py-8">
        <div class="rag-card w-full max-w-2xl mx-auto">
            <div class="text-center mb-8">
                <i class="fas fa-comments text-green-500 text-5xl mb-4"></i>
                <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-2">RAGBot</h1>
                <p class="text-gray-400 mt-2">Ask me about Ada Lovelace, Jupiter, or CRISPR</p>
            </div>
            
            <form method="post" action="/ask" id="ragForm" class="space-y-4">
                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="flex-1">
                        <input 
                            type="text" 
                            name="question" 
                            id="question"
                            class="form-control w-full px-4 py-3 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                            placeholder="e.g., Who was Ada Lovelace?" 
                            required
                        />
                    </div>
                    <button type="submit" class="btn-custom-green px-6 py-3 rounded-lg flex items-center justify-center gap-2 transition-all">
                        <i class="fas fa-paper-plane"></i>
                        <span>Ask</span>
                    </button>
                </div>
            </form>
            
            <!-- Loading indicator -->
            <div id="loading" class="loading text-center py-4">
                <i class="fas fa-spinner fa-spin text-green-500 text-2xl"></i>
                <p class="mt-2 text-gray-400">Thinking...</p>
            </div>
            
            <!-- Response container -->
            <div id="response" class="response-container hidden">
                <div class="flex items-start gap-3">
                    <i class="fas fa-robot text-green-500 mt-1"></i>
                    <div class="flex-1">
                        <p class="font-semibold mb-2">RAGBot:</p>
                        <p id="answerText" class="text-gray-300"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-black border-t border-green-700 py-6 mt-8">
        <div class="container mx-auto px-4 text-center">
            <p class="text-gray-400">
                Another Website by 
                <a href="https://raiiarcomio.com" target="_blank" rel="noopener noreferrer" class="footer-link font-semibold">
                    Julius Olatokunbo <i class="fas fa-external-link-alt text-xs ml-1"></i>
                </a>
            </p>
            <div class="mt-3">
                <button type="button" class="footer-link text-sm flex items-center justify-center gap-2 mx-auto" data-bs-toggle="modal" data-bs-target="#contactModal">
                    <i class="fas fa-envelope"></i>
                    <span>Contact Us</span>
                </button>
            </div>
        </div>
    </footer>

    <!-- Scrollable Modal for Contact -->
    <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable modal-lg">
            <div class="modal-content">
                <div class="modal-header border-b border-green-700">
                    <h5 class="modal-title text-white" id="contactModalLabel">
                        <i class="fas fa-address-card text-green-500 mr-2"></i>
                        Contact Information
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-0" style="max-height: 70vh;">
                    <iframe 
                        src="https://raiiarcomio.com/contact2" 
                        class="w-100" 
                        style="width: 100%; height: 500px; border: none;"
                        title="Contact Form"
                        loading="lazy"
                    ></iframe>
                </div>
                <div class="modal-footer border-t border-green-700">
                    <button type="button" class="btn-custom-green px-4 py-2 rounded" data-bs-dismiss="modal">
                        <i class="fas fa-times mr-2"></i>
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- JavaScript for handling form submission -->
    <script>
        // Handle form submission with AJAX for better UX
        document.getElementById('ragForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const question = document.getElementById('question').value;
            const loadingDiv = document.getElementById('loading');
            const responseDiv = document.getElementById('response');
            const answerText = document.getElementById('answerText');
            
            // Show loading, hide previous response
            loadingDiv.classList.add('show');
            responseDiv.classList.add('hidden');
            responseDiv.classList.remove('show');
            
            try {
                // Simulate API call - Replace with your actual endpoint
                // For demo purposes, we'll simulate a response
                // In production, replace this with your actual /ask endpoint
                
                // Uncomment for actual backend integration:
                /*
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `question=${encodeURIComponent(question)}`
                });
                const data = await response.json();
                answerText.textContent = data.answer || "No response received";
                */
                
                // Demo simulation (remove in production)
                await new Promise(resolve => setTimeout(resolve, 1500));
                const demoAnswers = {
                    "ada": "Ada Lovelace was a mathematician and writer, known for her work on Charles Babbage's Analytical Engine. She is often considered the first computer programmer.",
                    "lovelace": "Ada Lovelace was a mathematician and writer, known for her work on Charles Babbage's Analytical Engine. She is often considered the first computer programmer.",
                    "jupiter": "Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass more than two and a half times that of all other planets combined.",
                    "crispr": "CRISPR is a family of DNA sequences found in bacteria. The CRISPR-Cas9 system has been adapted for genome editing, allowing scientists to modify DNA sequences with precision.",
                    "default": `Based on the documents, I found information about ${question}. The documents discuss various topics including Ada Lovelace (mathematics and computing), Jupiter (astronomy), and CRISPR (genetic engineering). Could you be more specific?`
                };
                
                let answer = demoAnswers.default;
                const lowerQ = question.toLowerCase();
                for (const [key, value] of Object.entries(demoAnswers)) {
                    if (lowerQ.includes(key)) {
                        answer = value;
                        break;
                    }
                }
                
                answerText.textContent = answer;
                
            } catch (error) {
                console.error('Error:', error);
                answerText.textContent = 'Sorry, there was an error processing your request. Please try again.';
            } finally {
                // Hide loading, show response
                loadingDiv.classList.remove('show');
                responseDiv.classList.remove('hidden');
                responseDiv.classList.add('show');
            }
        });
        
        // Optional: Add loading animation when modal iframe loads
        const modalIframe = document.querySelector('#contactModal iframe');
        if (modalIframe) {
            modalIframe.addEventListener('load', function() {
                console.log('Contact form loaded');
            });
        }
    </script>
</body>
</html>
    """

@app.post("/ask", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    answer = bot.ask(question)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>RAGBot Answer - AI Assistant Response</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome 6 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* Custom overrides while maintaining Tailwind */
        body {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Inter', Arial, sans-serif;
        }
        
        /* Custom button styling - Green buttons */
        .btn-custom-green {
            background-color: #28a745;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        
        .btn-custom-green:hover {
            background-color: #218838;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        }
        
        .btn-custom-green:active {
            transform: translateY(0);
        }
        
        /* Modal styling for dark theme */
        .modal-content {
            background-color: #1a1a1a;
            color: white;
        }
        
        .modal-header {
            border-bottom-color: #28a745;
        }
        
        .modal-footer {
            border-top-color: #28a745;
        }
        
        .btn-close {
            filter: invert(1);
        }
        
        /* Answer card styling */
        .answer-card {
            background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
            border-left: 4px solid #28a745;
            transition: transform 0.3s ease;
        }
        
        .answer-card:hover {
            transform: translateY(-4px);
        }
        
        /* Question badge */
        .question-badge {
            background-color: #28a74520;
            border: 1px solid #28a745;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        
        /* Responsive text */
        @media (max-width: 640px) {
            h1 {
                font-size: 1.75rem;
            }
            
            .answer-card {
                margin: 1rem;
                padding: 1.25rem;
            }
            
            .content-container {
                padding: 1rem;
            }
        }
        
        /* Custom scrollbar for modal */
        .modal-body::-webkit-scrollbar {
            width: 8px;
        }
        
        .modal-body::-webkit-scrollbar-track {
            background: #2a2a2a;
        }
        
        .modal-body::-webkit-scrollbar-thumb {
            background: #28a745;
            border-radius: 4px;
        }
        
        .modal-body::-webkit-scrollbar-thumb:hover {
            background: #218838;
        }
        
        /* Animation for content */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.5s ease-out;
        }
        
        /* Copy button styling */
        .copy-btn {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .copy-btn:hover {
            color: #28a745;
            transform: scale(1.1);
        }
        
        /* Code block styling for answer */
        .answer-text {
            line-height: 1.6;
        }
        
        .answer-text a {
            color: #28a745;
            text-decoration: none;
        }
        
        .answer-text a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body class="bg-black text-white">
    <!-- Header with Contact Modal Trigger -->
    <nav class="bg-black border-b border-green-700 shadow-lg">
        <div class="container mx-auto px-4 py-3">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-robot text-green-500 text-2xl sm:text-3xl"></i>
                    <div>
                        <span class="text-xl sm:text-2xl font-bold">RAGBot</span>
                        <p class="text-xs text-gray-400 hidden sm:block">Retrieval-Augmented Generation Bot</p>
                    </div>
                </div>
                <button type="button" class="btn-custom-green px-4 py-2 rounded-lg flex items-center gap-2 transition-all" data-bs-toggle="modal" data-bs-target="#contactModal">
                    <i class="fas fa-envelope"></i>
                    <span class="hidden sm:inline">Contact</span>
                    <i class="fas fa-chevron-right text-xs sm:hidden"></i>
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8 sm:py-12">
        <div class="max-w-4xl mx-auto fade-in-up">
            <!-- Header with icon -->
            <div class="text-center mb-8 sm:mb-12">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-green-500 rounded-full mb-4">
                    <i class="fas fa-comment-dots text-black text-2xl"></i>
                </div>
                <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-2">
                    RAGBot <span class="text-green-500">Answer</span>
                </h1>
                <p class="text-gray-400 text-sm sm:text-base">Here's what I found based on your question</p>
            </div>
            
            <!-- Question Section -->
            <div class="mb-6">
                <div class="question-badge inline-flex items-center gap-2 mb-3">
                    <i class="fas fa-question-circle text-green-500"></i>
                    <span class="font-semibold text-gray-300">Your Question:</span>
                </div>
                <div class="bg-gray-900 rounded-lg p-4 sm:p-5 border border-gray-700">
                    <p class="text-white text-base sm:text-lg font-medium" id="questionText">
                        {question}
                    </p>
                </div>
            </div>
            
            <!-- Answer Section -->
            <div class="mb-8">
                <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                    <div class="inline-flex items-center gap-2">
                        <i class="fas fa-robot text-green-500"></i>
                        <span class="font-semibold text-gray-300">RAGBot Answer:</span>
                    </div>
                    <button onclick="copyAnswer()" class="copy-btn text-gray-400 hover:text-green-500 transition-colors flex items-center gap-1 text-sm">
                        <i class="fas fa-copy"></i>
                        <span>Copy</span>
                    </button>
                </div>
                <div class="answer-card rounded-lg p-5 sm:p-6 shadow-xl">
                    <div class="answer-text text-gray-200 text-base sm:text-lg leading-relaxed" id="answerText">
                        {answer}
                    </div>
                </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="/" class="btn-custom-green px-6 py-3 rounded-lg text-center inline-flex items-center justify-center gap-2 transition-all">
                    <i class="fas fa-plus-circle"></i>
                    <span>Ask Another Question</span>
                </a>
                <button onclick="window.print()" class="bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 rounded-lg inline-flex items-center justify-center gap-2 transition-all">
                    <i class="fas fa-print"></i>
                    <span>Print Answer</span>
                </button>
            </div>
            
            <!-- Feedback Section -->
            <div class="mt-8 pt-6 border-t border-gray-800 text-center">
                <p class="text-gray-500 text-sm flex items-center justify-center gap-2 flex-wrap">
                    <i class="fas fa-lightbulb text-yellow-500"></i>
                    <span>Was this helpful?</span>
                    <button onclick="provideFeedback(true)" class="text-green-500 hover:text-green-400 mx-1">
                        <i class="fas fa-thumbs-up"></i> Yes
                    </button>
                    <span class="text-gray-600">|</span>
                    <button onclick="provideFeedback(false)" class="text-red-500 hover:text-red-400 mx-1">
                        <i class="fas fa-thumbs-down"></i> No
                    </button>
                </p>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-black border-t border-green-700 mt-12 py-6">
        <div class="container mx-auto px-4">
            <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
                <div class="text-center sm:text-left">
                    <p class="text-gray-400 text-sm">
                        Another Website by 
                        <a href="https://raiiarcomio.com" target="_blank" rel="noopener noreferrer" class="footer-link text-green-500 hover:text-white transition-colors font-semibold">
                            Julius Olatokunbo <i class="fas fa-external-link-alt text-xs ml-1"></i>
                        </a>
                    </p>
                </div>
                <div class="flex gap-6">
                    <button type="button" class="footer-link text-green-500 hover:text-white transition-colors flex items-center gap-2" data-bs-toggle="modal" data-bs-target="#contactModal">
                        <i class="fas fa-envelope"></i>
                        <span>Contact</span>
                    </button>
                    <a href="#" class="text-gray-400 hover:text-green-500 transition-colors">
                        <i class="fab fa-twitter"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-green-500 transition-colors">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="#" class="text-gray-400 hover:text-green-500 transition-colors">
                        <i class="fab fa-linkedin"></i>
                    </a>
                </div>
            </div>
            <div class="text-center mt-4 text-gray-600 text-xs">
                <i class="fas fa-shield-alt"></i> Powered by RAG technology with Azure OpenAI
            </div>
        </div>
    </footer>

    <!-- Scrollable Modal for Contact -->
    <div class="modal fade" id="contactModal" tabindex="-1" aria-labelledby="contactModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-b border-green-700">
                    <h5 class="modal-title text-white" id="contactModalLabel">
                        <i class="fas fa-address-card text-green-500 mr-2"></i>
                        Contact Information
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-0">
                    <iframe 
                        src="https://raiiarcomio.com/contact2" 
                        class="w-100" 
                        style="width: 100%; height: 500px; border: none;"
                        title="Contact Form"
                        loading="lazy"
                        sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
                    ></iframe>
                </div>
                <div class="modal-footer border-t border-green-700">
                    <button type="button" class="btn-custom-green px-4 py-2 rounded" data-bs-dismiss="modal">
                        <i class="fas fa-times mr-2"></i>
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- JavaScript for enhanced functionality -->
    <script>
        // Function to copy answer to clipboard
        async function copyAnswer() {
            const answerText = document.getElementById('answerText').innerText;
            try {
                await navigator.clipboard.writeText(answerText);
                // Show temporary notification
                showNotification('Answer copied to clipboard!', 'success');
            } catch (err) {
                console.error('Failed to copy:', err);
                showNotification('Failed to copy answer', 'error');
            }
        }
        
        // Function to show notification
        function showNotification(message, type) {
            // Create notification element
            const notification = document.createElement('div');
            notification.className = `fixed top-20 right-4 bg-${type === 'success' ? 'green' : 'red'}-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-all duration-300`;
            notification.innerHTML = `
                <div class="flex items-center gap-2">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                    <span>${message}</span>
                </div>
            `;
            document.body.appendChild(notification);
            
            // Remove notification after 3 seconds
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        // Function to handle feedback
        function provideFeedback(helpful) {
            const message = helpful ? 'Thanks for your feedback! Glad we could help.' : 'Sorry to hear that. We\'ll work on improving!';
            showNotification(message, 'success');
            
            // Here you could send feedback to your backend
            console.log(`Feedback provided: ${helpful ? 'Helpful' : 'Not helpful'}`);
        }
        
        // Add loading animation when modal iframe loads
        const modalIframe = document.querySelector('#contactModal iframe');
        if (modalIframe) {
            modalIframe.addEventListener('load', function() {
                console.log('Contact form loaded successfully');
            });
        }
        
        // Optional: Handle dynamic content if question/answer comes from URL params
        document.addEventListener('DOMContentLoaded', function() {
            // You can extract question and answer from URL parameters if needed
            const urlParams = new URLSearchParams(window.location.search);
            const questionParam = urlParams.get('question');
            const answerParam = urlParams.get('answer');
            
            if (questionParam) {
                document.getElementById('questionText').textContent = decodeURIComponent(questionParam);
            }
            if (answerParam) {
                document.getElementById('answerText').innerHTML = decodeURIComponent(answerParam);
            }
        });
        
        // Add keyboard shortcut (Ctrl+C to copy answer)
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
                // Check if we're not in an input/textarea
                if (!document.activeElement.matches('input, textarea')) {
                    e.preventDefault();
                    copyAnswer();
                }
            }
        });
    </script>
</body>
</html>
    """