%define _varlogdir      %{_localstatedir}/log/smsd
%define _varrundir      %{_localstatedir}/run/smsd

# enable PIE (RHBZ #955265)
%global _hardened_build 1

Name:           smstools
Version:        3.1.15
Release:        14%{?dist}
Summary:        Tools to send and receive short messages through GSM modems or mobile phones

License:        GPLv2+
Group:          Applications/Communications
URL:            http://smstools3.kekekasvi.com
Source0:        http://smstools3.kekekasvi.com/packages/smstools3-%{version}.tar.gz
Source1 :       smsd.init
Source2:        smsd.logrotate
Source3:        smsd.tmpfiles
Patch0:         smstools3-3.1.5-loglocation.patch
Patch1:         smstools3-3.1.15-rundirectory.patch
Patch2:         smstools3-3.1.15-Makefiletab.patch
Patch3:         smstools3-3.1.15-enablestats.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  mm-devel
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
Requires(pre): shadow-utils

%description
The SMS Server Tools are made to send and receive short messages through
GSM modems. It supports easy file interfaces and it can run external
programs for automatic actions. 

%prep
%setup -q -n smstools3
%patch0 -p1 -b .loglocation
%patch1 -p1 -b .rundirectory
%patch2 -p1 -b .Makefiletab
%patch3 -p1 -b .enablestats
mv doc manual
mv examples/.procmailrc examples/procmailrc
mv examples/.qmailrc examples/qmailrc
find scripts/ examples/ manual/ -type f -print0 |xargs -0 chmod 644

