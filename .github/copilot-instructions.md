<!-- Use this file to provide workspace-specific custom instructions to Copilot. -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions
- [ ] Compile the Project
- [ ] Create and Run Task
- [ ] Launch the Project
- [ ] Ensure Documentation is Complete

## Project Contract

Follow the pinned Project Constitution supplied by the project owner. Use the locked FastAPI/Python backend and React/TypeScript/Vite frontend stack, with uv and pnpm respectively. Preserve the required layered layout, testing standards, accessibility floor, and deprecated-pattern exclusions. Do not add dependencies outside the constitution without approval.

## Product

Ultimate Tic-Tac-Toe: a 3x3 macro board whose nine cells each contain a 3x3 micro board. A move routes the next player to the micro board matching the played micro-cell. A won micro board is displayed as the winner's mark in its macro cell. If the routed board is won or full, the next player may choose any open board. The frontend game rules must be isolated and tested.

## Execution

Use the current workspace directory as the project root. Keep changes focused, validate after edits, and keep README.md and DECISIONS.md current. Do not commit or create branches.
