const uploadQueue = [];

document.addEventListener('click', async (event) => {
    // Look for an <sl-button> with the 'data-file-picker' attribute
    const button = event.target.closest('sl-icon-button[data-file-picker]');
    if (!button) return; // Ignore unrelated buttons

    try {
        // Open file picker
        const [fileHandle] = await window.showOpenFilePicker({
            types: [
                {
                    description: 'Image and Video files',
                    accept: {
                        'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
                        'video/*': ['.mp4', '.mov', '.avi', '.mkv']
                    }
                }
            ]
        });
        const file = await fileHandle.getFile();
        const filename = fileHandle.name
        const skate_id = parseInt(button.getAttribute('skate-id'));
        const creation_datetime = await extractCreationTime(file);

        stage_file(file, filename, skate_id, creation_datetime)

        console.log(`Added to Queue: ${filename}`);

    } catch (error) {
        console.error('File selection cancelled or not supported.', error);
    }
});

async function stage_file(file, filename, skate_id, creation_datetime) {
    try {
        const uploadRequest = {
                file: file,
                filename: filename,
                skate_id: skate_id,
                creation_datetime: creation_datetime
            };

        const exists = uploadQueue.some(u => {
            const isVideo = isVideoFile(u.filename) && isVideoFile(uploadRequest.filename);

            return isVideo && u.creation_datetime === uploadRequest.creation_datetime;
        });

        if (exists) {
            throw new Error(`A video file with the creation datetime ${uploadRequest.creation_datetime} already exists. Skipping this file.`)
        } else {
            uploadQueue.push(uploadRequest);
        }

        add_staged_badges(skate_id)
        console.log(`File ${filename} added to skate #${skate_id}!`)
    } catch (error) {
        console.error('File not staged.', error)
    }
}

// Function to actually upload the files
async function uploadFilesToServer(limit=3) {
    const queue = [...uploadQueue]; // Clone the array
    const activeUploads = new Set();

    async function processNext() {
        if (queue.length === 0) return;

        const upload = queue.shift(); // Take the next file
        const formData = new FormData();
        formData.append("uploaded_file", upload.file);
        formData.append("file_name", upload.filename);
        formData.append("skate_id", upload.skate_id);
        formData.append("creation_datetime", upload.creation_datetime);

        const uploadPromise = fetch("/files", {
            method: "POST",
            body: formData,
        }).then(response => {
            if (!response.ok) throw new Error(`Failed to upload ${upload.filename}`);
            console.log(`Successfully uploaded ${upload.filename}`);
        }).catch(error => {
            console.error(`Error uploading ${upload.filename}:`, error);
        }).finally(() => {
            activeUploads.delete(uploadPromise);
            processNext(); // Start the next upload
        });

        activeUploads.add(uploadPromise);

        // Wait if we have reached the limit
        if (activeUploads.size >= limit) {
            await Promise.race(activeUploads);
        }

        processNext();
    }

    await Promise.all([...Array(limit)].map(() => processNext())); // Start limited workers
}
