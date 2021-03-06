function buildGrid(websites_list, container, document)  {
    // iterate over all websites and add a brick div for each of them
    for (var i = 0; i < websites_list.length; i++) {
        var new_brick = buildBrick(websites_list[i], document);
        container.append(new_brick);
    }
}


function updateBricks(results, document) {
    for (var website_name in results) {
        // update status
        var time = results[website_name]["response_time"];
        var time_li = document.getElementById("time_" + website_name);
        time_li.innerHTML = "<b>response time: </b> " + time + " ms";

        // update reason
        var reason = results[website_name]["reason"];
        var reason_li = document.getElementById("reason_" + website_name);

        if (reason.length >= 30) {
            // if error message is long make the font smaller
            reason_li.innerHTML = "<b>error: </b> <span style='font-size:x-small'>" + reason + "</span>";
        } else if (reason !== "") {
            reason_li.innerHTML = "<b>error: </b> " + reason;

        }

        var status = "UP";

        // update brick class (site-up, site-down, site-incorrect)
        var brick = document.getElementById(website_name);
        brick.classList.remove("site-default");
        if (results[website_name]["content_ok"] === true) {
            // if content is ok then we also know that the site is up (obviously)
            brick.classList.remove("site-down");
            brick.classList.remove("site-incorrect");
            brick.classList.add("site-up");

            // update items' visibility
            time_li.style.display = "";
            reason_li.style.display = "none";

        } else if (results[website_name]["is_up"] === true) {
            // content was incorrect but the site is up, change
            // it to site-incorrect
            brick.classList.remove("site-down");
            brick.classList.remove("site-up");
            brick.classList.add("site-incorrect");
            status = "Incorrect content";

            // update items' visibility
            time_li.style.display = "";
            reason_li.style.display = "none";
        } else {
            // site is down
            brick.classList.remove("site-up");
            brick.classList.remove("site-incorrect");
            brick.classList.add("site-down");
            status = "DOWN";

            // update items' visibility
            time_li.style.display = "none";
            console.debug(reason_li);
            reason_li.style.display = "block";
        }

        // update status
        var status_li = document.getElementById("status_" + website_name);
        status_li.innerHTML = "<b>status: </b> " + status;
        status_li.style.display = "";
    }
}

function buildBrick(website_name, document) {
    // first create a brick div, the most outer one
    var brick = document.createElement("div");
    brick.classList.add("brick");
    brick.classList.add("large");
    // at first by default they're all gonna be 'up'
    brick.classList.add("site-default");
    // websites url will be the div's id
    brick.id = website_name;

    // create a panel
    var panel = document.createElement("div");
    panel.classList.add("panel");
    panel.classList.add("panel-default");
    panel.classList.add("panel-custom");

    // create a panel heading and add it to the panel div
    var panel_heading = document.createElement("div");
    panel_heading.classList.add("panel-heading");
    panel_heading.classList.add("panel-heading-custom");
    panel_heading.innerHTML = "<b>" + website_name + "</b>";
    panel.append(panel_heading);

    var panel_body = document.createElement("div");
    panel_body.classList.add("panel-body");
    panel_body.classList.add("panel-body-custom");

    // create a list containing default website data
    // for now all elements are hidden
    var website_data_list = document.createElement("ul");
    website_data_list.style.listStyleType = "none";
    website_data_list.style.paddingLeft = "0";

    var status = document.createElement("li");
    status.id = "status_" + website_name;
    status.style.display = "none";
    website_data_list.append(status);

    var response_time = document.createElement("li");
    response_time.id = "time_" + website_name;
    response_time.style.display = "none";
    website_data_list.append(response_time);

    // add an empty (and hidden) 'reason' element - will only be visible
    // if reaon is not an empty string
    var reason = document.createElement("li");
    reason.id = "reason_" + website_name;
    reason.style.display = "none";
    website_data_list.append(reason);

    panel_body.append(website_data_list);
    // create a panel body and add it to the panel div
    panel.append(panel_body);

    // add the ready panel to the brick
    brick.append(panel);
    return brick;
}
