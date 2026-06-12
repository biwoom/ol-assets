import os
import shutil
from pathlib import Path

def migrate():
    # Base log directory
    log_base = Path("BuddhaStory/log")
    
    # Fallback lookup if not run from the correct directory
    if not log_base.exists():
        alternative = Path(__file__).resolve().parents[3] / "log"
        if alternative.exists():
            log_base = alternative
        else:
            print("Error: BuddhaStory/log directory not found.")
            return

    # Target directories
    draft1_dir = log_base / "draft-1"
    draft2_dir = log_base / "draft-2"

    # Create target directories
    draft1_dir.mkdir(parents=True, exist_ok=True)
    draft2_dir.mkdir(parents=True, exist_ok=True)

    print(f"Base log directory: {log_base.resolve()}")
    print(f"Target Draft-1: {draft1_dir.resolve()}")
    print(f"Target Draft-2: {draft2_dir.resolve()}")

    # Iterate files directly in log_base (not recursively, so we don't scan subdirectories)
    moved_count = 0
    for item in log_base.iterdir():
        if item.is_file() and item.suffix == ".md":
            filename = item.name
            if filename.endswith("-draft2-log.md"):
                dest = draft2_dir / filename
                print(f"Moving {filename} -> draft-2/")
                shutil.move(str(item), str(dest))
                moved_count += 1
            elif filename.endswith("-log.md"):
                dest = draft1_dir / filename
                print(f"Moving {filename} -> draft-1/")
                shutil.move(str(item), str(dest))
                moved_count += 1

    print(f"\nMigration completed. Total {moved_count} file(s) migrated.")

if __name__ == "__main__":
    migrate()
