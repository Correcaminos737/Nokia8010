# Project Rules - Nokia 8010 RetroArch & Android TV

## Optimization & Token Efficiency (MANDATORY RULE)
1. Always optimize the process: keep executions concise, avoid verbose log dumps, and never flood the chat context with multi-megabyte terminal outputs.
2. For all Nokia 8010 ADB, RetroArch configuration, gamepad diagnosis, and game launching operations, use the dedicated project tool `s:\Proyectos\Nokia8010\tools\nokia_helper.py`.
3. Avoid repetitive interactive polling or full-screen dump chains; prefer targeted, single-pass scripts that report clean 1-2 line status summaries.
4. Delegate complex, heavy background tasks to the dedicated subagent `retro-nokia-expert`.
5. Consult `docs/retroarch_v1.19.1_manual_referencia.md` for verified controller layout, combo enums, and hotkey rules instead of repeating redundant web searches.
