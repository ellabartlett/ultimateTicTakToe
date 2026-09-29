import { useState } from 'react';
import { createGame, playMove, type GameState, type Player } from './game';

function Mark({ value }: { value: Player | null }) {
  return value ? <span className={`mark mark-${value.toLowerCase()}`}>{value}</span> : null;
}

function App() {
  const [game, setGame] = useState<GameState>(() => createGame());
  const [message, setMessage] = useState('Choose any small square to begin.');

  const reset = () => {
    setGame(createGame());
    setMessage('Choose any small square to begin.');
  };

  const chooseCell = (boardIndex: number, cellIndex: number) => {
    try {
      const next = playMove(game, boardIndex, cellIndex);
      setGame(next);
      setMessage(next.winner ? `${next.winner === 'draw' ? 'Draw' : `${next.winner} wins`} the match.` : next.nextBoard === null ? 'The destination board is open. Choose any board.' : `Your move is routed to board ${next.nextBoard + 1}.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'That move is unavailable.');
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand"><span className="brand-dot" /> ULTIMATE <strong>TTT</strong></div>
        <button className="reset-button" onClick={reset} aria-label="Start a new game">New game <span>↻</span></button>
      </header>

      <section className="intro">
        <p className="eyebrow">Nine boards. One battlefield.</p>
        <h1>Think three moves<br /><em>ahead.</em></h1>
        <p className="lede">Win the small boards to conquer the big one.<br />Every move decides where your opponent must play next.</p>
      </section>

      <section className="game-layout" aria-label="Ultimate Tic-Tac-Toe game">
        <div className="game-meta">
          <div className="turn-card"><span className="turn-label">CURRENT TURN</span><span className={`turn-mark mark-${game.currentPlayer.toLowerCase()}`}>{game.currentPlayer}</span><span className="turn-copy">Make your move</span></div>
          <div className="rule-note"><span className="rule-number">01</span><span>Send your opponent to the board matching the square you choose.</span></div>
        </div>

        <div className="macro-board" aria-label="Ultimate Tic-Tac-Toe board">
          {game.boards.map((board, boardIndex) => {
            const status = game.statuses[boardIndex];
            const playable = !game.winner && status === null && (game.nextBoard === null || game.nextBoard === boardIndex || !game.statuses[game.nextBoard] || game.boards[game.nextBoard].every(Boolean));
            return <div className={`micro-board ${game.nextBoard === boardIndex && playable ? 'is-target' : ''} ${status ? 'is-claimed' : ''}`} key={boardIndex} aria-label={`Small board ${boardIndex + 1}`}>
              {status && status !== 'draw' ? <div className="claimed-mark"><Mark value={status} /></div> : null}
              {board.map((cell, cellIndex) => <button key={cellIndex} className="cell" disabled={!playable || Boolean(cell)} onClick={() => chooseCell(boardIndex, cellIndex)} aria-label={`Board ${boardIndex + 1}, square ${cellIndex + 1}${cell ? `, ${cell}` : ''}`}><Mark value={cell} /></button>)}
            </div>;
          })}
        </div>

        <div className="status-line"><span className="status-pulse" />{message}</div>
      </section>

      <footer className="footer"><span><strong>X</strong> goes first</span><span className="footer-rule" /><span>Small board wins become big board marks</span><span className="footer-rule" /><span>Draws keep the board open</span></footer>
    </main>
  );
}

export default App;
