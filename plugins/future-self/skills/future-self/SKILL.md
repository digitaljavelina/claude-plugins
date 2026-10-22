---
name: future-self
description: Run the Future-Self Prompt, a four-step goal exercise. The user writes what they want a few years out, Claude narrates a day in that life, the user marks what feels real, and Claude turns those parts into a daily routine and a 90-day plan. Saves every run to one running Obsidian note and compares against the last run. Use when the user says "future self", "run the future-self prompt", "day in my life 3 years from now", "quarterly goal reset", "90-day plan from my goals", or starts a new quarter and wants to re-run it.
---

# Future-Self Prompt

A goal list lives in your head. A day you can picture feels real enough to act on. So this skill asks for the story first and the plan second. Adapted from the anaverse.ai "Future-Self Prompt" kit.

## Where runs are saved

One running note: `/Users/michaelhenry/Obsidian/Living/Future Self.md`. Create it on the first run. Each run is a new `## YYYY-MM-DD (QN YYYY)` section added at the top, under the frontmatter, so the newest run reads first. Follow vault rules: one paragraph per line, never hard-wrap.

## The steps

Run them in order. Steps 1 and 3 are the user's. Do not skip ahead or do their part for them.

**1. Write down what you want.** Ask the user to write everything they want a few years from now: who they are, what they have built, what their days look like. Tell them to go big. If a previous run exists, show its "What I wrote" line so they can edit rather than start cold. Wait for their answer.

**2. Ask for the day, not the plan.** Default horizon is 3 years unless the user names another. Treat what they wrote as if they had sent:

    Create a day in my life 3 years from now based on this.

Write one day, morning to evening, in second person and present tense. Concrete times, places, people, small sensory details. A story, never a to-do list. About 200 to 300 words.

**3. Find what feels real.** Ask the user to read it slowly and name the parts that feel real, not impossible. Those parts are what they actually want. The rest is noise to drop. Wait for their answer. If they say "all of it", ask which two or three parts they would miss most.

**4. Turn it into a daily routine.** Treat it as if they had sent:

    Now give me a daily routine and the 90-day plan to start moving toward it.

Build only from the parts the user kept in step 3. Give:

- A daily routine: a short list of blocks with times, sized for a real week, not the dream week.
- A 90-day plan in three phases (Weeks 1-2, Weeks 3-6, Weeks 7-12), each with one or two concrete actions.
- "Start this week": the one or two things to do in the next seven days.

## Save and compare

Append the run to the note with these headings: What I wrote, The day, What felt real, Daily routine, 90-day plan, Start this week.

If an earlier run exists, add a "Drift since last run" section: what got closer, what changed, what dropped out. The drift shows what the user actually cares about. Reset the 90-day plan off the newest run only.

Tell the user the note path when done, and suggest re-running at the start of next quarter.
