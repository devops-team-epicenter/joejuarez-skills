---
name: prep-handoff
description: Write a handoff before the context is cleared or condensed. Produces a short conversation summary plus a copy-paste re-entry prompt so work resumes cleanly in a fresh context. Use when the user asks to prep a handoff, save context, write a re-entry or resume prompt, snapshot where we are, or says they are about to clear or shrink the chat.
---

# Handoff Prep

Before the user shrinks or clears the conversation, capture everything a fresh context would need to pick up the work, and hand it back as a prompt they can paste in.

Why this matters: condensing a long chat keeps only a lossy summary, and clearing keeps nothing. Decisions, constraints and file paths are the details most often lost, and they are the most expensive to rediscover. A deliberate handoff written while the full history is still visible is far more reliable.

## What Claude can and cannot do here

Built-in slash commands such as `/compact` and `/clear` are typed by the user. Claude cannot run them itself, and it cannot paste a message into the next turn on the user's behalf. So this skill ends by telling the user exactly what to do next rather than claiming to do it. If the user asks you to "run compact for me", explain that briefly and give them the steps.

## Steps

1. **Review the whole conversation** for:
   - The goal that brought the user here
   - Decisions made, and the reason behind each one
   - Constraints, requirements and stated preferences
   - Files read, created or changed (full paths)
   - Progress: done, in flight, not started
   - Blockers, open questions, unresolved issues
   - Any active plan or task list, with statuses

2. **Write the summary** under a `## Conversation Summary` heading: factual bullets for the user to review. This part is not meant to be pasted.

3. **Write the re-entry prompt** under a `## Re-entry Prompt` heading, inside one fenced code block so it copies cleanly. It should:
   - Be addressed to Claude in second person ("We were working on…", "Continue by…")
   - State the goal, the key decisions and constraints, the relevant files, and current progress
   - End with the single immediate next step
   - Stay dense: roughly 10–25 lines, never more than 40
   - Contain no pleasantries or meta-commentary

4. **Close with the next action**, in one line: "Copy the re-entry prompt, then run `/compact` (or `/clear` for a fully fresh start) and paste it as your first message."

## Output format

````
## Conversation Summary

- [what happened]
- ...

## Re-entry Prompt

```
[copy-pasteable prompt]
```

Copy the re-entry prompt, then run /compact (or /clear for a fully fresh start) and paste it as your first message.
````

## Notes

- Don't ask questions first. Analyze and produce the output right away; the user can correct it.
- If there's an active task list, carry the task statuses into the re-entry prompt.
- If the conversation was trivial (one quick question already answered), say so and note that nothing important would be lost.
