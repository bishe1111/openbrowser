import gi
gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, WebKit, Gio, GdkPixbuf
import os

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("openbrowser")
        self.set_default_size(1024, 768)
        
        
        icon_path = os.path.join(os.path.dirname(__file__), "ob.png")
        if os.path.exists(icon_path):
            try:
                
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 64, 64)
                self.set_icon(pixbuf)
            except:
                print("آیکون بارگذاری نشد!")
        else:
            
            self.set_icon_name("web-browser")

        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(main_box)
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        toolbar.set_margin_start(5)
        toolbar.set_margin_end(5)
        toolbar.set_margin_top(5)
        toolbar.set_margin_bottom(5)
        main_box.append(toolbar)

        
        self.back_btn = Gtk.Button.new_with_label("🦖")
        self.back_btn.connect("clicked", self.go_back)
        toolbar.append(self.back_btn)

        self.forward_btn = Gtk.Button.new_with_label("✈️")
        self.forward_btn.connect("clicked", self.go_forward)
        toolbar.append(self.forward_btn)

        reload_btn = Gtk.Button.new_with_label("🦕")
        reload_btn.connect("clicked", self.reload_page)
        toolbar.append(reload_btn)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_hexpand(True)
        self.url_entry.connect("activate", self.on_url_enter)
        toolbar.append(self.url_entry)

        go_btn = Gtk.Button.new_with_label("Go")
        go_btn.connect("clicked", self.on_url_enter)
        toolbar.append(go_btn)

        # WebView
        self.webview = WebKit.WebView()
        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.connect("notify::uri", self.on_uri_changed)
        self.webview.load_uri("https://google.com")
        main_box.append(self.webview)

    def go_back(self, button):
        self.webview.go_back()

    def go_forward(self, button):
        self.webview.go_forward()

    def reload_page(self, button):
        self.webview.reload()

    def on_url_enter(self, widget):
        url = self.url_entry.get_text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.webview.load_uri(url)

    def on_load_changed(self, webview, event):
        self.back_btn.set_sensitive(webview.can_go_back())
        self.forward_btn.set_sensitive(webview.can_go_forward())

    def on_uri_chang(self, webview, prop):
        self.url_entry.set_text(webview.get_uri() or "")

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.mybrowser")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = MainWindow(app)
        win.present()

if __name__ == "__main__":
    app = MyApp()
    app.run(None)
