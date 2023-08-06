from os.path import abspath, basename, dirname, isdir, isfile, join
from copy import deepcopy
from glob import glob
from json import load as load_json

from click import get_app_dir
from diskcache import Cache
from jinja2 import Template
from requests import get

from .utils import font_metrics
from .utils.svg import text2path
from .utils.xml import format_xml


class Badges():
    # Built-in fonts
    fonts = {
        # (1) Hack
        # See https://github.com/source-foundry/Hack
        'hack-regular': 'hack/Hack-Regular.ttf',
        'hack-bold': 'hack/Hack-Bold.ttf',
        'hack-italic': 'hack/Hack-Italic.ttf',
        'hack-bolditalic': 'hack/Hack-BoldItalic.ttf',

        # (2) Inter
        # See https://github.com/rsms/inter
        'inter-thin': 'inter/Inter-Thin.otf',
        'inter-thinitalic': 'inter/Inter-ThinItalic.otf',
        'inter-extralight': 'inter/Inter-ExtraLight.otf',
        'inter-extralightitalic': 'inter/Inter-ExtraLightItalic.otf',
        'inter-light': 'inter/Inter-Light.otf',
        'inter-lightitalic': 'inter/Inter-LightItalic.otf',
        'inter-regular': 'inter/Inter-Regular.otf',
        'inter-italic': 'inter/Inter-Italic.otf',
        'inter-medium': 'inter/Inter-Medium.otf',
        'inter-mediumitalic': 'inter/Inter-MediumItalic.otf',
        'inter-semibold': 'inter/Inter-SemiBold.otf',
        'inter-semibolditalic': 'inter/Inter-SemiBoldItalic.otf',
        'inter-bold': 'inter/Inter-Bold.otf',
        'inter-bolditalic': 'inter/Inter-BoldItalic.otf',
        'inter-extrabold': 'inter/Inter-ExtraBold.otf',
        'inter-extrabolditalic': 'inter/Inter-ExtraBoldItalic.otf',
        'inter-black': 'inter/Inter-Black.otf',
        'inter-blackitalic': 'inter/Inter-BlackItalic.otf',
    }


    # Cache expiry time (in seconds)
    ttl = 60 * 60 * 24


    def __init__(self, template: str = 'standard', cache_dir: str = None) -> None:
        # Load template configuration
        self.template = template

        # Initialize file cache
        self.cache = Cache(cache_dir or get_app_dir('cb-badges'))


    def get_template_dir(self, template: str) -> str:
        # Set base directory
        base_dir = join(abspath(dirname(__file__)), 'data', 'templates')

        # Assume 'template' representing directory
        template_dir = template

        # If built-in template is available ..
        if template and isdir(join(base_dir, template)):
            # .. load it
            template_dir = join(base_dir, template)

        # If directory does not exist ..
        if not template_dir or not isdir(template_dir):
            # .. raise exception
            raise ValueError('Cannot load template: "%s"' % template)

        return template_dir


    def get_theme(self, theme: str) -> str:
        # Assume 'theme' representing file path
        theme_file = theme

        # If theme is supported ..
        if theme in self.themes:
            # .. load it
            theme_file = join(self.template_dir, 'themes', '%s.json' % theme)

        # If theme file does not exist ..
        if not isfile(theme_file):
            # .. raise exception
            raise ValueError('Cannot load theme: "%s"' % theme)

        return theme_file


    def get_font(self, font: str) -> str:
        # Set base directory
        base_dir = join(abspath(dirname(__file__)), 'data', 'fonts')

        # Assume 'font' representing file path
        font_file = font

        # If font is supported ..
        if font.lower() in self.fonts:
            # .. load it
            font_file = join(base_dir, self.fonts[font.lower()])

        # If font file does not exist ..
        if not isfile(font_file):
            # .. raise exception
            raise ValueError('Cannot load font: "%s"' % font)

        return font_file


    @property
    def template(self) -> str:
        return basename(self.template_dir)


    @template.setter
    def template(self, template: str) -> None:
        # Determine template directory
        template_dir = self.get_template_dir(template)

        # Check if required template files exist ..
        for file in ['config.json', 'template.j2']:
            if not isfile(join(template_dir, file)):
                raise ValueError('Missing required template file: "%s"' % file)

        # Process template files
        # (1) Load configuration file
        with open(join(template_dir, 'config.json'), 'r') as file:
            self.config = load_json(file)

        # (2) Load jinja template
        with open(join(template_dir, 'template.j2'), 'r') as file:
            self.jinja_template = Template(file.read())

            # Provide template functions
            self.jinja_template.globals.update(
                int = int,
                str = str,
                float = float,
                text2path = text2path,
                font_metrics = self.font_metrics,
                render_text = self.render_text
            )

        # Reset themes
        self.themes = []

        # (3) Load themes
        # If theme directory exists ..
        if isdir(join(template_dir, 'themes')):
            # .. assign available themes
            self.themes = [basename(theme)[:-5] for theme in glob(join(template_dir, 'themes', '*.json'))]

        # Assign template directory
        self.template_dir = template_dir


    def render_text(self, text: str, font: str, font_size: int, x: int = 0, y: int = 0) -> dict:
        # Import modules
        from svgpathtools.parser import parse_path

        # Create path
        path = text2path(text, self.get_font(font), font_size, x, y)

        # Determine width & height of path
        x_min, x_max, y_min, y_max = parse_path(path).bbox()

        return {
            'path': '<path d="%s" />' % path,
            'width': x_max - x_min,
            'height': y_max - y_min,
        }


    def font_metrics(self, font: str, font_size: int) -> dict:
        # Determine font file & provide metrics
        return font_metrics(self.get_font(font), font_size)


    def fetch(self, url: str, content_type: str = 'json') -> dict:
        # Check if cache entry exists ..
        if url not in self.cache:
            # ..otherwise create it
            # (1) Fetch data from URL
            response = get(url)

            # (2) Validate it
            if response.status_code != 200:
                raise Exception('Access to API failed with error code: "%s"' % response.reason)

            # (3) Respect content type
            response = response.json() if content_type == 'json' else response.text

            # (4) Create cache entry for URL
            self.cache.set(url, response, self.ttl)

        return self.cache[url]


    def render(self, data: dict, theme: str = None, provider: str = None, minify: bool = False) -> str:
        # Load template configuration
        config = deepcopy(self.config)

        # If no theme provided but template specifies default ..
        if not theme and 'theme' in config:
            # .. fallback to its default theme
            theme = config['theme']

        # Let template know current theme being used
        config['theme'] = theme

        # If theme provided ..
        if theme:
            # .. update configuration
            with open(self.get_theme(theme), 'r') as file:
                config.update(load_json(file))

        # Include custom settings like data or theme options
        config.update(data)

        # If (valid) provider provided ..
        if provider:
            # (1) .. check for repository ..
            if not 'repo' in data:
                # .. otherwise throw exception
                raise Exception('No "repo" specified for provider: "%s"' % provider)

            # (2) .. create data array
            repo = None

            # (3) .. fetch data for current repository
            if provider.lower() in ['cb', 'codeberg']:
                # Popular placeholders:
                #
                # {size}
                # {stars_count}
                # {forks_count}
                # {watchers_count}
                # {open_issues_count}
                # {open_pr_counter}
                # {release_counter}
                # {default_branch}
                repo = self.fetch('https://codeberg.org/api/v1/repos/%s' % data['repo'])

                # For more information,
                # see https://try.gitea.io/api/swagger

                # Add status for 'Woodpecker CI'
                #
                # Placeholder:
                #
                # {status}
                status = 'none'

                svg_string = self.fetch('https://ci.codeberg.org/api/badges/%s/status.svg' % data['repo'], 'text')

                if 'success' in svg_string:
                    status = 'success'

                if 'failure' in svg_string:
                    status = 'failure'

                # Store status information
                repo['status'] = status

            if provider.lower() in ['gh', 'github']:
                # Popular placeholders:
                #
                # {size}
                # {stargazers_count}
                # {watchers_count}
                # {language}
                # {forks_count}
                # {open_issues_count}
                # {default_branch}
                # {license/key}
                # {license/name}
                # {license/spdx_id}
                repo = self.fetch('https://api.github.com/repos/%s' % data['repo'])

                # For more information,
                # see https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api

            # If no repository data is available ..
            if not repo or ('message' in repo and repo['message'].lower() == 'not found'):
                # .. abort execution
                raise Exception('No repository data available: "%s"' % data['repo'])

            # Iterate over data items but skip ..
            for key, value in config.items():
                # (1) .. non-strings
                if not isinstance(value, str):
                    continue

                # (2) .. non-placeholders
                if value[:1] != '{':
                    continue

                # (3) .. reserved keywords
                if key in ['repo']:
                    continue

                # Format placeholder value
                value = value.strip('{}')

                # If placeholder value is present ..
                if value in repo:
                    # .. replace matching entries with repository data
                    config[key] = str(repo[value])

                # Look for nested values
                if '/' in value:
                    value = value.split('/')

                    # If nested placeholder value is present ..
                    if value[0] in repo and value[1] in repo[value[0]]:
                        # .. replace matching entries with nested repository data
                        config[key] = repo[value[0]][value[1]]

        # Render SVG string using data & theme settings
        return format_xml(self.jinja_template.render(data = config), minify)
