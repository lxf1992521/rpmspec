Name:		vim-keepalived
Version:	0.1.0
Release:	1%{?dist}
Summary:	Vim syntax highlighting for keepalived

Group:		Applications/System
License:	GPL-2.0+
URL:		https://github.com/glidenote/keepalived-syntax.vim
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	vim-filesystem

%description
Vim syntax highlighting for keepalived

%prep
%setup -q


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/vim/vimfiles/
mv ftdetect syntax %{buildroot}/usr/share/vim/vimfiles/

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc
/usr/share/vim/vimfiles
/usr/share/vim/vimfiles/ftdetect
/usr/share/vim/vimfiles/ftdetect/keepalived.vim
/usr/share/vim/vimfiles/syntax
/usr/share/vim/vimfiles/syntax/keepalived.vim


%changelog
* Thu Dec 22 2016 Xiangfei Liang <liangxiangfei@domob.cn>
- init package
