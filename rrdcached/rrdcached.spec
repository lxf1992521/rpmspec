Name:		rrdcached
Version:	1.4.8
Release:	1%{?dist}
Summary:	The data caching daemon for RRDTool

Group:		System Environment/Daemons
License:	GPL
URL:		https://oss.oetiker.ch/rrdtool
Source0:        rrdcached.init
Source1:        rrdcached.sysconfig
Requires:	rrdtool >= 1.4.8

%description
This package contains the data caching daemon for RRDTool. The
daemon receives updates to existing RRD files, accumulates them and writes
the updates to the RRD file. It was written with big setups in mind, which
usually run into IO related problems sooner or later.


%prep
%build

%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_initrddir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/lib/rrdcached/{db,jnl}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_localstatedir}/run/rrdcached

%{__install} -m 0755 %{SOURCE0} ${RPM_BUILD_ROOT}%{_initrddir}/rrdcached
%{__install} -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/rrdcached

%pre
if ! getent group  rrdcached >/dev/null 2>&1; then
  /usr/sbin/groupadd -r rrdcached
fi
if ! getent passwd rrdcached >/dev/null 2>&1; then
  /usr/sbin/useradd  -r -g rrdcached       \
	-d %{_localstatedir}/lib/rrdcached \
	-c "Rrdcached Service user" -M     \
	-s /sbin/nologin rrdcached
fi
exit 0			# Always pass

%post
/sbin/chkconfig --add rrdcached

%preun
if [ $1 -eq 0 ]; then	# Remove
  /sbin/service rrdcached stop >/dev/null 2>&1
  /sbin/chkconfig --del rrdcached
fi

%postun
if [ $1 -ge 1 ]; then	# Upgrade
  /sbin/service rrdcached condrestart >/dev/null 2>&1 || :
fi

%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_initrddir}/rrdcached
%config(noreplace) %{_sysconfdir}/sysconfig/rrdcached
%attr(750,rrdcached,rrdcached) %dir %{_localstatedir}/lib/rrdcached
%attr(770,rrdcached,rrdcached) %dir %{_localstatedir}/lib/rrdcached/db
%attr(750,rrdcached,rrdcached) %dir %{_localstatedir}/lib/rrdcached/jnl
%attr(750,rrdcached,rrdcached) %dir %{_localstatedir}/run/rrdcached

%changelog
* Tue Mar 20 2018 Xiangfei Liang <liangxiangfei@domob.cn>
- init package for rrdtool 1.4.8
