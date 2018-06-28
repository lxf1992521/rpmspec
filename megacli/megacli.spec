%if 0%{?rhel} == 7
  %define dist .el7
  # CentOS 7 would force ".el7.centos", we want to avoid that.
%endif

%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:		megacli
Version:	8.07.14
Release:	2%{?dist}
Summary:	LSI Logic MegaCLI

Group:		System Environment/Base
License:	Proprietary
URL:		http://www.lsilogic.com/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Obsoletes:	MegaCli

%description
LSI Logic MegaCLI.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -p -D -m 0755 bin/MegaCli64 %{buildroot}%{_sbindir}/megacli

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/megacli

%changelog
* Tue Jun 27 2017 Xiangfei Liang <liangxiangfei@domob.cn>
- re-package for x86_64 arch
