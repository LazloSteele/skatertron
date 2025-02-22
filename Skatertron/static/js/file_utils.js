async function extractCreationTime(file) {
    // Convert the file to an ArrayBuffer asynchronously using FileReader
    try {
        const slice = file.slice(0, 200 * 1024); // get first 50kb for ensuring metadata is contained

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

function isVideoFile(fileName) {
    const videoExtensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm'];
    return videoExtensions.some(ext => fileName.toLowerCase().endsWith(ext));
}

// Helper to determine if a file is an image (based on file extension)
function isImageFile(fileName) {
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'];
    return imageExtensions.some(ext => fileName.toLowerCase().endsWith(ext));
}
