const legs_default = {
    "human": [1,2,3,4,5,6],
    "computer": [1,2,3,4,5,6],
};

let legs = {};
let target = 0;
let winner = null;
let computer_strategy = null;

async function set_defaults() {

    legs = {};
    for (player in legs_default) {
        legs[player] = [];
        for (const leg of legs_default[player]) {
            legs[player].push(leg);
        }
    }

    target = parseInt(document.getElementById("target_select").value);
    winner = null;

    computer_strategy = await fetch('computer_strategies/112233445566_' + target.toString() + '.json').then((response) => response.json());
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
        if (selectable) {
            td.setAttribute("onclick", "next_move(" + i.toString() + ")");
        }
        row.appendChild(td);
    }
    td = document.createElement("td");
    row.appendChild(td);
}

async function create_game() {
    await set_defaults();
    create_player_row(document.getElementById("human_options"), "human", true);
    create_player_row(document.getElementById("computer_options"), "computer", false);
    reset_game();
}

function update_display() {
    document.getElementById("target_display").textContent = target.toString();
    update_player_row_display(document.getElementById("human_options"), "human", true);
    update_player_row_display(document.getElementById("computer_options"), "computer", false);
    if (winner !== null) {
        document.getElementById("result_display").textContent = winner + " wins!";
    }
    else {
        document.getElementById("result_display").textContent = "";
    }
}

async function reset_game() {
    console.log("Starting new game...");
    await set_defaults();
    update_display();
}

function next_computer_move() {
    // Placeholder 'AI' strategy

    let computer_options = legs["computer"].toSorted();
    let strategy_key = computer_options.join('');
    let strat_probs = computer_strategy[strategy_key]["strategy"]

    r = Math.random();
    let prob_total = 0;
    let move_index_sorted = -1;
    for (let i = 0;i < strat_probs.length;i++) {
        prob_total += strat_probs[i];
        if (r < prob_total) {
            move_index_sorted = i;
            break;
        }
    }
    if (move_index_sorted === -1) {
        throw "Bad AI strategy";
    }

    let legs_move = computer_options[move_index_sorted];
    for (let i = 0;i < legs["computer"].length;i++) {
        if (legs["computer"][i] === legs_move) {
            return i;
        }
    }
    throw "Bad AI strategy";
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
        winner = "human";
    }
    else if (get_total("computer") == target) {
        winner = "computer";
    }
    else {
        winner = null;
    }
}

function next_move(leg_index) {
    if (winner !== null) {
        return;
    }

    let computer_move = next_computer_move();
    
    let human_leg = legs.human[leg_index];
    let computer_leg = legs.computer[computer_move];

    legs.human[leg_index] = computer_leg;
    legs.computer[computer_move] = human_leg;

    check_victory();
    update_display();
}