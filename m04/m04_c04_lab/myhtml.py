# API to display python objects in Jupyter Notebook
# Written by Cristóbal Montecino

class Html:
    def __init__(self, html):
        self.html = html
        
    def _repr_html_(self):
        return self.html

def _get_html_of(object):
    if '_repr_html_' not in dir(object):
        return str(object)

    return object._repr_html_()

class Tag():
    def __init__(self, tag, object, attributes='', style=''):
        if style != '':
            style_builder = ['style="', style, '"']
            style = ''.join(style_builder)
            
        html_builder = ['<', tag, attributes, style, '>', _get_html_of(object), '</', tag, '>']
        
        self.html = ''.join(html_builder)
            
    def _repr_html_(self):
        return self.html

class TableObject:
    def __init__(self, body, head=None, style=''):
        self.body = body
        self.head = head
        self.style = style

    def _repr_html_(self):
        html_builder = []
        html_builder.append('<table')
        
        html_builder.append(' style="margin-bottom: 0;padding-bottom: 0;')
        html_builder.append(self.style)
        html_builder.append('"')
        
        html_builder.append('>')
        
        if self.head is not None:
            html_builder.append('<thead>')
            for row in self.head:
                html_builder.append('<tr>')
                for displayable in row:
                    html_builder.append('<th style="vertical-align: top; text-align: center;">')
                    html_builder.append(_get_html_of(displayable))
                    html_builder.append('</th>')
                html_builder.append('</tr>')
            html_builder.append('</thead>')
        
        html_builder.append('<tbody>')
        for row in self.body:
            html_builder.append('<tr>')
            for displayable in row:
                html_builder.append('<td style="vertical-align: top; text-align: center;">')
                html_builder.append(_get_html_of(displayable))
                html_builder.append('</td>')
            html_builder.append('</tr>')
        html_builder.append('</tbody>')
        
        html_builder.append('</table>')
    
        return ''.join(html_builder)

BoldTag = lambda x: Tag('b', x)

def Bold(object):    
    if '__iter__' in dir(object) and type(object) is not str:
        return [BoldTag(x) for x in object]
    
    return BoldTag(object)

def Title(object, bold=True, style='', size='h4'):
    if bold is True:
        object = Bold(object)
        
    return Tag(size, object, style=style)
    
def Table(body, head=None, title=None):    
    if title is not None:
        align_to_center = 'margin: auto;'
        table = TableObject(body, head=head, style=align_to_center)
        return TableObject([[table]], head=[[Title(title)]])
    
    return TableObject(body, head=head)