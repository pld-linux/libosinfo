#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	vala		# Vala binding
#
Summary:	A library for managing OS information for virtualization
Summary(pl.UTF-8):	Biblioteka do zarządzania informacjami dotyczącymi OS na potrzeby wirtualizacji
Name:		libosinfo
Version:	0.2.10
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.gz
# Source0-md5:	02708aec32212c8b153d11b23e35c4e0
URL:		https://fedorahosted.org/libosinfo/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libsoup-gnome-devel >= 2.4
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	libxslt-devel >= 1.0.0
BuildRequires:	pkgconfig
%{?with_vala:BuildRequires:	vala}
Requires:	/lib/hwdata/pci.ids
Requires:	/lib/hwdata/usb.ids
Requires:	hwdata >= 0.243-5
Requires:	libxml2 >= 1:2.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libosinfo is a library that allows virtualization provisioning tools
to determine the optimal device settings for a hypervisor/operating
system combination.

%description -l pl.UTF-8
libosinfo to biblioteka umożliwiająca narzędziom wirtualizacyjnym
określenie optymalnych ustawień dla danej kombinacji hipernadzorcy
i systemu operacyjnego.

%package devel
Summary:	Header files for libosinfo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libosinfo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	libsoup-gnome-devel >= 2.4
Requires:	libxml2-devel >= 1:2.6.0

%description devel
Header files for libosinfo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libosinfo.

%package static
Summary:	Static libosinfo library
Summary(pl.UTF-8):	Statyczna biblioteka libosinfo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libosinfo library.

%description static -l pl.UTF-8
Statyczna biblioteka libosinfo.

%package apidocs
Summary:	libosinfo API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libosinfo
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for libosinfo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libosinfo.

%package -n vala-libosinfo
Summary:	libosinfo API for Vala language
Summary(pl.UTF-8):	API libosinfo dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-libosinfo
libosinfo API for Vala language.

%description -n vala-libosinfo -l pl.UTF-8
API libosinfo dla języka Vala.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable apidocs gtk-doc} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--enable-udev \
	%{!?with_vala:--disable-vala} \
	--with-html-dir=%{_gtkdocdir} \
	--with-pci-ids-path=/lib/hwdata/pci.ids \
	--with-usb-ids-path=/lib/hwdata/usb.ids
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/osinfo-db-validate
%attr(755,root,root) %{_bindir}/osinfo-detect
%attr(755,root,root) %{_bindir}/osinfo-install-script
%attr(755,root,root) %{_bindir}/osinfo-query
%attr(755,root,root) %{_libdir}/libosinfo-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosinfo-1.0.so.0
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib
%{_datadir}/libosinfo
/lib/udev/rules.d/95-osinfo.rules
%{_mandir}/man1/osinfo-db-validate.1*
%{_mandir}/man1/osinfo-detect.1*
%{_mandir}/man1/osinfo-install-script.1*
%{_mandir}/man1/osinfo-query.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libosinfo-1.0.so
%{_datadir}/gir-1.0/Libosinfo-1.0.gir
%{_includedir}/libosinfo-1.0
%{_pkgconfigdir}/libosinfo-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libosinfo-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/Libosinfo
%endif

%if %{with vala}
%files -n vala-libosinfo
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libosinfo-1.0.vapi
%endif
