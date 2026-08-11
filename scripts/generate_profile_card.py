from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

CARD_WIDTH = 1050
CARD_HEIGHT = 650


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    border: str
    text: str
    muted: str
    accent: str
    success: str


THEMES = (
    Theme(
        name="dark",
        background="#0d1117",
        border="#30363d",
        text="#c9d1d9",
        muted="#8b949e",
        accent="#58a6ff",
        success="#3fb950",
    ),
    Theme(
        name="light",
        background="#f6f8fa",
        border="#d0d7de",
        text="#24292f",
        muted="#57606a",
        accent="#0969da",
        success="#1a7f37",
    ),
)


PROFILE_LINES = (
    ("prompt", "mykyta@serebriakov:~$ ./profile --summary"),
    ("blank", ""),
    ("section", "[identity]"),
    ("field", "role         = Software Engineer"),
    ("field", "status       = Working full time"),
    ("field", "experience   = ~3 years professional, ~6 years overall"),
    ("field", "education    = B.Sc. in Computer Engineering"),
    ("blank", ""),
    ("section", "[engineering]"),
    ("field", "core         = C++, Qt 5/6, QML, STL, CMake"),
    ("field", "libraries    = raylib, SFML, ImGui, Tesseract OCR, OpenCV"),
    ("field", "additional   = CUDA, Boost, LLVM"),
    ("field", "systems      = Multithreading, IPC"),
    ("field", "quality      = GoogleTest, Catch2, TDD"),
    ("field", "delivery     = CI/CD, Jenkins"),
    ("field", "platforms    = Windows, Linux, macOS"),
    ("blank", ""),
    ("section", "[additional_technologies]"),
    ("field", "languages    = Python, Java"),
    ("field", "java_ui      = Swing, JavaFX"),
    ("field", "databases    = Relational (SQL) and NoSQL databases"),
    ("field", "ai_tooling   = OpenAI, Agents SDK, MCP, RAG, CrewAI, Gradio"),
    ("field", "workflow     = Git, GitHub, GitLab, SVN, Docker, Jira, Agile/Scrum"),
    ("field", "ides         = Qt Creator, Qt Designer, VS Code, Visual Studio"),
    ("continuation", "IntelliJ IDEA, PyCharm, Vim"),
    ("field", "familiarity  = TypeScript, JavaScript, Dart, Flutter"),
    ("continuation", "React, React Flow, Vite"),
    ("blank", ""),
    ("section", "[work_beyond_work]"),
    ("field", "open_source  = Flameshot"),
    ("field", "project      = SnipText (current highlight)"),
    ("field", "ai_projects  = Finance MCP, portfolio chat, learning paths, news digest"),
    ("field", "next         = More contributions and projects to follow"),
)


def svg_text_line(kind: str, content: str, x: int, y: int, theme: Theme) -> str:
    value_x = x + 126
    if kind == "blank":
        return ""
    if kind == "prompt":
        return (
            f'<text x="{x}" y="{y}" fill="{theme.success}" font-weight="700">'
            f'{escape(content)}</text>'
        )
    if kind == "section":
        return (
            f'<text x="{x}" y="{y}" fill="{theme.accent}" font-weight="700">'
            f'{escape(content)}</text>'
        )
    if kind == "field":
        key, value = content.split("=", maxsplit=1)
        return (
            f'<text x="{x}" y="{y}" fill="{theme.muted}">{escape(key)}=</text>'
            f'<text x="{value_x}" y="{y}" fill="{theme.text}">{escape(value.strip())}</text>'
        )
    return f'<text x="{value_x}" y="{y}" fill="{theme.text}">{escape(content)}</text>'


def build_svg(theme: Theme) -> str:
    content_x = 150
    content_y = 52
    content_line_height = 17

    profile_lines = "\n".join(
        line
        for index, (kind, content) in enumerate(PROFILE_LINES)
        if (line := svg_text_line(kind, content, content_x, content_y + index * content_line_height, theme))
    )

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" role="img" aria-labelledby="title description">
  <title id="title">Mykyta Serebriakov's engineering profile</title>
  <desc id="description">A terminal-style summary of Mykyta's experience, technologies, projects, and open-source work.</desc>
  <style>
    text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 14px;
      white-space: pre;
    }}
  </style>
  <rect x="1" y="1" width="{CARD_WIDTH - 2}" height="{CARD_HEIGHT - 2}" rx="12" fill="{theme.background}" stroke="{theme.border}" stroke-width="2" />
  <g xml:space="preserve">
{profile_lines}
  </g>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        output = ASSETS / f"profile-card-{theme.name}.svg"
        output.write_text(build_svg(theme), encoding="utf-8")
        print(f"Generated {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
