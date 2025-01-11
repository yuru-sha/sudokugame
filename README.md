# Sudoku Game

A Python-based Sudoku game with a graphical user interface built using Pygame. The game offers four difficulty levels and features a clean, modern interface.

## Features

- Four difficulty levels: Easy, Normal, Hard, and Expert
- Clean and intuitive user interface
- Real-time error checking
- Solution viewer
- Progress saving
- Keyboard and mouse input support

## Requirements

- Python 3.8 or higher
- Poetry (dependency management)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yuru-sha/sudokugame.git
cd sudokugame
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
make install
```

## Development

### Available Commands

```bash
make help      # Show help message
make install   # Install dependencies
make update    # Update dependencies
make clean     # Clean build artifacts
make test      # Run tests
make lint      # Check code style
make format    # Format code
make run       # Run the game
make build     # Build the project
make shell     # Spawn a shell within the virtual environment
```

### How to Play

1. Start the game:
```bash
make run
```

2. Select a difficulty level:
   - Easy: 41 numbers pre-filled
   - Normal: 31 numbers pre-filled
   - Hard: 26 numbers pre-filled
   - Expert: 21 numbers pre-filled

3. Game Controls:
   - Click a cell to select it
   - Type numbers (1-9) to fill the selected cell
   - Press Backspace to clear a cell
   - Click "Check Answer" to verify your solution
   - Click "Quit" to return to the difficulty selection screen

## Project Structure

```
src/sudokugame/
├── core/           # Core game functionality
├── game/           # Game logic and state management
│   └── states/     # Game state handling
└── ui/             # User interface components
    └── screens/    # Game screens and menus
```

## Development

The project uses a modular architecture with clear separation of concerns:
- `core`: Contains the main game loop and constants
- `game`: Handles game logic and state management
- `ui`: Manages all user interface components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Managed with [Poetry](https://python-poetry.org/)
- Inspired by classic Sudoku games 