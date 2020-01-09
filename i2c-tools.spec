# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2007 Hans de Goede <j.w.r.degoede@hhs>, the Fedora project.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:           i2c-tools
Version:        3.1.0
Release:        3%{?dist}
Summary:        A heterogeneous set of I2C tools for Linux
Group:          Applications/System
License:        GPLv2+
URL:            http://www.lm-sensors.org/wiki/I2CTools
Source0:        http://dl.lm-sensors.org/i2c-tools/releases/%{name}-%{version}.tar.bz2

# Autoload i2c-dev module when needed
Patch0:         i2c-tools-3.1.0-load-i2c-dev-mod.patch
# for /etc/udev/makedev.d resp /etc/modprobe.d ownership
Requires:       udev module-init-tools
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


%prep
%setup -q 

%patch0 -p1


%build
make CFLAGS="$RPM_OPT_FLAGS"
pushd eepromer
make CFLAGS="$RPM_OPT_FLAGS -I../include"
popd


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
install -m 755 eepromer/{eepromer,eeprom,eeprog} \
  $RPM_BUILD_ROOT%{_sbindir}
# cleanup
rm -f $RPM_BUILD_ROOT%{_bindir}/decode-edid.pl
# Remove userland kernel headers, belong in glibc-kernheaders.
rm -rf $RPM_BUILD_ROOT%{_includedir}/linux
# for i2c-dev ondemand loading through kmod
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d 
echo "alias char-major-89-* i2c-dev" > \
  $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/i2c-dev.conf
# for /dev/i2c-# creation (which are needed for kmod i2c-dev autoloading)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d
for (( i = 0 ; i < 8 ; i++ )) do
  echo "i2c-$i" >> $RPM_BUILD_ROOT%{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README
%config(noreplace) %{_sysconfdir}/modprobe.d/i2c-dev.conf
%config(noreplace) %{_sysconfdir}/udev/makedev.d/99-i2c-dev.nodes
%{_bindir}/*
%{_sbindir}/*
%exclude %{_sbindir}/eepro*
%{_mandir}/man8/*.8.gz

%files eepromer
%defattr(-,root,root,-)
%doc eepromer/README*
%{_sbindir}/eepro*


%changelog
* Tue Jun 03 2014 Michal Minar <miminar@redhat.com> 3.1.0-3
- Made sure i2c-dev module is loaded.
- Resolves #914728

* Thu Mar 22 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.0-1
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
