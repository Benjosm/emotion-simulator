# Emotion Simulator: Human-Like Memory & Emotion Prototype

A lightweight Python CLI tool that simulates believable emotional responses based on short-term memory and contextual events. No setup required — just describe a scenario and see real-time emotional shifts.

## Features

- **Dynamic Emotion Heatmap**: Visualizes active emotions (happiness, frustration, excitement, etc.)
- **Memory Chain Tracking**: See how recent events influence current emotional state
- **Real-Time Memory Decay**: Older memories fade in influence
- **Zero Config CLI**: Immediate use with auto-generated help
- **Pure Python**: No databases, APIs, or complex dependencies

## Tech Stack

- **Python + Typer**: For instant CLI with `--help` support
- **In-Memory Graph**: Dictionary-based emotion relationships
- **Deque Memory**: O(1) operations for memory add/expire
- **No External APIs**: Fully self-contained

## Quick Start

### 1. Install Dependencies
```bash
pip install typer
```

### 2. Run Simulation
```bash
# Example 1: Positive event
python agent.py --event "You found $20"

# Example 2: Negative event
python agent.py --event "Your flight was canceled"

# Debug mode: View internal state
python agent.py --event "You aced your exam" --debug
```

## Example Output
```
Event: You found $20
New memory added: YOU_FOUND_$_20 (impact: {"happiness":0.4,"excitement":0.3})
Emotions shift: happiness ↑, excitement ↑

Current Emotion Heatmap:
happiness    ██████ 0.40
excitement   ████ 0.30
calm         █ 0.12
```

## Use Cases
- Writers: Test character reactions
- Game Designers: Prototype NPC behaviors
- Psychology Students: Explore emotion dynamics

## How It Works

1. **Event Input**: Text is parsed for emotional keywords.
2. **Memory Update**: Event is stored with emotional impact.
3. **Emotion Propagation**: Triggers related emotions via an internal graph.
4. **Decay**: Older memories lose influence over time.

## License
MIT
