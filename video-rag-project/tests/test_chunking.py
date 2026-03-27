import sys
sys.path.append('..')

from chunking import build_chunks, expand_fragment


def test_build_chunks():
    segments = [
        {"text": "Hello world", "start": 0, "end": 2},
        {"text": "This is a test", "start": 2, "end": 4},
        {"text": "Another segment", "start": 4, "end": 6}
    ]
    
    chunks = build_chunks(segments, max_tokens=5, overlap=2)
    
    assert len(chunks) > 0
    assert all("start" in c and "end" in c and "text" in c for c in chunks)
    print("✓ test_build_chunks passed")


def test_expand_fragment():
    chunk = {
        "video_file": "video1.mp4",
        "start": 10,
        "end": 20,
        "text": "Sample text"
    }
    
    expanded = expand_fragment(chunk, temporal_window=5)
    
    assert expanded["start"] == 5
    assert expanded["end"] == 25
    assert expanded["video_file"] == "video1.mp4"
    print("✓ test_expand_fragment passed")


if __name__ == "__main__":
    test_build_chunks()
    test_expand_fragment()
    print("\nAll tests passed!")
