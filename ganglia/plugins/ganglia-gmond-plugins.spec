%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define conf_dir /etc/ganglia

Name:		ganglia-gmond-plugins
Version:	3.7.2
Release:	9%{?dist}
Summary:	Ganglia Gmond Plugins

Group:		System Environment/Base
License:	BSD
URL:		http://www.domob.cn
Source0:	%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python >= 2.4
Requires:	ganglia-gmond >= 3.4.0, python >= 2.4

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond modules support package provides the capability of loading gmetric/python modules
via DSO at daemon start time instead of via gmetric


%prep
%setup -q

%build

%install
rm -rf %{buildroot}
%__install -d -m 0755 $RPM_BUILD_ROOT%{conf_dir}/conf.d
%__cp -f conf/*.pyconf* $RPM_BUILD_ROOT%{conf_dir}/conf.d/
%__install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/
%{__python} -c 'import compileall; compileall.compile_dir("python_modules", 1, "/", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("python_modules", 1, "/", 1)' > /dev/null
%__cp -f python_modules/*.{py,pyc,pyo} $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/

%clean
rm -rf %{buildroot}

%post
/sbin/service gmond restart

%postun
/sbin/service gmond restart

%files
%defattr(-,root,root,-)
%config(noreplace) %{conf_dir}/conf.d/*.pyconf*
%{_libdir}/ganglia/python_modules/*.py*

%changelog
* Tue May 15 2018 Liang Xiangfei <liangxiangfei@domob.cn>
- add python module: entropy_avail, multi_interface
* Mon Nov 28 2016 Liang Xiangfei <liangxiangfei@domob.cn>
- fix diskfree chroot bugs
* Thu Nov 17 2016 Liang Xiangfei <liangxiangfei@domob.cn>
- init
