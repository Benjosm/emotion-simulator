import typer
from collections import deque
from typing import Dict, List
import json

app = typer.Typer()

# In-memory emotion graph (no external libraries)
EMOTION_GRAPH: Dict[str, Dict[str, float]] = {
    "happiness": {"excitement": 0.5, "calm": 0.3},
    "frustration": {"anger": 0.6, "sadness": 0.4},
    "excitement": {"happiness": 0.4, "anxiety": 0.3},
    "sadness": {"reflection": 0.5, "fatigue": 0.4},
    "fear": {"anxiety": 0.7, "caution": 0.5}
}

# Base emotional state
EMOTIONS: Dict[str, float] = {
    "happiness": 0.0,
    "frustration": 0.0,
    "excitement": 0.0,
    "sadness": 0.0,
    "fear": 0.0,
    "calm": 0.0,
    "anger": 0.0,
    "anxiety": 0.0,
    "reflection": 0.0,
    "fatigue": 0.0,
    "caution": 0.0
}

# Short-term memory with O(1) append and pop
MEMORY: deque = deque(maxlen=5)  # Keep last 5 events

# Map event keywords to emotion impacts
EVENT_IMPACTS: Dict[str, Dict[str, float]] = {
    "found": {"happiness": 0.4, "excitement": 0.3},
    "aced": {"happiness": 0.6, "excitement": 0.5},
    "won": {"happiness": 0.7, "excitement": 0.6},
    "died": {"sadness": 0.6, "grief": 0.5},
    "broke": {"frustration": 0.5, "sadness": 0.3},
    "canceled": {"frustration": 0.7, "disappointment": 0.5},
    "lost": {"sadness": 0.6, "frustration": 0.4},
    "scared": {"fear": 0.8, "anxiety": 0.6},
    "hurt": {"pain": 0.7, "sadness": 0.5}
}

def extract_keywords(event: str) -> List[str]:
    """Extract triggering keywords from event text."""
    words = event.lower().split()
    return [word.strip(".,!?\"'") for word in words]

def update_emotions_from_event(event: str):
    """Update emotional state based on event keywords."""
    keywords = extract_keywords(event)
    impacts = {}
    for word in keywords:
        if word in EVENT_IMPACTS:
            for emotion, strength in EVENT_IMPACTS[word].items():
                impacts[emotion] = impacts.get(emotion, 0.0) + strength
    for emotion, delta in impacts.items():
        if emotion in EMOTIONS:
            EMOTIONS[emotion] += delta
        else:
            EMOTIONS[emotion] = delta  # Add new derived emotion
    return impacts

def propagate_emotions():
    """Propagate emotions through the emotion graph."""
    new_impacts = {}
    for emotion, strength in EMOTIONS.items():
        if strength > 0.1 and emotion in EMOTION_GRAPH:
            for linked, multiplier in EMOTION_GRAPH[emotion].items():
                impact = strength * multiplier
                new_impacts[linked] = new_impacts.get(linked, 0.0) + impact
    for emotion, delta in new_impacts.items():
        EMOTIONS[emotion] = EMOTIONS.get(emotion, 0.0) + delta

def decay_memories():
    """Reduce emotional impact of older memories (simplified decay)."""
    decay_factor = 0.9
    for memory in MEMORY:
        for emotion in memory["impacts"]:
            if emotion in EMOTIONS:
                EMOTIONS[emotion] *= decay_factor

@app.command()
def main(event: str = typer.Option(None, "--event", "-e"),
         debug: bool = typer.Option(False, "--debug", "-d")):
    """
    Simulate emotional response to an event.
    Example: python agent.py --event "You found $20"
    Use --debug to see internal state.
    """
    if event is None:
        typer.echo("No event provided. Use --event 'description'")
        raise typer.Exit()

    typer.echo(f"Event: {event}")

    # Decay existing memories
    decay_memories()

    # Extract impact from event
    impacts = update_emotions_from_event(event)

    # Add to memory
    memory_entry = {
        "event": event.upper().replace(" ", "_"),
        "impacts": impacts
    }
    MEMORY.append(memory_entry)
    impact_str = ", ".join([f"{k} ↑" for k in impacts.keys()])
    typer.echo(f"New memory added: {memory_entry['event']} (impact: {json.dumps(impacts, separators=(',', ':'))})")
    if impact_str:
        typer.echo(f"Emotions shift: {impact_str}")

    # Propagate through emotion graph
    propagate_emotions()

    if debug:
        typer.echo("\n--- DEBUG MODE ---")
        typer.echo("Current Emotion Graph:")
        typer.echo(json.dumps(EMOTION_GRAPH, indent=2))
        typer.echo("Current Memory:")
        typer.echo(json.dumps(list(MEMORY), indent=2))
        typer.echo("Current Emotional State:")
        active_emotions = {k: round(v, 2) for k, v in EMOTIONS.items() if v > 0.1}
        typer.echo(json.dumps(active_emotions, indent=2))

    # Show top emotions
    typer.echo("\nCurrent Emotion Heatmap:")
    sorted_emotions = sorted(EMOTIONS.items(), key=lambda x: x[1], reverse=True)
    for emo, val in sorted_emotions:
        if val > 0.1:
            bar = "█" * int(val * 10)
            typer.echo(f"{emo:12} {bar} {val:.2f}")

if __name__ == "__main__":
    app()
