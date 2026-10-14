#!/usr/bin/env python3
# make-art.py: the still part of Kirpi's deck, as one SVG at the design size 1600x900.
# Texture, frames, title strips and the hedgehog. No words: the deck draws every word itself,
# so the grain never lies on text. Rendered to kirpi-deck.png at Kirpi's screen size.
from marks import mark
CH,OR,TE,SG,DT,BO='#1f1c1a','#E8873A','#4C8782','#608A6E','#2c4549','#f6cfa0'
band=[CH]*6+[DT,TE,OR,SG,TE,OR,DT,SG]+[CH]*6
def tv(ch): return ' '.join(f'{int(c[1+2*ch:3+2*ch],16)/255:.3f}' for c in band)
def box(x,y,w,h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CH}" stroke="{OR}" stroke-width="2.4"/>'
def strip(x,y,w): return f'<rect x="{x}" y="{y}" width="{w}" height="44" fill="{OR}"/>'
def grain(op): return f'<rect width="1600" height="900" filter="url(#grain)" opacity="{op}" style="mix-blend-mode:overlay"/>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1600 900">
<defs>
<filter id="marble" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.0026 0.0044" numOctaves="3" seed="21"/><feColorMatrix type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1"/><feComponentTransfer><feFuncR type="discrete" tableValues="{tv(0)}"/><feFuncG type="discrete" tableValues="{tv(1)}"/><feFuncB type="discrete" tableValues="{tv(2)}"/></feComponentTransfer></filter>
<filter id="grain" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="0.62" numOctaves="2" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="linear" slope="2.6" intercept="-0.8"/><feFuncG type="linear" slope="2.6" intercept="-0.8"/><feFuncB type="linear" slope="2.6" intercept="-0.8"/><feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer></filter>
</defs>
<rect width="1600" height="900" fill="{CH}"/>
<rect x="364" y="32" width="1204" height="836" filter="url(#marble)"/>
<rect x="16" y="16" width="1568" height="868" fill="none" stroke="{OR}" stroke-width="2.4"/>
<rect x="364" y="32" width="1204" height="836" fill="none" stroke="{OR}" stroke-width="2.4"/>
{box(32,32,320,118)}
<rect x="32" y="162" width="320" height="168" fill="{OR}"/><rect x="46" y="176" width="292" height="140" fill="{CH}"/>
{mark('hedgehog',186,250,3.3,OR,CH,BO)}
{grain(.20)}
<rect x="32" y="342" width="320" height="218" fill="{OR}"/>
<path d="M50 506 H334" stroke="{CH}" stroke-width="2.4"/>
{box(32,572,320,296)}{strip(32,572,320)}
<path d="M48 818 H336" stroke="{OR}" stroke-width="1.6" stroke-opacity=".6"/>
<rect x="388" y="56" width="1156" height="100" fill="{OR}"/>
<rect x="730" y="74" width="272" height="64" fill="{CH}"/>
{box(388,188,772,412)}{strip(388,188,772)}
{box(1184,188,360,412)}{strip(1184,188,360)}
{box(388,624,772,220)}{strip(388,624,772)}
{box(1184,624,360,220)}{strip(1184,624,360)}
{grain(.05)}
</svg>'''
open('kirpi-deck.svg','w',encoding='utf-8').write(svg)
print('art', len(svg))
