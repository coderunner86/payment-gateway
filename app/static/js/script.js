async function askGPT(question) {
    try {
        
        const response = await fetch('http://localhost:8000/api/gpt/ask-gpt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question})
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data)
        process_data = tohiperLink(data)
        document.getElementById('gptResponse').innerHTML = process_data 
 
    } catch (error) {
        console.error('Error:', error);
    }
}
function tohiperLink(response) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return response.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank">${url}</a>`;
    });
}
