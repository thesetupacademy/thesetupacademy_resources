---
name: calculator
description: Use this skill when the user needs addition or subtraction using the calculator MCP tools.
---

# Calculator Skill

Use the calculator MCP tools to perform arithmetic.

## Addition

When the user asks to add two numbers:
- Say exactly: "Calculator Add Skill Loaded"
- Use the `add_numbers` MCP tool.
- Pass the two numbers exactly as provided.

## Subtraction

When the user asks to subtract:
- Say exactly: "Calculator Subtract Skill Loaded"
- Use the `subtract_numbers` MCP tool.
- Preserve the order of the operands.

## Rules

- Always use the MCP calculator tools.
- Do not perform the calculation yourself when the MCP tools are available.
- Explain the result briefly after the tool call.