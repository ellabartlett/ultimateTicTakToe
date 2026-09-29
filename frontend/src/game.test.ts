import { describe, expect, it } from 'vitest';
import { createGame, playMove } from './game';

describe('ultimate tic-tac-toe rules', () => {
  it('routes the next move to the played cell', () => {
    const state = playMove(createGame(), 0, 4);
    expect(state.nextBoard).toBe(4);
    expect(state.currentPlayer).toBe('O');
  });

  it('rejects a move outside the routed board', () => {
    const state = playMove(createGame(), 0, 4);
    expect(() => playMove(state, 1, 0)).toThrow('highlighted board');
  });

  it('claims a micro-board after three marks in a row', () => {
    let state = createGame();
    state = playMove(state, 0, 0);
    state = playMove(state, 0, 3);
    state = playMove(state, 3, 1);
    state = playMove(state, 1, 0);
    state = playMove(state, 0, 1);
    state = playMove(state, 1, 3);
    state = playMove(state, 3, 2);
    state = playMove(state, 2, 0);
    state = playMove(state, 0, 2);
    expect(state.statuses[0]).toBe('X');
  });

  it('allows any open board when the destination is already claimed', () => {
    let state = createGame();
    state = { ...state, statuses: ['X', null, null, null, null, null, null, null, null], nextBoard: 0 };
    expect(() => playMove(state, 1, 0)).not.toThrow();
  });

  it('resets to an empty X turn', () => {
    const state = createGame();
    expect(state.boards.flat().every((cell) => cell === null)).toBe(true);
    expect(state.currentPlayer).toBe('X');
  });
});
