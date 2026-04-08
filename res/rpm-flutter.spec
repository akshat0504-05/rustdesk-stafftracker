Name:       STRemote
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://STRemote.com
Vendor:     STRemote <info@STRemote.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/STRemote" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/STRemote"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/STRemote.service -t "%{buildroot}/usr/share/STRemote/files"
install -Dm 644 $HBB/res/STRemote.desktop -t "%{buildroot}/usr/share/STRemote/files"
install -Dm 644 $HBB/res/STRemote-link.desktop -t "%{buildroot}/usr/share/STRemote/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/STRemote.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/STRemote.svg"

%files
/usr/share/STRemote/*
/usr/share/STRemote/files/STRemote.service
/usr/share/icons/hicolor/256x256/apps/STRemote.png
/usr/share/icons/hicolor/scalable/apps/STRemote.svg
/usr/share/STRemote/files/STRemote.desktop
/usr/share/STRemote/files/STRemote-link.desktop

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
ln -sf /usr/share/STRemote/STRemote /usr/bin/STRemote
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
    rm /usr/bin/STRemote || true
    rmdir /usr/lib/STRemote || true
    rmdir /usr/local/STRemote || true
    rmdir /usr/share/STRemote || true
    rm /usr/share/applications/STRemote.desktop || true
    rm /usr/share/applications/STRemote-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/STRemote || true
    rmdir /usr/local/STRemote || true
  ;;
esac
