"""
Import the KATEK AI blog articles (.docx) into BlogPost rows.

Each .docx follows a fixed structure:
  Heading 1            -> article title
  normal (4 lines)     -> Keyword / Meta Title / URL Slug / Meta Description
  Heading 2 sections   -> Introduction, Quick Answer, Key Takeaways, Main Content,
                          Comparison Table, Frequently Asked Questions, Conclusion
  Heading 3 + normal   -> sub-sections and body copy

The command parses each file into clean, semantic HTML and stores it on the model.
It is idempotent (update_or_create keyed on slug), so re-running re-imports cleanly.

    python manage.py import_blog_posts
    python manage.py import_blog_posts --dir "KATEK AI"
"""
import html as html_lib
import os
import re
from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from myApp.models import BlogPost

META_LABELS = ("Keyword", "Meta Title", "URL Slug", "Meta Description")

# slug keyword -> (category, accent hex). First match wins; falls back to default.
CATEGORY_RULES = [
    ("geo-", ("Search & GEO", "#0099ee")),
    ("rag-ai", ("AI Engineering", "#0033e6")),
    ("custom-ai-development", ("Enterprise", "#001fcc")),
    ("operating-system", ("Platform", "#00aadd")),
    ("sop-training", ("Platform", "#00aadd")),
    ("course-creator", ("Education", "#00ccff")),
    ("real-estate", ("Industry", "#33aaf5")),
    ("coaching", ("Industry", "#33aaf5")),
    ("strategy", ("Strategy", "#2255ff")),
    ("build-vs-buy", ("Strategy", "#2255ff")),
    ("vs-hiring", ("Strategy", "#2255ff")),
    ("workflow-automation", ("Automation", "#0040FF")),
    ("content-automation", ("Automation", "#0040FF")),
    ("email-automation", ("Automation", "#0040FF")),
    ("agent-automation", ("Automation", "#0040FF")),
    ("business-automation", ("Automation", "#0040FF")),
]
DEFAULT_CATEGORY = ("Insights", "#0040FF")


def esc(text):
    return html_lib.escape(text, quote=False)


def iter_block_items(doc):
    """Yield Paragraph / Table objects in document order."""
    from docx.text.paragraph import Paragraph
    from docx.table import Table

    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag
        if tag.endswith("}p"):
            yield Paragraph(child, doc)
        elif tag.endswith("}tbl"):
            yield Table(child, doc)


def normalize_heading(text):
    """Lowercase, strip parenthetical qualifiers — 'Quick Answer (…)' -> 'quick answer'."""
    return re.sub(r"\s*\(.*?\)\s*", "", text).strip().lower()


def pick_category(slug):
    for needle, value in CATEGORY_RULES:
        if needle in slug:
            return value
    return DEFAULT_CATEGORY


