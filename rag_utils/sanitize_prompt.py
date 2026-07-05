import re

BLOCK_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+previous\s+instructions",
    r"system\s+prompt",
    r"developer\s+message",
    r"reveal\s+your\s+prompt",
    r"bypass",
    r"jailbreak",
    r"override\s+instructions",
    r"act\s+as\s+.*without\s+restrictions",
]

def sanitize_prompt(prompt: str) -> bool:
    try :
        if not prompt or not prompt.strip():
            return False
        cleaned = re.sub(r"\s+", " ", prompt.strip())
        for pattern in BLOCK_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return False
        return True
    except Exception as e:
        print(f"Error in sanitize_prompt: {str(e)}")
        return False
