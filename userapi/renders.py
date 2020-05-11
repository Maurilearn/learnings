import markdown

def render_md(mdtext):
    extensions = ['extra', 'smarty']
    html = markdown.markdown(mdtext, extensions=extensions, output_format='html5')
    return html