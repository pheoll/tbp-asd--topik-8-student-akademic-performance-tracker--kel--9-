from src.data_structures.stack import Stack

def test_stack_operations():
    stack = Stack()
    
    assert stack.is_empty() is True
    assert len(stack) == 0
    
    # Push
    stack.push("Nilai ELT101 A")
    stack.push("Nilai ELT102 B+")
    stack.push("Nilai ELT103 C")
    
    assert len(stack) == 3
    assert stack.peek() == "Nilai ELT103 C"
    
    # Pop (LIFO)
    assert stack.pop() == "Nilai ELT103 C"
    assert stack.pop() == "Nilai ELT102 B+"
    assert len(stack) == 1
    
    assert stack.pop() == "Nilai ELT101 A"
    assert stack.is_empty() is True
    assert stack.pop() is None  # pop dari stack kosong