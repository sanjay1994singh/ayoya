from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "u", "h2", "h3", "h4",
    "ul", "ol", "li", "blockquote", "a", "span",
}
VOID_TAGS = {"br"}
DANGEROUS_TAGS = {"script", "style", "iframe", "object", "embed", "svg", "math"}


class _DescriptionSanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.blocked_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in DANGEROUS_TAGS:
            self.blocked_depth += 1
            return
        if self.blocked_depth or tag not in ALLOWED_TAGS:
            return
        safe_attrs = []
        if tag == "a":
            for name, value in attrs:
                if name.lower() != "href" or not value:
                    continue
                parsed = urlparse(value.strip())
                if parsed.scheme.lower() in {"", "http", "https", "mailto", "tel"}:
                    safe_attrs.append(f'href="{escape(value, quote=True)}"')
            safe_attrs.extend(['rel="nofollow noopener"', 'target="_blank"'])
        suffix = f" {' '.join(safe_attrs)}" if safe_attrs else ""
        self.output.append(f"<{tag}{suffix}>")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in DANGEROUS_TAGS:
            self.blocked_depth = max(0, self.blocked_depth - 1)
            return
        if not self.blocked_depth and tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.output.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.blocked_depth:
            self.output.append(escape(data))


@register.filter
def safe_description(value):
    """Decode legacy escaped editor HTML, then render only approved markup."""
    parser = _DescriptionSanitizer()
    parser.feed(unescape(str(value or "")))
    parser.close()
    return mark_safe("".join(parser.output))
