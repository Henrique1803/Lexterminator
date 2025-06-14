from typing import Tuple


class LR0Item:
    def __init__(self, head: str, body: Tuple[str, ...], dot_pos: int):
        self.head = head
        self.body = body
        self.dot_pos = dot_pos

    def __eq__(self, other):
        return (self.head, self.body, self.dot_pos) == (other.head, other.body, other.dot_pos)

    def __hash__(self):
        return hash((self.head, self.body, self.dot_pos))

    def __repr__(self):
        return f"{self.head} → {self.to_string()}"

    def to_string(self):
        before_dot = ' '.join(self.body[:self.dot_pos])
        after_dot = ' '.join(self.body[self.dot_pos:])
        if before_dot and after_dot:
            return f"{before_dot} • {after_dot}"
        elif before_dot:
            return f"{before_dot} •"
        else:
            return f"• {after_dot}"