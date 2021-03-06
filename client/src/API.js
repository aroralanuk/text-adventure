import axios from "axios";

// PRODUCTION server link
const server = "https://plane-crash-text-adventure.herokuapp.com";
// const server = "http://localhost:5000";

const API = {
  createGame: function () {
    return axios.get(`${server}/api/create_game`);
  },

  updateGame: function (game_id, choice_input) {
    return axios.patch(`${server}/api/game/${game_id}`, choice_input);
  },

  getGameUpdate: function (game_id) {
    return axios.get(`${server}/api/game/${game_id}`);
  },
};

export default API;
