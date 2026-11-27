import AVFoundation
import AppKit

let input = CommandLine.arguments[1]
let output = CommandLine.arguments[2]
let asset = AVURLAsset(url: URL(fileURLWithPath: input))
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
for second in [2.0, 15.0, 30.0, 45.0, 52.0] {
    let requested = CMTime(seconds: second, preferredTimescale: 600)
    let image = try generator.copyCGImage(at: requested, actualTime: nil)
    let rep = NSBitmapImageRep(cgImage: image)
    let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.82])!
    try data.write(to: URL(fileURLWithPath: "\(output)-\(Int(second)).jpg"))
}
