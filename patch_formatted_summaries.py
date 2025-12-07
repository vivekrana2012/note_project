import os
import glob
from summary_formatter import format

def patch_formatted_summaries():
    """
    Find and format all final_summary files in the resources directory
    """
    resources_dir = "resources"
    
    if not os.path.exists(resources_dir):
        print(f"Resources directory not found: {resources_dir}")
        return
    
    # Find all final_summary files
    pattern = os.path.join(resources_dir, "**", "final_summary__*.txt")
    summary_files = glob.glob(pattern, recursive=True)
    
    if not summary_files:
        print("No final summary files found.")
        return
    
    print(f"Found {len(summary_files)} summary files to process.\n")
    
    successful = 0
    failed = 0
    
    for i, filepath in enumerate(summary_files, 1):
        print(f"\n{'='*80}")
        print(f"Processing {i}/{len(summary_files)}: {filepath}")
        print(f"{'='*80}")
        
        try:
            formatted_file = format(filepath)
            print(f"✓ Successfully formatted: {formatted_file}")
            successful += 1
        except Exception as e:
            print(f"✗ Error formatting {filepath}: {e}")
            failed += 1
            continue
    
    print(f"\n{'='*80}")
    print(f"Batch processing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"{'='*80}")

if __name__ == "__main__":
    patch_formatted_summaries()
