Summary:	Java runtime library for gcc
Summary(pl):	�rodowisko uruchomieniowe Javy dla gcc
Name:		libgcj
Version:	2.95.1
Release:	3
Epoch:		1
License:	GPL
Group:		Libraries
Source0:	ftp://sourceware.cygnus.com/pub/java/%{name}-%{version}.tar.gz
URL:		http://sourceware.cygnus.com/java/
BuildRequires:	gcc-java
Requires:	binutils >= 2.9.1.0.25
Requires:	zip >= 2.1
Provides:	gcc-%{name}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	gcc-%{name}

%description
The Java runtime library. You will need this package to compile your
Java programs using the gcc Java compiler (gcj).

%description -l pl
Biblioteka uruchomieniowa Javy. Jest potrzebna do kompilacji program�w
w Javie przy u�yciu gcj.

%package static
Summary:	Static java runtime library for gcc
Summary(pl):	Statyczna biblioteka uruchomieniowa Javy dla gcc
Group:		Development/Libraries
Requires:	%{name} = %{version}
Provides:	gcc-%{name}-static
Obsoletes:	gcc-%{name}-static

%description static
The static Java runtime library. You will need this package to
statically compile your Java programs using the gcc Java compiler
(gcj).

%description static -l pl
Statyczna biblioteka uruchomieniowa Javy. Jest potrzebna do
statycznego kompilowania program�w w Javie przy u�yciu gcj.

%prep
%setup -q

%build
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform} 

CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--enable-shared \
%ifnarch sparc sparc64
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

gzip -9nf ../ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.gz libjava/doc/*
%attr(755,root,root) %{_bindir}/jv-convert

%{_libdir}/*.spec

%attr(755,root,root) %{_libdir}/lib*gcj*.so
%attr(755,root,root) %{_libdir}/lib*gcj*.so.*.*.*
%{_libdir}/lib*gcj*.la

%{_datadir}/libgcj.zip

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*gcj*.a