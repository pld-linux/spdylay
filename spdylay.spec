#
# Conditional build:
%bcond_without	tests		# don't perform "make check"
%bcond_without	static_libs	# don't build static library

Summary:	SPDY C library
Summary(pl.UTF-8):	Biblioteka C SPDY
Name:		spdylay
Version:	1.2.4
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tatsuhiro-t/spdylay/releases
Source0:	https://github.com/tatsuhiro-t/spdylay/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	e38ea10685d792b735162e7fc2bd6408
URL:		http://tatsuhiro-t.github.io/spdylay/
%{?with_tests:BuildRequires:	CUnit >= 2.1}
BuildRequires:	libevent-devel >= 2.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 1:2.7.7
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.2.3
Requires:	libevent >= 2.0.8
Requires:	libxml2 >= 1:2.7.7
Requires:	openssl >= 1.0.1
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an experimental implementation of Google's SPDY protocol in C.
This library provides SPDY version 2 and 3 framing layer
implementation. It does not perform any I/O operations. When the
library needs them, it calls the callback functions provided by the
application. It also does not include any event polling mechanism, so
the application can freely choose the way of handling events. This
library code does not depend on any particular SSL library (except for
example programs which depend on OpenSSL 1.0.1 or later).

%description -l pl.UTF-8
Ta biblioteka jest eksperymentalną implementacją protokołu SPDY
Google'a w C. Udostępnia implementację warstwy ramek SPDY w wersji 2 i
3. Nie wykonuje żadnych operacji we/wy - w razie potrzeby odwołuje się
do wywołań wstecznych dostarczonych przez aplikację. Nie zawiera także
żadnego mechanizmu typu poll - aplikacja może dowolnie wybrać metodę
obsługi zdarzeń. Biblioteka nie zależy od żadnej konkretnej biblioteki
SSL (poza programami przykładowymi, które wymagają OpenSSL >= 1.0.1).

%package devel
Summary:	Files needed for developing with libspdylay
Summary(pl.UTF-8):	Pliki niezbędne do tworzenia aplikacji z użyciem libspdylay
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel >= 1.2.3

%description devel
Files needed for building applications with libspdylay.

%description devel -l pl.UTF-8
Pliki niezbędne do tworzenia aplikacji z użyciem libspdylay.

%package static
Summary:	Static libspdylay library
Summary(pl.UTF-8):	Statyczna biblioteka libspdylay
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libspdylay library.

%description static -l pl.UTF-8
Statyczna biblioteka libspdylay.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspdylay.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/spdylay

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README.rst
%attr(755,root,root) %{_bindir}/shrpx
%attr(755,root,root) %{_bindir}/spdycat
%attr(755,root,root) %{_bindir}/spdyd
%attr(755,root,root) %{_libdir}/libspdylay.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspdylay.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspdylay.so
%{_includedir}/spdylay
%{_pkgconfigdir}/libspdylay.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspdylay.a
%endif
