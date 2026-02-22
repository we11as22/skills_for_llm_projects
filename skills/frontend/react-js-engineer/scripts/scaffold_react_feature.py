#!/usr/bin/env python3
"""Generate a React feature module scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path

API_TEMPLATE = """import {{ apiClient }} from \"@/shared/api/client\";

export type {pascal}Dto = {{
  id: string;
  title: string;
}};

export async function fetch{pascal}List(): Promise<{pascal}Dto[]> {{
  const response = await apiClient.get<{pascal}Dto[]>(\"/{kebab}\");
  return response.data;
}}
"""

MODEL_TEMPLATE = """export type {pascal} = {{
  id: string;
  title: string;
}};
"""

HOOKS_TEMPLATE = """import {{ useQuery }} from \"@tanstack/react-query\";
import {{ fetch{pascal}List }} from \"./api\";

export function use{pascal}List() {{
  return useQuery({{
    queryKey: [\"{kebab}\"],
    queryFn: fetch{pascal}List,
  }});
}}
"""

COMPONENT_TEMPLATE = """import {{ use{pascal}List }} from \"../hooks\";

export function {pascal}Panel() {{
  const {{ data, isLoading, isError }} = use{pascal}List();

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Failed to load data.</p>;

  return (
    <section>
      <h2>{pascal}</h2>
      <ul>
        {{data?.map((item) => (
          <li key={{item.id}}>{{item.title}}</li>
        ))}}
      </ul>
    </section>
  );
}}
"""

TEST_TEMPLATE = """import {{ describe, expect, it }} from \"vitest\";

describe(\"{pascal} feature\", () => {{
  it(\"has stable placeholder test\", () => {{
    expect(true).toBe(true);
  }});
}});
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("_", "-").split("-") if part)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature", help="Feature name in kebab-case, e.g. order-history")
    parser.add_argument(
      "--src",
      type=Path,
      default=Path("src"),
      help="Source directory root",
    )
    args = parser.parse_args()

    kebab = args.feature.strip().lower()
    pascal = to_pascal(kebab)
    feature_dir = args.src / "features" / kebab

    write(feature_dir / "api.ts", API_TEMPLATE.format(kebab=kebab, pascal=pascal))
    write(feature_dir / "model.ts", MODEL_TEMPLATE.format(pascal=pascal))
    write(feature_dir / "hooks.ts", HOOKS_TEMPLATE.format(kebab=kebab, pascal=pascal))
    write(
      feature_dir / "components" / f"{pascal}Panel.tsx",
      COMPONENT_TEMPLATE.format(pascal=pascal),
    )
    write(feature_dir / "__tests__" / f"{kebab}.test.ts", TEST_TEMPLATE.format(pascal=pascal))

    print(f"React feature scaffolded: {feature_dir}")


if __name__ == "__main__":
    main()
