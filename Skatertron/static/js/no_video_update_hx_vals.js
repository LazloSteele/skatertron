function updateHxVals(checkbox) {
    // Dynamically set the hx-vals attribute based on the checkbox state
    checkbox.setAttribute('hx-vals', JSON.stringify({'new_no_video': !checkbox.checked}));
}