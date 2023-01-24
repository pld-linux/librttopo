#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	RT Topology library
Summary(pl.UTF-8):	Biblioteka RT Topology
Name:		librttopo
Version:	1.1.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://git.osgeo.org/gitea/rttopo/librttopo/archive/%{name}-%{version}.tar.gz
# Source0-md5:	0952b78943047ca69a9e6cbef6146869
URL:		https://git.osgeo.org/gogs/rttopo/librttopo
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	geos-devel >= 3.5.0
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The RT Topology Library exposes an API to create and manage standard
(ISO 13249 aka SQL/MM) topologies using user-provided data stores
(DATASTORES.md).

%description -l pl.UTF-8
Biblioteka RT Topology udostępnia API do tworzenia i zarządzania
standardowymi topologiami (ISO 13249, inaczej SQL/MM) przy użyciu
dostarczanych przez użytkownika kontenerów z danymi (DATASTORES.md).

%package devel
Summary:	Header files for RT Topology library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki RT Topology
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for RT Topology library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki RT Topology.

%package static
Summary:	Static RT Topology library
Summary(pl.UTF-8):	Statyczna biblioteka RT Topology
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static RT Topology library.

%description static -l pl.UTF-8
Statyczna biblioteka RT Topology.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librttopo.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS NEWS.md README.md TODO doc/DATASTORES.md
%attr(755,root,root) %{_libdir}/librttopo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librttopo.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librttopo.so
%{_includedir}/librttopo.h
%{_includedir}/librttopo_geom.h
%{_pkgconfigdir}/rttopo.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librttopo.a
%endif
