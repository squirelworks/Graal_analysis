#!/usr/bin/env python3
"""Draw manual/figures/system-map.svg, the §0.12 system map.

Run from anywhere: python tools/manual/system_map.py. Edit the boxes and
edges below, rerun, and rebuild the PDF.
"""
from pathlib import Path
import html
W, H = 1584, 920
out = []
def esc(s): return html.escape(s, quote=False)
FILL = {'client':'#e8f0fb','server':'#e6f4ea','staff':'#fdf0e1','data':'#f1ecf8','island':'#f3f3f3'}
STROKE = {'client':'#2b5797','server':'#2e7d32','staff':'#b26a00','data':'#5e35b1','island':'#666'}
def box(x,y,w,h,kind,title,lines,ref=None,size=15,dash=False):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{FILL[kind]}" stroke="{STROKE[kind]}" stroke-width="2"{" stroke-dasharray=\"8 5\"" if dash else ""}/>')
    out.append(f'<text x="{x+12}" y="{y+24}" class="t" fill="{STROKE[kind]}">{esc(title)}</text>')
    if ref:
        out.append(f'<text x="{x+w-12}" y="{y+24}" class="r" text-anchor="end">{esc(ref)}</text>')
    for i,l in enumerate(lines):
        out.append(f'<text x="{x+12}" y="{y+46+i*(size+4)}" class="b" style="font-size:{size}px">{esc(l)}</text>')
def sub(x,y,w,h,title,lines,ref):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" stroke="#2b5797" stroke-width="1.2"/>')
    out.append(f'<text x="{x+10}" y="{y+19}" class="s">{esc(title)}</text>')
    out.append(f'<text x="{x+w-10}" y="{y+19}" class="r" text-anchor="end">{esc(ref)}</text>')
    for i,l in enumerate(lines):
        out.append(f'<text x="{x+10}" y="{y+38+i*17}" class="b" style="font-size:13.5px">{esc(l)}</text>')
def edge(pts, label=(), lx=None, ly=None, both=False, dash=False, anchor='middle'):
    d = 'M' + ' L'.join(f'{a},{b}' for a,b in pts)
    out.append(f'<path d="{d}" fill="none" stroke="#333" stroke-width="2"{" stroke-dasharray=\"7 5\"" if dash else ""} marker-end="url(#a)"{" marker-start=\"url(#a)\"" if both else ""}/>')
    for i,l in enumerate(label):
        cls = 'e' if i == 0 else 'el'
        out.append(f'<text x="{lx}" y="{ly+i*17}" class="{cls}" text-anchor="{anchor}">{esc(l)}</text>')

# clients column
box(30,40,360,600,'client','Clients','',ref='Parts I, IV')
eras = [
 ('Eras Z to G: Java, then Delphi',['1998 to 2005: Java applets, then Delphi','1st Graal to 2.31 on Windows','GS1 arrives as source and is parsed here'],'§1.1, §1.6'),
 ('Era H: Torque 3.x',['Linux 3.04, Mac OS X 3.153','C++ on the Torque Game Engine'],'Part X'),
 ('Era I: 4.04r2, 4.20r6, 4.20r8',['Delphi launcher + GraalEngine.dll','(+ Graal3DEngine.dll); GS2 bytecode'],'§1.8.5'),
 ('Era J: 5.00r7, 5.12; 5.24 to 5.31',['5.00 and 5.12 as era I;','one MSVC executable from 5.24'],'§1.8.6'),
 ('Era K: 6.00 to 6.03r7, Mac 6.11',['one native C++ program per platform,','no Torque layer'],'§1.8, §1.9'),
 ('Separate lines',['v7 (Windows x64); Android Classic','and Era 1.6 to 2.2 (read statically)'],'§4.11.11'),
]
y = 76
hs = [96,78,78,78,78,78]
for (t,l,r),h in zip(eras,hs):
    sub(44,y,332,h,t,l,r); y += h+10

# servers column
box(620,40,320,120,'server','Listserver',['the server list; checks each','game-server login (VERIACC2)'],ref='Part VI')
box(620,250,320,190,'server','Game server',['GServer13 (1999), 39ster 2.1,','GServer-v2 reference behaviour;','accounts, allowed versions,','levels, file transfer, word filter,','board respawn'],ref='§5.1 to §5.4')
box(620,500,320,110,'server','3D server',['eras H to J; listed as "3 …";','Graal TCP on the listed port,','Torque UDP on port + 1'],ref='§10.2, §10.3')

