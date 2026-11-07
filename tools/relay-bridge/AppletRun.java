import java.applet.*; import java.awt.*; import java.net.*; import java.util.*;
public class AppletRun {
  public static void main(String[] a) throws Exception {
    URL base = new URL(a[0]); String cls = a[1];
    URLClassLoader cl = new URLClassLoader(new URL[]{new URL(base, "Graal.jar")});
    Applet ap = (Applet) cl.loadClass(cls).getDeclaredConstructor().newInstance();
    Frame f = new Frame(a.length > 2 ? a[2] : cls);
    ap.setStub(new AppletStub() {
      public boolean isActive() { return true; }
      public URL getDocumentBase() { return base; }
      public URL getCodeBase() { return base; }
      public String getParameter(String n) { return null; }
      public AppletContext getAppletContext() { return new AppletContext() {
        public AudioClip getAudioClip(URL u) { return null; }
        public Image getImage(URL u) { return Toolkit.getDefaultToolkit().getImage(u); }
        public Applet getApplet(String n) { return null; }
        public Enumeration<Applet> getApplets() { return Collections.enumeration(java.util.List.of(ap)); }
        public void showDocument(URL u) {} public void showDocument(URL u, String t) {}
        public void showStatus(String s) { System.out.println("status: " + s); }
        public void setStream(String k, java.io.InputStream s) {} public java.io.InputStream getStream(String k) { return null; }
        public Iterator<String> getStreamKeys() { return Collections.emptyIterator(); } }; }
      public void appletResize(int w, int h) {}
    });
    f.add(ap); f.setSize(530, 450); f.setVisible(true);
    ap.init(); ap.start();
  }
}
