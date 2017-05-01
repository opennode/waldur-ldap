Name: nodeconductor-ldap
Summary: LDAP plugin for NodeConductor
Group: Development/Libraries
Version: 0.1.0
Release: 1.el7
License: MIT
Url: http://nodeconductor.com
Source0: %{name}-%{version}.tar.gz

Requires: nodeconductor > 0.136.1
Requires: python-ldap >= 2.4.38

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
NodeConductor plugin for structure units management through remote LDAP databases.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Mon May 1 2017 Dmitri Tsumak <dmitri@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package
