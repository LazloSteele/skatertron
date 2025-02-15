const uploadQueue = [];

document.addEventListener('click', async (event) => {
    // Look for an <sl-button> with the 'data-file-picker' attribute
    const button = event.target.closest('sl-button[data-file-picker]');
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
        const skate_id = button.getAttribute('skate-id');
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

            if (uploadQueue.length === 0) {
                const triggerElement = document.querySelector("#bulk_upload_placeholder");
                if (triggerElement) {
                    // Dispatch a custom event or simulate the event that triggers htmx (e.g., 'click', 'change', etc.)
                    htmx.trigger(triggerElement, 'click');
                }
            }

            uploadQueue.push(uploadRequest);

            const triggerElement = document.querySelector(`#staged_message_${skate_id}`);
            if (triggerElement) {
                // Dispatch a custom event or simulate the event that triggers htmx (e.g., 'click', 'change', etc.)
                htmx.trigger(triggerElement, 'click');

            }
    } catch (error) {
        console.error('File not staged.', error)
    }
}

// Function to actually upload the files
async function uploadFilesToServer() {
    const formData = new FormData();

    const skateIds = [];
    // Iterate through the uploadQueue and add files to FormData
    for (const request of uploadQueue) {
        formData.append('files', file);
        skateIds.push(request.skate_id);
    }

    // Append the skate_ids as a separate form field, serialized as a JSON string
    formData.append('skate_ids', JSON.stringify(skateIds));

    // Send the request via fetch
    const response = await fetch('/files/bulk_upload', {
        method: 'POST',
        body: formData
    });

    // Check the response status (200 OK) and clear the queue if successful
    if (response.ok) {
        const result = await response.json();
        console.log(result);  // Log the result of the upload

        // Clear the upload queue after successful upload
        uploadQueue.length = 0;  // This will empty the uploadQueue array
        console.log("Upload queue cleared.");
    } else {
        console.error("Upload failed with status:", response.status);
    }

}

async function extractCreationTime(file) {
    // Convert the file to an ArrayBuffer asynchronously using FileReader
    try {
        const slice = file.slice(0, 50 * 1024); // get first 50kb for ensuring metadata is contained

        const formData = new FormData();
        formData.append("file_slice", slice, file.name);

        const response = await fetch('/files/get_creation_datetime', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        console.log(result);

        return result.creation_time;

    } catch (error) {
        console.error('Error while sending file slice...', error);
    }
}


// TODO: skate_position should start at 0, increment by 1 for each skate, and only reset on new rink or new competition,
// TODO: skate_position should also change based on event_position, when event is reordered, the skate_positions should
// TODO:     also change...
// TODO: get skate.position and skate.event_id to go down nested tree
async function auto_populate_video(starting_skate_id) {
    try {
        const directoryHandle = await window.showDirectoryPicker();

        const response = await fetch(`skates/${starting_skate_id}/details/json`);
        const result = await response.json();

        let current_skate_position = result.skate_position + 1;

        for await (const entry of directoryHandle.values()) {
            if (entry.kind === 'file' && isVideoFile(entry.name)) {
                const file = await entry.getFile();
                const filename = entry.name;
                const skate_id = 1;
                const creation_datetime = await extractCreationTime(file);

                const exists = uploadQueue.some(upload => upload.creation_datetime === creation_datetime);

                if (exists) {
                    console.log(`A video with the creation datetime ${creation_datetime} already exists. Skipping this file.`);
                    continue;  // Skip this file and move to the next
                }

                stage_file(file, filename, skate_id, creation_datetime);
            }
        }

        console.log(uploadQueue);
    } catch (error) {
        console.error('Error while auto populating video...', error);
    }
}

function isVideoFile(fileName) {
    const videoExtensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm'];
    return videoExtensions.some(ext => fileName.toLowerCase().endsWith(ext));
}
