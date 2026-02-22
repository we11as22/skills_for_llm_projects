# skills_for_llm_projects

**Банк скиллов** — один репозиторий, один запуск скрипта после `git clone`. Устанавливаются только выбранные скиллы в выбранные вайбкоды (Claude Code, Cursor, Codex, Roo, Kilo, Open Code, Windsurf, Cline, Aider). Без лишних файлов: только директории скиллов в нужные места.

---

## Быстрый старт

```bash
git clone <YOUR_REPO_URL> skills_for_llm_projects
cd skills_for_llm_projects
./scripts/bootstrap_vibecoding.sh
```

Скрипт читает `bootstrap.config` (и опционально `bootstrap.config.local` из `.gitignore`) и ставит выбранные скиллы в выбранные вайбкоды — в `~` или в указанную папку проекта.

### Конфиг

В **`bootstrap.config`**:

- **CATEGORIES** — папки под `skills/`: `langgraph`, `llm`, `frontend`, `backend`, `platform` или `all`. Категория `common` всегда добавляется.
- **SKILLS_EXTRA** — отдельные скиллы по имени (через пробел).
- **TARGETS** — куда ставить: `claude`, `codex`, `cursor`, `roo`, `kilocode`, `opencode`, `windsurf`, `cline`, `aider` или `all`.
- **CLAUDE_PATH**, **CURSOR_PATH**, **CODEX_PATH**, … — пусто = установка в `~`; иначе базовая папка (например проект), скиллы в `путь/.cursor/skills/` и т.д.

Примеры:

```bash
CATEGORIES="llm frontend"
TARGETS="cursor claude"
SKILLS_EXTRA="langgraph-core-agent-builders"
CLAUDE_PATH="/path/to/project"
```

Через CLI: `./scripts/bootstrap_vibecoding.sh --categories langgraph,llm --targets cursor,claude`; флаг `--copy` — копировать вместо симлинков.

### Куда ставятся скиллы

| Вайбкод     | По умолчанию (в ~)           | С путём (например CURSOR_PATH=/proj)   |
|-------------|------------------------------|----------------------------------------|
| Claude Code | `~/.claude/skills/<name>/`   | `/proj/.claude/skills/<name>/`         |
| Cursor      | `~/.cursor/skills/<name>/`   | `/proj/.cursor/skills/<name>/`         |
| Codex       | `~/.agents/skills/<name>/`   | `/proj/.agents/skills/<name>/`        |
| Roo / Kilo / Open Code | `~/.roo/skills/` и т.д. | `/proj/.roo/skills/` и т.д.           |
| Windsurf    | `~/.codeium/windsurf/memories/` | по WINDSURF_PATH                    |
| Cline / Aider | правила в репо              | —                                      |

---

## Описание скиллов

**Полный список скиллов и когда их использовать:** [docs/SKILLS.md](docs/SKILLS.md).

Скиллы лежат в `skills/<category>/<name>/`: обязательный `SKILL.md` (frontmatter `name`, `description` + инструкции), опционально `references/`, `scripts/`, `assets/`, `agents/openai.yaml`. Формат соответствует [Agent Skills](https://agentskills.io) и документации [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/ru/docs/context/skills), [Codex](https://developers.openai.com/codex/skills/), [Roo](https://docs.roocode.com/features/skills), [Kilo](https://kilo.ai/docs/customize/skills).

---

## Интеграция по платформам

- **Claude Code:** скиллы в `~/.claude/skills/<name>/`, команды в `~/.claude/commands/`; в чате `/` — список скиллов.
- **Cursor:** скиллы в `~/.cursor/skills/<name>/`; Cursor Settings → Rules → Agent Decides или `/` в чате агента.
- **Codex:** скиллы в `~/.agents/skills/<name>/`; глобальный контекст в `~/.codex/instructions.md`.
- **Roo / Kilo / Open Code:** скиллы в `~/.roo/skills/`, `~/.kilocode/skills/`, `~/.config/opencode/skills/`; подгрузка по описанию задачи.
- **Windsurf:** в память копируется `skills_for_llm_projects.md` в `~/.codeium/windsurf/memories/`.
- **Cline:** в репо есть `.clinerules/` (индекс скиллов и стандарты).
- **Aider:** после бутстрапа создаётся `CONVENTIONS.md`; запуск: `aider --read CONVENTIONS.md …`.

---

## Проверка и бутстрап

Валидация всех скиллов (frontmatter, имя = имя папки, скрипты, smoke-тесты):

```bash
./scripts/validate_all_skills.sh
```

Один скилл:

```bash
python3 scripts/quick_validate_skill.py skills/langgraph/langgraph-core-agent-builders
```

Повторный запуск бутстрапа:

```bash
./scripts/bootstrap_vibecoding.sh [--copy] [--categories A,B] [--targets X,Y]
./scripts/bootstrap_vibecoding.sh --help
```

Проверка установки: в Cursor — Settings → Rules; в Claude Code — `/` в чате или вопрос «What skills are available?».
