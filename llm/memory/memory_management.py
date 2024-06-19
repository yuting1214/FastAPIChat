from typing import List, Tuple, Optional

def format_memory(history: List[Tuple[str, Optional[str]]], window_size: int = 3) -> List[Tuple[str, str]]:
    """
    Format the memory format in chat and arena mode.

    Args:
        history (List[Tuple[str, Optional[str]]]): The list of messages containing in the message history.
    
    Returns:
        List[Tuple[str, str]]: The formatted messages as a memory.
        
    """
    memory_messages = []
    for user_message, assistant_message in history[-window_size:]:
        memory_messages.append(('human', user_message))
        memory_messages.append(('ai', assistant_message))
    return memory_messages
