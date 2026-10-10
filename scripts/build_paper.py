#!/usr/bin/env python3
"""Generate a self-contained LaTeX source; optionally export PDF with installed Tectonic."""
from pathlib import Path
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIGURES = [r'''
\begin{center}
\begin{tikzpicture}
\node[box,text width=29mm] (op) at (-4,0) {OPERATE\\approved work};
\node[box,text width=29mm] (im) at (0,0) {IMPROVE\\evidence and proposal};
\node[box,text width=29mm] (dv) at (4,0) {DEVELOP\\capabilities and tests};
\node[box,text width=85mm] (sr) at (0,1.8) {Semantic and capability registries\\immutable bundles; version-aware knowledge service};
\node[box,text width=38mm] (orc) at (0,3.6) {Durable orchestration\\lifecycle state and delegation};
\node[box,text width=29mm] (ev) at (4,-2.2) {Independent evaluation\\semantics\\policy and state};
\node[box,text width=29mm] (ag) at (0,-2.2) {Approval gateway\\exact bundle and scope};
\node[box,text width=29mm] (dc) at (-4,-2.2) {Deployment controller\\activation epoch};
\node[box,text width=29mm] (ax) at (-4,-4.4) {Action gateway\\authority, epoch, facts};
\node[box,text width=29mm] (au) at (0,-4.4) {Audit and evidence\\decision records};
\node[box,text width=29mm] (ex) at (4,-4.4) {External systems\\consequential effects};
\draw[flow] (op) -- (im);
\draw[flow] (im) -- (dv);
\draw[flow] (dv) -- (ev);
\draw[flow] (ev) -- (ag);
\draw[flow] (ag) -- (dc);
\draw[flow] (dc) -- (op);
\draw[flow] (op.west) -- ++(-.4,0) |- (ax.west);
\draw[flow] (ax) -- (au);
\draw[flow] (ax.south) -- ++(0,-.6) -| (ex.south);
\draw[flow] (orc) -- (sr);
\draw[flow] (sr) -- (im);
\draw[flow] (sr.south -| op.north) -- (op.north);
\draw[flow] (sr.south -| dv.north) -- (dv.north);
\end{tikzpicture}
\end{center}
''', r'''
\begin{center}
\begin{tikzpicture}
\node[box,text width=32mm] (r) at (-4,0) {Report and investigate};
\node[box,text width=32mm] (p) at (0,0) {Candidate proposal};
\node[box,text width=32mm] (b) at (4,0) {Authorized build};
\node[box,text width=32mm] (v) at (4,-1.5) {Validate exact bundle};
\node[box,text width=32mm] (a) at (0,-1.5) {Independent approval};
\node[box,text width=32mm] (s) at (-4,-1.5) {Stage and verify state};
\node[box,text width=32mm] (act) at (-4,-3) {Activate at new epoch};
\node[box,text width=32mm] (mon) at (0,-3) {Monitor\\active release};
\node[box,text width=32mm] (rec) at (4,-3) {Recovery or retirement};
\draw[flow] (r) -- (p);
\draw[flow] (p) -- (b);
\draw[flow] (b) -- (v);
\draw[flow] (v) -- (a);
\draw[flow] (a) -- (s);
\draw[flow] (s) -- (act);
\draw[flow] (act) -- (mon);
\draw[flow] (mon) -- (rec);
\draw[flow,dashed] (rec.south) -- ++(0,-.65) -| ([xshift=-4mm]s.west) -- (s.west);
\node[align=center,font=\footnotesize\sffamily,text width=110mm] at (0,-4.9) {Rejected candidates remain recorded. Recovery needs an approved compatible bundle. Development authorization does not authorize deployment.};
\end{tikzpicture}
\end{center}
''']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', action='store_true', help='Export with already-installed Tectonic after generating source')
    args = parser.parse_args()
    source = (ROOT / 'paper.md').read_text()
    source = source.replace('# Declarations {.unnumbered}',
        '```{=latex}\n\\Needspace{16\\baselineskip}\n```\n\n# Declarations {.unnumbered}')
    source = source.replace('# References {.unnumbered}',
        '# References {.unnumbered}\n\n```{=latex}\n\\begingroup\n'
        '\\small\n\\setlength{\\parindent}{-1.5em}\n'
        '\\setlength{\\leftskip}{1.5em}\n\\setlength{\\parskip}{3pt}\n'
        '\\interlinepenalty=10000\n```')
    source += '\n\n```{=latex}\n\\endgroup\n```\n'
    figures = iter(FIGURES)
    def render_figure(match):
        caption = subprocess.check_output(
            ['pandoc', '--from=markdown', '--to=latex'], input=match[1], text=True).strip()
        diagram = next(figures).replace(r'\begin{center}', '').replace(r'\end{center}', '')
        return ('\n```{=latex}\n\\begin{figure}[htbp]\n\\centering\n' + diagram
                + '\n\\caption{' + caption + '}\n\\end{figure}\n```\n')
    source, figure_count = re.subn(r'```mermaid\n.*?\n```\s*\*Figure \d+\. (.*?)\*',
                                  render_figure, source, flags=re.S)
    if figure_count != len(FIGURES):
        raise ValueError('Expected a numbered caption for each manuscript figure')
    temp = ROOT / 'tmp'
    temp.mkdir(exist_ok=True)
    prepared = temp / 'paper-render.md'
    prepared.write_text(source)
    # Read identifiers from manuscript metadata while keeping the final TeX standalone.
    metadata = json.loads(subprocess.check_output(
        ['pandoc', str(prepared), '--from=markdown+tex_math_dollars+raw_tex', '--to=json'],
        text=True))['meta']
    orcid = ''.join(item.get('c', '') for item in metadata['orcid']['c'] if item['t'] == 'Str')
    if not re.fullmatch(r'https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[\dX]', orcid):
        raise ValueError('Expected a complete ORCID URL in manuscript metadata')
    release = ROOT / 'release'
    release.mkdir(exist_ok=True)
    subprocess.run(['pandoc', str(prepared), '--standalone', '--to=latex',
                    '--from=markdown+tex_math_dollars+raw_tex', '--number-sections',
                    '--top-level-division=section', '--pdf-engine=tectonic',
                    '--template=' + str(ROOT / 'scripts/journal-template.tex'),
                    '-V', 'orcid-id=' + orcid.rsplit('/', 1)[-1],
                    '--include-in-header=' + str(ROOT / 'scripts/paper-header.tex'),
                    '-o', str(release / 'paper.tex')], check=True)
    # These short prose tables fit on one page; floats prevent orphaned rows.
    tex_path = release / 'paper.tex'
    tex = tex_path.read_text()
    table_number = 0
    def keep_table_together(match):
        nonlocal table_number
        table_number += 1
        table = match[0]
        caption_start = table.index(r'\caption{')
        caption_end = table.index(r'\tabularnewline', caption_start)
        preamble = table[:caption_start].replace(r'\begin{longtable}[]', r'\begin{tabular}')
        caption = table[caption_start:caption_end]
        header = table[table.index(r'\toprule'):table.index(r'\endfirsthead')]
        body = table[table.index(r'\endlastfoot') + len(r'\endlastfoot'):table.index(r'\end{longtable}')]
        gap = '7pt' if table_number == 1 else '4pt'
        body = body.replace(r'\\', r'\\' + '\n' + r'\addlinespace[' + gap + ']')
        return ('\n' + r'\begin{table}[!htbp]\centering\footnotesize' + '\n'
                + caption + '\n' + r'\medskip' + '\n' + preamble + header + body
                + r'\bottomrule' + '\n' + r'\end{tabular}' + '\n' + r'\end{table}' + '\n')
    tex = re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}',
                 keep_table_together, tex, flags=re.S)
    tex_path.write_text(tex)
    if args.pdf:
        subprocess.run(['tectonic', '--outdir', str(release), '--keep-logs', str(release / 'paper.tex')], check=True)
    print(release / ('paper.pdf' if args.pdf else 'paper.tex'))

if __name__ == '__main__':
    main()
