Summary:	Java runtime library for gcc
Summary(pl.UTF-8):	Środowisko uruchomieniowe Javy dla gcc
Name:		libgcj
Version:	2.95.1
Release:	5
Epoch:		1
License:	GPL
Group:		Libraries
Source0:	ftp://sourceware.cygnus.com/pub/java/%{name}-%{version}.tar.gz
# Source0-md5:	63f61b33ef099caf55ec55553a668576
Patch0:		%{name}-sigcontext.patch
Patch1:		%{name}-cni_h.patch
Patch2:		%{name}-exception_cc.patch
Patch3:		%{name}-jvm_h.patch
Patch4:		%{name}-boolean.patch
Patch5:		%{name}-boehm_gc.patch
Patch6:		%{name}-misc.patch

URL:		http://sourceware.cygnus.com/java/
BuildRequires:	gcc-java
Requires:	binutils
Requires:	zip >= 2.1
Provides:	gcc-%{name}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	gcc-%{name}

%description
The Java runtime library. You will need this package to compile your
Java programs using the gcc Java compiler (gcj).

%description -l pl.UTF-8
Biblioteka uruchomieniowa Javy. Jest potrzebna do kompilacji programów
w Javie przy użyciu gcj.

%package static
Summary:	Static java runtime library for gcc
Summary(pl.UTF-8):	Statyczna biblioteka uruchomieniowa Javy dla gcc
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}
Provides:	gcc-%{name}-static
Obsoletes:	gcc-%{name}-static

%description static
The static Java runtime library. You will need this package to
statically compile your Java programs using the gcc Java compiler
(gcj).

%description static -l pl.UTF-8
Statyczna biblioteka uruchomieniowa Javy. Jest potrzebna do
statycznego kompilowania programów w Javie przy użyciu gcj.

%prep
%setup -q
%patch -P0
%patch -P1 -p0
%patch -P2 -p0
%patch -P3 -p0
%patch -P4 -p0
%patch -P5 -p1
%patch -P6 -p1

%build
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--enable-shared \
%ifnarch sparc sparc64 ppc
	--enable-threads \
	--enable-haifa \
%endif
	--with-gnu-as \
	--with-gnu-ld \
	--with-gxx-include-dir="\$\{prefix\}/include/g++" \
	%{_target_platform}

%{__make} LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog libjava/doc/*
%attr(755,root,root) %{_bindir}/jv-convert

%{_libdir}/*.spec

%attr(755,root,root) %{_libdir}/lib*gcj*.so
%attr(755,root,root) %{_libdir}/lib*gcj*.so.*.*.*
%{_libdir}/lib*gcj*.la

%{_datadir}/libgcj.zip

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*gcj*.a
