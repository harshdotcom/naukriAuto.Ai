def read_file(filepath, default=""):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return default


def get_resume():
    return read_file("data/resume.txt", "")


def get_system_prompt():
    return read_file("data/system_prompt.txt", "You are an AI assistant...")


def get_human_prompt():
    return read_file(
        "data/human_prompt.txt",
        "Resume:\n\"\"\"\n{resume}\n\"\"\"\n\nOptions:\n{options}\n\nQuestion:\n{question}"
    )