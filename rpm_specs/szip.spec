# $Revision: 1.9 $, $Date: 2011/06/26 04:16:18 $
#
# Example usage:
# rpmbuild -ba --define 'BUILD_RELEASE 3' szip.spec
#
# Conditional build:
%bcond_without	encoder		# build with encoder (using may require license)
#
Summary:	SZIP - Science Data Lossless Compression library
Summary(pl.UTF-8):	SZIP - biblioteka bezstratnej kompresji danych naukowych
Name:		szip
Version:	2.1
Release:        %{BUILD_RELEASE}%{?dist}        	
%if %{with encoder}
License:	free for use in HDF software (decoder), free for non-commercial, scientific use only in HDF software (encoder)
%else
License:	free for use in HDF software
%endif
Group:		Libraries
Source0:	ftp://ftp.hdfgroup.org/lib-external/szip/%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	63894a65bc470011fd2049f3ca65d2bf
Patch0:		%{name}-opt.patch
Patch1:		%{name}-linking.patch
URL:		http://hdf.ncsa.uiuc.edu/doc_resource/SZIP/
BuildRequires:	cmake
# BuildRequires:	autoconf >= 2.54
# BuildRequires:	automake
# BuildRequires:	automake >= 1:1.7
# BuildRequires:	libtool
# BuildRequires:	libtool >= 1:1.4.2-9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SZIP is an implementation of the extended-Rice lossless compression
algorithm. The Consultative Committee on Space Data Systems (CCSDS)
has adopted the extended-Rice algorithm for international standards
for space applications. SZIP is reported to provide fast and effective
compression, specifically for the EOS data generated by the NASA Earth
Observatory System (EOS). It was originally developed at University of
New Mexico (UNM) and integrated with HDF4 by UNM researchers and
developers.

%description -l pl.UTF-8
SZIP to implementacja rozszerzonego algorytmu kompresji bezstratnej
Rice'a. CCSDS (Consultative Committee on Space Data Systems)
zaadoptowało rozszerzony algorytm Rice'a na potrzeby międzynarodowych
standardów aplikacji przestrzennych. SZIP daje szybką i efektywną
kompresję, szczególnie dla danych EOS generowanych przez NASA Earth
Observatory System (EOS). Pierwotnie biblioteka została stworzona w
University of New Mexico (UNM) i zintegrowana z HDF4 przez naukowców i
programistów UNM.

%package devel
Summary:	Header files for SZIP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SZIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for SZIP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SZIP.

%package static
Summary:	Static SZIP library
Summary(pl.UTF-8):	Statyczna biblioteka SZIP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SZIP library.

%description static -l pl.UTF-8
Statyczna biblioteka SZIP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build

mkdir -p build
pushd build
%cmake ..
%{__make}
popd

%install

pushd build
make install DESTDIR=%{buildroot}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%{_libdir}/libszip.so*
%doc COPYING HISTORY.txt RELEASE.txt

# Weed out un-wanted things:
%exclude %{_includedir}/SZconfig.h
%exclude /usr/lib/SZIP-targets-noconfig.cmake
%exclude /usr/lib/SZIP-targets.cmake
%exclude /usr/lib/cmake/SZIP-2.1/SZIP-config-version.cmake
%exclude /usr/lib/cmake/SZIP-2.1/SZIP-config.cmake

%files devel
%{_includedir}/ricehdf.h
%{_includedir}/szip_adpt.h
%{_includedir}/szlib.h


%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* %{date} PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

$Log: szip.spec,v $
Revision 1.9  2011/06/26 04:16:18  qboosh
- new Source URL and tarball
- encoder enabled by default
- release 2

Revision 1.8  2009/09/10 08:34:56  tommat
- added linking patch, builds now
- ghost soname symlink

Revision 1.7  2008/08/11 06:19:08  draenog
- new URL

Revision 1.6  2007/10/30 12:53:47  draenog
- updated to 2.1
- new path to Source0
- link.patch removed; implemented in different way in sources

Revision 1.5  2007/02/12 22:09:17  glen
- tabs in preamble

Revision 1.4  2007/02/12 01:06:34  baggins
- converted to UTF-8

Revision 1.3  2006/12/14 08:48:25  qboosh
- cleanup: automake copies config.*

Revision 1.2  2006/12/13 23:51:46  wrobell
- fixed linking of examples
- rel. 2

Revision 1.1  2005/02/27 21:30:14  qboosh
- new

