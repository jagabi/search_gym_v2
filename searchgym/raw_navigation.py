"""Source-only previews for d3 document navigation. No lexical ranking or summaries."""

from bisect import bisect_right
import re


def source_sections(text, markdown):
    """Contiguous original Markdown sections, including the unheaded opening."""
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    result, stack, start, headings = [], [], 0, []
    for token in markdown.parse(text):
        if token.level != 0 or token.type != 'heading_open' or token.map is None:
            continue
        lo, hi = token.map
        position = offsets[lo]
        if position > start:
            result.append({'start': start, 'stop': position, 'headings': headings,
                           'text': text[start:position]})
        level = int(token.tag[1:])
        stack = [(depth, label) for depth, label in stack if depth < level]
        stack.append((level, ''.join(lines[lo:hi]).strip()))
        headings = [label for _, label in stack]
        start = position
    if start < len(text):
        result.append({'start': start, 'stop': len(text), 'headings': headings,
                       'text': text[start:]})
    return result


def section_preview(sections, start, stop, chunker, limit):
    """Position samples of original headings/paragraphs; never relevance ranking."""
    subset = sections[start:stop]
    headings = [' > '.join(section['headings']) for section in subset if section['headings']]
    parts = ['Incomplete navigation sample; links and headings are leads, not answer evidence.']
    if headings:
        parts.append('Original section headings:\n' + chunker.prefix('\n'.join(
            headings[i] for i in sample_indices(len(headings), 12)), max(1, limit//3)))
    paragraphs = [p for section in subset for p in section['text'].split('\n\n') if p.strip()]
    for i in sample_indices(len(paragraphs), 3):
        parts.append('Original excerpt:\n' + chunker.prefix(paragraphs[i], max(1, limit//6)))
    return chunker.prefix('\n\n'.join(parts), limit)


def marker_context(text, marker, chunker, limit):
    """Bound a long original passage around the literal internal link marker."""
    if chunker.count(text) <= limit:
        return text
    match = re.search(r'(?<!\w)' + re.escape(marker) + r'(?!\w)', text)
    if match is None:
        return chunker.prefix(text, limit)
    position = match.start()
    encoded = chunker.encoder.encode(text, add_special_tokens=False)
    starts = [lo for lo, _ in encoded.offsets]
    center = max(0, bisect_right(starts, position)-1)
    lo = starts[max(0, center-limit//2)]
    return chunker.prefix(text[lo:], limit)


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
