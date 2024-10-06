const legs_default = {
    "human": [1,2,3,4,5,6],
    "computer": [1,2,3,4,5,6],
};

const target_default = 22;

let legs = {};
let target = 0;
let in_progress = true;

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
    for (let i = 0;i < legs[player_name].length;i++) {
        td = document.createElement("td");
        td.setAttribute("onclick", "next_move(" + i.toString() + ")")
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
    in_progress = true;
}

function next_computer_move() {
    // Placeholder 'AI' strategy
    return legs['computer'].length - 1;
}

function get_total(player) {
    let total = 0;
    for (const leg of legs[player]) {
        total += leg;
    }
    return total;
}

function check_victory() {
    if (get_total("human") == target) {
        return "human";
    }
    if (get_total("computer") == target) {
        return "computer";
    }
    return null;
}

function next_move(leg_index) {
    if (!in_progress) {
        return;
    }

    let computer_move = next_computer_move();
    
    let human_leg = legs.human[leg_index];
    let computer_leg = legs.computer[computer_move];

    legs.human[leg_index] = computer_leg;
    legs.computer[computer_move] = human_leg;

    update_display();

    let victory_check = check_victory();
    if (victory_check === null) {
        return;
    }
    
    document.getElementById("result_display").textContent = victory_check + " wins!";
    in_progress = false;
}