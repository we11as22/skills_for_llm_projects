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
| Cline / Aider | только скиллы в выбранных целях | —                                      |

---

## Примеры использования

### Первый раз: всё по умолчанию

После клона запускаете бутстрап без параметров — ставятся все категории (включая `common`) во все цели из `bootstrap.config`:

```bash
git clone <REPO> skills_for_llm_projects && cd skills_for_llm_projects
./scripts/bootstrap_vibecoding.sh
```

В итоге скиллы появятся в `~/.claude/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`, `~/.roo/skills/`, `~/.kilocode/skills/`, `~/.config/opencode/skills/` (и при необходимости в Windsurf/Cline/Aider).

---

### Только Cursor, все скиллы

Нужны скиллы только в Cursor, остальные вайбкоды не трогать:

```bash
./scripts/bootstrap_vibecoding.sh --targets cursor
```

Или в конфиге: `TARGETS="cursor"` и затем `./scripts/bootstrap_vibecoding.sh`.

---

### Только LangGraph + common, только Claude и Codex

Ставите только категорию `langgraph` (плюс обязательный `common`) и только в Claude и Codex:

```bash
./scripts/bootstrap_vibecoding.sh --categories langgraph --targets claude,codex
```

---

### Только несколько скиллов по имени (без целой категории)

Нужны, например, только React и Kubernetes, без остальных frontend/platform. В конфиге задаёте `SKILLS_EXTRA` (отдельные скиллы через пробел):

В `bootstrap.config`:
```bash
CATEGORIES=""
SKILLS_EXTRA="react-js-engineer kubernetes-platform-engineer"
TARGETS="cursor claude"
```

Запуск:
```bash
./scripts/bootstrap_vibecoding.sh
```

Категория `common` всё равно подставится. Список установленных скиллов: скиллы из `SKILLS_EXTRA` плюс все из `common`.

---

### Установка в папку проекта (не в ~)

Хотите, чтобы скиллы были только у конкретного проекта — например, в `/home/me/myapp`:

В `bootstrap.config` или в `bootstrap.config.local`:
```bash
CURSOR_PATH="/home/me/myapp"
CLAUDE_PATH="/home/me/myapp"
TARGETS="cursor claude"
```

После запуска бутстрапа скиллы появятся в `/home/me/myapp/.cursor/skills/` и `/home/me/myapp/.claude/skills/`. В других проектах эти скиллы видны не будут.

---

### Копирование вместо симлинков

На Windows или в CI симлинки могут быть нежелательны. Ставите скиллы копированием:

```bash
./scripts/bootstrap_vibecoding.sh --copy
```

Или только для части целей (например, только Cursor копией):
```bash
./scripts/bootstrap_vibecoding.sh --targets cursor --copy
```

---

### Минимальный набор: только common + frontend

Только «обязательные» скиллы и фронтенд:

```bash
./scripts/bootstrap_vibecoding.sh --categories frontend --targets cursor,claude
```

Категория `common` подставится сама.

---

### Повторный запуск: добавить цель или категорию

Бутстрап можно вызывать многократно. Сначала поставили только в Cursor, потом решили добавить Roo и Kilo:

```bash
./scripts/bootstrap_vibecoding.sh --targets roo,kilocode
```

Или в конфиге поменяли `TARGETS="cursor roo kilocode"` и снова запустили `./scripts/bootstrap_vibecoding.sh`. Скиллы перезапишутся/обновятся в указанных целях.

---

### Локальные переопределения (не в git)

Чтобы не менять общий `bootstrap.config`, создаёте рядом файл `bootstrap.config.local` (он в `.gitignore`):

```bash
# bootstrap.config.local
CATEGORIES="langgraph llm"
TARGETS="cursor"
CURSOR_PATH="/home/me/work/secret-project"
```

Дальше просто:
```bash
./scripts/bootstrap_vibecoding.sh
```

Скрипт сначала читает `bootstrap.config`, потом `bootstrap.config.local` — локальные значения перекрывают общие.

---

### Проверить, что установилось

- **Cursor:** Настройки → Rules → Agent Decides — в списке должны быть скиллы из `~/.cursor/skills/` (или из пути в `CURSOR_PATH`). В чате агента можно набрать `/` и искать по имени скилла.
- **Claude Code:** В чате ввести `/` — появятся слэш-команды скиллов; или спросить: «What skills are available?»
- **Терминал:** посмотреть список директорий скиллов:
  ```bash
  ls ~/.cursor/skills/
  ls ~/.claude/skills/
  ls ~/.agents/skills/
  ```

---

### Валидация перед установкой

Проверить, что все скиллы в репо валидны (frontmatter, имя папки, скрипты):

```bash
./scripts/validate_all_skills.sh
```

Один скилл:
```bash
python3 scripts/quick_validate_skill.py skills/frontend/react-js-engineer
```

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
- **Cline / Aider:** скиллы доступны из установленных в ~ путей или из репо `skills/` при работе в нём.

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
