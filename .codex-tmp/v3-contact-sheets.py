from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,sys
root=Path('design/2026-11-13-v3')
actual=Path(sys.argv[1])
out=Path('.codex-tmp/v3-visual-review');out.mkdir(exist_ok=True)
ids=[r['id'] for r in json.loads((root/'coverage.json').read_text(encoding='utf-8-sig'))['routes'] if r['id'] not in ['component-lab','motion-lab']]
for offset in range(0,len(ids),3):
    sheet=Image.new('RGB',(1920,1140),'#777777');draw=ImageDraw.Draw(sheet)
    for row,id in enumerate(ids[offset:offset+3]):
        for col,(theme,kind) in enumerate([('light','V3'),('light','APP'),('dark','V3'),('dark','APP')]):
            file=root/'screenshots'/f'{theme}-{id}.png' if kind=='V3' else actual/f'parity-{theme}-{id}.png'
            draw.text((col*480+8,row*380+8),f'{id} | {theme} | {kind}',fill='white')
            if file.exists():
                im=Image.open(file).convert('RGB');im=im.crop((0,0,im.width,min(im.height,1050)))
                im.thumbnail((480,350));sheet.paste(im,(col*480,row*380+28))
    sheet.save(out/f'{offset//3+1:02}.png')
print(json.dumps({'directory':str(out),'sheets':(len(ids)+2)//3,'screens':len(ids),'order':ids},ensure_ascii=False))
