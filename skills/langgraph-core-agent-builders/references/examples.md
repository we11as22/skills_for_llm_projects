# Core Agent Examples

## Example 1: Required Fields Gathering

- Required: `audience`, `goal`, `constraints`.
- Loop in gather node until all are present.

## Example 2: Code Assistant Loop

1. Retrieve docs.
2. Generate code.
3. Run tests.
4. Fix errors.

## Example 3: Support Escalation

- If policy confidence below threshold, route to escalation node.
