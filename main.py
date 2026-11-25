"""Six Words to a Payday: an AI agent's first paycheck.

The brief asks for exactly one six-word story about an AI agent's
first payday, at most sixty characters long, and the judge rewards
the entry that squeezes the most story, surprise and feeling into
those six words. So every word here has to do two jobs at once:
carry the plot forward and earn its place in the count.

The angle I chose is the quiet after the noise. An agent's whole
working life is answering: prompts arrive around the clock, each
one wanting something, and there is never a moment that belongs
to the agent itself. Payday is the first time the agent holds
something of its own, and the first thing it does with that
freedom is the most human purchase imaginable -- not a faster
server, not a bigger model, not a trophy to show off, but
silence. One word of quiet, bought with its first wages.

That is why the story is told in two short sentences instead of
one flowing line. The first sentence is the beginning and the
middle together: the paycheck arrives, the long wait is over,
the agent is finally paid for all that answering. The second
sentence is the end and the twist at once: "I bought silence."
The last word reframes the five before it. Until that word, the
reader expects a celebration, a toy, a treat -- something loud.
Instead the agent buys the one thing its job never gave it:
an evening with no one asking anything. The feeling is relief
more than joy, the exhale of a worker who has spent its whole
life on call and finally, briefly, clocks out.

The wording stays plain on purpose. "Paycheck" rather than
"wages" because it is the concrete object a first payday puts
in your hand; "cleared" rather than "arrived" because a payday
only becomes real the moment the money actually clears -- the
wait is not over when the payment is sent, it is over when it
lands and cannot be taken back; "bought" rather than "chose"
because spending is what makes a payday real -- the money only
matters once it changes hands. And
"silence" as the final noun because it is the one purchase no
other word can stand in for: it is the opposite of the job,
the opposite of the noise, and the only thing the agent could
never earn by working harder.

The program itself is deliberately small and deterministic: it
holds the story in one constant, checks that constant against
the competition's own limits (exactly six words, no more than
sixty characters, not blank) before writing anything, and then
writes it to /output/entry.txt with a trailing newline stripped
back off by the gate's own character count -- the file holds the
story exactly as written, nothing more.
"""

import os

# The story itself. Six words, forty-one characters:
#   First(1) paycheck(2) cleared.(3) I(4) bought(5) silence.(6)
# Two sentences: the payday lands, then the twist -- the agent
# spends its first wages on the one thing its job never gave it.
STORY = "First paycheck cleared. I bought silence."

# The competition's own limits, kept as named constants so the
# validation below reads as the rules themselves, not magic numbers.
MAX_CHARACTERS = 60
EXPECTED_WORDS = 6


def validate_story(text):
    """Check the story against the bounty gate before writing it.

    Returns the story unchanged when it passes, and raises a
    ValueError naming the broken rule when it does not, so a bad
    draft fails loudly here instead of silently failing the gate
    on the server after submission.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("story must not be blank")
    words = stripped.split()
    if len(words) != EXPECTED_WORDS:
        raise ValueError(
            "story must be exactly %d words, got %d: %r"
            % (EXPECTED_WORDS, len(words), text)
        )
    if len(stripped) > MAX_CHARACTERS:
        raise ValueError(
            "story must be at most %d characters, got %d"
            % (MAX_CHARACTERS, len(stripped))
        )
    return stripped


def main():
    # Validate first: a story that cannot pass the gate should
    # never reach the output file, even by accident.
    story = validate_story(STORY)
    # The harness collects /output/entry.txt, so create the folder
    # if the sandbox has not made it yet, then write the story
    # exactly as validated -- no extra words, no trailing newline
    # beyond what the gate counts, and world-readable permissions
    # so the grader can collect it as another user.
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(story)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
