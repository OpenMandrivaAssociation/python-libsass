%global srcname libsass

Name:           python-%{srcname}
Version:        0.22.0
Release:        1
Summary:        Python bindings for libsass
Group:          Development/Python

License:        MIT
URL:            https://github.com/sass/libsass-python
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
# Patch for correct naming of manpages
Patch0:         python-libsass-man.patch
Patch1:         0001-Fix-sphinx-extlinks-warning.patch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-six
BuildRequires:  python3-pytest
BuildRequires:  python3-werkzeug
BuildRequires:  pkgconfig(libsass)
BuildRequires:  gcc-c++
# Needed for docs
BuildRequires:  python3-sphinx

%description
This package provides a simple Python extension module
sass which is binding Libsass (written in C/C++ by Hampton
Catlin and Aaron Leung).

%package -n python3-%{srcname}
Summary:        Python 3 bindings for libsass
Group:          Development/Python
%{?python_provide:%python_provide python3-%{srcname}}

Requires:       python3-six

%description -n python3-%{srcname}
This package provides a simple Python 3 extension module
sass which is binding Libsass (written in C/C++ by Hampton
Catlin and Aaron Leung).

%prep
%autosetup -n %{srcname}-python-%{version} -p1

%build
# Export SYSTEM_SASS environment variable to use the
# system library, not the bundled one
export SYSTEM_SASS="true"
%pyproject_wheel
pushd docs
# There are differences between Python's naming of arches and the
# %%{_arch} macro. We need to ask Python for the platform name
LIBPATH=$(python3 -c "import os.path, glob; print(os.path.basename(glob.glob('../build/lib*')[0]))")
export PYTHONPATH=../build/${LIBPATH}
make man    SPHINXBUILD=sphinx-build-3
popd

# lib.linux-x86_64-cpython-310
# lib.linux-x86_64-cpython-3.10
%install
# Same as above
export SYSTEM_SASS="true"
%pyproject_install
install -m 644 -D docs/_build/man/pysassc.1 %{buildroot}%{_mandir}/man1/pysassc.1

%check
export PYTHONPATH=%{buildroot}%{python3_sitearch}
py.test-3 sasstests.py

%files -n python3-%{srcname}
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
