#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests
%bcond_without	vala		# Vala binding

Summary:	A library for managing OS information for virtualization
Summary(pl.UTF-8):	Biblioteka do zarządzania informacjami dotyczącymi OS na potrzeby wirtualizacji
Name:		libosinfo
Version:	1.12.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://releases.pagure.org/libosinfo/%{name}-%{version}.tar.xz
# Source0-md5:	b074a8ccac5c8aa2fa30489acaca7cc5
URL:		https://libosinfo.org/
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.10.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.10}
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	libxslt-devel >= 1.0.0
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala}
BuildRequires:	xz
Requires:	/lib/hwdata/pci.ids
Requires:	/lib/hwdata/usb.ids
Requires:	glib2 >= 1:2.44
Requires:	hwdata >= 0.243-5
Requires:	libxml2 >= 1:2.6.0
Requires:	osinfo-db >= 20180612
Suggests:	osinfo-db-tools >= 1.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libosinfo is a library that allows virtualization provisioning tools
to determine the optimal device settings for a hypervisor/operating
system combination.

%description -l pl.UTF-8
libosinfo to biblioteka umożliwiająca narzędziom wirtualizacyjnym
określenie optymalnych ustawień dla danej kombinacji hipernadzorcy i
systemu operacyjnego.

%package devel
Summary:	Header files for libosinfo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libosinfo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44

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
BuildArch:	noarch

%description apidocs
API documentation for libosinfo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libosinfo.

%package -n vala-libosinfo
Summary:	libosinfo API for Vala language
Summary(pl.UTF-8):	API libosinfo dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description -n vala-libosinfo
libosinfo API for Vala language.

%description -n vala-libosinfo -l pl.UTF-8
API libosinfo dla języka Vala.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Denable-gtk-doc=false} \
	%{!?with_vala:-Denable-vala=false} \
	-Dwith-pci-ids-path=/lib/hwdata/pci.ids \
	-Dwith-usb-ids-path=/lib/hwdata/usb.ids

%ninja_build -C build

%if %{with tests}
%ninja_test -C build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# unify
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{zh_Hans,zh_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/osinfo-detect
%attr(755,root,root) %{_bindir}/osinfo-install-script
%attr(755,root,root) %{_bindir}/osinfo-query
%attr(755,root,root) %{_libdir}/libosinfo-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosinfo-1.0.so.0
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib
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
%{_datadir}/vala/vapi/libosinfo-1.0.deps
%{_datadir}/vala/vapi/libosinfo-1.0.vapi
%endif
