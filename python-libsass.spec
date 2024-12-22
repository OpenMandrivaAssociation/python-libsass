%global srcname libsass

Name:           python-%{srcname}
Version:        0.22.0
Release:        1
Summary:        Python bindings for libsass
Group:          Development/Python
License:        MIT
URL:            https://github.com/sass/libsass-python
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  python-devel
BuildRequires:  python-six
#BuildRequires:  python3-pytest
BuildRequires:  python-werkzeug
BuildRequires:  pkgconfig(libsass)
# Needed for docs
#BuildRequires:  python-sphinx

Requires:       python3-six

%description
This package provides a simple Python extension module
sass which is binding Libsass (written in C/C++ by Hampton
Catlin and Aaron Leung).

%prep
%autosetup -n %{srcname}-python-%{version} -p1

%build
# Export SYSTEM_SASS environment variable to use the
# system library, not the bundled one
export SYSTEM_SASS="true"
%py_build

%install
# Same as above
export SYSTEM_SASS="true"
%py_install
#install -m 644 -D docs/_build/man/pysassc.1 %{buildroot}%{_mandir}/man1/pysassc.1

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/_sass*.so
%{python3_sitearch}/%{srcname}-%{version}.dist-info/
%{python3_sitearch}/sass.py
%{python3_sitearch}/pysassc.py
%{python3_sitearch}/sasstests.py
%{python3_sitearch}/sassutils/
%{_mandir}/man1/pysassc.1.*
%{_bindir}/pysassc
