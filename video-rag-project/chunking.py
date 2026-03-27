def build_chunks(segments, max_tokens=80, overlap=30):
    chunks = []
    current = []
    token_count = 0

    for seg in segments:
        tokens = seg["text"].split()
        n = len(tokens)

        if token_count + n > max_tokens and current:
            text = " ".join([s["text"] for s in current])

            chunks.append({
                "start": current[0]["start"],
                "end": current[-1]["end"],
                "text": text
            })

            overlap_segments = current[-1:]
            current = overlap_segments
            token_count = sum(len(s["text"].split()) for s in current)

        current.append(seg)
        token_count += n

    if current:
        text = " ".join([s["text"] for s in current])

        chunks.append({
            "start": current[0]["start"],
            "end": current[-1]["end"],
            "text": text
        })

    return chunks


def expand_fragment(chunk, temporal_window=6):
    return {
        "video_file": chunk["video_file"],
        "start": max(0, chunk["start"] - temporal_window),
        "end": chunk["end"] + temporal_window,
        "text": chunk["text"]
    }
