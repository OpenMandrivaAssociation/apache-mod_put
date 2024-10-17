#Module-Specific definitions
%define mod_name mod_put
%define mod_conf 96_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module that implement DELETE and PUT http methods
Name:		apache-%{mod_name}
Version:	2.0.9
Release:	10
Group:		System/Servers
License:	Apache License
URL:		https://www.gknw.net/development/apache/
Source0: 	http://www.gknw.net/development/apache/httpd-2.0/unix/modules/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
This small module implements the HTTP/1.1 PUT and DELETE methods
for apache. Please notice that it can be a big security 
hole to activate them without securing the web server.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

# fix strange perms
chmod 644 *

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc mod_put.html my_cfg.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-9mdv2012.0
+ Revision: 772748
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-8
+ Revision: 678402
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-7mdv2011.0
+ Revision: 588048
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-6mdv2010.1
+ Revision: 516164
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-5mdv2010.0
+ Revision: 406635
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-4mdv2009.1
+ Revision: 326220
- rebuild

  + Michael Scherer <misc@mandriva.org>
    - better summary

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-3mdv2009.0
+ Revision: 235070
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-2mdv2009.0
+ Revision: 215621
- fix rebuild

* Thu May 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.9-1mdv2009.0
+ Revision: 207568
- 2.0.9

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.8-5mdv2008.1
+ Revision: 181839
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:2.0.8-4mdv2008.1
+ Revision: 170742
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.8-3mdv2008.0
+ Revision: 82661
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-2mdv2007.1
+ Revision: 140730
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.8-1mdv2007.1
+ Revision: 79484
- Import apache-mod_put

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.8-1mdv2007.0
- 2.0.8

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.7-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.7-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0.7-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0.7-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.7-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.7-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.7-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.7-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.0.7-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.0.7-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0.7-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.0.7-1mdk
- 2.0.7
- built for apache 2.0.49

