import gettext

__t = gettext.translation(domain="modul_graph", localedir="./locales", languages=["de"])
__t.install()

_ = __t.gettext
