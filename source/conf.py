# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import re

def replace_gfm_callouts(app, docname, source):
    """
    将 GFM 风格的 callout:
    > [!NOTE]
    > 内容
    转换为 MyST 指令：
    ```{note}
    内容
    ```
    支持大小写、不同行尾（CRLF/LF）、inline 内容，以及多行 body。
    """
    if not source:
        return
    text = source[0]
    if not isinstance(text, str):
        return

    # 规范换行，避免 CRLF 导致匹配问题
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    lines = text.splitlines(keepends=True)
    out_lines = []
    i = 0

    open_re = re.compile(r'^[ \t]*>\s*\[!(note|tip|warning|important|caution)\]\s*(.*)$', re.IGNORECASE)
    body_re = re.compile(r'^[ \t]*>\s?(.*)$')

    while i < len(lines):
        m = open_re.match(lines[i])
        if not m:
            out_lines.append(lines[i])
            i += 1
            continue

        kind = m.group(1).lower()
        first_inline = m.group(2)  # 可能为空，也可能是 inline 内容（无换行）
        body_parts = []

        # 如果开头行包含 inline 内容，先加入
        if first_inline:
            # 保留内容，但不自动添加换行（后面会处理）
            body_parts.append(first_inline)

        j = i + 1
        # 收集所有以 '>' 开头的行作为 body
        while j < len(lines):
            mb = body_re.match(lines[j])
            if not mb:
                break
            content = mb.group(1)
            # lines[j] 带有原始换行符，保持换行
            if lines[j].endswith('\n'):
                content = content + '\n'
            body_parts.append(content)
            j += 1

        # 组装 body_text，保证末尾有换行
        if body_parts:
            # 如果第一个元素没有换行且后面有多行，则补换行
            if not body_parts[0].endswith('\n') and len(body_parts) > 1:
                body_parts[0] = body_parts[0] + '\n'
            body_text = ''.join(body_parts)
        else:
            body_text = ''

        if body_text and not body_text.endswith('\n'):
            body_text = body_text + '\n'

        new_block = f"```{{{kind}}}\n{body_text}```\n"
        out_lines.append(new_block)
        i = j

    source[0] = ''.join(out_lines)

def setup(app):
    app.connect("source-read", replace_gfm_callouts)

project = 'TonyPi & TonyPi Pro'
copyright = '2025, Hiwonder'
author = 'Hiwonder'
release = 'v2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_markdown_tables','myst_parser','sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"  # 或者其他主题，如 'friendly', 'monokai'
html_codeblock_linenos_style = 'table'  # 推荐的样式

myst_enable_extensions = [
    "attrs_block",
    "colon_fence",
    "substitution",
    "dollarmath",
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['style.css']
html_js_files = ['custom.js']
html_theme_options = {
    'style_nav_header_background': '#f98800',
}
