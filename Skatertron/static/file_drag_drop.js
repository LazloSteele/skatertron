// Get the drop zone element
const dropzone = document.getElementById('FileBrowserFrame');

dropzone.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropzone.classList.add('drag-over');
});

dropzone.addEventListener('dragleave', function (e) {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
});

dropzone.addEventListener('drop', function (e) {
    e.preventDefault();
    dropzone.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    for (let i = 0; i < files.length; i++) {
        file = {
            skate_id: 1,
            file_name: files[i].name,
        };

        fetch('/files/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(file),
            }
        )

        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
                return response.json(); // Parse the JSON from the response
        })

        .then(data => {
            console.log('Response from FastAPI:', data);
            // Handle the response from the server
        })

        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
});