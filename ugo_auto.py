#!/usr/bin/env python3
"""
UGO Auto - Automated Permission Management
Handles User/Group/Other permission automation for Hogeii Ultimate
"""

import os
import stat
from pathlib import Path
from datetime import datetime


class UGOAuto:
    """Automated UGO (User/Group/Other) permission management"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.issues_found = []
        self.fixes_applied = []

    def log(self, message):
        """Log message"""
        if self.verbose:
            print(f"[UGO-AUTO] {message}")

    def check_permissions(self, path):
        """Check file/directory permissions"""
        try:
            st = os.stat(path)
            mode = st.st_mode

            # Get octal permission string
            perms = oct(stat.S_IMODE(mode))[-3:]

            return {
                "path": path,
                "permissions": perms,
                "owner": st.st_uid,
                "group": st.st_gid,
                "mode": mode
            }
        except Exception as e:
            self.log(f"Error checking {path}: {e}")
            return None

    def is_insecure(self, perms_dict):
        """Check if permissions are insecure"""
        if not perms_dict:
            return False

        perms = perms_dict['permissions']

        # Check for overly permissive settings
        insecure_patterns = [
            '777',  # Everyone has full access
            '666',  # Everyone can read/write
            '776',  # Group and others have too much access
        ]

        return perms in insecure_patterns

    def scan_permissions(self, target_path):
        """Scan directory for permission issues"""
        self.log(f"Scanning permissions for: {target_path}")

        path = Path(target_path)

        if not path.exists():
            self.log(f"Path does not exist: {target_path}")
            return

        if path.is_file():
            perms = self.check_permissions(target_path)
            if perms and self.is_insecure(perms):
                self.issues_found.append(perms)
                self.log(f"INSECURE: {target_path} has permissions {perms['permissions']}")
        else:
            # Scan directory recursively
            for item in path.rglob('*'):
                perms = self.check_permissions(str(item))
                if perms and self.is_insecure(perms):
                    self.issues_found.append(perms)
                    self.log(f"INSECURE: {item} has permissions {perms['permissions']}")

        self.log(f"Scan complete. Found {len(self.issues_found)} issues")

    def fix_permissions(self, path, new_perms='644'):
        """Fix insecure permissions"""
        try:
            os.chmod(path, int(new_perms, 8))
            self.log(f"Fixed: {path} -> {new_perms}")
            self.fixes_applied.append({
                "path": path,
                "new_permissions": new_perms,
                "timestamp": datetime.now().isoformat()
            })
            return True
        except Exception as e:
            self.log(f"Error fixing {path}: {e}")
            return False

    def auto_fix_permissions(self):
        """Automatically fix permission issues"""
        self.log("Running UGO auto-fix...")

        if not self.issues_found:
            self.log("No issues found to fix")
            return

        for issue in self.issues_found:
            path = issue['path']
            current = issue['permissions']

            # Determine appropriate permissions
            if os.path.isdir(path):
                new_perms = '755'  # rwxr-xr-x for directories
            else:
                new_perms = '644'  # rw-r--r-- for files

            self.log(f"Fixing {path}: {current} -> {new_perms}")
            self.fix_permissions(path, new_perms)

        self.log(f"Auto-fix complete. Applied {len(self.fixes_applied)} fixes")

    def generate_report(self):
        """Generate UGO permissions report"""
        print("\n" + "="*50)
        print("UGO AUTO PERMISSIONS REPORT")
        print("="*50)
        print(f"Issues found: {len(self.issues_found)}")
        print(f"Fixes applied: {len(self.fixes_applied)}")
        print(f"Report generated: {datetime.now()}")
        print("="*50)

        if self.issues_found:
            print("\nIssues Detected:")
            for issue in self.issues_found[:10]:  # Show first 10
                print(f"  {issue['path']}: {issue['permissions']}")

        if self.fixes_applied:
            print("\nFixes Applied:")
            for fix in self.fixes_applied[:10]:  # Show first 10
                print(f"  {fix['path']}: -> {fix['new_permissions']}")

        print()


if __name__ == "__main__":
    # Standalone mode
    import sys

    ugo = UGOAuto(verbose=True)

    if len(sys.argv) > 1:
        target = sys.argv[1]
        ugo.scan_permissions(target)
        ugo.auto_fix_permissions()
        ugo.generate_report()
    else:
        print("Usage: python3 ugo_auto.py <path>")
