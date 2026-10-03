%define plasmaver %(echo %{version} |cut -d. -f1-3)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

Summary:	Plasma display manager
Name:		plasma-login-manager
Version:	6.7.5
Release:	2
License:	GPLv2+
Group:		Graphical desktop/KDE
URL:		https://invent.kde.org/plasma/plasma-login-manager
Source0:	http://download.kde.org/%{stable}/plasma/%{plasmaver}/%{name}-%{version}.tar.xz
Source1:	plasmalogin.pam
Source2:	plasmalogin-autologin.pam
Source3:	plasmalogin-greeter.pam

BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6QuickTest)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6Package)
BuildRequires:	cmake(KF6WindowSystem)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6Auth)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(PlasmaQuick)
BuildRequires:	cmake(LayerShellQt)
BuildRequires:	cmake(LibKWorkspace)
BuildRequires:	cmake(LibKLookAndFeel)
BuildRequires:	cmake(KF6Screen)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pam-devel

BuildSystem:	cmake
BuildOption:	-DINSTALL_PAM_CONFIGURATION:BOOL=OFF
BuildOption:	-DBUILD_TESTING:BOOL=OFF
BuildOption:	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
BuildOption:	-DSESSION_COMMAND:PATH=%{_sysconfdir}/X11/Xsession
BuildOption:	-DWAYLAND_SESSION_COMMAND:PATH=%{_datadir}/plasmalogin/scripts/wayland-session

Requires:	kwin
Requires:	pam
Provides:	dm
# Optional: the KCM is useful only if System Settings is installed

%description
Plasma Login is a display manager forked from SDDM, with a QML greeter,
wallpaper plugin integration and a System Settings module.

This package is available as an alternative to SDDM. The default
OpenMandriva desktop still uses SDDM.

%install -a
install -Dpm 644 %{SOURCE1} %{buildroot}%{_prefix}/lib/pam.d/plasmalogin
install -Dpm 644 %{SOURCE2} %{buildroot}%{_prefix}/lib/pam.d/plasmalogin-autologin
install -Dpm 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/pam.d/plasmalogin-greeter
mkdir -p %{buildroot}%{_sysconfdir}/plasmalogin.conf.d
mkdir -p %{buildroot}%{_localstatedir}/lib/plasmalogin
mkdir -p %{buildroot}%{_rundir}/plasmalogin
# Avoid clashing with SDDM's org.freedesktop.DisplayManager.conf
if [ -f %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf ]; then
	mv %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf \
	   %{buildroot}%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-plasmalogin.conf
fi

%files -f %{name}.lang
%{_bindir}/plasmalogin
%{_bindir}/startplasma-login-wayland
%{_bindir}/plasma-login-wallpaper
%{_libdir}/libexec/plasmalogin-helper
%{_libdir}/libexec/plasmalogin-helper-start-x11user
%{_libdir}/libexec/plasma-login-greeter
%{_prefix}/lib/pam.d/plasmalogin
%{_prefix}/lib/pam.d/plasmalogin-autologin
%{_prefix}/lib/pam.d/plasmalogin-greeter
%dir %{_sysconfdir}/plasmalogin.conf.d
%{_datadir}/plasmalogin
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager-plasmalogin.conf
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmplasmalogin.service
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmplasmalogin.conf
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmplasmalogin.policy
%{_datadir}/applications/kcm_plasmalogin.desktop
%{_qtdir}/plugins/plasma/kcms/systemsettings/kcm_plasmalogin.so
%{_libdir}/libexec/kf6/kauth/kcmplasmalogin_authhelper
%{_unitdir}/plasmalogin.service
%{_userunitdir}/plasma-login.service
%{_userunitdir}/plasma-login-kwin_wayland.service
%{_userunitdir}/plasma-login-wayland.target
%{_userunitdir}/plasma-wallpaper.service
%{_tmpfilesdir}/plasmalogin.conf
%{_sysusersdir}/plasmalogin.conf
%attr(0711,root,plasmalogin) %dir %{_rundir}/plasmalogin
%attr(1770,plasmalogin,plasmalogin) %dir %{_localstatedir}/lib/plasmalogin
