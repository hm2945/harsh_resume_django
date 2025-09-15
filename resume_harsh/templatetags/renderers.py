from __future__ import annotations
from typing import Iterable, Mapping, Optional
from django import template
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.safestring import mark_safe


#Render the resume page via a Django template *tag* so the template itself so no HTML 
register = template.Library()
ACCENT = "#2A0761"       
CONTAINER_W = "850px"    

def _fmt_range(start: Optional[str], end: Optional[str]) -> str:
    """Return 'start – end' or a single value if one is missing."""
    if start and end and start != end:
        return f"{start} \u2013 {end}"
    return (start or end or "")

def _css() -> str:
    # Return the CSS styles as a <style> blocck 
    return mark_safe(f"""
<style>
:root {{ --accent: {ACCENT}; }}
*{{box-sizing:border-box}}
body{{margin:0;font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;color:#111;line-height:1.5}}
.container{{max-width:{CONTAINER_W};margin:2rem auto;padding:0 1rem 2rem}}
.header{{text-align:center;margin-bottom:1rem}}
.contact{{color:#555;margin-top:.25rem}}
.section{{margin-top:1.4rem}}
.section h2{{text-align:left;border-bottom:2px solid #eee;padding-bottom:.25rem;margin-bottom:.5rem}}
.item{{display:flex;align-items:baseline;gap:1rem;margin-top:.35rem}}
.title{{font-weight:600;margin:0}}
.subtitle{{margin:.15rem 0 0 0;color:#555;font-size:.95rem}}
.when{{margin-left:auto;white-space:nowrap;color:#666;font-size:.95rem}}
.bullets{{margin:.35rem 0 0 1.25rem}}
.desc{{margin:.25rem 0 .25rem 0;color:#333}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
@media print {{
  body{{font-size:12px}}
  .section h2{{border:0}}
  a{{color:inherit;text-decoration:none}}
}}
</style>
""").strip()
def _header(r: Mapping[str, str]) -> str:
    """Name + contact row (name centered)."""
    esc = conditional_escape
    return format_html(
        '<header class="header">'
        '  <h1>{}</h1>'
        '  <p class="contact">{} • {} • <a href="mailto:{}">{}</a> • '
        '  <a href="{}" target="_blank" rel="noopener">linkedin.com/in/harshmenaria</a></p>'
        "</header>",
        esc(r["name"]), esc(r["location"]), esc(r["phone"]),
        esc(r["email"]), esc(r["email"]), esc(r["linkedin"])
    )

def _section(title: str, inner_html: str) -> str:
    """Standard section wrapper with left-aligned heading."""
    return format_html('<section class="section"><h2>{}</h2>{}</section>',
                       conditional_escape(title), mark_safe(inner_html))

def _p(text: str) -> str:
    """Paragraph with escaping."""
    return format_html("<p>{}</p>", conditional_escape(text))

def _skills(items: Iterable[str]) -> str:
    """Unordered list of skills from Python list."""
    lis = format_html_join("", "<li>{}</li>", ((conditional_escape(s),) for s in items))
    return format_html('<ul class="bullets">{}</ul>', lis)

def _projects(items: Iterable[Mapping[str, str]]) -> str:
    """Rows with title/desc and right-aligned dates."""
    rows = []
    for p in items:
        when = _fmt_range(p.get("start"), p.get("end"))
        rows.append(format_html(
            '<div class="item"><div>'
            '  <p class="title">{}</p>'
            '  <p class="desc">{}</p>'
            '</div><span class="when">{}</span></div>',
            conditional_escape(p["title"]),
            conditional_escape(p["desc"]),
            conditional_escape(when),
        ))
    return mark_safe("".join(rows))

def _experience(items: Iterable[Mapping[str, object]]) -> str:
    """Job header + bullet list for each role."""
    blocks = []
    for e in items:
        when = _fmt_range(e.get("start"), e.get("end"))
        head = format_html(
            '<div class="item"><div>'
            '  <p class="title">{} \u2014 {}</p>'
            '  <p class="subtitle">{}</p>'
            '</div><span class="when">{}</span></div>',
            conditional_escape(e["title"]),
            conditional_escape(e["company"]),
            conditional_escape(e.get("subtitle", "")),
            conditional_escape(when),
        )
        bullets = format_html_join("", "<li>{}</li>", ((conditional_escape(b),) for b in e["bullets"]))  # type: ignore[index]
        blocks.append(mark_safe(head + f'<ul class="bullets">{bullets}</ul>'))
    return mark_safe("".join(blocks))

def _pairs(items: Iterable[Mapping[str, str]], label_key: str, when_key: str) -> str:
    """Generic renderer for simple (label, date) pairs."""
    return mark_safe("".join(format_html(
        '<div class="item"><p class="title">{}</p><span class="when">{}</span></div>',
        conditional_escape(it[label_key]), conditional_escape(it[when_key])
    ) for it in items))

def _education(items: Iterable[Mapping[str, str]]) -> str:
    """Education rows using consistent date formatting."""
    return mark_safe("".join(format_html(
        '<div class="item"><p class="title">{}</p><span class="when">{}</span></div>',
        conditional_escape(ed["name"]),
        conditional_escape(_fmt_range(ed.get("start"), ed.get("end")))
    ) for ed in items))

@register.simple_tag
def render_full_resume(resume: Mapping[str, object]) -> str:
    """
    Build the entire resume page as HTML from Python data.
    """
    esc_name = conditional_escape(resume["name"])
    head = mark_safe(
        f"<!doctype html><html lang='en'><head>"
        f"<meta charset='utf-8'>"
        f"<title>{conditional_escape(resume['name'])} — Resume</title>"
        f"{_css()}</head><body>"
    )
    parts = [
        "<main class='container'>",
        _header(resume),
        _section("Professional Summary", _p(resume["summary"])),
        _section("Skills", _skills(resume["skills"])),
        _section("Projects", _projects(resume["projects"])),
        _section("Experience", _experience(resume["experience"])),
        _section("Certifications", _pairs(resume["certs"], "name", "date")),
        _section("Education", _education(resume["education"])),
        "</main>",
        "</body></html>",
    ]
    return mark_safe(head + "".join(parts))
