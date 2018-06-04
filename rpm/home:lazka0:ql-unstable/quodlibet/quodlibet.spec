%define hash a4a693ce9
%define longhash a4a693ce986aa6fd5cf654ee783cb596fe14a1c3
%define revision 9790
 
Name:           quodlibet
Version:        4.1.99
Release:        3.%{revision}.%{hash}%{?dist}
Summary:        A music management program

%if 0%{?suse_version}
Group:          Productivity/Multimedia/Sound/Players
%else
# fedora
Group:          Applications/Multimedia
%endif
License:        GPL-2.0
URL:            https://github.com/quodlibet/quodlibet
Source0:        https://github.com/quodlibet/quodlibet/archive/%{longhash}.zip

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  python3 >= 3.5
%if 0%{?fedora}
BuildRequires:  python3-devel >= 3.5
%endif
BuildRequires:  unzip

Requires:       exfalso = %{version}-%{release}

Requires:       python3-feedparser

%if 0%{?suse_version}
Requires:       dbus-1-python3
Requires:       gstreamer >= 1.8
Requires:       gstreamer-plugins-base >= 1.8
Requires:       gstreamer-plugins-good >= 1.8
# suse has extra packages for typelibs
Requires:       typelib-1_0-Gst-1_0
Requires:       typelib-1_0-GstPbutils-1_0
Requires:       typelib-1_0-Soup-2_4
%else
# fedora
Requires:       python3-dbus
Requires:       gstreamer1 >= 1.8
Requires:       gstreamer1-plugins-base >= 1.8
Requires:       gstreamer1-plugins-good >= 1.8
Requires:       libsoup
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

Requires:       python3 >= 3.5
Requires:       python3-mutagen >= 1.34
Requires:       gtk3 >= 3.18
Requires:       python3-feedparser
Requires:       python3-musicbrainzngs >= 0.5
Requires:       python3-gobject >= 3.18
Requires:       python3-cairo

%if 0%{?fedora}
Requires:       librsvg2
%else
Requires:       librsvg-2-2
Requires:       python3-gobject-cairo >= 3.18
Requires:       typelib-1_0-Gtk-3_0
Requires:       python3-gobject-Gdk
%endif

%description -n exfalso
Ex Falso is a tag editor with the same tag editing interface as Quod Libet,
but it does not play files.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.

%prep
%setup -q -n quodlibet-%{longhash}

%build
cd quodlibet
%{__python3} setup.py build

%install
rm -rf %{buildroot}

cd quodlibet
%{__python3} setup.py install --root=%{buildroot} --prefix=%{_prefix}

desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/io.github.quodlibet.QuodLibet.desktop
desktop-file-install                                            \
        --dir %{buildroot}%{_datadir}/applications              \
        --delete-original                                       \
        %{buildroot}%{_datadir}/applications/exfalso.desktop

%{find_lang} quodlibet

%clean
rm -rf %{buildroot}

%post
%if 0%{?suse_version}
%icon_theme_cache_post
%desktop_database_post
%else
# fedora
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%postun
%if 0%{?suse_version}
%icon_theme_cache_postun
%desktop_database_postun
%else
# fedora
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%endif

%posttrans
%if 0%{?fedora}
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/quodlibet
%{_datadir}/applications/io.github.quodlibet.QuodLibet.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.quodlibet.QuodLibet.png
%{_datadir}/icons/hicolor/*/apps/io.github.quodlibet.QuodLibet.svg
%{_datadir}/icons/hicolor/*/apps/io.github.quodlibet.QuodLibet-symbolic.svg
%if 0%{?suse_version}
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/search-providers
%dir %{_datadir}/appdata
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/vendor-completions
%endif
%{_datadir}/dbus-1/services/net.sacredchao.QuodLibet.service
%{_datadir}/appdata/io.github.quodlibet.QuodLibet.appdata.xml
%{_datadir}/gnome-shell/search-providers/io.github.quodlibet.QuodLibet-search-provider.ini
%{_mandir}/man1/quodlibet.1*
%{_datadir}/zsh/vendor-completions/_quodlibet


%files -n exfalso -f quodlibet/%{name}.lang
%defattr(-,root,root,-)
%doc quodlibet/COPYING quodlibet/NEWS quodlibet/README
%{_bindir}/exfalso
%{_bindir}/operon
%{_datadir}/applications/exfalso.desktop
%if 0%{?suse_version}
%dir %{_datadir}/appdata
%endif
%{_datadir}/appdata/exfalso.appdata.xml
%{_datadir}/icons/hicolor/*/apps/exfalso.png
%{_datadir}/icons/hicolor/*/apps/exfalso.svg
%{_datadir}/icons/hicolor/*/apps/exfalso-symbolic.svg
%{_mandir}/man1/exfalso.1*
%{_mandir}/man1/operon.1*
%{python3_sitelib}/quodlibet/
%{python3_sitelib}/quodlibet-*.egg-info

%changelog
* Fri Dec  7 2012 Christoph Reiter <reiter.christoph@gmail.com>
- unstable build

* Mon Jul 30 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4.1-1
- Update to recent upstream release 2.4.1
