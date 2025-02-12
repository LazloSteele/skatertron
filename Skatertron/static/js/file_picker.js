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
        const skate_id = button.getAttribute('skate-id');
        const creation_datetime = await extractCreationTime(file);

        const uploadRequest = {
            file: file,
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

        console.log(`Added to Queue: ${fileHandle.name}`);

        const triggerElement = document.querySelector(`#staged_message_${skate_id}`);
        if (triggerElement) {
            // Dispatch a custom event or simulate the event that triggers htmx (e.g., 'click', 'change', etc.)
            htmx.trigger(triggerElement, 'click');
        }

    } catch (error) {
        console.error('File selection cancelled or not supported.', error);
    }
});

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
    const slice = file.slice(0, 25 * 1024); // get first 20kb for ensuring metadata is contained

    const formData = new FormData();
    formData.append("file_slice", slice, file.name);

    const response = await fetch('/files/get_creation_datetime', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    console.log(result);
    } catch (error) {
        console.error('Error while sending file slice...', error);
    }
}



