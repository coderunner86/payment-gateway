async function askGPT(question) {
    try {
        
        // const session_id = document.getElementById('session_id').value;
        const response = await fetch('http://localhost:8000/api/gpt/ask-gpt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // ,'session_id': session_id
            },
            body: JSON.stringify({ question: question, userId:15})
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);
 
    } catch (error) {
        console.error('Error:', error);
    }
}


//  async function askGPT() {
//             try {
//                 const question = document.getElementById('question').value;


//                 var products = await fetch(`/api/products/all_products`, {
//                     method: 'GET',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     }
//                 })
//                     .then(response => response.json())
//                     .catch(error => {
//                         console.log('error', error);
//                         return [];
//                     });

//                 var productDescriptions = products.map(product => `${product.name}: ${product.description}`).join(", ");

//                 const promptText = `${question}. Aquí hay algunos libros disponibles: ${productDescriptions}. Basado en esto, ¿cuál recomendarías?`;

//                 const response = await fetch('https://api.openai.com/v1/engines/gpt-3.5-turbo-instruct/completions', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'Authorization': 'Bearer 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'
//                     },
//                     body: JSON.stringify({
//                         prompt: promptText,
//                         temperature: 0.7,
//                         max_tokens: 60
//                     })
//                 });

//                 const data = await response.json();
//                 document.getElementById('gptResponse').innerText = data.choices[0].text;
//             } catch (error) {
//                 console.error('Error:', error);
//                 document.getElementById('gptResponse').innerText = 'Error al obtener respuesta de GPT.';
//             }
//         }