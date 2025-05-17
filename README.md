# Multiagent Pacman AI

This project is an in-depth implementation of multi-agent search algorithms for the classic Pacman game. It was developed as part of the UC Berkeley CS188: Introduction to Artificial Intelligence course. The project explores decision-making in adversarial environments using search strategies like Reflex, Minimax, Alpha-Beta Pruning, and Expectimax. It also includes ghost agent behaviors, an autograding system, and both text and graphical interfaces for gameplay.

## Features

- Implementation of four AI agents:
  - Reflex Agent
  - Minimax Agent
  - Alpha-Beta Pruning Agent
  - Expectimax Agent
- Support for multiple ghost types (RandomGhost, DirectionalGhost)
- Graphical and text-based game interfaces
- Comprehensive autograder and test framework
- Keyboard-controlled Pacman agent for manual play
- Modular design with support for extensibility

## File Overview

| File                       | Description |
|----------------------------|-------------|
| `pacman.py`                | Main game controller and entry point |
| `multi_agents.py`          | AI agent implementations (Reflex, Minimax, etc.) |
| `ghost_agents.py`          | Ghost behavior classes |
| `keyboard_agents.py`       | Keyboard-controlled agents |
| `game.py`                  | Core mechanics and game loop |
| `util.py`                  | Utility functions (e.g., distances, counters) |
| `layout.py`                | Handles maze layout parsing and game board setup |
| `graphics_display.py`      | Graphical interface using Tkinter |
| `graphics_utils.py`        | Low-level drawing primitives |
| `text_display.py`          | Console-based rendering for Pacman |
| `autograder.py`            | Autograder runner script |
| `grading.py`               | Grade tracking and evaluation logic |
| `test_classes.py`          | Base test class definitions |
| `test_parser.py`           | Parses `.test` files for automated testing |
| `multiagent_test_classes.py` | Test cases for multi-agent search correctness |
| `project_params.py`        | Global parameters and constants |
| `submission_autograder.py` | Wrapper for running autograder on student code |
| `autograder_output.txt`    | Sample grading output with scores and results |

## How to Run

### Playing the Game

Run the default game:
```bash
python pacman.py

```
Run Pacman with a specific agent:
```bash
python pacman.py -p MinimaxAgent -l mediumClassic -a depth=3
```

Control Pacman manually with keyboard (WASD or arrow keys):
```bash
python pacman.py -p KeyboardAgent

```
### Running the Autograder

Run all tests:
```bash
python autograder.py
```

Run a specific question:
```bash
python autograder.py -q q2
```

Mute output for faster grading:
```bash
python autograder.py --mute
```

### Layouts

You can use different layouts with the `-l` flag. Examples:
- `mediumClassic`
- `smallClassic`
- `testClassic`

## Evaluation Metrics

Autograder evaluates based on:
- Average score across multiple games
- Win rate
- Number of states explored
- Correctness of agent logic via search trees

Each question in the project corresponds to a different agent or evaluation function, and points are awarded accordingly.

## Customization

You can modify the evaluation function in `multi_agents.py` to improve ReflexAgent performance. You can also tune `depth` for Minimax and Expectimax agents and change ghost behavior using `ghost_agents.py`.

## Credits

This project is based on the UC Berkeley CS188 Pacman Projects:
- Developed by John DeNero and Dan Klein
- Additional contributions by Pieter Abbeel, Brad Miller, Nick Hay

You are free to use or extend this code for **educational purposes only**, provided that:
1. You do **not** distribute or publish your solutions.
2. You **retain** this notice.
3. You **credit** the original authors and link to [http://ai.berkeley.edu](http://ai.berkeley.edu).
