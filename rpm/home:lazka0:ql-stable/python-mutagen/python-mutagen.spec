%global realname mutagen

Name:           python-%{realname}
Version:        1.32
Release:        1%{?dist}
Summary:        Mutagen is a Python module to handle audio meta-data

Group:          Development/Languages
License:        GPLv2
URL:            https://bitbucket.org/lazka/mutagen/overview
Source0:        https://bitbucket.org/lazka/mutagen/downloads/mutagen-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?suse_version}
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif

%description
Mutagen is a Python module to handle audio meta-data. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bit-streams.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root,-)
%doc NEWS README.rst
%{_bindir}/m*
%{_mandir}/*/*
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*.egg-info

%changelog
* Mon Oct 19 2015 Christoph Reiter <reiter.christoph@gmail.com>
- Unstable build

* Mon Dec 15 2014 Michele Baldessari <michele@acksyn.org> - 1.27-1
- New upstream release
- Only use macro style for buildroot
