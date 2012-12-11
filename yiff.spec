%define	name	yiff
%define	version 2.14.7
%define release %mkrel 5
%define major	%{version}
%define	libname %mklibname %name %major
%define	develname %mklibname %name -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	YIFF Sound Systems
License: 	GPL
Group: 		System/Servers
Url: 		http://wolfpack.twu.net/YIFF/index.html
Source0:	http://wolfsinger.com/~wolfpack/packages/%{name}-%{version}.tar.bz2
Patch:		%{name}-2.14.5.build.patch
BuildRequires:	gtk+-devel
BuildRequires:	zlib-devel
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

%description -n %{libname}
This package contains the library needed to run programs dynamically linked 
with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %name -d 2.14.5

%description -n %{develname}
This package contains the headers that programmers will need to develop 
applications which will use %{name}.

%prep
%setup -q
%patch -p0

%build
pushd libY2
%make -f Makefile.Linux CFLAGS="%{optflags} %{ldflags} -fPIC"
popd
pushd yiff
%make -f Makefile.Linux CFLAGS="%{optflags} %{ldflags} -DOSS_BUFFRAG"
popd
pushd yiffconfig
%make -f Makefile.Linux CFLAGS="%{optflags} %{ldflags} `gtk-config --cflags`"
popd
pushd yiffutils
%make -f Makefile.Linux CFLAGS="%{optflags} %{ldflags} -D__USE_BSD"
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
%doc INSTALL INSTALL_MANUAL LICENSE README
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


%changelog
* Wed Dec 01 2010 Funda Wang <fwang@mandriva.org> 2.14.7-5mdv2011.0
+ Revision: 604368
- bunzip2 the patch
- use our own link flags

* Mon Sep 21 2009 Thierry Vignaud <tv@mandriva.org> 2.14.7-4mdv2010.0
+ Revision: 446310
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.7-3mdv2009.1
+ Revision: 354874
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.7-2mdv2009.1
+ Revision: 354775
- new devel policy

* Thu Mar 12 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.7-1mdv2009.1
+ Revision: 354410
- new version

* Sun Dec 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.5-7mdv2009.1
+ Revision: 314328
- add starty script in %%{_bindir}

* Thu Dec 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.5-6mdv2009.1
+ Revision: 312889
- rebuild with -DOSS_BUFFRAG (should fix #36958)

* Mon Aug 04 2008 Thierry Vignaud <tv@mandriva.org> 2.14.5-5mdv2009.0
+ Revision: 262952
- rebuild

* Mon Aug 04 2008 Thierry Vignaud <tv@mandriva.org> 2.14.5-4mdv2009.0
+ Revision: 262801
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 2.14.5-2mdv2008.1
+ Revision: 141006
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - import yiff


* Tue Aug 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.5-2mdv2007.0
- Rebuild

* Thu May 04 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.5-1mdk
- New release 2.14.5
- rediff patch

* Wed Sep 21 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.2-5mdk
- fix x86_64 build

* Thu Jul 28 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.2-4mdk 
- less intrusive patch

* Sat Jul 09 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.14.2-3mdk 
- fix build with gcc 4

* Sat Jun 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.14.2-2mdk
- rebuild
- rpmbuildupdate aware

* Tue Aug 05 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.14.2-1mdk
- 2.14.2

* Tue Jul 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.14.1-2mdk
- rebuild for new rpm devel computation

* Thu Jun 05 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.14.1-1mdk
- 2.14.1
- cleaned patch

* Sun May 11 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.4-9mdk
- %%{libname}-devel provides lib%%{name}-devel

* Thu May 08 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.4-8mdk
- rebuild
- use %%mklibame macro
- changed library package name to %%{libname}
- added missing man pages
- proper build flags

* Sat Oct 27 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.4-7mdk
- buildrequires zlib1-devel
- no explicit requires

* Fri Oct 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.12.4-6mdk
- rebuild for dependencies.

* Tue Oct 23 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 2.12.4-5mdk 
- rebuild for rpmlint

* Thu Sep 06 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.12.4-4mdk
- rebuild

* Fri Jun 22 2001 Etienne Faure    <etienne@mandrakesoft.com> 2.12.4-3mdk
- rebuild for contribs

* Mon May 07 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.4-2mdk
- new source file, as the first one was corrupted

* Sat May 05 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.4-1mdk
- 2.12.4
- corrected requires tag
- corrected file list to make rpmlint happy

* Thu Feb 15 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.3-1mdk
- 2.12.3

* Tue Feb 06 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.2-2mdk
- added yiffconfig corrections
- added instruction to description

* Sat Feb 03 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.12.2-1mdk
- first Mandrake release
