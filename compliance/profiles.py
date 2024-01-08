import xml.etree.ElementTree as ET
import collections
import compliance.scap

from compliance.constants import (
    NAMESPACES, SSG_PROFILE_PREFIX, SSG_RULE_PREFIX)

Profile = collections.namedtuple("Profile", ["id", "title", "description"])


def get_profiles(ds_path):
    profiles = dict()
    root = ET.parse(ds_path).getroot()
    profiles_xpath = ".//xccdf:Profile"
    for profile_el in root.findall(profiles_xpath, namespaces=NAMESPACES):
        id_ = profile_el.get("id").replace(SSG_PROFILE_PREFIX, "")
        title_el = profile_el.find("./xccdf:title", namespaces=NAMESPACES)
        title = "".join(title_el.itertext())
        description_el = profile_el.find(
            "./xccdf:description", namespaces=NAMESPACES)
        description = "".join(description_el.itertext())
        profile = Profile(id=id_, title=title, description=description)
        profiles[id_] = profile
    return profiles


def list_profiles(args):
    ds = compliance.scap.find_ds()
    profiles = get_profiles(ds)
    for profile in profiles.values():
        print(f"{profile.id:20} {profile.title}")


def _get_selected_rules(profile_el):
    rules = []
    selects = profile_el.findall("./xccdf:select", namespaces=NAMESPACES)
    for select in selects:
        idref = select.get("idref")
        if idref.startswith(SSG_RULE_PREFIX):
            rule_id = idref.replace(SSG_RULE_PREFIX, "")
            rules.append(rule_id)
    return sorted(rules)

def info_profile(args):
    ds = compliance.scap.find_ds()
    root = ET.parse(ds).getroot()
    full_id = SSG_PROFILE_PREFIX + args.profile
    profile_xpath = f".//xccdf:Profile[@id='{full_id}']"
    profile_el = root.find(profile_xpath, namespaces=NAMESPACES)
    title_el = profile_el.find("./xccdf:title", namespaces=NAMESPACES)
    title = "".join(title_el.itertext())
    print(title)
    print("*" * len(title))
    print()

    profile_id = profile_el.get("id").replace(SSG_PROFILE_PREFIX, "")
    print(f"Profile ID: {profile_id}")
    print()


    description_el = profile_el.find("./xccdf:description", namespaces=NAMESPACES)
    description = "".join(description_el.itertext())
    print(description)

    if args.list_rules:
        print()
        print("Rules:")
        for rule_id in _get_selected_rules(profile_el):
            print(f"- {rule_id}")
