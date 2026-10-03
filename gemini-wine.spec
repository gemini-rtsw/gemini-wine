# gemini-wine: Wine, built to run the Motorola DSP56K tools (32-bit Windows
# console programs) that assemble the GNIRS DC SDSU/ARC firmware. Build tool
# only -- gnirsdc-dsp BuildRequires it.
#
# Wine 10 in "new WoW64" mode (--enable-archs=i386,x86_64): 32-bit Windows
# programs run inside an ordinary 64-bit build, with the 32-bit side compiled by
# the MinGW cross compilers. No 32-bit Linux libraries are needed, which EL9
# would otherwise require (and EPEL's wine package is not installable on
# current EL9). Everything graphical or networked is configured out: the tools
# are console programs that read and write files.
#
# Installed under /opt/gemini-wine so it can never collide with a distro wine.
# Source: SOURCES/wine-<version>.tar.xz, the upstream release tarball
# (https://dl.winehq.org/wine/source/), used as Source0 by build_rpm.sh.

%global specver 10.0
# $GIT_HASH first: build_rpm.sh computes it on the host and passes it in.
%define git_hash %(if [ -n "$GIT_HASH" ]; then echo "$GIT_HASH"; else git rev-parse --short HEAD 2>/dev/null || echo nogit; fi)

%global wineprefix /opt/gemini-wine

# Half of what is installed is Windows PE code; leave all of it as built, and
# keep the private libraries out of the global Provides.
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global __provides_exclude_from ^%{wineprefix}/.*$
%global __requires_exclude_from ^%{wineprefix}/lib/wine/.*-windows/.*$

Name:           gemini-wine
Version:        %{specver}
Release:        1.git%{git_hash}%{?dist}
Summary:        Wine for the DSP56K firmware tools (GNIRS DC build tool)
License:        LGPLv2+
URL:            https://www.winehq.org/
Source0:        wine-%{version}.tar.xz
ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc

%description
Wine %{version} built in WoW64 mode under %{wineprefix}, so the 32-bit
Motorola DSP56K assembler, linker and loader run on a 64-bit EL9 host. Used to
build the GNIRS DC SDSU/ARC firmware (gnirsdc-dsp). Console only.

%prep
%setup -q -n wine-%{version}

%build
./configure --prefix=%{wineprefix} \
    --enable-archs=i386,x86_64 --disable-tests \
    --without-x --without-wayland --without-opengl --without-vulkan --without-osmesa \
    --without-freetype --without-fontconfig --without-gnutls --without-krb5 \
    --without-alsa --without-pulse --without-gstreamer --without-sdl \
    --without-cups --without-sane --without-gphoto --without-v4l2 --without-capi \
    --without-dbus --without-udev --without-usb --without-pcap --without-pcsclite \
    --without-netapi --without-unwind --without-inotify \
    --without-xcomposite --without-xcursor --without-xfixes --without-xinerama \
    --without-xinput --without-xinput2 --without-xrandr --without-xshm --without-xxf86vm
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
# The installed tree must run a 32-bit Windows console program.
export WINEPREFIX=$(mktemp -d) WINEDEBUG=-all
out=$(timeout 300 %{buildroot}%{wineprefix}/bin/wine cmd.exe /C echo gemini-wine-ok 2>&1 | tr -d '\r')
%{buildroot}%{wineprefix}/bin/wineserver -k 2>/dev/null || :
echo "$out" | grep -q gemini-wine-ok || { echo "ERROR: wine did not run cmd.exe:"; echo "$out"; exit 1; }

%files
%{wineprefix}

%changelog
* Fri Oct 02 2026 Hawi Stecher <hawi.stecher@noirlab.edu> - 10.0-1
- Wine 10.0 in WoW64 mode for EL9, built with gemini-rtsw-ci. Replaces the
  GitLab-era 32-bit wine 7.0 build.
