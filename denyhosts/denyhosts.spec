%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(0)')

Name: denyhosts
Version: 2.10
Release: 1%{?dist}
License: GPL
Group: Applications/Internet
URL: https://github.com/denyhosts/denyhosts
Buildarch: noarch
Requires: python-ipaddr
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
Source0: https://github.com/denyhosts/denyhosts/archive/v%{version}.tar.gz
Source1: denyhosts.conf
Summary: Scan ssh server logs and block hosts

%description
DenyHosts is a script intended to help Linux system administrators thwart
ssh server attacks. DenyHosts scans an ssh server log, updates
/etc/hosts.deny after a configurable number of failed attempts from a
rogue host is determined, and alerts the administrator of any suspicious
logins.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --root="%{buildroot}" --prefix="%{_prefix}"
%{__rm} %{buildroot}/%{_bindir}/daemon-control-dist
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/denyhosts

%{__install} -p -D -m 0644 denyhosts.service %{buildroot}%{_unitdir}/denyhosts.service
%{__install} -m 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/denyhosts.conf

%clean
%{__rm} -rf %{buildroot}

%post
%systemd_post denyhosts.service
%preun
%systemd_preun denyhosts.service
%postun
%systemd_postun denyhosts.service

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG.txt LICENSE.txt README.md
%config (noreplace) %{_sysconfdir}/denyhosts.conf
%{_bindir}/denyhosts.py
%{_unitdir}/denyhosts.service
%{python_sitearch}/DenyHosts
%{python_sitearch}/DenyHosts-*.egg-info
%{_datadir}/man/man8/denyhosts.8.gz
%dir %{_localstatedir}/lib/denyhosts
