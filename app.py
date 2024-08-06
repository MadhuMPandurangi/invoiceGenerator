from weasyprint import HTML
html = HTML('invoice.html')
html.write_pdf('invoice.pdf')