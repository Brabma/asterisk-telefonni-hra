import json
import re
from pathlib import Path


SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SAFE_AUDIO = re.compile(r"^[a-zA-Z0-9_./-]+$")
DTMF_KEYS = set("0123456789*#")


class StoryError(ValueError):
    pass


def load_story(path: str | Path) -> dict:
    story_path = Path(path)
    try:
        return json.loads(story_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StoryError(f"Soubor neexistuje: {story_path}") from exc
    except json.JSONDecodeError as exc:
        raise StoryError(
            f"Neplatny JSON na radku {exc.lineno}, sloupci {exc.colno}: {exc.msg}"
        ) from exc


def validate_story(story: dict) -> list[str]:
    errors: list[str] = []
    game = story.get("game")
    nodes = story.get("nodes")

    if not isinstance(game, dict):
        return ["Chybi objekt 'game'."]
    if not isinstance(nodes, dict) or not nodes:
        return ["Chybi neprázdny objekt 'nodes'."]

    game_id = game.get("id")
    if not isinstance(game_id, str) or not SAFE_ID.fullmatch(game_id):
        errors.append("game.id smi obsahovat jen mala pismena, cisla a pomlcky.")

    extension = game.get("entry_extension")
    if not isinstance(extension, str) or not extension.isdigit():
        errors.append("game.entry_extension musi byt retezec slozeny z cislic.")

    sound_directory = game.get("sound_directory")
    if not isinstance(sound_directory, str) or not SAFE_AUDIO.fullmatch(sound_directory):
        errors.append("game.sound_directory obsahuje nepovolene znaky.")

    invalid_audio = game.get("invalid_audio")
    if not isinstance(invalid_audio, str) or not SAFE_AUDIO.fullmatch(invalid_audio):
        errors.append("game.invalid_audio obsahuje nepovolene znaky.")

    invalid_text = game.get("invalid_text")
    if not isinstance(invalid_text, str) or not invalid_text.strip():
        errors.append("game.invalid_text musi obsahovat hlasovou hlasku.")

    start = game.get("start_node")
    if start not in nodes:
        errors.append(f"Startovni uzel '{start}' neexistuje.")

    endings = 0
    for node_id, node in nodes.items():
        if not isinstance(node_id, str) or not SAFE_ID.fullmatch(node_id):
            errors.append(f"Neplatne ID uzlu: {node_id!r}.")
            continue
        if not isinstance(node, dict):
            errors.append(f"Uzel '{node_id}' musi byt objekt.")
            continue

        audio = node.get("audio")
        if not isinstance(audio, str) or not SAFE_AUDIO.fullmatch(audio):
            errors.append(f"Uzel '{node_id}' nema platne audio.")

        text = node.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"Uzel '{node_id}' nema text pro hlasovou nahravku.")

        is_end = node.get("end") is True
        choices = node.get("choices")
        next_node = node.get("next")
        if is_end:
            endings += 1
            if choices:
                errors.append(f"Koncovy uzel '{node_id}' nesmi obsahovat choices.")
            continue

        if isinstance(next_node, str):
            if choices:
                errors.append(f"Uzel '{node_id}' nesmi mit soucasne next a choices.")
            if next_node not in nodes:
                errors.append(f"Uzel '{node_id}' miri pres next na neznamy uzel '{next_node}'.")
            continue

        if not isinstance(choices, dict) or not choices:
            errors.append(f"Uzel '{node_id}' musi mit volby nebo end: true.")
            continue

        choice_labels = node.get("choice_labels")
        if not isinstance(choice_labels, dict) or set(choice_labels) != set(choices):
            errors.append(f"Uzel '{node_id}' musi mit popisek pro kazdou volbu.")
        elif any(not isinstance(label, str) or not label.strip() for label in choice_labels.values()):
            errors.append(f"Uzel '{node_id}' obsahuje prazdny popisek volby.")

        for key, target in choices.items():
            if key not in DTMF_KEYS:
                errors.append(f"Uzel '{node_id}' pouziva neplatnou DTMF klavesu '{key}'.")
            if target not in nodes:
                errors.append(f"Uzel '{node_id}', volba '{key}', miri na neznamy uzel '{target}'.")

    if endings == 0:
        errors.append("Pribeh nema zadny koncovy uzel.")

    if start in nodes:
        reachable: set[str] = set()
        pending = [start]
        while pending:
            node_id = pending.pop()
            if node_id in reachable or node_id not in nodes:
                continue
            reachable.add(node_id)
            node = nodes[node_id]
            if isinstance(node, dict) and isinstance(node.get("choices"), dict):
                pending.extend(node["choices"].values())
            if isinstance(node, dict) and isinstance(node.get("next"), str):
                pending.append(node["next"])
        for node_id in sorted(set(nodes) - reachable):
            errors.append(f"Uzel '{node_id}' neni dosazitelny ze startu.")

    return errors
