# gemini-wine

Wine, built to run the Motorola DSP56K tools -- 32-bit Windows console
programs -- that assemble the GNIRS DC SDSU/ARC firmware. It is a build tool:
[gnirsdc-dsp](https://github.com/gemini-rtsw/gnirsdc-dsp) `BuildRequires` it,
and nothing deployed runs it.

Built and published by [gemini-rtsw-ci](https://github.com/gemini-rtsw/gemini-rtsw-ci)
as the `gemini-wine` RPM (EL9), installed to `/opt/gemini-wine`:

```bash
WINEPREFIX=$(mktemp -d) WINEDEBUG=-all /opt/gemini-wine/bin/wine cmd.exe /C CompileDSP.bat
```

## How it is built

Wine 10 in **new WoW64** mode (`--enable-archs=i386,x86_64`): 32-bit Windows
programs run inside a normal 64-bit build, with the 32-bit side compiled by
EPEL's MinGW cross compilers. That needs no 32-bit Linux libraries, which is
what makes it buildable on EL9 -- EPEL's own wine package is not installable on
current EL9, and it has no 32-bit support. Everything graphical, audio or
networked is configured out.

The source is the upstream release tarball in `SOURCES/`, which the pipeline
uses directly as the spec's `Source0`. `%check` runs `cmd.exe` from the built
tree, so a wine that cannot run a 32-bit console program fails the build.

The CI build compiles all of Wine and takes a while (about 20-30 minutes on a
GitHub runner); it only runs when this repo changes.

## Updating Wine

1. Download the new release into `SOURCES/` (remove the old tarball) and check
   its checksum against winehq.org.
2. Set `specver` in `gemini-wine.spec` to the new version.
3. Open a pull request, then move gnirsdc-dsp's pin once it is published.

This replaces the GitLab-era gemini-wine, a prebuilt 32-bit wine 7.0 for EL8
that installed under `/gem_base/epics/ioc/gemini-wine/wine-7.0`.
