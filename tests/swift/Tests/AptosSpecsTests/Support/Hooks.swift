import Foundation

/// Helper functions for tests

/// Convert hex string to bytes
func hexToBytes(_ hex: String) -> [UInt8]? {
    var hexString = hex
    if hexString.hasPrefix("0x") {
        hexString = String(hexString.dropFirst(2))
    }
    
    guard hexString.count % 2 == 0 else { return nil }
    
    var bytes: [UInt8] = []
    var index = hexString.startIndex
    
    while index < hexString.endIndex {
        let nextIndex = hexString.index(index, offsetBy: 2)
        guard let byte = UInt8(hexString[index..<nextIndex], radix: 16) else {
            return nil
        }
        bytes.append(byte)
        index = nextIndex
    }
    
    return bytes
}

/// Convert bytes to hex string
func bytesToHex(_ bytes: [UInt8], prefix: Bool = true) -> String {
    let hex = bytes.map { String(format: "%02x", $0) }.joined()
    return prefix ? "0x" + hex : hex
}
