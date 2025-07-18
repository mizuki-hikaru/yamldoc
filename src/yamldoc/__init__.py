import sys
import yaml
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from mistletoe import markdown

TEMPLATE_NAME_REGEX = r'[a-zA-Z0-9._-]+'

def is_valid_template_name(s):
    return re.fullmatch(TEMPLATE_NAME_REGEX, s) is not None

def yamldoc(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Load YAML data
    with input_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if "template" not in data:
        raise ValueError("YAML file must contain a 'template' field at the top level.")

    template_name = data.pop("template")
    if not is_valid_template_name(template_name):
        raise Exception("Invalid template name")

    templates_dir = Path("templates")

    if not (templates_dir / template_name).exists():
        raise FileNotFoundError(f"Template '{template_name}' not found in 'templates/' directory.")

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=select_autoescape(['html', 'xml']))
    env.filters["markdown"] = lambda text: markdown(text or "")
    template = env.get_template(template_name)
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
    parser.add_argument("output", help="Path to output HTML or PDF file")
    args = parser.parse_args()

    try:
        yamldoc(args.input, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
