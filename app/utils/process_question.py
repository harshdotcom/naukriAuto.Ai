import re

def normalize(text):
    text = text.lower()
    #Find every character that is not a lowercase letter, a digit, or a space, and replace it with nothing
    # text = re.sub(r'[^a-z0-9 ]', '', text)
    return text.strip()



def build_query(question: str, options: list[str] | None = None) -> str:
    # normalize question
    q = normalize(question)

    if not options:
        return q
    
    # normalize + clean options
    cleaned_opts = [
        opt.strip().lower()
        for opt in options
        if opt and opt.strip()
    ]

    # sort to avoid order issues
    cleaned_opts.sort()

    # join everything into one string
    return q + " | " + " | ".join(cleaned_opts)