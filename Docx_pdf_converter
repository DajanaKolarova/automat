# file path
INPUT_DIR=""
OUTPUT_DIR="$INPUT_DIR/pdf_output"
MERGED="$OUTPUT_DIR/mergedfile.pdf"

# find LibreOffice CLI
if [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
  LO="/Applications/LibreOffice.app/Contents/MacOS/soffice"
elif command -v soffice >/dev/null; then
  LO="soffice"
else
  echo "Error: soffice Not Found (LibreOffice CLI). Instal LibreOffice." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
echo "1) Converting DOCX → PDF…"
for docx in "$INPUT_DIR"/*.docx; do
  echo "   → $(basename "$docx")"
  "$LO" --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$docx"
done

echo "2)PDF merging"
if command -v gs >/dev/null; then
  gs -dBATCH -dNOPAUSE -q \
     -sDEVICE=pdfwrite \
     -sOutputFile="$MERGED" \
     "$OUTPUT_DIR"/*.pdf
  echo "Merged PDF: $MERGED"
elif command -v pdfunite >/dev/null; then
  pdfunite "$OUTPUT_DIR"/*.pdf "$MERGED"
  echo "Merged PDF: $MERGED"
else
  echo "Ghostscript (gs) or pdfunite not found – not merged PDF in $OUTPUT_DIR"
fi

echo "Done ✅"

