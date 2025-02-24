async function auto_populate_files() {
    try {
        const starting_skate_id = selectedSkateId;

        if (starting_skate_id === null) {
            throw new Error('Please select a skate!')
        } else {
            const directoryHandle = await window.showDirectoryPicker();
            console.log(`before video: ${uploadQueue}`)

            await auto_populate_video(starting_skate_id, directoryHandle);
            console.log(`after auto_populate_video: ${uploadQueue}`)
            // sort the videos in chronological order
            uploadQueue.sort((a, b) => new Date(a.creation_datetime) - new Date(b.creation_datetime));

            await auto_populate_images(directoryHandle);

        }
    } catch (error) {
        console.error('Error with selected skate: ', error);
    }
}

async function auto_populate_video(starting_skate_id, directoryHandle) {
    try {
        // Fetch details of the starting skate
        const response = await fetch(`skates/${starting_skate_id}/details/json`);
        const result = await response.json();

        const starting_skate_position = result.skate_position;
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
                const existingSkates = (skatesByCompetition[competitionKey] || []).sort((a, b) => a.skate_position - b.skate_position);

                // Debugging: Check if the existing skates are correctly matched by competition_id and event_rink
                console.log('Existing skates for competitionKey:', competitionKey, existingSkates);

                // Move to the next skate position if the current skate has no video
                while (existingSkates[current_skate_position] && existingSkates[current_skate_position].no_video) {
                    console.log(`Skipping skate at position ${current_skate_position} because no_video is True`);
                    current_skate_position++;  // Skip to the next position
                }

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
        await Promise.all(newUploads.map(async (upload) => {
            // Get the skate_id based on the final skate_position
            const skateIdForPosition = getSkateIdFromPosition(upload.skate_position);
            console.log(`Assigning skate_id ${skateIdForPosition} to position ${upload.skate_position}`);

            // Stage the file for processing
            await stage_file(upload.file, upload.filename, skateIdForPosition, upload.creation_datetime);
        }));

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

            const imageCreationDate = creationDatetime;

            // Determine which video range this image falls into
            let assignedSkateId = null;

            const videoQueue = uploadQueue.filter(item => isVideoFile(item.filename));
            for (let i = 0; i < videoQueue.length - 1; i++) {
                const videoA = videoQueue[i];
                const videoB = videoQueue[i + 1];

                const videoADate = videoA.creation_datetime;
                const videoBDate = videoB.creation_datetime;

                console.log(`video A: ${new Date(videoADate)} --- image: ${new Date(imageCreationDate)} --- video B: ${new Date(videoBDate)}`)
                console.log(`image created later than videoA: ${new Date(imageCreationDate) >= new Date(videoADate)}`)
                console.log(`image created earlier than videoB: ${new Date(imageCreationDate) < new Date(videoBDate)}`)

                // Check if the image's creation time is between videoA and videoB
                if (new Date(imageCreationDate) >= new Date(videoADate) && new Date(imageCreationDate) < new Date(videoBDate)) {
                    console.log(`both`)
                    assignedSkateId = videoA.skate_id;
                    break;
                }
            }

            // Handle the case where the image is after the last video in the array
            const lastVideo = videoQueue[videoQueue.length - 1];
            const lastVideoDate = lastVideo.creation_datetime;

            console.log(`last video: ${lastVideo.filename} --- image: ${new Date(imageCreationDate)}`);
            console.log(`image created later than last video: ${new Date(imageCreationDate) >= new Date(lastVideoDate)}`);

            if (new Date(imageCreationDate) >= new Date(lastVideoDate)) {
                console.log(`image assigned to last video`);
                assignedSkateId = lastVideo.skate_id;
            }

            // Optionally, handle images outside any video range:
            if (!assignedSkateId && uploadQueue.length > 0) {
                const firstVideo = uploadQueue[0];
                const lastVideo = uploadQueue[uploadQueue.length - 1];
                const firstVideoDate = firstVideo.creation_datetime;
                const lastVideoDate = lastVideo.creation_datetime;
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