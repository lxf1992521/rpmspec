Name:              gost
Version:           2.8.1
Release:           1%{?dist}
BuildArch:         x86_64
License:           MIT
Group:             System Environment/Base
URL:               https://github.com/ginuerzh/gost
Summary:           GO Simple Tunnel

Source0:           https://github.com/ginuerzh/gost/releases/download/v%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1:           gost.service
Source2:           gost.conf

Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
A simple security tunnel written in Golang.

%prep
%setup -c -q
cp %{SOURCE1} %{SOURCE2} .

%install
install -p -D -m 0644 gost.conf %{buildroot}%{_sysconfdir}/gost.conf
install -p -D -m 0644 gost.service %{buildroot}%{_unitdir}/gost.service
install -p -D -m 0755 %{name}_%{version}_linux_amd64/gost %{buildroot}%{_bindir}/gost

%pre
getent group gost > /dev/null || groupadd -r gost
getent passwd gost > /dev/null || \
    useradd -r -d %{_localstatedir}/lib/gost -g gost \
    -s /sbin/nologin -c "go simple tunnel" gost
exit 0
%post
%systemd_post gost.service
%preun
%systemd_preun gost.service
%postun
%systemd_postun gost.service

%files
%config(noreplace) %attr(0640,gost,gost) %{_sysconfdir}/gost.conf
%{_bindir}/gost
%{_unitdir}/gost.service
