let token = '';

function setToken() {
    token = document.getElementById('token').value;
    alert('Token set!');
}

async function moderateImage() {
    const imageUrl = document.getElementById('imageUrl').value;
    const resultDiv = document.getElementById('result');
    
    if (!token) {
        resultDiv.innerHTML = '<p>Please set a token first.</p>';
        return;
    }

    try {
        const response = await fetch('http://localhost:7000/moderate', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image_url: imageUrl })
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.innerHTML = `
                <p>Is Safe: ${data.is_safe}</p>
                <p>Categories: ${JSON.stringify(data.categories, null, 2)}</p>
            `;
        } else {
            resultDiv.innerHTML = `<p>Error: ${data.detail}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}