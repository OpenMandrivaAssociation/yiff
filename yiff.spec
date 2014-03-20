%define	name	yiff
%define	version 2.14.7
%define release 6
%define major	%{version}
%define	libname %mklibname %name %major
%define	develname %mklibname %name -d
%define debug_package	%{nil}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	YIFF Sound Systems
License: 	GPL
Group: 		System/Servers
Url: 		http://wolfpack.twu.net/YIFF/index.html
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch:		%{name}-2.14.5.build.patch
BuildRequires:	pkgconfig(gtk+)
BuildRequires:	zlib-devel


%description
YIFF is a high performance, stable, and fully  documented sound server for UNIX
games and applications. It employs a network transparent API which allows 
multiple client programs to access sound capabilities in a similar way to how X
clients do graphics.

Run yiffconfig after install to generate a starty script.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
This package contains the library needed to run programs dynamically linked 
with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%mklibname %name -d 2.14.5

%description -n %{develname}
This package contains the headers that programmers will need to develop 
applications which will use %{name}.

%prep
%setup -q
%patch -p0

%build
pushd libY2
%make -f Makefile.Linux CFLAGS="%{optflags -wall} %{ldflags} -fPIC"
popd
pushd yiff
%make -f Makefile.Linux CFLAGS="%{optflags -wall} %{ldflags} -DOSS_BUFFRAG"
popd
pushd yiffconfig
%make -f Makefile.Linux CFLAGS="%{optflags -wall} %{ldflags} `gtk-config --cflags`"
popd
pushd yiffutils
%make -f Makefile.Linux CFLAGS="%{optflags -wall} %{ldflags} -D__USE_BSD"
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

cat >> %{buildroot}%{_bindir}/starty <<EOF
#!/bin/sh

# Locations of YIFF compoents and resources, make any changes as needed.
#
YIFF_PROGRAM=/usr/sbin/yiff
YIFF_CONFIGURATION=/etc/yiffrc

# Run the YIFF Sound Server, syntax is; "<program> <config_file>"
# YIFF will put the process into background by itself.
#
$YIFF_PROGRAM $YIFF_CONFIGURATION

# Put list of Y hosts that you would like to allow connecting to the
# Y server in this section. Note that localhost (127.0.0.1) is always
# given permission to connect when the YIFF server is runned.
#
#yhost 127.0.0.1

# Play a sound object on successful startup?
#yplay -m /usr/share/sounds/startup1.wav
EOF
chmod +x %{buildroot}%{_bindir}/starty



%files

%doc INSTALL_MANUAL LICENSE README
%config(noreplace) %{_sysconfdir}/yiffrc
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

%files -n %{develname}
%defattr(-,root,root)
%doc LICENSE
%{_includedir}/*
%_libdir/*.so


