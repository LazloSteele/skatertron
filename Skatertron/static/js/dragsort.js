console.log('sortable_loaded');

// Throttle timer variables to track the last HTMX swap
let lastSwapTime = 0;
const throttleDelay = 2000; // 2 seconds delay to limit reinitialization frequency

// Function to initialize Sortable.js
const initializeSortable = () => {
    const EventsList = document.querySelector('#EventsList');

    console.log(`EventsList: ${EventsList} loaded`);

    let sortableInitialized = false;
    let sortableInstance = null;

    if (EventsList) {

        if (sortableInstance) {
            sortableInstance.destroy();
            console.log('Previous Sortable instance destroyed.');
        }

        // Initialize Sortable.js
        Sortable.create(EventsList, {
            animation: 150,
            handle: 'sl-tree-item.event_branch', // Handle for drag
            draggable: 'sl-tree-item.event_branch', // Draggable selector

            onEnd: async (evt) => {
                const allItems = EventsList.querySelectorAll('.event_branch');
                let eventIdList = [];

                allItems.forEach((item, index) => {
                    eventIdList.push(parseInt(item.dataset.id, 10));
                });

                try {
                    const response = await fetch('/events/update_position', {
                        method: 'PUT', // Use appropriate HTTP method
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            event_id_list: eventIdList
                        }),
                    });

                    if (!response.ok) {
                        console.error('Error updating position:', await response.text());
                    } else {
                        console.log('Position updated successfully');
                    }
                } catch (error) {
                    console.error('Error hitting FastAPI endpoint:', error);
                }
            },
        });
        sortableInitialized = true;
        console.log('Sortable.js initialized');
    } else {
        console.error('Element with ID "EventsList" not found.');
    }
};

// Function to handle HTMX swap events, with delay
const handleHTMXSwap = () => {
    const currentTime = Date.now();

    // If enough time has passed since the last initialization, initialize again
    if (currentTime - lastSwapTime >= throttleDelay) {
        console.log('HTMX swap finished, initializing Sortable.js');
        initializeSortable();
        lastSwapTime = currentTime; // Update the last swap time
    }
};

document.body.addEventListener('htmx:afterSwap', handleHTMXSwap);
document.body.addEventListener('sortable:end', initializeSortable);