fetchAndRenderBoard();

let selected = null;

const pieceMap = {
  K: "♔",
  Q: "♕",
  R: "♖",
  B: "♗",
  N: "♘",
  P: "♙",
  k: "♚",
  q: "♛",
  r: "♜",
  b: "♝",
  n: "♞",
  p: "♟",
  "*": "·",
  " ": "",
};

function loadBoard(board) {
  const chessboard = document.getElementById("chessboard");
  chessboard.innerHTML = ""; // Clear board

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const square = document.createElement("div");
      square.classList.add("square");
      square.classList.add((row + col) % 2 === 0 ? "light" : "dark");
      square.dataset.row = row;
      square.dataset.col = col;
      square.innerText = pieceMap[board[row][col]];
      square.addEventListener("click", handleClick);
      chessboard.appendChild(square);
    }
  }
}

function handleClick(e) {
  const square = e.target;
  const row = square.dataset.row;
  const col = square.dataset.col;

  if (!selected) {
    selected = { row, col };
    square.classList.add("selected");
  } else {
    fetch("/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source: selected,
        target: { row, col },
      }),
    })
    fetchAndRenderBoard();
  }
}

const overlay = document.getElementById("overlay");
const overlayText = document.getElementById("overlay-text");

function fetchAndRenderBoard() {
  fetch("/get_board")
    .then((res) => res.json())
    .then((data) => {
      loadBoard(data.board, data.turn);
      selected = null;

      if (data.game_state !== "UNFINISHED") {
        overlayText.innerText =
          data.game_state === "WHITE_WON" ? "White Wins! ♚ " : "Black Wins! ♔ ";
        overlay.style.display = "flex";
      }
    });
}

function resetGame() {
  fetch("/reset", {
    method: "POST",
  }).then(() => {
    overlay.style.display = "none";
    fetchAndRenderBoard();
  });
}
