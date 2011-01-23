%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:	XYZCommander is a pure console visual file manager
Name:		xyzcmd
Version:	0.0.5
Release:	3%{?dist}
Source0:	http://xyzcmd.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:	xyzcmd_ru.mo
Source2:	xyzcmd_uk.mo
Patch0:     xyzcmd-0.0.5-locale.patch     
License:	LGPL
Group:		System Environment/Shells
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://xyzcmd.syhpoon.name
Requires:	python >= 2.4, python-urwid
BuildRequires: python >= 2.4
BuildArch:  noarch

%description
XYZCommander is a pure console visual file manager.

%prep
%setup -q
%patch0 -p1 -b .locale

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{python_sitelib}/libxyz
%{__python} setup.py install --no-compile --root %{buildroot}
%{__rm} -rf %{buildroot}%{_docdir}/%{name}
%{__rm} -f %{buildroot}%{_datadir}/%{name}/locale/xyzcmd.pot
%{__rm} -f %{buildroot}%{_datadir}/%{name}/locale/ru/LC_MESSAGES/xyzcmd.po*
%{__rm} -f %{buildroot}%{_datadir}/%{name}/locale/uk/LC_MESSAGES/xyzcmd.po*
# temporary workaround (until locale will be fixed in upstream)
%{__rm} -f %{buildroot}%{_datadir}/%{name}/locale/ru/LC_MESSAGES/xyzcmd.mo
%{__install} -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/%{name}/locale/ru/LC_MESSAGES/xyzcmd.mo
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/locale/uk/LC_MESSAGES/xyzcmd.mo


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog COPYING COPYING.LESSER README
%doc doc/api/
%doc doc/user-manual/
%doc doc/overview.pdf
%{_bindir}/xyzcmd
%{python_sitelib}/libxyz/
%if 0%{?fedora} >= 14
%{python_sitelib}/xyzcmd-0.0.5-py2.7.egg-info
%endif
%if 0%{?fedora} == 13 || 0%{?rhel} >= 6
%{python_sitelib}/xyzcmd-0.0.5-py2.6.egg-info
%endif
%dir %{_datadir}/%{name}/conf
%{_datadir}/%{name}/conf/*.xyz
%{_datadir}/%{name}/plugins/
%{_datadir}/%{name}/skins/
%{_datadir}/%{name}/locale/ru/LC_MESSAGES/xyzcmd.mo
%{_datadir}/%{name}/locale/uk/LC_MESSAGES/xyzcmd.mo
%{_mandir}/man1/xyzcmd.1.gz

%changelog
* Sun Jan 23 2011 Vlad V. Teterya <vlad@server-labs.com.ua> - 0.0.5-3
- Add ukrainian locale
- Fix typos in russian locale

* Sat Jan 22 2011 Vlad V. Teterya <vlad@server-labs.com.ua> - 0.0.5-2
- Fix docs and locale install

* Sat Jan 22 2011 Vlad V. Teterya <vlad@server-labs.com.ua> - 0.0.5-1
- Rebuild for fc14
