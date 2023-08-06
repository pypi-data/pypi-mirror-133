from lxml import etree


def format_xml(xml_string: str, minify: bool = False) -> str:
    """
    Formats XML string, making it pretty or minified
    """

    # Parse string & remove blank lines
    root = etree.XML(xml_string, parser = etree.XMLParser(remove_blank_text = True))

    # Format XML string
    return etree.tostring(root, pretty_print = not minify, encoding = 'unicode')

    # For more information,
    # see http://www.ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace
