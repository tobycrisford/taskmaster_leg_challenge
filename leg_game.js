const legs_default = {
    "human": [1,2,3,4,5,6],
    "computer": [1,2,3,4,5,6],
};

const target_default = 22;

let legs = {};
let target = 0;

function set_defaults() {

    legs = {};
    for (player in legs_default) {
        legs[player] = [];
        for (const leg of legs_default[player]) {
            legs[player].push(leg);
        }
    }

    target = target_default;
}

function update_player_row_display(row, player_name) {
    let total = 0;
    for (let i = 0;i < legs[player_name].length;i++) {
        row.children[i].textContent = legs[player_name][i].toString();
        total += legs[player_name][i];
    }
    row.children[legs[player_name].length].textContent = "Total: " + total.toString();
}

function create_player_row(row, player_name, selectable) {
    for (const leg of legs[player_name]) {
        td = document.createElement("td");
        row.appendChild(td);
    }
    td = document.createElement("td");
    row.appendChild(td);
}

function create_game() {
    set_defaults();
    create_player_row(document.getElementById("human_options"), "human", true);
    create_player_row(document.getElementById("computer_options"), "computer", false);
    reset_game();
}

function update_display() {
    document.getElementById("target_display").textContent = target.toString();
    update_player_row_display(document.getElementById("human_options"), "human", true);
    update_player_row_display(document.getElementById("computer_options"), "computer", false);
}

function reset_game() {
    console.log("Starting new game...");
    set_defaults();
    update_display();
}