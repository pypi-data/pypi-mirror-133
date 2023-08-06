from IPython.core.magic import register_cell_magic
from IPython.display import IFrame
from IPython.core.display import display
from urllib.parse import quote


@register_cell_magic
def tutor(line, cell):
    
    url = "https://pythontutor.com/iframe-embed.html#code="
    url += quote(cell.strip())
    url += "&origin=opt-frontend.js&cumulative=false&heapPrimitives=false"
    url += "&textReferences=false&"
    url += "py=3&rawInputLstJSON=%5B%5D&curInstr=0&codeDivWidth=350&codeDivHeight=500"
    
    display(IFrame(url, height=320, width="100%"))

    