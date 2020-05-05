/*
	Prefs to ensure that we can correctly open and close Firefox
	with the script. These ensure we do not see dialog boxes
	and will always profile a startup to about:home.
*/

pref("browser.shell.checkDefaultBrowser", true);
pref("browser.tabs.warnOnClose", false);
pref("browser.shell.defaultBrowserCheckCount", 100);
pref("browser.startup.firstrunSkipsHomepage", false);
pref("browser.startup.homepage_override.mstone", "ignore");
pref("startup.homepage_welcome_url", "about:home");
pref("browser.startup.homepage", "about:home");