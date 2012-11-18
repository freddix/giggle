Summary:	Graphical frontend for git
Name:		giggle
Version:	0.6.2
Release:	2
License:	GPL v2
Group:		X11/Development/Tools
Source0:	http://download.gnome.org/sources/giggle/0.6/%{name}-%{version}.tar.xz
# Source0-md5:	32381a8c7e2b162e7b336e0c74218ff2
Patch0:		%{name}-ac.patch
URL:		http://developer.imendio.com/projects/giggle
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	evolution-data-server-devel
BuildRequires:	gtksourceview3-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	vte-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	git
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Giggle is a graphical frontend for the git directory tracker.

%package libs
Summary:	Giggle libraries
Group:		libraries

%description libs
Giggle libraries.

%prep
%setup -q
%patch0 -p1

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules	\
	--with-git-command="%{_bindir}/git"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/giggle.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
%update_icon_cache hicolor
%update_desktop_database

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/giggle/plugins/%{version}/*.so
%dir %{_libdir}/giggle
%dir %{_libdir}/giggle/plugins
%dir %{_libdir}/giggle/plugins/%{version}
%{_libdir}/giggle/plugins/%{version}/*.xml
%{_datadir}/%{name}
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/*/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgiggle*.so.?
%attr(755,root,root) %{_libdir}/libgiggle*.so.*.*.*


