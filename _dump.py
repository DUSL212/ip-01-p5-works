import zipfile,re,html
z=zipfile.ZipFile('作业三_成果展示与汇报.pptx')
names=sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)],
             key=lambda n:int(re.search(r'(\d+)',n.split('/')[-1]).group(1)))
for n in names[:2]:
    x=z.read(n).decode('utf-8')
    print('==================',n, len(x))
    # split into sp / pic / grpSp blocks
    for m in re.finditer(r'<p:(sp|pic|graphicFrame|cxnSp)>.*?</p:/1>', x, re.S):
        blk=m.group(0)
        tag=m.group(1)
        nm=re.search(r'<p:cNvPr[^>]*name="([^"]*)"',blk)
        off=re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>',blk)
        ext=re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>',blk)
        txt=''.join(re.findall(r'<a:t>(.*?)</a:t>',blk,re.S))
        txt=html.unescape(txt)[:40]
        geom=re.search(r'<a:prstGeom prst="(\w+)"',blk)
        fill=re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"',blk)[:6]
        szs=re.findall(r'sz="(\d+)"',blk)[:6]
        print(f'{tag:12} {nm.group(1) if nm else "":22} off={off.groups() if off else None} ext={ext.groups() if ext else None} geom={geom.group(1) if geom else "-"} col={fill} sz={szs} txt={txt!r}')