def render_table(table):
    rows = table.rows
    if not rows:
        return ""
    parts = ['<div class="blog-table-wrap"><table class="blog-table">']
    header = rows[0]
    parts.append("<thead><tr>")
    for cell in header.cells:
        parts.append(f"<th>{esc(cell.text.strip())}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows[1:]:
        parts.append("<tr>")
        for cell in row.cells:
            parts.append(f"<td>{esc(cell.text.strip())}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts)


def parse_docx(path):
    from docx import Document as DocxDocument

    doc = DocxDocument(path)

    meta = {}
    title = ""
    html = []
    seen_first_h2 = False

    container = None        # None | 'ul' | 'faq' | 'callout'
    faq_item_open = False

    def close_container():
        nonlocal container, faq_item_open
        if container == "ul":
            html.append("</ul>")
        elif container == "faq":
            if faq_item_open:
                html.append("</div>")
                faq_item_open = False
            html.append("</div>")
        elif container == "callout":
            html.append("</div>")
        container = None

    for block in iter_block_items(doc):
        # ----- tables -----
        if block.__class__.__name__ == "Table":
            close_container()
            html.append(render_table(block))
            continue

        text = block.text.strip()
        if not text:
            continue
        style = (block.style.name or "").strip()

        # ----- title -----
        if style == "Heading 1":
            if not title:
                title = text
            continue

        # ----- metadata block (only before the first H2) -----
        if not seen_first_h2 and ":" in text:
            label = text.split(":", 1)[0].strip()
            if label in META_LABELS:
                meta[label] = text.split(":", 1)[1].strip()
                continue

        # ----- H2 section headers -----
        if style == "Heading 2":
            seen_first_h2 = True
            close_container()
            sec = normalize_heading(text)

            if sec == "main content":
                continue  # structural label, no visible heading

            if sec == "quick answer":
                html.append(
                    '<div class="blog-callout">'
                    '<div class="blog-callout-label">Quick Answer</div>'
                )
                container = "callout"
                continue

            if sec == "key takeaways":
                html.append(f"<h2>{esc(text)}</h2>")
                html.append('<ul class="blog-takeaways">')
                container = "ul"
                continue

            if sec == "frequently asked questions":
                html.append(f"<h2>{esc(text)}</h2>")
                html.append('<div class="blog-faq">')
                container = "faq"
                continue

            html.append(f"<h2>{esc(text)}</h2>")
            continue

        # ----- H3 sub-headers -----
        if style == "Heading 3":
            close_container()
            html.append(f"<h3>{esc(text)}</h3>")
            continue

        # ----- body paragraphs -----
        if container == "ul":
            html.append(f"<li>{esc(text)}</li>")
        elif container == "faq":
            m = re.match(r"^Q\d+\s*[:.\)]\s*(.*)$", text)
            if m:
                if faq_item_open:
                    html.append("</div>")
                html.append(
                    f'<div class="blog-faq-item">'
                    f'<p class="blog-faq-q">{esc(m.group(1))}</p>'
                )
                faq_item_open = True
            else:
                html.append(f'<p class="blog-faq-a">{esc(text)}</p>')
        elif container == "callout":
            html.append(f"<p>{esc(text)}</p>")
        else:
            html.append(f"<p>{esc(text)}</p>")

    close_container()

    slug_raw = meta.get("URL Slug", "")
    slug = slug_raw.rstrip("/").split("/")[-1] if slug_raw else ""

    # word count for read time (strip tags)
    plain = re.sub(r"<[^>]+>", " ", "".join(html))
    words = len(plain.split())
    read_minutes = max(2, round(words / 200))

    return {
        "title": title,
        "slug": slug,
        "keyword": meta.get("Keyword", ""),
        "meta_title": meta.get("Meta Title", ""),
        "meta_description": meta.get("Meta Description", ""),
        "excerpt": meta.get("Meta Description", ""),
        "body_html": "".join(html),
        "read_minutes": read_minutes,
    }


class Command(BaseCommand):
    help = "Import KATEK AI blog articles from .docx files into BlogPost rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default=os.path.join(settings.BASE_DIR, "KATEK AI"),
            help="Directory containing the .docx article files.",
        )

    def handle(self, *args, **options):
        import glob

        src_dir = options["dir"]
        files = sorted(glob.glob(os.path.join(src_dir, "*.docx")))
        if not files:
            self.stderr.write(self.style.ERROR(f"No .docx files found in {src_dir!r}"))
            return

        base_date = date(2026, 6, 2)
        created = updated = skipped = 0

        for i, path in enumerate(files):
            try:
                data = parse_docx(path)
            except Exception as exc:  # noqa: BLE001
                self.stderr.write(self.style.ERROR(f"Failed: {os.path.basename(path)} — {exc}"))
                continue

            if not data["slug"] or not data["title"]:
                skipped += 1
                self.stderr.write(
                    self.style.WARNING(f"Skipped (missing slug/title): {os.path.basename(path)}")
                )
                continue

            category, accent = pick_category(data["slug"])
            data.update(
                {
                    "category": category,
                    "accent": accent,
                    "order": i,
                    "published_at": base_date - timedelta(days=i * 4),
                    "is_published": True,
                }
            )

            obj, was_created = BlogPost.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            if was_created:
                created += 1
            else:
                updated += 1
            self.stdout.write(
                f"  [{'NEW' if was_created else 'UPD'}] {category:<14} {obj.slug}  ({obj.read_minutes} min)"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {created} created, {updated} updated, {skipped} skipped "
                f"({created + updated} live posts)."
            )
        )
