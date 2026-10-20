import json
import sys
import unittest
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_dialplan import build  # noqa: E402
from story_model import validate_story  # noqa: E402


class StoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.story = json.loads((ROOT / "game" / "story.json").read_text(encoding="utf-8"))

    def test_story_is_valid(self) -> None:
        self.assertEqual(validate_story(self.story), [])

    def test_every_decision_has_two_or_three_labeled_choices(self) -> None:
        for node_id, node in self.story["nodes"].items():
            if node.get("end") is True or "next" in node:
                continue
            self.assertIn(set(node["choices"]), ({"1", "2"}, {"1", "2", "3"}), node_id)
            self.assertEqual(set(node["choice_labels"]), set(node["choices"]), node_id)

    def test_automatic_transition_builds_playback_then_goto(self) -> None:
        story = {
            "game": {**self.story["game"], "start_node": "start"},
            "nodes": {
                "start": {"audio": "story/start", "text": "Začátek.", "next": "cil"},
                "cil": {"audio": "story/cil", "text": "Konec.", "end": True},
            },
        }
        self.assertEqual(validate_story(story), [])
        dialplan = build(story)
        self.assertIn("same => n,Goto(telefonni-adventura-cil,s,1)", dialplan)

    def test_audio_exists_and_has_telephone_format(self) -> None:
        audio_root = ROOT / "audio"
        if not audio_root.is_dir():
            self.skipTest("Working TTS audio is intentionally not stored in Git.")

        audio_names = [self.story["game"]["invalid_audio"]]
        audio_names.extend(node["audio"] for node in self.story["nodes"].values())
        self.assertEqual(len(audio_names), len(set(audio_names)))

        for audio_name in audio_names:
            path = audio_root / f"{audio_name}.wav"
            self.assertTrue(path.is_file(), audio_name)
            with wave.open(str(path), "rb") as wav_file:
                self.assertEqual(wav_file.getnchannels(), 1, audio_name)
                self.assertEqual(wav_file.getframerate(), 8000, audio_name)
                self.assertEqual(wav_file.getsampwidth(), 2, audio_name)

    def test_generated_dialplan_is_isolated(self) -> None:
        dialplan = build(self.story)
        self.assertIn("[telefonni-adventura-entry]", dialplan)
        self.assertIn("exten => 555,1,Answer()", dialplan)
        for forbidden in ("System(", "SHELL(", "AGI(", "Dial(", "Record("):
            self.assertNotIn(forbidden, dialplan)


if __name__ == "__main__":
    unittest.main()
