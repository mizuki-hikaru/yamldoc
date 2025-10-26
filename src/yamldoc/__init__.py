import sys
import yaml
import re
from markupsafe import Markup
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mistletoe import markdown

def yamldoc(input_path, template_path, output_path):
    input_path = Path(input_path)
    template_path = Path(template_path)
    output_path = Path(output_path)

    # Load YAML data
    with input_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    templates_dir = template_path.parent

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=select_autoescape(['html', 'xml']))
    env.filters["markdown"] = lambda text: Markup(markdown(text or ""))
    template = env.get_template(template_path.name)
    rendered_html = template.render(**data, _context=data)

    # Output
    if output_path.suffix == ".pdf":
        from weasyprint import HTML
        HTML(string=rendered_html, base_url=".").write_pdf(str(output_path))
    else:
        output_path.write_text(rendered_html, encoding='utf-8')

def cli():
    import argparse

    parser = argparse.ArgumentParser(description="Render HTML or PDF from a YAML file and Jinja2 template.")
    parser.add_argument("input", help="Path to input YAML file")
    parser.add_argument("template", help="Path to Jinja2 template file")
    parser.add_argument("output", help="Path to output HTML or PDF file")
    args = parser.parse_args()

    try:
        yamldoc(args.input, args.template, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
