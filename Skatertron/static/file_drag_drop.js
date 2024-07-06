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
        file = files[i]

        if (file && (file.type.startsWith('image/') || file.type.startsWith('video/'))) {

            var formData = new FormData();
            formData.append('uploaded_file', file);
            formData.append('skate_id', 1);
            formData.append('competition', "testyyyy");
            formData.append('event', "testyyyy");
            formData.append('skater', "testyyyy");

            fetch('/files/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: formData,
                }
            )

            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                    return response;
            })

            .then(data => {
                console.log('Response from FastAPI:', data);
                
                // Handle the response from the server

            })

            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        }

        else {
        throw new Error('Not a valid video or photo file.');
        return;
    };
    }

});