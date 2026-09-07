---
description: "One sentence naming the prompt contract this entry point assembles."
argument-hint: "__OPTIONAL_ARGUMENT_HINT__"
allowed-tools: "__BOUNDED_BUILDER_INVOCATION__"
---

Run `python3 scripts/prompt-input.py __CONTRACT_IDENTIFIER__` from the repository
root and use its output as the request. The builder reads only the inputs
`.agents/prompts/__CONTRACT_IDENTIFIER__.md` declares, makes no model call, and
writes nothing to the repository or to Git state. When it exits non-zero, report
its diagnostic instead of producing a draft.
