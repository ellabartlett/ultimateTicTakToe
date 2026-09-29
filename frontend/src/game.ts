export type Player = 'X' | 'O';
export type Cell = Player | null;
export type MicroBoard = Cell[];
export type BoardStatus = Player | 'draw' | null;

export type GameState = {
  boards: MicroBoard[];
  statuses: BoardStatus[];
  currentPlayer: Player;
  nextBoard: number | null;
  winner: Player | 'draw' | null;
};

const LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6],
];

export function createGame(): GameState {
  return {
    boards: Array.from({ length: 9 }, () => Array<Cell>(9).fill(null)),
    statuses: Array<BoardStatus>(9).fill(null),
    currentPlayer: 'X',
    nextBoard: null,
    winner: null,
  };
}

export function hasLine(cells: Cell[]): Player | null {
  for (const [first, second, third] of LINES) {
    if (cells[first] && cells[first] === cells[second] && cells[first] === cells[third]) {
      return cells[first];
    }
  }
  return null;
}

function isFull(board: MicroBoard): boolean {
  return board.every(Boolean);
}

function openBoard(state: GameState, index: number): boolean {
  return state.statuses[index] === null && !isFull(state.boards[index]);
}

export function playMove(state: GameState, boardIndex: number, cellIndex: number): GameState {
  if (state.winner) throw new Error('The game is over.');
  if (!openBoard(state, boardIndex)) throw new Error('That board is not available.');
  if (state.nextBoard !== null && state.nextBoard !== boardIndex && openBoard(state, state.nextBoard)) {
    throw new Error('You must play in the highlighted board.');
  }
  if (state.boards[boardIndex][cellIndex]) throw new Error('That cell is already marked.');

  const boards = state.boards.map((board) => [...board]);
  boards[boardIndex][cellIndex] = state.currentPlayer;
  const statuses = [...state.statuses];
  const boardWinner = hasLine(boards[boardIndex]);
  statuses[boardIndex] = boardWinner ?? (isFull(boards[boardIndex]) ? 'draw' : null);
  const macroWinner = hasLine(statuses.map((status) => status === 'draw' ? null : status));
  const macroFull = statuses.every((status) => status !== null);

  return {
    boards,
    statuses,
    currentPlayer: state.currentPlayer === 'X' ? 'O' : 'X',
    nextBoard: openBoard({ ...state, boards, statuses }, cellIndex) ? cellIndex : null,
    winner: macroWinner ?? (macroFull ? 'draw' : null),
  };
}
