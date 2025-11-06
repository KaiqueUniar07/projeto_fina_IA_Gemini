const form = document.getElementById('travelForm');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const guideText = document.getElementById('guideText');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    
    const data = {
        country: document.getElementById('country').value.trim(),
        city: document.getElementById('city').value.trim(),
        start_date: document.getElementById('start_date').value,
        days: parseInt(document.getElementById('days').value),
        preferences: document.getElementById('preferences').value.trim()
    };

    
    if (!data.country || !data.city || !data.start_date || !data.days) {
        alert("Por favor, preencha todos os campos obrigatórios!");
        return;
    }

    
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    guideText.textContent = "";

    try {
        
        const response = await fetch('http://localhost:8000/generate-guide', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const err = await response.text();
            throw new Error(`Erro do servidor: ${response.status}\n${err}`);
        }

        const result = await response.json();
        guideText.textContent = result.guide || "Nenhum guia retornado.";
        resultDiv.classList.remove('hidden');

    } catch (error) {
        alert("Erro ao gerar o guia:\n" + error.message);
    } finally {
        loadingDiv.classList.add('hidden');
    }
});