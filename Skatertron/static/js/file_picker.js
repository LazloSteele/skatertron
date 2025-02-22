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
            const isImage = isImageFile(u.filename) && isImageFile(uploadRequest.filename);

            return (isVideo || isImage) && u.creation_datetime === uploadRequest.creation_datetime;
        });

        if (exists) {
            throw new Error(`A file with the creation datetime ${uploadRequest.creation_datetime} already exists. Skipping this file.`)
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

async function auto_populate_files(starting_skate_id) {
    const directoryHandle = await window.showDirectoryPicker();
    auto_populate_video(starting_skate_id, directoryHandle);
    auto_populate_images(directoryHandle)
}

async function auto_populate_video(starting_skate_id, directoryHandle) {
    try {
        // Fetch details of the starting skate
        const response = await fetch(`skates/${starting_skate_id}/details/json`);
        const result = await response.json();

        const starting_skate_position = result.skate_position + 1;
        let current_skate_position = starting_skate_position;
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
                const creation_datetime = await extractCreationTime(file);

                // Check if the creation_datetime exists in uploadQueue, ascending with skate_position for this competition_id
                const competitionKey = `${result.competition_id}-${result.event_rink}`; // add join to events table to get these values correctly
                const existingSkates = skatesByCompetition[competitionKey];

                // Debugging: Check if the existing skates are correctly matched by competition_id and event_rink
                console.log('Existing skates for competitionKey:', competitionKey, existingSkates);

                // Add new file to the temporary list of uploads with its creation_datetime and skate_position
                newUploads.push({
                    file,
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

// Function that processes all images in a directory handle
async function auto_populate_images(directoryHandle) {
    try {
        // Read all entries from the directory into an array
        const entries = [];
        for await (const entry of directoryHandle.values()) {
            entries.push(entry);
        }

        // Filter for image files
        const imageFiles = entries.filter(
            entry => entry.kind === 'file' && isImageFile(entry.name)
        );

        // Process each image file
        for (const imageEntry of imageFiles) {
            // Get the File object for this entry
            const file = await imageEntry.getFile();
            // Extract the creation time (assuming extractCreationTime returns an ISO string)
            const creationDatetime = await extractCreationTime(file);

            if (!creationDatetime) {
                console.warn(`Could not extract creation time for ${imageEntry.name}`);
                continue;
            }

            const imageCreationDate = new Date(creationDatetime);

            // Determine which video range this image falls into
            let assignedSkateId = null;

            const videoQueue = uploadQueue.filter(item => isVideoFile(item.filename));
            for (let i = 0; i < uploadQueue.length - 1; i++) {
                const videoA = uploadQueue[i];
                const videoB = uploadQueue[i + 1];
                const videoADate = new Date(videoA.creation_datetime);
                const videoBDate = new Date(videoB.creation_datetime);
                // Check if the image's creation time is between videoA and videoB
                if (imageCreationDate >= videoADate && imageCreationDate < videoBDate) {
                    assignedSkateId = videoA.skate_id;
                    break;
                }
            }

            // Optionally, handle images outside any video range:
            if (!assignedSkateId && uploadQueue.length > 0) {
                const firstVideo = uploadQueue[0];
                const lastVideo = uploadQueue[uploadQueue.length - 1];
                const firstVideoDate = new Date(firstVideo.creation_datetime);
                const lastVideoDate = new Date(lastVideo.creation_datetime);
                if (imageCreationDate < firstVideoDate) {
                    assignedSkateId = firstVideo.skate_id;
                } else if (imageCreationDate >= lastVideoDate) {
                    assignedSkateId = lastVideo.skate_id;
                }
            }

            // If we found an assignment, stage the file for further processing
            if (assignedSkateId !== null) {
                stage_file(file, imageEntry.name, assignedSkateId, creationDatetime);
                console.log(`Image ${imageEntry.name} assigned skate_id ${assignedSkateId}`);
            } else {
                console.log(`No matching video range found for image ${imageEntry.name}`);
            }
        }
    } catch (error) {
        console.error("Error while auto populating images:", error);
    }
}
