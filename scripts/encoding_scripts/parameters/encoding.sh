#!/bin/bash
python3 scripts/convert_md_to_tei.py markdown/ tei/
python3 scripts/additional_modifications.py tei/ tei/
python3 scripts/correct_regex.py tei/ tei/