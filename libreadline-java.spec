%define editline_ver    2.9
%define src_dirs        org test
%define gcj_support     1

Name:    libreadline-java
Version: 0.8.0
Release: 24.3%{?dist}
Summary: Java wrapper for the EditLine library
Group:   Development/Libraries

License: LGPLv2+
URL:     http://java-readline.sf.net/
Source0: http://download.sf.net/java-readline/%{name}-%{version}-src.tar.gz
Patch0:  %{name}-ncurses.patch
Patch1:  %{name}-libdir.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: jpackage-utils >= 1.5
BuildRequires: libedit-devel >= %{editline_ver}
BuildRequires: ncurses-devel
%if %{gcj_support}
BuildRequires: java-gcj-compat-devel >= 1.0.31
%else
BuildRequires: java-devel >= 1.4.2
%endif

Requires:         libedit >= %{editline_ver}
%if %{gcj_support}
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
Requires:         java >= 1.4.2
%endif

%description
libreadline-java provides Java bindings for libedit though a JNI
wrapper.

%package javadoc
Summary: Javadoc for %{name}
Group:   Development/Libraries

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0
%patch1
sed -i 's|@LIBDIR@|%{_libdir}|' src/org/gnu/readline/Readline.java

%build
export JAVA_HOME=%{java_home}
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
make CFLAGS="$RPM_OPT_FLAGS -fPIC -DPOSIX" T_LIBS=JavaEditline
make apidoc

# fix debuginfo package
rm -f %{src_dirs}
for dir in %{src_dirs}
do
  ln -s src/$dir
done

%install
rm -rf $RPM_BUILD_ROOT

# install jar file and JNI library under %{_libdir}/%{name}
# FIXME: fix jpackage-utils to handle multilib correctly
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
install -m 644 %{name}.jar \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}.jar
install -m 755 libJavaEditline.so $RPM_BUILD_ROOT%{_libdir}/%{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# natively compile
%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc ChangeLog NEWS README README.1st VERSION COPYING.LIB
%dir %{_libdir}/%{name}
%attr(-,root,root) %{_libdir}/%{name}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Fri Jan 15 2010 Andrew Overholt <overholt@redhat.com> 0.8.0-24.3
- Fix license.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0.8.0-24.2
- Add Public Domain to License

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.0-24.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 14 2008 David Walluck <dwalluck@redhat.com> 0.8.0-22
- add unversioned javadoc symlink
- remove unnecessary gcc-java requirement
- fix permissions

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.0-21
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.0-20
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.8.0-19
- Rebuild for selinux ppc32 issue.

* Thu Jul  5 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-18
- Specify full path to libedit backing library.
- Default to libedit backing library.
- Satisfy termcap requirements with ncurses.
- Resolves: rhbz#231209

* Mon Mar 26 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-17
- Honor $RPM_OPT_FLAGS.

* Mon Mar 26 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-16
- Install jar file and JNI library under libdir.
- Group BuildRequires and Requires.
- Eliminate devel subpackage.
- Remove ldconfig requirements.
- Reformat.

* Fri Mar 23 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-15
- Fix libJavaEditline.so symlink typo.

* Fri Mar 23 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.8.0-14
- Rebuild against unorphaned libedit.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-13
- Changed summary and description to describe the change to editline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-12
- Remove dependency on readline and readline-devel.
- Add dependency on libedit{,-devel}, change make argument to JavaEditline
  from JavaReadline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-11
- Doubled percent signs in changelog section.
- Fixed dependency on readline to be >= instead of =.
- Move jar to %%{_javadir} from %%{_jnidir}
- Added dist tag.
- Added COPYING.LIB to doc files.

* Mon Jun 26 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_3fc
- Moved the unversioned .so file into a -devel package 
- Changed Group of the -javadoc package to Development/Libraries

* Fri Jun 23 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_2fc
- Remove Vendor and Distribution tags
- Change group to Development/Libraries
- Removed Epoch, and Epoch in Requires for libreadline
- Added (post) and (postun) to Requires of /sbin/ldconfig
- Changed Source0 to use the version and name macros
- Fixed debuginfo package

* Wed May 31 2006 Igor Foox <ifoox@redhat.com> 0:0.8.0-10jpp_1fc
- Natively compile
- Changed BuildRoot to what Extras expects

* Wed Nov 09 2005 Fernando Nasser <fnasser@redhat.com> 0:0.8.0-10jpp
- Rebuild for readline 5.0

* Tue Mar 29 2005 David Walluck <david@jpackage.org> 0:0.8.0-9jpp
- fix duplicate files in file list
- set java bins in path

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-8jpp
- Move jars into %%{_jnidir}

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-7jpp
- Replace build dep on termcap-devel with dep on %%{_libdir}/libtermcap.so
  (needed on RH/FC systems)

* Sat Oct 09 2004 David Walluck <david@jpackage.org> 0:0.8.0-6jpp
- rebuild for JPackage 1.5 devel

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0:0.8.0-5jpp
- rebuild for JPackage 1.5

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0.8.0-4jpp
- AutoReqProvides: no
- Strict requires on readline version and /sbin/ldconfig

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 0.8.0-3jpp
- set JAVA_HOME/bin in PATH

* Wed Jan 22 2003 David Walluck <david@anti-microsoft.org> 0.8.0-2jpp
- 1jpp was missing %%changelog
