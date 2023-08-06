import click

from . import Badges
from .utils import extract_data


@click.command(context_settings = dict(ignore_unknown_options = True,allow_extra_args = True))
@click.argument('output', type = click.File('w'))
@click.option('-s', '--style', help = 'Set style (name or directory).')
@click.option('-t', '--theme', help = 'Set theme (name or file path).')
@click.option('-p', '--provider', help = 'Set provider (Codeberg, GitHub, ..).')
@click.option('-m', '--minify', is_flag = True, help = 'Whether to minify SVG output.')
@click.option('-v', '--verbose', count = True, help = 'Enable verbose mode.')
@click.version_option('0.3.1')
@click.pass_context
def cli(ctx,
    output: click.File,
    style: str,
    theme: str,
    provider: str,
    minify: bool,
    verbose: int
) -> None:
    """
    Writes SVG file to OUTPUT
    """

    # Attempt to ..
    try:
        # .. load template
        template = style or 'standard'

        # .. initalize object
        badges = Badges(template)

        # .. generate data from unknown arguments
        data = extract_data(ctx.args)

        # .. write SVG string to file
        output.write(badges.render(data, theme, provider, minify))

    # .. otherwise ..
    except Exception as error:
        # (1) .. print error message
        click.echo(error)
