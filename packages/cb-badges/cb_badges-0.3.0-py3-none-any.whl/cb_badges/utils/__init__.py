def extract_data(args: list) -> dict:
    """
    Processes unknown `click` arguments
    """

    # Create data array
    data = {}

    # Iterate over unknown arguments and ..
    for i, arg in enumerate(args):
        # (1) .. skip values & shorthand arguments
        if arg[:2] != '--':
            continue

        # (2) .. attempt to ..
        try:
            # .. treat them as options
            if args[i + 1][:2] != '--':
                data[arg[2:]] = args[i + 1]

            # .. unless they are flags
            else:
                data[arg[2:]] = True

        # .. otherwise ..
        except IndexError:
            # .. treat them as flags
            data[arg[2:]] = True

    return data

# For more information,
# see https://stackoverflow.com/a/32946412


def font_metrics(font_path: str, font_size: int) -> dict:
    """
    Extracts font metrics
    """

    # Import modules
    from fontline.metrics import MetricsObject
    from fontTools import ttLib

    # Gather information about given font
    # (1) Initialize tooling
    tt = ttLib.TTFont(font_path)
    metrics = MetricsObject(tt, font_path)

    # (2) Extract relevant metrics
    return {
        'metrics': metrics,
        'height': font_size * metrics.hheaascdesc_to_upm,
        'x_height': font_size * metrics.os2_x_height / metrics.units_per_em,
        'ascent': font_size * metrics.hhea_ascent / metrics.units_per_em,
        'descent': font_size * abs(metrics.hhea_descent) / metrics.units_per_em,
    }
