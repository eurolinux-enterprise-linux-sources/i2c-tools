# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2007 Hans de Goede <j.w.r.degoede@hhs>, the Fedora project.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:           i2c-tools
Version:        3.1.0
Release:        10%{?dist}
Summary:        A heterogeneous set of I2C tools for Linux
Group:          Applications/System
License:        GPLv2+
URL:            http://www.lm-sensors.org/wiki/I2CTools
Source0:        http://dl.lm-sensors.org/i2c-tools/releases/%{name}-%{version}.tar.bz2

# Introducing man pages for binaries in the eepromer subpackage
# Introducing -r switch in the i2cset help
Patch0:         i2c-tools-3.1-man-eeproX.patch
# Introducing man pages for decode-* binaries
Patch1:         i2c-tools-3.1-man-decodeX.patch

# for /etc/udev/makedev.d resp /etc/modprobe.d ownership
Requires:       udev module-init-tools
BuildRequires:  python-devel
ExcludeArch:    s390 s390x

%description
This package contains a heterogeneous set of I2C tools for Linux: a bus
probing tool, a chip dumper, register-level access helpers, EEPROM
decoding scripts, and more.


%package eepromer
Summary:        Programs for reading / writing i2c / smbus eeproms
Group:          Applications/System
# For the device nodes
Requires:       %{name} = %{version}-%{release}

%description eepromer
Programs for reading / writing i2c / smbus eeproms. Notice that writing the
eeproms in your system is very dangerous and is likely to render your system
unusable. Do not install, let alone use this, unless you really, _really_ know
what you are doing.

%package python
Summary:        Python bindings for Linux SMBus access through i2c-dev
Group:          Applications/System

%description python

%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS"
pushd eepromer
make CFLAGS="$RPM_OPT_FLAGS -I../include"
popd
pushd py-smbus
CFLAGS="$RPM_OPT_FLAGS -I../include" %{__python} setup.py build
popd


%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
install -m 755 eepromer/{eepromer,eeprom,eeprog} \
  $RPM_BUILD_ROOT%{_sbindir}
install -m 644 eepromer/{eepromer,eeprom,eeprog}.8 \
  $RPM_BUILD_ROOT%{_mandir}/man8
install -d 755 $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 eeprom/{decode-dimms,decode-vaio}.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1
pushd py-smbus
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT
popd
# cleanup
rm -f $RPM_BUILD_ROOT%{_bindir}/decode-edid.pl
# Remove userland kernel headers, belong in glibc-kernheaders.
rm -rf $RPM_BUILD_ROOT%{_includedir}/linux
# Remove unpleasant DDC tools.  KMS already exposes the EDID block in sysfs,
# and edid-decode is a more complete tool than decode-edid.
rm -f $RPM_BUILD_ROOT%{_bindir}/{ddcmon,decode-edid}
# for i2c-dev ondemand loading through kmod
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d 
echo "alias char-major-89-* i2c-dev" > \
  $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/i2c-dev.conf
# for /dev/i2c-# creation (which are needed for kmod i2c-dev autoloading)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d
for (( i = 0 ; i < 8 ; i++ )) do
  echo "i2c-$i" >> $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
done


%files
%doc CHANGES COPYING README
%config(noreplace) %{_sysconfdir}/modprobe.d/i2c-dev.conf
%config(noreplace) %{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/decode-*.1.gz
%exclude %{_sbindir}/eepro*
%{_mandir}/man8/*.8.gz
%exclude %{_mandir}/man8/eepro*

%files eepromer
%doc eepromer/README*
%{_sbindir}/eepro*
%{_mandir}/man8/eepro*.8.gz

%files python
%doc py-smbus/README
#/usr/lib64/python2.7/site-packages/smbus-1.1-py2.7.egg-info
#/usr/lib64/python2.7/site-packages/smbus.so
%{python_sitearch}/*



%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.0-10
- Mass rebuild 2013-12-27

* Thu Oct 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-9
- Introducing man pages for decode-* binaries
- Cleaning the spec
- Resolves: rhbz#948819

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.1.0-7
- Perl 5.18 rebuild

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-6
- Installing the man pages and putting them in the files section

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 3.1.0-5
- Introducing man pages for binaries in the eepromer subpackage
- Introducing -r switch in the i2cset help

* Sat Jun  1 2013 Henrik Nordstrom <henrik@henriknordstrom.net> - 3.1.0-4
- Package python interface

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Adam Jackson <ajax@redhat.com> 3.1.0-1
- i2c-tools 3.1.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 3.0.3-1
- i2c-tools 3.0.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 3.0.2-3
- mv /etc/modprobe.d/i2c-dev /etc/modprobe.d/i2c-dev.conf (#495455)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Adam Jackson <ajax@redhat.com> 3.0.2-1
- i2c-tools 3.0.2

* Wed Mar  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-3
- Change /dev/i2c-# creation from /lib/udev/devices to /etc/udev/makedev.d
  usage
- Add an /etc/modprobe.d/i2c-dev file to work around bug 380971

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.0-2
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-1
- Initial Fedora package, based on Suse specfile

* Mon Oct 15 2007 - jdelvare@suse.de
- Initial release.
