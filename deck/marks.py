# Animal marks. Each is drawn around the origin, about 40 units wide.
def turtle(c, g):
    return (f'<ellipse cx="-13" cy="-7" rx="9" ry="3.6" transform="rotate(-38 -13 -7)" fill="{c}"/>'
            f'<ellipse cx="13" cy="-7" rx="9" ry="3.6" transform="rotate(38 13 -7)" fill="{c}"/>'
            f'<ellipse cx="-10" cy="13" rx="5.5" ry="3" transform="rotate(40 -10 13)" fill="{c}"/>'
            f'<ellipse cx="10" cy="13" rx="5.5" ry="3" transform="rotate(-40 10 13)" fill="{c}"/>'
            f'<circle cx="0" cy="-16" r="4.6" fill="{c}"/>'
            f'<ellipse cx="0" cy="1" rx="11.5" ry="14" fill="{c}"/>'
            f'<path d="M0 -7 L5.5 -3.5 V4.5 L0 8 L-5.5 4.5 V-3.5 Z" fill="none" stroke="{g}" stroke-width="1.4"/>'
            f'<path d="M0 -7 V-12.5 M5.5 -3.5 L10 -6.5 M5.5 4.5 L10 7.5 M0 8 V14.5 M-5.5 4.5 L-10 7.5 M-5.5 -3.5 L-10 -6.5" fill="none" stroke="{g}" stroke-width="1.2"/>')
def fox(c, g, p):
    return (f'<path d="M-15 -17 L-4 -7 L-16 -2 Z" fill="{c}"/><path d="M15 -17 L4 -7 L16 -2 Z" fill="{c}"/>'
            f'<path d="M-16 -4 Q0 -13 16 -4 L0 17 Z" fill="{c}"/>'
            f'<path d="M-16 -4 L0 17 L-4.5 3 Z" fill="{p}"/><path d="M16 -4 L0 17 L4.5 3 Z" fill="{p}"/>'
            f'<circle cx="0" cy="15.2" r="2.3" fill="{g}"/>'
            f'<circle cx="-6.5" cy="-1.5" r="1.6" fill="{g}"/><circle cx="6.5" cy="-1.5" r="1.6" fill="{g}"/>')
def cat(c, g):
    return (f'<path d="M-15 -16 L-4 -9 L-15 1 Z" fill="{c}"/><path d="M15 -16 L4 -9 L15 1 Z" fill="{c}"/>'
            f'<ellipse cx="0" cy="3" rx="15" ry="12.5" fill="{c}"/>'
            f'<ellipse cx="-6" cy="1" rx="1.9" ry="3.1" fill="{g}"/><ellipse cx="6" cy="1" rx="1.9" ry="3.1" fill="{g}"/>'
            f'<path d="M-2.2 7 H2.2 L0 9.6 Z" fill="{g}"/>'
            f'<path d="M-10 8 L-21 6 M-10 10.5 L-21 12.5 M10 8 L21 6 M10 10.5 L21 12.5" fill="none" stroke="{c}" stroke-width="1.1"/>')
def hedgehog(c, g, p):
    return (f'<path d="M-17 9 L-20 1 L-14 0 L-17 -8 L-10 -7 L-9 -15 L-3 -11 L1 -17 L5 -10 L11 -13 L11 -5 L17 -4 L14 2 L13 9 Z" fill="{c}"/>'
            f'<path d="M13 9 V-1 L21.5 5 Q23.5 8.2 19.5 9 Z" fill="{p}"/>'
            f'<circle cx="21.4" cy="6.2" r="1.7" fill="{g}"/><circle cx="16.2" cy="3.6" r="1.2" fill="{g}"/>'
            f'<rect x="-10" y="9" width="4.5" height="3" rx="1" fill="{c}"/><rect x="3" y="9" width="4.5" height="3" rx="1" fill="{c}"/>')
def mark(kind, x, y, s, c, g='var(--ground)', p='var(--text)'):
    body = {'turtle': lambda: turtle(c, g), 'fox': lambda: fox(c, g, p), 'cat': lambda: cat(c, g), 'hedgehog': lambda: hedgehog(c, g, p)}[kind]()
    return f'<g transform="translate({x} {y}) scale({s})">{body}</g>'
