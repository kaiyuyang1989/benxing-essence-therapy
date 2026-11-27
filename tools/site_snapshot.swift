import AppKit
import WebKit

let address = URL(string: CommandLine.arguments[1])!
let width = Int(CommandLine.arguments[2])!
let height = Int(CommandLine.arguments[3])!
let output = URL(fileURLWithPath: CommandLine.arguments[4])

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)

final class Capture: NSObject, WKNavigationDelegate {
    let output: URL
    let width: Int
    let height: Int
    init(output: URL, width: Int, height: Int) {
        self.output = output
        self.width = width
        self.height = height
    }
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            let configuration = WKSnapshotConfiguration()
            configuration.rect = CGRect(x: 0, y: 0, width: self.width, height: self.height)
            configuration.snapshotWidth = NSNumber(value: self.width)
            webView.takeSnapshot(with: configuration) { image, error in
                if let image = image, let tiff = image.tiffRepresentation,
                   let bitmap = NSBitmapImageRep(data: tiff),
                   let png = bitmap.representation(using: .png, properties: [:]) {
                    try? png.write(to: self.output)
                    print(self.output.path)
                } else {
                    fputs("Snapshot failed: \(String(describing: error))\n", stderr)
                }
                fflush(stdout)
                exit(0)
            }
        }
    }
}

let frame = NSRect(x: -2200, y: -2200, width: width, height: height)
let window = NSWindow(contentRect: frame, styleMask: [.borderless], backing: .buffered, defer: false)
let webView = WKWebView(frame: NSRect(x: 0, y: 0, width: width, height: height))
let capture = Capture(output: output, width: width, height: height)
webView.navigationDelegate = capture
window.contentView = webView
window.orderFront(nil)
webView.load(URLRequest(url: address))
DispatchQueue.main.asyncAfter(deadline: .now() + 18) { exit(2) }
app.run()
