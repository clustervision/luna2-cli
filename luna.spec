%define name python3-luna
%define version 2.0
%define release 1

Summary: Luna CLI tool to manage Luna Daemon
Name: %{name}
Version: %{version}
Release: %{release}
Source0: luna-%{version}.tar.gz
Source1: luna.ini
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/luna-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Sumit Sharma <sumit.sharma@clustervision.com>
Url: https://gitlab.taurusgroup.one/clustervision/luna2-cli.git

%description
Luna CLI is a tool to manage Luna Daemon. It's a part of Trinity project.

%prep
%autosetup -n luna

%build
%py3_build

%install
%py3_install
mkdir %{buildroot}/usr/local
mkdir %{buildroot}/usr/local/bin
cp %{buildroot}/%{_bindir}/luna  %{buildroot}/usr/local/bin
mkdir -p %{buildroot}/trinity
mkdir -p %{buildroot}/trinity/local
mkdir -p %{buildroot}/trinity/local/luna
mkdir -p %{buildroot}/trinity/local/luna/config
cp %{SOURCE1} %{buildroot}/trinity/local/luna/config/
mkdir -p %{buildroot}/var
mkdir -p %{buildroot}/var/log/
mkdir -p %{buildroot}/var/log/luna
echo '' >> %{buildroot}/var/log/luna/luna2-cli.log

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{name}
%doc README.md
%{_bindir}/luna
/usr/local/bin/luna
/trinity/local/luna/config/luna.ini
/var/log/luna/luna2-cli.log
%{python3_sitelib}/luna
%{python3_sitelib}/luna-%{version}-py%{python3_version}.egg-info

%changelog
* Wed May  10 2023 Sumit Sharma <sumit.sharma@clustervision.com> - 2.0
- It's a first version of Luna CLI tool. The project is still in development mode.