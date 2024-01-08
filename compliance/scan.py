import compliance.scap
import os
import subprocess
import tempfile

import compliance.profiles
from compliance.constants import SSG_PROFILE_PREFIX

def scan(args):
    ds = compliance.scap.find_ds()
    arf = None
    profiles = compliance.profiles.get_profiles(ds)
    if args.profile not in profiles:
        print(f"Profile {args.profile} doesn't exist. Available profiles are:")
        for profile in profiles.values():
            print(f"{profile.id:20} {profile.title}")
        exit(1)
    
    full_id = SSG_PROFILE_PREFIX + args.profile
    cmd = ["oscap", "xccdf", "eval", "--progress", "--profile", full_id]
    if args.report or args.json:
        arf = tempfile.NamedTemporaryFile(delete=False).name
        cmd += ["--results-arf", arf]
    cmd.append(ds)
    proc = subprocess.run(cmd)
    if args.report:
        cmd = ["oscap-report", "--output", args.report, arf]
        subprocess.run(cmd)
    if args.json:
        cmd = ["oscap-report", "-f", "JSON", "--output", args.json, arf]
        subprocess.run(cmd)
        os.unlink(arf)
