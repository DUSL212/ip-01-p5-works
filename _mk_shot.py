import re, sys, subprocess, os
src = open('orbis-mandala.html', encoding='utf-8').read()

EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

def build(name, theme_idx, burst, extra_css=""):
    inject = """
<script>
(function(){
  Element.prototype.setPointerCapture = function(){};
  Element.prototype.releasePointerCapture = function(){};
  window.addEventListener('load', function(){
    var c = document.getElementById('art');
    var btns = document.querySelectorAll('.th');
    %s
    var W = window.innerWidth, H = window.innerHeight;
    var x = W*0.5 + 150, y = H*0.5 - 90;
    function mk(t,px,py){ c.dispatchEvent(new PointerEvent(t,{clientX:px,clientY:py,bubbles:true,cancelable:true,pointerId:1,pointerType:'mouse',isPrimary:true})); }
    setTimeout(function(){
      mk('pointermove', x, y);
      %s
    }, 120);
  });
})();
</script>
""" % (
  ("btns[%d].click();" % theme_idx) if theme_idx else "btns[0].click();",
  ("setTimeout(function(){ mk('pointermove', W*0.5+40, H*0.5-30); mk('pointerdown', W*0.5+40, H*0.5-30); mk('pointerup', W*0.5+40, H*0.5-30); }, 300);" if burst else "")
)
    html = src.replace("</body>", inject + "</body>")
    p = "_v_%s.html" % name
    open(p, 'w', encoding='utf-8').write(html)
    return p

def shot(htmlfile, out, w, h, budget):
    url = "file:///C:/Users/APand/Desktop/" + htmlfile
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
           "--force-device-scale-factor=1", "--window-size=%d,%d" % (w, h),
           "--virtual-time-budget=%d" % budget,
           "--screenshot=C://Users//APand//Desktop//" + out, url]
    subprocess.run(cmd, capture_output=True)
    print(out, os.path.getsize(out))

# 主视觉（金色，无爆点）
shot(build("hero", 0, False), "_orbis_hero.png", 1920, 1080, 9000)
# 交互瞬间（有涟漪/火花）
shot(build("burst", 0, True), "_orbis_burst.png", 1920, 1080, 1400)
# 四色样张
for i, nm in enumerate(["jade", "rose", "ice"], start=1):
    shot(build(nm, i, False), "_orbis_%s.png" % nm, 900, 900, 6000)
