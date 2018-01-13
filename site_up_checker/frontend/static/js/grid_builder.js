function buildGrid(websites_list, container, document)  {
    // iterate over all websites and add a brick div for each of them
    for (var i = 0; i < websites_list.length; i++) {
        var new_brick_div = document.createElement("div");

        new_brick_div.classList.add("brick");
        new_brick_div.classList.add("large");

        // at first by default they're all gonna be 'up'
        new_brick_div.classList.add("site-up");

        // websites url will be the div's id
        new_brick_div.id = websites_list[i];
        console.debug(new_brick_div);
        container.append(new_brick_div)
    }
}


function updateBricks(results, dashboard) {
    console.debug("results:");
    console.debug(results);
    console.debug("end of results");
}
