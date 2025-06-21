# yamldoc

yamldoc takes a YAML file and a Jinja2 template and renders a HTML or PDF file,
populating the variables in the  Jinja2 template with data from your YAML file.

## Installation

    pip install https://yamldoc.org/yamldoc.tar.gz

If you need to add it to requirements.txt, add this line:

    https://yamldoc.org/yamldoc.tar.gz

## Usage

Put your Jinja2 template in a directory called `templates/`.

At the beginning of your YAML file, add this value, replacing `example.yaml`
with the name of your template.

    template: example.html

Then, on the command line, run either of these commands:

    % yamldoc input.yaml output.html
    % yamldoc input.yaml output.pdf

Or in Python, you can use it like this:

    from yamldoc import yamldoc

    yamldoc("input.yaml", "output.html")
    yamldoc("input.yaml", "output.pdf")

## Markdown support

You can use markdown in your YAML file and render it with something like this
in the template:

    {{ some_markdown_variable | markdown }}
