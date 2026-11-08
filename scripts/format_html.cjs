/* Optional source formatting after generation; no effect on runtime dependencies. */
const fs = require('node:fs');
const path = require('node:path');
const { html: format } = require(process.argv[2] || 'js-beautify');
const root = path.resolve(__dirname, '..');
for (const file of fs.readdirSync(root).filter(file => file.endsWith('.html'))) {
  const target = path.join(root, file);
  fs.writeFileSync(target, format(fs.readFileSync(target, 'utf8'), {
    indent_size: 4,
    wrap_line_length: 120,
    preserve_newlines: true,
    end_with_newline: true,
    content_unformatted: ['pre', 'textarea', 'script'],
  }), 'utf8');
}
console.log('Formatted generated HTML with four-space indentation.');
