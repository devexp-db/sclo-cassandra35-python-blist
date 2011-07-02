%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-blist
Version:        1.3.4
Release:        1%{?dist}
Summary:        A faster list implementation for Python

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/blist/
Source0:        http://pypi.python.org/packages/source/b/blist/blist-%{version}.tar.gz
Patch0:		blist-1.2.1-use-sys-setuptools.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel python-setuptools

%description
The BList is a type that looks, acts, and quacks like a Python list,
but has better performance for for modifying large lists.

For small lists (fewer than 128 elements), BLists and the built-in
list have very similar performance, although BLists are memory
inefficient if you need to create a larger number of small lists.


%prep
%setup -q -n blist-%{version}
%patch0 -p1 -b .use-sys-setuptools

# Replace the not-zip-safe file; keep rpmlint happy by not having
# CRLF line endings
echo > not-zip-safe
touch -r blist.egg-info/not-zip-safe not-zip-safe
rm blist.egg-info/not-zip-safe
# egg-info files should not be executables
chmod -x blist.egg-info/*
# Move the new not-zip-safe file back
mv not-zip-safe blist.egg-info/


%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%check
%{__python} setup.py test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python_sitearch}/*


%changelog
* Sat Jul  2 2011 Michel Salim <salimma@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 26 2010 Michel Salim <salimma@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Fri May 21 2010 Michel Salim <salimma@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Fri Oct 23 2009 Michel Salim <salimma@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Sat Oct 10 2009 Michel Salim <salimma@fedoraproject.org> - 1.0.1-1
- Initial package

