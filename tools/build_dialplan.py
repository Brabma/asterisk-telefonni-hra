import sys
from pathlib import Path

from story_model import StoryError, load_story, validate_story


def context_name(game_id: str, node_id: str) -> str:
    return f"{game_id}-{node_id}"


def build(story: dict) -> str:
    game = story["game"]
    nodes = story["nodes"]
    game_id = game["id"]
    sound_dir = game["sound_directory"].rstrip("/")
    invalid_audio = f"{sound_dir}/{game['invalid_audio']}"
    start_context = context_name(game_id, game["start_node"])

    lines = [
        "; Generated file. Edit game/story.json, not this dialplan.",
        f"; Game: {game.get('title', game_id)}",
        "",
        f"[{game_id}-entry]",
        f"exten => {game['entry_extension']},1,Answer()",
        f" same => n,Goto({start_context},s,1)",
        "",
    ]

    for node_id, node in nodes.items():
        context = context_name(game_id, node_id)
        audio = f"{sound_dir}/{node['audio']}"
        lines.append(f"[{context}]")
        if node.get("end") is True:
            lines.extend(
                [
                    f"exten => s,1,Playback({audio})",
                    " same => n,Hangup()",
                    "",
                ]
            )
            continue

        if isinstance(node.get("next"), str):
            target_context = context_name(game_id, node["next"])
            lines.extend(
                [
                    f"exten => s,1,Playback({audio})",
                    f" same => n,Goto({target_context},s,1)",
                    "",
                ]
            )
            continue

        lines.extend(
            [
                f"exten => s,1(start),Read(CHOICE,{audio},1,,1,12)",
                " same => n,GotoIf($[\"${CHOICE}\" = \"\"]?invalid)",
            ]
        )
        for key, target in node["choices"].items():
            target_context = context_name(game_id, target)
            lines.append(f" same => n,GotoIf($[\"${{CHOICE}}\" = \"{key}\"]?{target_context},s,1)")
        lines.extend(
            [
                " same => n(invalid),Playback(" + invalid_audio + ")",
                " same => n,Goto(start)",
                "",
            ]
        )

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print("Pouziti: py tools/build_dialplan.py game/story.json build/extensions.conf")
        return 2

    try:
        story = load_story(sys.argv[1])
    except StoryError as exc:
        print(f"CHYBA: {exc}")
        return 1

    errors = validate_story(story)
    if errors:
        for error in errors:
            print(f"CHYBA: {error}")
        return 1

    output = Path(sys.argv[2])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(story), encoding="utf-8", newline="\n")
    print(f"Vytvoren dialplan: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
