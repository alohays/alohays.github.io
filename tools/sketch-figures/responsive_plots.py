"""Numerical SVG marks for responsive HTML figures.

Run: uv run --no-project --with matplotlib --with numpy python tools/sketch-figures/responsive_plots.py
Titles, units, legends and explanations live in wrapping HTML beside these plots.
The narrow SVG canvas keeps numeric tick labels readable on a 320px phone.
"""
from pathlib import Path
import io
import json
import math
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / 'docs/assets/images/blog/physical-units/plots'
DATA = json.loads((HERE / 'energy-data.json').read_text())
INK, MUTED, BLUE, AMBER, GRID = '#202c35', '#50616e', '#226794', '#966014', '#d6dfe4'
plt.rcParams.update({
    'svg.fonttype': 'none', 'font.family': 'DejaVu Sans', 'font.size': 17,
    'xtick.labelsize': 17, 'ytick.labelsize': 17, 'text.color': INK,
    'axes.edgecolor': INK, 'xtick.color': INK, 'ytick.color': INK,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'none', 'axes.facecolor': 'none',
    'svg.hashsalt': 'physical-units-responsive-20260927',
})

def canvas(height=3.7):
    fig, ax = plt.subplots(figsize=(4, height))
    fig.subplots_adjust(left=.17, right=.95, bottom=.16, top=.94)
    ax.tick_params(length=0, pad=8)
    ax.grid(axis='y', color=GRID, linewidth=.8)
    ax.set_axisbelow(True)
    return fig, ax

def save(fig, name, alt):
    dest = OUT / f'{name}.svg'
    buf = io.StringIO()
    fig.savefig(buf, format='svg', metadata={'Date': None})
    plt.close(fig)
    s = re.sub(r'<\?xml.*?\?>|<!DOCTYPE.*?>|<metadata>.*?</metadata>', '', buf.getvalue(), flags=re.S)
    s = re.sub(r'<defs>\s*<style.*?</style>\s*</defs>', '', s, flags=re.S)
    for color, token in [(INK,'--pu-ink'),(MUTED,'--pu-muted'),(BLUE,'--pu-accent'),(AMBER,'--pu-amber'),(GRID,'--pu-grid')]:
        s = s.replace(color, f'var({token}, {color})')
    s = re.sub(r'\s(width|height)="[^"]+pt"', '', s, count=2)
    s = s.replace('<svg ', f'<svg role="img" aria-label="{alt}" ', 1)
    # Multiple figures share a document. Never share clip/marker IDs.
    ids = re.findall(r'id="([^"]+)"', s)
    for id_ in sorted(ids, key=len, reverse=True):
        s = s.replace(f'id="{id_}"', f'id="{name}-{id_}"').replace(f'#{id_}"', f'#{name}-{id_}"').replace(f'#{id_})', f'#{name}-{id_})')
    OUT.mkdir(exist_ok=True)
    dest.write_text('\n'.join(line.rstrip() for line in s.strip().splitlines())+'\n')

def build():
    fig, ax = canvas()
    p = np.linspace(.5,.995,500)
    ax.plot(p*100,np.log(.5)/np.log(p),lw=2.5,color=BLUE)
    ax.plot(p*100,np.log(2)/(1-p),lw=1.5,color=MUTED,ls='--')
    ax.scatter([90,99],[math.log(.5)/math.log(.9),math.log(.5)/math.log(.99)],s=48,color=BLUE,zorder=4)
    ax.set(xlim=(48,102),ylim=(.8,180),yscale='log',xticks=[50,70,90,99])
    ax.yaxis.set_major_locator(FixedLocator([1,10,100]));ax.yaxis.set_major_formatter(FixedFormatter(['1','10','100']));ax.minorticks_off()
    save(fig,'horizon','H50 = ln(0.5) / ln(p). At 90% step success: 6.6 steps; at 99%: 69. A calculated example.')

    fig, ax = canvas()
    t=np.linspace(1,10,400)
    ax.plot(t,10/t,color=BLUE,lw=2)
    ax.scatter([10,1],[1,10],s=75,color=BLUE,zorder=3)
    ax.scatter([1],[1],s=90,color=AMBER,zorder=3,marker='s')
    ax.set(xlim=(0,11),ylim=(0,11.5),xticks=[1,5,10],yticks=[1,5,10])
    for x,y,label in [(8.7,2.0,'A'),(1.9,9.8,'B'),(1.8,1.0,'C')]:
        ax.text(x,y,label,fontsize=19,weight='bold')
    save(fig,'energy-time','Equal verified performance: A uses 1 J in 10 s, B uses 10 J in 1 s, C uses 1 J in 1 s. A and B lie on E times T = 10.')

    fig, ax = canvas(4.0)
    fig.subplots_adjust(left=.12,right=.94,bottom=.16,top=.92)
    selected=[DATA['hardware']['operations'][i] for i in [0,1,2,5]]
    for i,op in enumerate(selected):
        lo,hi=op['low_pj'],op['high_pj'];y=4-i
        ax.plot([lo,hi],[y,y],color=BLUE,lw=5,solid_capstyle='round')
        ax.plot(math.sqrt(lo*hi),y,'o',color=BLUE,ms=7)
    ax.set(xscale='log',xlim=(.04,20000),ylim=(.5,4.5),yticks=[1,2,3,4])
    ax.set_yticklabels(['4','3','2','1'])
    ax.xaxis.set_major_locator(FixedLocator([.1,10,1000]));ax.xaxis.set_major_formatter(FixedFormatter(['0.1','10','1,000']));ax.minorticks_off()
    save(fig,'hardware-energy','Hardware rows 1 to 4: 0.1, 4, 10, and 1300 to 2600 pJ per specified operation. Logarithmic x axis.')

    fig, ax = canvas(2.9)
    fig.subplots_adjust(left=.12,right=.94,bottom=.22,top=.88)
    ratios=[op['estimated_joules']/(DATA['boltzmann_joule_per_kelvin']*DATA['temperature_kelvin']*math.log(op['alphabet_size'])) for op in DATA['biology']['operations']]
    ax.scatter(ratios,[2,1],s=80,color=AMBER)
    ax.set(xscale='log',xlim=(.7,1500),ylim=(.4,2.6),yticks=[1,2])
    ax.set_yticklabels(['2','1'])
    ax.xaxis.set_major_locator(FixedLocator([1,10,100,1000]));ax.xaxis.set_major_formatter(FixedFormatter(['1','10','100','1,000']));ax.minorticks_off()
    save(fig,'biology-energy','Biological rows 1 and 2: approximately 26 and 165 times each operation-specific bound. Logarithmic x axis.')
    print('Built four numerical plot panels from explicit inputs.')

if __name__ == '__main__': build()
