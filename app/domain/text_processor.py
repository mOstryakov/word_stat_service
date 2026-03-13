import re
from dataclasses import dataclass, field
from typing import Dict, List
import pymorphy3

morph = pymorphy3.MorphAnalyzer()


@dataclass
class WordStats:
    total_count: int = 0
    line_distribution: Dict[int, int] = field(default_factory=dict)


class TextProcessor:
    def __init__(self):
        self.stats: Dict[str, WordStats] = {}
        self.total_lines = 0

    def process_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                self._process_line(line, idx)
                self.total_lines = idx + 1
        return self._prepare_result()

    def _process_line(self, line: str, line_idx: int):
        words = re.findall(r"[а-яА-ЯёЁa-zA-Z0-9]+", line.lower())
        for word in words:
            parsed = morph.parse(word)[0]
            lemma = parsed.normal_form

            if lemma not in self.stats:
                self.stats[lemma] = WordStats()

            self.stats[lemma].total_count += 1
            self.stats[lemma].line_distribution[line_idx] = (
                self.stats[lemma].line_distribution.get(line_idx, 0) + 1
            )

    def _prepare_result(self) -> List[dict]:
        result = []
        for lemma, stat in self.stats.items():
            distribution = [
                str(stat.line_distribution.get(i, 0))
                for i in range(self.total_lines)
            ]
            result.append(
                {
                    "lemma": lemma,
                    "total": stat.total_count,
                    "distribution": ",".join(distribution),
                }
            )
        return sorted(result, key=lambda x: x["total"], reverse=True)
