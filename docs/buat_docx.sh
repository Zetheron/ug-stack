#!/bin/sh
# Membuat LAPORAN_UG-STACK.docx dari berkas Markdown (butuh pandoc). Jalankan dari folder docs/.
pandoc _laporan_docx.md -o LAPORAN_UG-STACK.docx --toc --toc-depth=2 --resource-path=. --highlight-style=tango -M toc-title="Daftar Isi"
