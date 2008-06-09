%define	name	yiff
%define	version 2.14.5
%define release %mkrel 2
%define major	%{version}
%define	libname %mklibname %name %major

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	YIFF Sound Systems
License: 	GPL
Group: 		System/Servers
Source:		http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
Patch:		%{name}-2.14.5.build.patch.bz2
Url: 		http://wolfpack.twu.net/YIFF/index.html
BuildRequires:	gtk+-devel
BuildRequires:	zlib1-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
YIFF is a high performance, stable, and fully  documented sound server for UNIX
games and applications. It employs a network transparent API which allows 
multiple client programs to access sound capabilities in a similar way to how X
clients do graphics.

Run yiffconfig after install to generate a starty script.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	libY2
Provides:	libY2

%description -n %{libname}
This package contains the library needed to run programs dynamically linked 
with %{name}.

%package -n %{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	libY2-devel
Provides:	libY2-devel

%description -n %{libname}-devel
This package contains the headers that programmers will need to develop 
applications which will use %{name}.

%prep
%setup -q
%patch -p 1

%build
pushd libY2
%make -f Makefile.Linux CFLAGS="$RPM_OPT_FLAGS -fPIC"
popd
pushd yiff
%make -f Makefile.Linux CFLAGS="$RPM_OPT_FLAGS"
popd
pushd yiffconfig
%make -f Makefile.Linux CFLAGS="$RPM_OPT_FLAGS `gtk-config --cflags`"
popd
pushd yiffutils
%make -f Makefile.Linux CFLAGS="$RPM_OPT_FLAGS -D__USE_BSD"
popd

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}/%{_sysconfdir}
install -d -m 755 %{buildroot}/%{_datadir}/icons
install -d -m 755 %{buildroot}/%{_datadir}/sounds
make PREFIX=%{buildroot}%{_prefix} YLIB_DIR=%{buildroot}%{_libdir} install
# move man from /usr to /usr/share
mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_mandir}
install -m 644 yiff/yiffrc %{buildroot}/%{_sysconfdir}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL INSTALL_MANUAL LICENSE README
%config(noreplace) %{_sysconfdir}/*
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_datadir}/icons/*
%{_datadir}/sounds/*

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc LICENSE
%{_includedir}/*
%_libdir/*.so

