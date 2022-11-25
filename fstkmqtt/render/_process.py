import re
import os

class GetRender:
    def _render_common( html, js, css) -> tuple:
        patternhead = '</head>'
        patternbody = '</body>'

        if js: jscode = f"<script>{js}</script>"
        else: jscode = ""

        if css: csscode = f"<style>{css}</style>"
        else: csscode = ""

        loc = html.find(patternhead)
        html = html[:loc] + jscode + html[loc:]

        loc = html.find(patternbody)
        html = html[:loc] + csscode + html[loc:]

        html = html.strip().encode()
        return html, len(html)

    def _render_with_base_html(basehtml, html, js, css) -> tuple:
        dpattern = {
            'block' : '%begin {name}%[\W\s<>\w]*%end {name}%',
            'blockbase': '%[a-zA-Z]*%',
        }

        _list_match = {}
        for match in re.finditer(dpattern['blockbase'], basehtml): 
            tmp_ = match.group().replace('%', '')
            try:
                tmp = re.search(f"{dpattern['block'].format(name=tmp_)}", html).group()
                tmp = tmp.splitlines()
                tmp = tmp[1:-1]
                tmp = '\n'.join([i.strip() for i in tmp])
            except:
                tmp = ""
            finally:
                basehtml = basehtml.replace(f'%{tmp_}%', tmp)
        patternEmptyNoUse = r'[ ]+\n'
        for i in re.finditer(patternEmptyNoUse, basehtml):
            basehtml = basehtml.replace(i.group(), '')
        return GetRender._render_common(basehtml, js, css)
 
    def Render(**options) -> tuple:
        '''
        \roptions:
        \r - filehtml strOrBytesPath
        \r - filecss strOrBytesPath
        \r - filejs strOrBytesPath
        \r - listfilecss strOrBytesPath
        \r - listfilejs strOrBytesPath
        \r - basehtml strOrBytesPath
        \r - basetohtml strOrBytesPath
        \r - basetocss strOrBytesPath
        \r - basetojs strOrBytesPath
        '''
        filehtml = options.pop('filehtml', None)
        if not filehtml: raise ValueError('')
        filecss = options.pop('filecss', None)
        filejs = options.pop('filejs', None)
        listfilecss = options.pop('listfilecss', [])
        listfilejs = options.pop('listfilejs', [])
        basehtml = options.pop('basehtml', None)
        basetohtml = options.pop('basetohtml', '')
        basetocss = options.pop('basetocss', '')
        basetojs = options.pop('basetojs', '')

        datahtml = None
        datacss = None
        datajs = None
        basehtml = None

        try: 
            with open(os.path.join(basetohtml, filehtml), 'rb') as f: datahtml = f.read().decode()
        except FileNotFoundError: print ("Not found file: '%s' with abspath is '%s'"%(filehtml, os.path.join(basetohtml, filehtml)))

        listfilejs.append(filejs)
        listfilecss.append(filecss)

        datacss = ''
        for file_css in listfilecss:
            try:
                with open(os.path.join(basetocss, file_css), 'rb') as f: datacss += "\n%s"%f.read().decode()
            except FileNotFoundError: print ("Not found file: '%s' with abspath is '%s'"%(file_css, os.path.join(basetocss, file_css)))
        datacss =datacss.strip()

        datajs = ''
        for file_js in listfilejs:
            try:
                with open(os.path.join(basetojs, file_js), 'rb') as f: datajs += "\n%s"%f.read().decode()
            except FileNotFoundError: print ("Not found file: '%s' with abspath is '%s'"%(file_js, os.path.join(basetojs, file_js)))
        datajs =datajs.strip()

        if basehtml:
            try: 
                with open(os.path.join(basetohtml, basehtml), 'rb') as f: basehtml = f.read().decode()
            except FileNotFoundError: print ("Not found file: '%s' with abspath is '%s'"%(basehtml, os.path.join(basetohtml, basehtml)))

        if basehtml:
            return GetRender._render_with_base_html(basehtml, datahtml, datajs, datacss) 
        else:
            return GetRender._render_common(datahtml, datajs, datacss)