#!/bin/bash

SRC_DIR="/usr/lib/ckan/default/src"

echo "Minifying all CSS and JS files in: $SRC_DIR"

# Minify CSS files
find "$SRC_DIR" -type f -name "*.css" ! -name "*.min.css" | while read -r css_file; do
    echo "Minifying CSS: $css_file"
    cleancss -o "$css_file" "$css_file"
done

# Minify JS files
find "$SRC_DIR" -type f -name "*.js" ! -name "*.min.js" | while read -r js_file; do
    echo "Minifying JS: $js_file"
    terser "$js_file" -o "$js_file" -c -m
done

echo "✅ All CSS and JS files have been minified in-place."
