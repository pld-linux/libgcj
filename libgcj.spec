Summary:	Java runtime library for gcc
Name:		libgcj
Version:	2.95.1
Release:	1
Epoch:		1
License:	GPL
Group:		Libraries
Group(pl):	Biblioteki
Group(fr):	Librairies
URL:		http://sourceware.cygnus.com/java/
Source0:	ftp://sourceware.cygnus.com/pub/java/%{name}-%{version}.tar.gz
Requires:	binutils >= 2.9.1.0.25
Requires:	zip >= 2.1
Provides:	gcc-%{name}
Obsoletes:	gcc-%{name}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Java runtime library. You will need this package to compile your
Java programs using the gcc Java compiler (gcj).

%package static
Summary:	Static java runtime library for gcc
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Group(fr):	Development/Librairies
URL:		http://sourceware.cygnus.com/java/
Requires:	%{name} = %{version}
Provides:	gcc-%{name}-static
Obsoletes:	gcc-%{name}-static

%description static
The static java runtime library. You will need this package to
staticly compile your Java programs using the gcc Java compiler (gcj).

%prep
%setup -q

%build
rm -rf obj-%{_target_platform}
install -d obj-%{_target_platform} && cd obj-%{_target_platform} 

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
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

%{__make} LDFLAGS_FOR_TARGET="-s" \
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

strip $RPM_BUILD_ROOT%{_bindir}/* || :
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so*

gzip -9nf ../ChangeLog

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

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
