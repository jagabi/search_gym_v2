"""Source-only previews for d3 document navigation. No lexical ranking or summaries."""


def partitions(start, stop, width):
    """Balanced, contiguous half-open intervals; every leaf remains addressable."""
    width = min(width, stop-start)
    return [(start + i*(stop-start)//width, start + (i+1)*(stop-start)//width)
            for i in range(width)] if width else []


def sample_indices(size, count):
    if size <= count:
        return list(range(size))
    if count == 1:
        return [size//2]
    return sorted({i*(size-1)//(count-1) for i in range(count)})


def region_preview(chunks, bundles, start, stop, chunker, limit):
    """Headings plus spaced verbatim samples, explicitly incomplete navigation text.

    Sampling represents positions, not relevance. Only d3 ranks these regions.
    Headings are deduplicated locally to avoid repeated page headers filling cards.
    """
    lo, hi = bundles[start]['chunk_ids'][0], bundles[stop-1]['chunk_ids'][-1]+1
    headings = list(dict.fromkeys(h for c in chunks[lo:hi] for h in c.headings))
    heading_text = '\n'.join(headings[i] for i in sample_indices(len(headings), 12))
    parts = [f'Incomplete source preview; bundles [{start},{stop}), chunks [{lo},{hi}).',
             'Section headings (may be sampled):\n' + chunker.prefix(heading_text, max(1, limit//3))]
    each = max(1, limit//6)
    for offset in sample_indices(hi-lo, 3):
        c = chunks[lo+offset]
        parts.append(f'Original excerpt at chunk {c.index}:\n' + chunker.prefix(c.text, each))
    return chunker.prefix('\n\n'.join(parts), limit)
