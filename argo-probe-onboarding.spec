%define underscore() %(echo %1 | sed 's/-/_/g')

Summary:       ARGO probes that check the quality of information collected during the on-boarding process.
Name:          argo-probe-onboarding
Version:       0.1.0
Release:       1%{?dist}
Source0:       %{name}-%{version}.tar.gz
License:       ASL 2.0
Group:         Development/System
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix:        %{_prefix}
BuildArch:     noarch

BuildRequires: python3-devel
Requires:      python3-requests


%description
ARGO probes that check the quality of information collected during the on-boarding process.

%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root)
%dir %{python3_sitelib}/%{underscore %{name}}/
%{python3_sitelib}/%{underscore %{name}}/*.py


%changelog
* Thu Mar 2 2023 Katarina Zailac <kzailac@srce.hr> - 0.1.0-1
- ARGO-4221 check_catalog probe returning wrong CRITICAL status
- ARGO-4211 Create a probe for on-boarding process monitoring