%build
make -C src 'CFLAGS=%{optflags} -D NUMBER_OF_MODEMS=64' LFLAGS="%{__global_ldflags}" %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/smsd
install -Dm 664 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/smstools
install -Dm 664 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/smstools.conf
install -Dm 600 examples/smsd.conf.easy $RPM_BUILD_ROOT%{_sysconfdir}/smsd.conf
install -Dm 755 src/smsd $RPM_BUILD_ROOT%{_sbindir}/smsd
install -Dm 755 scripts/sendsms $RPM_BUILD_ROOT%{_bindir}/smssend
install -Dm 755 scripts/sms2html $RPM_BUILD_ROOT%{_bindir}/sms2html
install -Dm 755 scripts/sms2unicode $RPM_BUILD_ROOT%{_bindir}/sms2unicode
install -Dm 755 scripts/sms2xml $RPM_BUILD_ROOT%{_bindir}/sms2xml
install -Dm 755 scripts/unicode2sms $RPM_BUILD_ROOT%{_bindir}/unicode2sms
install -dm 750 $RPM_BUILD_ROOT%{_localstatedir}/spool/sms/checked
install -dm 750 $RPM_BUILD_ROOT%{_localstatedir}/spool/sms/failed
install -dm 750 $RPM_BUILD_ROOT%{_localstatedir}/spool/sms/incoming
install -dm 770 $RPM_BUILD_ROOT%{_localstatedir}/spool/sms/outgoing
install -dm 750 $RPM_BUILD_ROOT%{_localstatedir}/spool/sms/sent
mkdir -p ${RPM_BUILD_ROOT}%{_varlogdir}
mkdir -p ${RPM_BUILD_ROOT}%{_varlogdir}/smsd_stats
mkdir -p ${RPM_BUILD_ROOT}%{_varrundir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/smstools


# Create ghost files
for n in smsd.log smsd_trouble.log; do
    touch ${RPM_BUILD_ROOT}%{_varlogdir}/$n
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group smstools >/dev/null || groupadd -r smstools

# on older releases we need to use uucp (here it seems only the uucp group exists)
# on newer releases it's dialout (here it seems both groups exist)
# it would be more elegant to base my if clause on the udev rules instead of the group existence
if [ `getent group dialout` ]
  then
    getent passwd smstools >/dev/null || useradd -r -d %{_localstatedir}/lib/smstools -m -g smstools -G dialout smstools
  else
    getent passwd smstools >/dev/null || useradd -r -d %{_localstatedir}/lib/smstools -m -g smstools -G uucp smstools
fi


%post
if [ $1 -eq 0 ]; then
        /sbin/chkconfig --add smsd
fi

# Create initial log files so that logrotate doesn't complain
for n in smsd.log smsd_trouble.log; do
        [ -f %{_varlogdir}/$n ] || touch %{_varlogdir}/$n
        chown smstools:smstools %{_varlogdir}/$n
        chmod 640 %{_varlogdir}/$n
done

%preun
if [ $1 -eq 0 ]; then
        /sbin/service smsd stop >/dev/null 2>&1
        /sbin/chkconfig --del smsd
fi

%postun
if [ $1 -ge 1 ]; then
        /sbin/service smsd condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%doc LICENSE manual/ examples/ scripts/checkhandler-utf-8 scripts/email2sms scripts/eventhandler-utf-8
%doc scripts/mysmsd scripts/regular_run scripts/smsevent scripts/smsresend scripts/sql_demo
%{_sbindir}/*
%{_bindir}/*
%{_initrddir}/smsd
%config(noreplace) %{_sysconfdir}/logrotate.d/smstools
%config %{_sysconfdir}/tmpfiles.d/smstools.conf
%config(noreplace) %{_sysconfdir}/smsd.conf
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/checked
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/failed
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/incoming
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/outgoing
%attr(-,smstools,smstools) %dir %{_localstatedir}/spool/sms/sent
%attr(-,smstools,smstools) %dir %{_localstatedir}/lib/smstools
%attr(0750,smstools,smstools) %dir %{_varlogdir}
%attr(0640,smstools,smstools) %ghost %{_varlogdir}/smsd.log
%attr(0640,smstools,smstools) %ghost %{_varlogdir}/smsd_trouble.log
%attr(0750,smstools,smstools) %dir %{_varlogdir}/smsd_stats
%attr(0700,smstools,smstools) %dir %{_varrundir}

%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-12
- enabled statistics [1119033]

* Tue Jul 14 2015 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-12
- src/Makefile was lacking a tab

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-9
- fixed two bogus dates in changelong

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-6
- fix for pidfile and infofile in /run, thanks Kaarle (RHBZ #961503)
- added LFLAGS="%{__global_ldflags}" to get PIE enabled correctly, thanks Dhiru (RHBZ #955265)

* Thu Apr 25 2013 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-5
- enabled PIE (RHBZ #955265)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 7 2012 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-3
- create /var/lib/smstools in install section

* Tue Nov 6 2012 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-3
- add /var/lib/smstools to files list (RHBZ #871437)

* Sat Oct 27 2012 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-2
- fixing fedpkg lint warnings

* Sat Oct 27 2012 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.15-1
- latest upstream (fixes RHBZ#863661, patch from 3.1.14-4 no longer needed)

* Sat Oct 06 2012 Daniele Vigano <daniele@vigano.me> 3.1.14-4
- Fixed segfault of outgoing file checker (BZ#863661)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.14-1
- New upstream release

* Fri Jan 21 2011 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.8-3
- corrected missing /var/run/smsd directory (BZ#605203)

* Thu Jan 20 2011 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.8-2
- added if clause for deciding between uucp and dialout group (BZ#605211)

* Mon May 31 2010 Marek Mahut <mmahut@fedoraproject.org> 3.1.8-1
- New upstream release

* Thu Oct 15 2009 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.5-4
- added flag -m to useradd

* Tue Oct 13 2009 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.5-3
- after deliberation, decided on having system user (mysql user also has shell, so this should be OK)

* Sun Oct 11 2009 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.5-2
- corrected typo in my name in previous changelog entry
- log files now go to /var/log/smsd (copied that bit from the uucp RPM)
- creating smstools user if it does not exist
- will run as user smstools now, did not manage to make it work as system user without login though

* Sun Sep 6 2009 Patrick C. F. Ernzer <smstools.spec@pcfe.net> 3.1.5-1
- bump to 3.1.5
- removed perm patch
- added -D NUMBER_OF_MODEMS=64 to make line

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.3-5
- Upstream release
- RHBZ#437620 root privileges are mandatory for sending/receiving an sms
- RHBZ#443790 smstools logrotate does not work properly
- RHBZ#461862 smssend creates rw------- files

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.10-2
- Autorebuild for GCC 4.3

* Sat Nov 10 2007 Marek Mahut <mmahut@fedoraproject.org> 3.0.10-1
- Rewrite of spec file.
- Updated to version 3.0.10

* Sat Apr 07 2007 Andreas Thienemann <andreas@bawue.net> 3.0.6-1
- Updated to version 3.0.6
- Reverted daemonize patch as it is not needed anymore

* Wed Nov 30 2005 Andreas Thienemann <andreas@bawue.net> 1.15.7-3
- Fixed logrotate script

* Tue Sep 13 2005 Andreas Thienemann <andreas@bawue.net> 1.15.7-2
- Now with statistics support

* Mon Sep 12 2005 Andreas Thienemann <andreas@bawue.net> 1.15.7-1
- Initial spec.

