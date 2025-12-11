import csv
import sys
from pathlib import Path

def create_mapping_file(source_csv, mapping_csv):
    """
    Step 1: Create a mapping file from the source CSV.
    Format: "key","original_text"
    Skips the first 3 header rows (Language, blank, NormalText)
    """
    rows_written = 0
    
    with open(source_csv, 'r', encoding='utf-8') as fin, \
         open(mapping_csv, 'w', encoding='utf-8', newline='') as fout:
        
        reader = csv.reader(fin)
        writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
        
        # Skip first 3 header rows
        for _ in range(3):
            next(reader, None)
        
        for row in reader:
            if len(row) >= 3:
                key = row[0]
                original_text = row[1]
                
                # Write only key and original text
                writer.writerow([key, original_text])
                rows_written += 1
    
    print(f"✅ Created mapping file: {mapping_csv}")
    print(f"   Extracted {rows_written} entries (skipped 3 header rows)")
    print(f"\n📝 Next step: Edit {mapping_csv} to replace column 2 with your translations")
    print(f"   Change format from: \"key\",\"original_text\"")
    print(f"   To:                 \"key\",\"new_text\"")


def build_translation_file(source_csv, mapping_csv, output_csv):
    """
    Step 2: Build the final translation CSV.
    Combines: "key" (from original), "original_text" (from original), "new_text" (from mapping)
    Preserves the first 3 header rows from the source.
    """
    # Load the mapping file (key -> new_text)
    translations = {}
    with open(mapping_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                key = row[0]
                new_text = row[1]
                translations[key] = new_text
    
    print(f"📖 Loaded {len(translations)} translations from {mapping_csv}")
    
    # Build the output CSV
    rows = []
    matched_count = 0
    header_count = 0
    
    with open(source_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Preserve first 3 header rows as-is
        for _ in range(3):
            header_row = next(reader, None)
            if header_row:
                rows.append(header_row)
                header_count += 1
        
        # Process data rows
        for row in reader:
            if len(row) >= 3:
                key = row[0]
                original_text = row[1]
                
                # Use new text from mapping, or fall back to original translation
                if key in translations:
                    new_text = translations[key]
                    matched_count += 1
                else:
                    new_text = row[2]  # Keep original if no mapping exists
                
                rows.append([key, original_text, new_text])
    
    # Write the final CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(rows)
    
    print(f"✅ Created translation file: {output_csv}")
    print(f"   Preserved {header_count} header rows")
    print(f"   Updated {matched_count} translations")
    print(f"   Total rows: {len(rows)}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Step 1: python translation_tool.py create <source.csv> [mapping.csv]")
        print("  Step 2: python translation_tool.py build <source.csv> <mapping.csv> [output.csv]")
        print("\nExample:")
        print("  python translation_tool.py create #GF_hypocritical.csv my_translations.csv")
        print("  # Edit my_translations.csv with your changes")
        print("  python translation_tool.py build #GF_hypocritical.csv my_translations.csv #GF_custom.csv")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        if len(sys.argv) < 3:
            print("❌ Error: Missing source file")
            print("Usage: python translation_tool.py create <source.csv> [mapping.csv]")
            return
        
        source_csv = sys.argv[2]
        mapping_csv = sys.argv[3] if len(sys.argv) > 3 else 'translations_to_edit.csv'
        
        if not Path(source_csv).exists():
            print(f"❌ Error: Source file not found: {source_csv}")
            return
        
        create_mapping_file(source_csv, mapping_csv)
    
    elif command == 'build':
        if len(sys.argv) < 4:
            print("❌ Error: Missing arguments")
            print("Usage: python translation_tool.py build <source.csv> <mapping.csv> [output.csv]")
            return
        
        source_csv = sys.argv[2]
        mapping_csv = sys.argv[3]
        output_csv = sys.argv[4] if len(sys.argv) > 4 else '#GF_custom.csv'
        
        if not Path(source_csv).exists():
            print(f"❌ Error: Source file not found: {source_csv}")
            return
        
        if not Path(mapping_csv).exists():
            print(f"❌ Error: Mapping file not found: {mapping_csv}")
            return
        
        build_translation_file(source_csv, mapping_csv, output_csv)
    
    else:
        print(f"❌ Error: Unknown command '{command}'")
        print("Valid commands: create, build")


if __name__ == '__main__':
    main()