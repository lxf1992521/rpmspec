Name:		interfacetable_v3t
Version:	0.5.1
Release:	2.icinga%{?dist}
Summary:	Interfacetable_v3t allows you to monitor the network interfaces of a node

Group:		Applications/System	
License:	GPLv2 and GPLv3
URL:		http://www.tontonitch.com/tiki/tiki-index.php?page=Nagios+plugins+-+interfacetable_v3t
Source0:	%{name}-%{version}.tar.gz
Source1:	root-rewrite-to-tables.php
Patch0:		remove-cgi-conf.patch
Patch1:		remove-resetcgi-in-checkscript.patch
Patch2:		fix-regex-warning.patch
Patch3:		fix-table-index.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	net-snmp-utils
BuildRequires:	perl 
BuildRequires:	perl-CGI
BuildRequires:	perl-Config-General 
BuildRequires:	perl-Sort-Naturally 
BuildRequires:	perl-Exception-Class 
%if 0%{?el6}
BuildRequires:	perl-Time-HiRes
%endif
Requires:	net-snmp-utils
Requires:	perl 
Requires:	perl-Config-General 
Requires:	perl-Sort-Naturally 
Requires:	perl-Exception-Class 
Requires:	perl-Time-HiRes
Requires:	perl-Net-SNMP
Requires:	icinga2
Requires:	httpd

%description
Interfacetable_v3t (formerly check_interface_table_v3t) is a Nagios(R) addon
that allows you to monitor the network interfaces of a node (e.g. router, 
switch, server) without knowing each interface in detail. Only the hostname 
(or ip address) and the snmp community string are required. It generates a 
html page gathering some info on the monitored node and a table of all 
interfaces/ports and their status. 

%package pnp4nagios
Summary: Pnp4nagios support for %{name}
Group: Applications/System
Requires: pnp4nagios >= 0.6
Requires: %{name} = %{version}

%description pnp4nagios
This package contains the templates for pnp4nagios for %{name}

%define pluginpath %{_libdir}/nagios/plugins
%define apachename httpd
%define apacheuser apache
%define apacheconf %{_sysconfdir}/%{apachename}/conf.d
%define icingawebauthname 'Icinga Access'
%define icingawebauthfile %{_sysconfdir}/%{name}/passwd
%define pnp4nagiostemplates %{_datadir}/pnp4nagios/html/templates

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --sysconfdir=%{_sysconfdir}/%{name} \
  --datarootdir=%{_datadir}/%{name} \
  --libdir=%{_libdir}/%{name} \
  --with-nagios-user=icinga \
  --with-nagios-group=icinga \
  --with-nagios-base=%{_datadir} \
  --with-nagios-libexec=%{pluginpath} \
  --with-nagios-etc=%{_sysconfdir}/icinga2 \
  --with-cachedir=%{_localstatedir}/cache/%{name} \
  --with-statedir=%{_sharedstatedir}/%{name} \
  --with-cgidir=%{_libdir}/%{name}/cgi \
  --with-httpd-conf=%{apacheconf} \
  --with-apache-user=%{apacheuser} \
  --with-apache-authname=%{icingawebauthname} \
  --with-apache-authfile=%{icingawebauthfile}
make %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL_OPTS=""
make install-apache-config DESTDIR=%{buildroot} INSTALL_OPTS=""
mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_defaultdocdir}/%{name} 
mv %{buildroot}%{_sysconfdir}/%{name}/settings.cfg-sample %{buildroot}%{_defaultdocdir}/%{name}/settings.cfg-sample
cp %{buildroot}%{_defaultdocdir}/%{name}/settings.cfg-sample %{buildroot}%{_sysconfdir}/%{name}/settings.cfg
mkdir -p %{buildroot}%{pnp4nagiostemplates} 
cp contrib/pnp4nagios/* %{buildroot}%{pnp4nagiostemplates}/
mv %{buildroot}%{pluginpath}/check_interface_table_v3t.pl %{buildroot}%{pluginpath}/check_interface_table_v3t
cp %{SOURCE1} %{buildroot}%{_datadir}/%{name}/index.php

%files
%defattr(-,root,root,-)
%config(noreplace) %{apacheconf}/%name.conf
%{_sysconfdir}/%{name}
%{_datadir}/%{name}
%dir %attr(-,icinga,icinga) %{_datadir}/%{name}/tables
%{_libdir}/%{name}
%{pluginpath}/check_interface_table_v3t
%dir %attr(-,icinga,icinga) %{_localstatedir}/cache/%{name}
%dir %attr(-,icinga,icinga) %{_sharedstatedir}/%{name}
%doc %{_defaultdocdir}/%{name}/settings.cfg-sample
%exclude %{_libdir}/%{name}/cgi

%files pnp4nagios
%defattr(-,root,root,-)
%{pnp4nagiostemplates}/*

%changelog
* Fri May 23 2014 Dirk Goetz <dirk.goetz@netways.de> - 0.05.1-1
- inital build