# right column
box(1150,40,400,100,'staff','RemoteControl (RC)',['staff client: chat, server flags,','accounts, player admin, file browser'],ref='§7.1, §11.5')
box(1150,200,400,100,'staff','NPC Control (NC)',['same program, own socket: NPCs,','classes and weapons'],ref='§7.2, §7.3')
box(1150,360,400,130,'server','NPC server',['separate program that logs into the game','server like a player; runs server-side','scripts and owns the NPCs of its levels'],ref='§5.5')

# bottom band
box(30,700,390,175,'data','Files and formats',['levels .graal/.nw §3.1, gmap §3.2,','gani §3.3, gobjset §3.4,','tiles and arrays §3.5, sign text §3.6,','saves §3.7, caches §3.8,','config §3.9, images and sounds §3.10'],ref='Part III')
box(510,700,330,175,'data','Tools',['built-in level editor (to 2.22),','GraalEditor, GraalShop (gani),','Terrain, Dungeon and Level','generators, gif2mng,','TextConvert and others'],ref='Part XI')
box(900,700,330,175,'data','Scripting',['GS1: source text in an NPC\'s','script prop, parsed by the client','GS2: compiled before it reaches','the client; one stack machine','Torque scripts: DSO v33'],ref='Part VIII, §10.4')
box(1290,700,250,175,'island','Graal3D (2000)',['own client and server,','TCP port 14901, UDP','between clients;','no .graal/.nw, gani,','tiles or NPC scripts'],ref='Part IX',dash=True)
out.append('<text x="1302" y="862" class="el">a side line; shares no format</text>')
out.append('<text x="30" y="905" class="el">Arrows point from the side that connects or acts; two heads mean both ways. Dashed: inside one program. Section numbers are where the manual describes each part or link.</text>')

# edges
edge([(390,100),(620,100)],['list request and reply','§6.1 to §6.4'],505,82,both=True)
edge([(390,300),(620,300)],['Graal TCP','framing §2.1, ciphers §2.2,','login §2.3, PLI §2.4,','PLO §2.5, props §2.6,','files §2.7, chat and PM §2.8,','UDP §2.9, server-defined §2.10'],505,330,both=True)
edge([(390,560),(620,560)],['Torque UDP','handshake, mission download'],505,590,both=True)
edge([(780,250),(780,160)],['server link §6.5','REGISTERV3, then','zlib frames'],792,190,anchor='start')
edge([(1150,90),(940,280)],['RC login and','commands §7.1'],1000,250,anchor='start')
edge([(1350,140),(1350,200)],['finds the NPC server','address: ids 94, 79 §7.2.2'],1362,165,anchor='start',dash=True)
edge([(1350,300),(1350,360)],['NC socket: zlib frames,','no cipher §7.2.1'],1362,325,anchor='start')
edge([(1150,410),(940,410)],['logs in','like a player'],1045,380,both=True)
edge([(210,640),(210,700)],['loads and caches'],222,675,anchor='start')
edge([(510,815),(420,815)],['write'],465,805)
edge([(390,640),(940,700)],['run GS1, GS2, Torque scripts'],700,648)
edge([(1200,490),(1150,700)],['runs server-side scripts;','sends the //#CLIENTSIDE part'],1190,590,anchor='start')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="DejaVu Sans, Helvetica, Arial, sans-serif">
<title>Graal system map: clients, servers, staff tools, formats and scripting, with the manual sections for each link</title>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#333"/></marker>
<style>.t{{font-size:20px;font-weight:bold}} .s{{font-size:14px;font-weight:bold;fill:#2b5797}} .r{{font-size:13px;fill:#555}} .b{{fill:#222}} .e{{font-size:14px;font-weight:bold;fill:#111}} .el{{font-size:13px;fill:#333}}</style></defs>
<rect width="{W}" height="{H}" fill="#fff"/>
''' + '\n'.join(out) + '\n</svg>\n'
(Path(__file__).resolve().parents[2] / 'manual' / 'figures' / 'system-map.svg').write_text(svg, encoding='utf-8')
