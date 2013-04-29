%define hash 2252393e8034
%define longhash 2252393e80342c96c0fad242ee93ba6a0debc695
%define revision 5729
%define pyversion 2.5._1

Name:           quodlibet
Version:        2.5.99
Release:        2.%{revision}.%{hash}%{?dist}
Summary:        A music management program

%if 0%{?suse_version}
Group:          Productivity/Multimedia/Sound/Players
%else
Group:          Applications/Multimedia
%endif
License:        GPL-2.0
URL:            http://code.google.com/p/quodlibet/
Source0:        http://quodlibet.googlecode.com/archive/%{longhash}.zip

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  python >= 2.6
BuildRequires:  gtk2 >= 2.6.0
BuildRequires:  unzip

%if 0%{?fedora}
# needed for py_byte_compile
BuildRequires:  python3-devel
%endif

Requires:       exfalso = %{version}-%{release}

%if 0%{?suse_version}
Requires:       python-gstreamer-0_10 >= 0.10.2
Requires:       gstreamer-0_10-plugins-good
Requires:       python-feedparser
Requires:       media-player-info
Requires:       dbus-1-python
Requires:       python-keybinder
Requires:       udisks
Requires:       python-gpod
%else
Requires:       gstreamer-python >= 0.10.2
Requires:       gstreamer-plugins-good
Requires:       python-feedparser
Requires:       media-player-info
Requires:       dbus-python
Requires:       python-keybinder
Requires:       udisks
Requires:       python-gpod
%endif


%description
Quod Libet is a music management program. It provides several different ways
to view your audio library, as well as support for Internet radio and
audio feeds. It has extremely flexible metadata tag editing and searching
capabilities.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.


%package -n exfalso
Summary: Tag editor for various music files
Group: Applications/Multimedia

Requires:       python >= 2.6
Requires:       pygtk2 >= 2.16
Requires:       python-mutagen >= 1.14

%if 0%{?fedora}
Requires:       python-CDDB
Requires:       python-musicbrainz2
%endif

%description -n exfalso
Ex Falso is a tag editor with the same tag editing interface as Quod Libet,
but it does not play files.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.

%prep
%setup -q -n quodlibet-%{hash}

%build
cd quodlibet
%{__python} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python_sitelib}/quodlibet/
cp -R plugins %{buildroot}%{python_sitelib}/quodlibet/

%if 0%{?fedora}
%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

%if 0%{?suse_version}
%py_compile %{buildroot}%{python_sitelib}/quodlibet/plugins
%endif

cd quodlibet
python setup.py install --root=%{buildroot} --prefix=%{_prefix}

# leave vendor for fedora to keep links alive
%if 0%{?fedora}
desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/quodlibet.desktop
desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/exfalso.desktop
%else
desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/quodlibet.desktop
desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/exfalso.desktop
%endif

%{find_lang} quodlibet

%clean
rm -rf %{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/quodlibet
%if 0%{?fedora}
%{_datadir}/applications/fedora-quodlibet.desktop
%else
%{_datadir}/applications/quodlibet.desktop
%endif
%{_datadir}/pixmaps/quodlibet.png
%{_datadir}/icons/hicolor/64x64/apps/quodlibet.png
%{_datadir}/icons/hicolor/scalable/apps/quodlibet.svg
%{_mandir}/man1/quodlibet.1*


%files -n exfalso -f quodlibet/%{name}.lang
%defattr(-,root,root,-)
%doc quodlibet/COPYING quodlibet/HACKING quodlibet/NEWS quodlibet/README
%{_bindir}/exfalso
%{_bindir}/operon
%if 0%{?fedora}
%{_datadir}/applications/fedora-exfalso.desktop
%else
%{_datadir}/applications/exfalso.desktop
%endif
%{_datadir}/pixmaps/exfalso.png
%{_datadir}/icons/hicolor/64x64/apps/exfalso.png
%{_datadir}/icons/hicolor/scalable/apps/exfalso.svg
%{_mandir}/man1/exfalso.1*
%{_mandir}/man1/operon.1*
%{python_sitelib}/quodlibet/
%{python_sitelib}/quodlibet-%{pyversion}-py*.egg-info

%changelog
* Fri Dec  7 2012 Christoph Reiter <reiter.christoph@gmail.com>
- unstable build

* Mon Jul 30 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4.1-1
- Update to recent upstream release 2.4.1
