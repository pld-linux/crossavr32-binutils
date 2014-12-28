Summary:	Cross AVR32 GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - AVR32 binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - AVR32 binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla AVR32 - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - AVR32 binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - AVR32 binutils
Name:		crossavr32-binutils
Version:	2.17
Release:	0.6
License:	GPL v2+
Group:		Development/Tools
Source0:	http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	e26e2e06b6e4bf3acf1dc8688a94c0d1
#based on http://www.avr32linux.org/twiki/bin/viewfile/Main/DevelopmentTools?rev=1;filename=500-avr32.patch.gz
Patch0:		%{name}.patch
#http://www.avr32linux.org/twiki/bin/viewfile/Main/DevelopmentTools?rev=1;filename=501-avr32-sreldyn-fix.patch.gz
Patch1:		%{name}-sreldyn-fix.patch
#http://www.avr32linux.org/twiki/bin/viewfile/Main/DevelopmentTools?rev=1;filename=502-avr32-bfd-dont-allow-direct-refs-to-bss.patch.gz
Patch2:		%{name}-bfd-dont-allow-direct-refs-to-bss.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-tools
%ifarch sparc sparc32
BuildRequires:	sparc32
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		avr32-pld-linux
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for Atmel AVR.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler,
konsolidator (linker), a także inne narzędzia do manipulowania
binarnymi plikami programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla platformy Atmel
AVR.

%prep
%setup -q -n binutils-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp /usr/share/automake/config.sub .

for i in bfd binutils gas ld opcodes
do
  cd $i
  %{__aclocal}
  %{__automake}
  %{__autoconf}
  cd ..
done

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
%ifarch sparc
sparc32 \
%endif
./configure \
	--enable-shared \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

rm -f $RPM_BUILD_ROOT%{_datadir}/locale/*/LC_MESSAGES/*.mo
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/*/*
%{_mandir}/man?/%{target}-*
%{_prefix}/i686-pc-linux-gnu/%{target}
