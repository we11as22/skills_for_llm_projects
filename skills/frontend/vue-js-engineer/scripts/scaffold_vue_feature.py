#!/usr/bin/env python3
"""Generate a Vue feature module scaffold using Composition API and Pinia."""

from __future__ import annotations

import argparse
from pathlib import Path

API_TEMPLATE = """import axios from \"axios\";

export type {pascal}Dto = {{
  id: string;
  title: string;
}};

export async function fetch{pascal}List(): Promise<{pascal}Dto[]> {{
  const response = await axios.get<{pascal}Dto[]>(\"/{kebab}\");
  return response.data;
}}
"""

COMPOSABLE_TEMPLATE = """import {{ ref, onMounted }} from \"vue\";
import {{ fetch{pascal}List }} from \"../api\";

export function use{pascal}List() {{
  const items = ref([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function load() {{
    isLoading.value = true;
    error.value = null;
    try {{
      items.value = await fetch{pascal}List();
    }} catch (exc) {{
      error.value = exc instanceof Error ? exc.message : \"Unknown error\";
    }} finally {{
      isLoading.value = false;
    }}
  }}

  onMounted(load);
  return {{ items, isLoading, error, load }};
}}
"""

STORE_TEMPLATE = """import {{ defineStore }} from \"pinia\";

export const use{pascal}Store = defineStore(\"{kebab}\", {{
  state: () => ({{ selectedId: null as string | null }}),
  actions: {{
    select(id: string) {{
      this.selectedId = id;
    }},
  }},
}});
"""

COMPONENT_TEMPLATE = """<script setup lang=\"ts\">
import {{ use{pascal}List }} from \"../composables/use{pascal}List\";

const {{ items, isLoading, error }} = use{pascal}List();
</script>

<template>
  <section>
    <h2>{pascal}</h2>
    <p v-if=\"isLoading\">Loading...</p>
    <p v-else-if=\"error\">{{{{ error }}}}</p>
    <ul v-else>
      <li v-for=\"item in items\" :key=\"item.id\">{{{{ item.title }}}}</li>
    </ul>
  </section>
</template>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("_", "-").split("-") if part)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature", help="Feature name in kebab-case")
    parser.add_argument("--src", type=Path, default=Path("src"), help="Source root")
    args = parser.parse_args()

    kebab = args.feature.strip().lower()
    pascal = to_pascal(kebab)
    base = args.src / "features" / kebab

    write(base / "api.ts", API_TEMPLATE.format(pascal=pascal, kebab=kebab))
    write(
        base / "composables" / f"use{pascal}List.ts",
        COMPOSABLE_TEMPLATE.format(pascal=pascal),
    )
    write(base / "stores" / f"{kebab}.store.ts", STORE_TEMPLATE.format(pascal=pascal, kebab=kebab))
    write(base / "components" / f"{pascal}Panel.vue", COMPONENT_TEMPLATE.format(pascal=pascal))

    print(f"Vue feature scaffolded: {base}")


if __name__ == "__main__":
    main()
