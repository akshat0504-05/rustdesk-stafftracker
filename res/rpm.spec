Name:       STRemote
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://STRemote.com
Vendor:     STRemote <info@STRemote.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/STRemote/
mkdir -p %{buildroot}/usr/share/STRemote/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/STRemote %{buildroot}/usr/bin/STRemote
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/STRemote/libsciter-gtk.so
install $HBB/res/STRemote.service %{buildroot}/usr/share/STRemote/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/STRemote.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/STRemote.svg
install $HBB/res/STRemote.desktop %{buildroot}/usr/share/STRemote/files/
install $HBB/res/STRemote-link.desktop %{buildroot}/usr/share/STRemote/files/

%files
/usr/bin/STRemote
/usr/share/STRemote/libsciter-gtk.so
/usr/share/STRemote/files/STRemote.service
/usr/share/icons/hicolor/256x256/apps/STRemote.png
/usr/share/icons/hicolor/scalable/apps/STRemote.svg
/usr/share/STRemote/files/STRemote.desktop
/usr/share/STRemote/files/STRemote-link.desktop
/usr/share/STRemote/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop STRemote || true
  ;;
esac

%post
cp /usr/share/STRemote/files/STRemote.service /etc/systemd/system/STRemote.service
cp /usr/share/STRemote/files/STRemote.desktop /usr/share/applications/
cp /usr/share/STRemote/files/STRemote-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable STRemote
systemctl start STRemote
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop STRemote || true
    systemctl disable STRemote || true
    rm /etc/systemd/system/STRemote.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/STRemote.desktop || true
    rm /usr/share/applications/STRemote-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
