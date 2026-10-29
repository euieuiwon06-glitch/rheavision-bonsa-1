"""src 조각을 합쳐 v1.html(본사 시안1)·v2.html(본사 시안2)을 만든다. 실행: python src/build.py"""
from pathlib import Path

SRC = Path(__file__).parent
ROOT = SRC.parent

SPECS = [
    ("display_settings", "text-blue-700", "MOD-01", "디스플레이", "직사광선 환경에서도 선명한 고휘도 패널",
     [("규격", "21.5\" FHD IPS", False), ("휘도", "700 nits", True), ("표면", "7H 안티글레어", False)]),
    ("center_focus_strong", "text-slate-900", "MOD-02", "센서 어레이", "초고속 비접촉 3D 광학 인식 카메라",
     [("광학계", "Dual 4K + IR", False), ("뎁스", "3D ToF 모듈", True), ("조명", "조도 반응형 LED", False)]),
    ("verified", "text-blue-700", "MOD-03", "섀시 &amp; 내구성", "밀링 알루미늄 유니바디 프레임",
     [("소재", "CNC 항공 알루미늄", False), ("방진/방수", "IP65 등급", True), ("내충격", "IK08 강화유리", False)]),
    ("hub", "text-slate-900", "MOD-04", "통신 &amp; 인터페이스", "스피드게이트 및 사내 BMS 즉시 연동",
     [("무선망", "Wi-Fi 6E / 5G", False), ("유선망", "Dual GbE + PoE+", True), ("프로토콜", "OSDP v2 / Wiegand", False)]),
]

CASES = [
    ("case1.jpg", "ENTERPRISE HQ", "스마트 사옥", "워크스루 무정차 출입", "처리율 +420%"),
    ("case2.jpg", "HEALTHCARE", "대형 병원", "완전 비접촉 감염 관리", "대기시간 -85%"),
    ("case3.jpg", "AVIATION", "공항 &amp; 호텔", "스마트패스 원스톱 수속", "수속 3.2초 완료"),
    ("case4.jpg", "FINANCE &amp; GOV", "금융 &amp; 전산센터", "FIPS 140-3 보안 인프라", "보안 침해 0건"),
]


def spec_card(icon, color, mod, title, desc, rows):
    row_html = "".join(
        f'<div class="flex justify-between py-1.5 bg-slate-50 px-2.5 rounded border border-slate-100">'
        f'<span class="text-slate-500">{k}</span>'
        f'<span class="{"text-blue-700 font-semibold" if hi else "text-slate-900 font-medium"}">{v}</span></div>'
        for k, v, hi in rows)
    return (f'<div class="flex flex-col bg-white p-7 rounded-xl border border-slate-200/90 shadow-sm hover:border-slate-300 transition-all">'
            f'<div class="flex items-center justify-between mb-4"><span class="material-symbols-outlined {color} text-[28px]">{icon}</span>'
            f'<span class="font-mono text-[11px] text-slate-500 font-semibold tracking-[.1em]">{mod}</span></div>'
            f'<h4 class="font-headline-sm text-headline-sm text-slate-900 mb-2">{title}</h4>'
            f'<p class="font-body-sm text-body-sm text-slate-600 mb-6">{desc}</p>'
            f'<div class="mt-auto flex flex-col gap-2 font-body-sm text-body-sm">{row_html}</div></div>')


def case_card(img, tag, title, desc, stat):
    return (f'<div class="flex flex-col bg-white rounded-xl overflow-hidden hover:-translate-y-1 transition-transform duration-300 border border-slate-200/90 shadow-sm hover:shadow-md">'
            f'<div class="relative h-44 w-full bg-cover bg-center" style="background-image:url(assets/{img})">'
            f'<span class="absolute top-3 left-3 px-2 py-0.5 rounded bg-slate-900/90 font-label-sm text-label-sm text-white uppercase font-semibold">{tag}</span></div>'
            f'<div class="p-5 flex flex-col flex-1"><h4 class="font-headline-sm text-headline-sm text-slate-900 mb-1">{title}</h4>'
            f'<p class="font-body-sm text-body-sm text-slate-600 mb-4">{desc}</p>'
            f'<div class="mt-auto pt-3 border-t border-slate-100 text-[11px] text-blue-700 font-mono font-bold">{stat}</div></div></div>')


def read(name):
    return (SRC / name).read_text(encoding="utf-8")


body = (read("body.html")
        .replace("{{SPECS}}", "\n".join(spec_card(*s) for s in SPECS))
        .replace("{{CASES}}", "\n".join(case_card(*c) for c in CASES)))

for out, title, hero, metric_h in [
    ("v1.html", "레아비전 · 본사 시안1", "hero1.html", 215),
    ("v2.html", "레아비전 · 본사 시안2", "hero2.html", 205),
]:
    html = (read("head.html").replace("{{TITLE}}", title) + read(hero)
            + body.replace("{{METRIC_H}}", str(metric_h)))
    (ROOT / out).write_text(html, encoding="utf-8")
    print("wrote", out)
    if out == "v1.html":  # GitHub Pages 첫 화면 = 본사 시안1
        (ROOT / "index.html").write_text(html, encoding="utf-8")
        print("wrote index.html")
