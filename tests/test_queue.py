from src.data_structures.queue_ll import Queue

def test_queue_operations():
    queue = Queue()
    
    assert queue.is_empty() is True
    assert queue.size() == 0
    
    queue.enqueue("Formula 1")
    queue.enqueue("Formula 2")
    queue.enqueue("Formula 3")
    
    assert queue.size() == 3
    assert queue.peek() == "Formula 1"
    
    # Dequeue FIFO
    assert queue.dequeue() == "Formula 1"
    assert queue.dequeue() == "Formula 2"
    assert queue.size() == 1
    
    assert queue.dequeue() == "Formula 3"
    assert queue.is_empty() is True
    assert queue.dequeue() is None