from distutils.core import setup


NAME = "argo-probe-onboarding"


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author="SRCE",
    author_email="kzailac@srce.hr",
    description="ARGO probes that check the quality of information collected "
                "during the on-boarding process.",
    url="https://github.com/ARGOeu-Metrics/argo-probe-onboarding",
    package_dir={'argo_probe_onboarding': 'modules'},
    packages=['argo_probe_onboarding'],
    data_files=[('/usr/libexec/argo/probes/onboarding', ['src/check_catalog'])]
)
