%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname blist

Name:           python-%{srcname}
Version:        1.3.6
Release:        6%{?dist}
Summary:        A faster list implementation for Python

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/blist/
Source0:        http://pypi.python.org/packages/source/b/blist/blist-%{version}.tar.gz
# EL7 has setuptools 0.9.8, not 1.1.6
# override the version specified in ez_setup.py
Patch0:         blist-1.3.6-el7_098.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%description
The blist is a drop-in replacement for the Python list that provides
better performance when modifying large lists. The blist package also
provides sortedlist, sortedset, weaksortedlist, weaksortedset,
sorteddict, and btuple types.

Python's built-in list is a dynamically-sized array; to insert or
remove an item from the beginning or middle of the list, it has to
move most of the list in memory, i.e., O(n) operations. The blist uses
a flexible, hybrid array/tree structure and only needs to move a small
portion of items in memory, specifically using O(log n) operations.

For small lists, the blist and the built-in list have virtually
identical performance.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        A faster list implementation for Python

%description -n python3-%{srcname}
The blist is a drop-in replacement for the Python list that provides
better performance when modifying large lists. The blist package also
provides sortedlist, sortedset, weaksortedlist, weaksortedset,
sorteddict, and btuple types.

Python's built-in list is a dynamically-sized array; to insert or
remove an item from the beginning or middle of the list, it has to
move most of the list in memory, i.e., O(n) operations. The blist uses
a flexible, hybrid array/tree structure and only needs to move a small
portion of items in memory, specifically using O(log n) operations.

For small lists, the blist and the built-in list have virtually
identical performance.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?el7}
%patch0 -p1 -b .el7_098
%endif

# Replace the not-zip-safe file; keep rpmlint happy by not having
# CRLF line endings
#echo > not-zip-safe
#touch -r blist.egg-info/not-zip-safe not-zip-safe
#rm blist.egg-info/not-zip-safe
# egg-info files should not be executables
# chmod -x blist.egg-info/*
# Move the new not-zip-safe file back
# mv not-zip-safe blist.egg-info/

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{python2_sitearch}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE README.rst
%{python3_sitearch}/*
%endif # with_python3


%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May  8 2014 Michel Salim <salimma@fedoraproject.org> - 1.3.6-1
- Update to 1.3.6
- Build for Python 3 as well on supported releases

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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

