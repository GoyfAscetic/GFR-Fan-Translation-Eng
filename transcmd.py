import csv
import argparse
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
    Copies the first 3 header rows EXACTLY as-is (no quote wrapping).
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
    
    matched_count = 0
    data_rows = []
    
    # Read source file and process
    with open(source_csv, 'r', encoding='utf-8') as fin:
        # Read first 3 lines RAW (no CSV parsing)
        header_lines = []
        for _ in range(3):
            line = fin.readline()
            if line:
                header_lines.append(line)
        
        # Now process the rest with CSV reader
        reader = csv.reader(fin)
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
                
                data_rows.append([key, original_text, new_text])
    
    # Write the final CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as fout:
        # Write first 3 header lines RAW (exactly as they were)
        for line in header_lines:
            fout.write(line)
        
        # Write data rows with quote wrapping
        writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
        writer.writerows(data_rows)
    
    print(f"✅ Created translation file: {output_csv}")
    print(f"   Preserved 3 header lines (raw copy)")
    print(f"   Updated {matched_count} translations")
    print(f"   Total data rows: {len(data_rows)}")


def main():
    """Main entry point with argparse"""
    parser = argparse.ArgumentParser(
        description='Translation tool for Gunfire Reborn CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Step 1: Create a mapping file
  python transcmd.py create #GF_hypocritical.csv -o my_translations.csv
  
  # Step 2: Edit my_translations.csv with your translations
  
  # Step 3: Build the final translation file
  python transcmd.py build #GF_hypocritical.csv my_translations.csv -o #GF_custom.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser(
        'create',
        help='Create a mapping file from source CSV'
    )
    create_parser.add_argument(
        'source',
        type=str,
        help='Source CSV file (e.g., #GF_hypocritical.csv)'
    )
    create_parser.add_argument(
        '-o', '--output',
        type=str,
        default='translations_to_edit.csv',
        help='Output mapping file (default: translations_to_edit.csv)'
    )
    
    # Build command
    build_parser = subparsers.add_parser(
        'build',
        help='Build final translation file from source and mapping'
    )
    build_parser.add_argument(
        'source',
        type=str,
        help='Source CSV file (e.g., #GF_hypocritical.csv)'
    )
    build_parser.add_argument(
        'mapping',
        type=str,
        help='Mapping CSV file with your translations'
    )
    build_parser.add_argument(
        '-o', '--output',
        type=str,
        default='#GF_custom.csv',
        help='Output translation file (default: #GF_custom.csv)'
    )
    
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Execute the appropriate command
    if args.command == 'create':
        source_path = Path(args.source)
        
        if not source_path.exists():
            print(f"❌ Error: Source file not found: {args.source}")
            return
        
        create_mapping_file(args.source, args.output)
    
    elif args.command == 'build':
        source_path = Path(args.source)
        mapping_path = Path(args.mapping)
        
        if not source_path.exists():
            print(f"❌ Error: Source file not found: {args.source}")
            return
        
        if not mapping_path.exists():
            print(f"❌ Error: Mapping file not found: {args.mapping}")
            return
        
        build_translation_file(args.source, args.mapping, args.output)


if __name__ == '__main__':
    main()