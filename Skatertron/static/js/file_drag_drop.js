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
            formData.append('skate_id', skate_id);
            formData.append('competition', current_competition);
            formData.append('event', current_event);
            formData.append('skater', current_skate);
            formData.append('uploaded_file', file);


            console.log(formData)

            fetch('/files/', {
                method: 'POST',
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