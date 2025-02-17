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

async function auto_populate_video(starting_skate_id) {
    try {
        const directoryHandle = await window.showDirectoryPicker();

        // Fetch details of the starting skate
        const response = await fetch(`skates/${starting_skate_id}/details/json`);
        const result = await response.json();

        const starting_skate_position = result.skate_position;
        let current_skate_position = starting_skate_position + 1;
        console.log(`next skate position: ${current_skate_position}`)

        // Fetch all skates to check for existing creation_datetime in upload queue
        const allSkatesResponse = await fetch(`skates/details/json`);
        const responseData = await allSkatesResponse.json();
        const allSkates = responseData.all_skates;  // Access the "skates" property that contains the array


        // Organize skates by competition_id and event_rink
        const skatesByCompetition = allSkates.reduce((acc, skate) => {
            const competitionId = skate.competition_id;
            const eventRink = skate.event_rink;

            if (!competitionId || !eventRink) {
                console.warn(`Skipping skate due to missing competition_id or event_rink:`, skate);
                return acc;  // Skip this skate if data is incomplete
            }

            const key = `${competitionId}-${eventRink}`;
            if (!acc[key]) acc[key] = [];
            acc[key].push(skate);
            return acc;
        }, {});

        const newUploads = [];

        for await (const entry of directoryHandle.values()) {
            if (entry.kind === 'file' && isVideoFile(entry.name)) {
                const file = await entry.getFile();
                const filename = entry.name;
                const skate_id = 1;
                const creation_datetime = await extractCreationTime(file);

                // Check if the creation_datetime exists in uploadQueue, ascending with skate_position for this competition_id
                const competitionKey = `${result.competition_id}-${result.event_rink}`; // add join to events table to get these values correctly
                const existingSkates = skatesByCompetition[competitionKey];

                // Debugging: Check if the existing skates are correctly matched by competition_id and event_rink
                console.log('Existing skates for competitionKey:', competitionKey, existingSkates);

                // Add new file to the temporary list of uploads with its creation_datetime and skate_position
                newUploads.push({
                    file,
                    skate_id,
                    filename,
                    creation_datetime,
                    skate_position: current_skate_position++
                });
            }
        }

        // Reorder all files based on creation_datetime
        newUploads.sort((a, b) => new Date(a.creation_datetime) - new Date(b.creation_datetime));

        // Reassign sequential skate_position values based on the sorted creation_datetime order
        newUploads.forEach((upload, index) => {
            upload.skate_position = index + starting_skate_position;
        });

        // Debugging: Check the final list of new uploads before adding them to the upload queue
        console.log('New uploads after sorting:', newUploads);

        // Retrieve the skate_id for a given skate_position
        function getSkateIdFromPosition(position) {
            const key = `${result.competition_id}-${result.event_rink}`;
            const skatesForEvent = skatesByCompetition[key] || [];
            const skate = skatesForEvent.find(skate => skate.skate_position === position);
            return skate ? skate.id : null;  // Return null if no skate is found for that position
        }

        // Now, add the files in order to the uploadQueue
        for (const upload of newUploads) {
            const exists = uploadQueue.some(u => u.creation_datetime === upload.creation_datetime);
            if (exists) {
                console.log(`A video with the creation datetime ${upload.creation_datetime} already exists. Skipping this file.`);
            } else {
                // Get the skate_id based on the final skate_position
                const skateIdForPosition = getSkateIdFromPosition(upload.skate_position);
                console.log(`Assigning skate_id ${skateIdForPosition} to position ${upload.skate_position}`);

                // Stage the file for processing
                stage_file(upload.file, upload.filename, skateIdForPosition, upload.creation_datetime);
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
