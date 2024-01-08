import subprocess
import tempfile

import compliance.scap

def remediate(args):
    ds = compliance.scap.find_ds()
    playbook = tempfile.NamedTemporaryFile(delete=False).name
    generate_playbook_cmd = [
        "oscap", "xccdf", "generate", "fix", "--fix-type", "ansible",
        "--profile", args.profile, "--output", playbook, ds]
    subprocess.run(generate_playbook_cmd)
    ansible_cmd = [
        "ansible-playbook", "--check", "-vvv", "-c", "local", "-i", "localhost,", playbook,
    ]
    subprocess.run(ansible_cmd)
