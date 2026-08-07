import SwiftUI

struct ContentView: View {
    @State private var bulbState = BulbState()
    @State private var selectedEffect: BulbEffect = .none
    private let service = MockBulbService()

    var body: some View {
        VStack(spacing: 20) {
            // Trạng thái đèn
            Circle()
                .fill(bulbState.isOn ? Color(red: bulbState.red, green: bulbState.green, blue: bulbState.blue) : .gray)
                .frame(width: 120, height: 120)
                .opacity(bulbState.isOn ? Double(bulbState.brightness) / 100.0 : 0.2)

            // Bật/tắt
            Toggle("Bật đèn", isOn: Binding(
                get: { bulbState.isOn },
                set: { newValue in
                    Task { bulbState = try! await service.setPower(newValue) }
                }
            ))
            .padding(.horizontal, 40)

            // Độ sáng
            VStack {
                Text("Độ sáng: \(bulbState.brightness)")
                Slider(value: Binding(
                    get: { Double(bulbState.brightness) },
                    set: { newValue in
                        Task { bulbState = try! await service.setBrightness(Int(newValue)) }
                    }
                ), in: 0...100)
            }
            .padding(.horizontal, 40)

            // Màu sắc
            ColorPicker("Chọn màu", selection: Binding(
                get: { Color(red: bulbState.red, green: bulbState.green, blue: bulbState.blue) },
                set: { color in
                    let uiColor = UIColor(color)
                    var r: CGFloat = 0, g: CGFloat = 0, b: CGFloat = 0
                    uiColor.getRed(&r, green: &g, blue: &b, alpha: nil)
                    Task { bulbState = try! await service.setColor(red: Double(r), green: Double(g), blue: Double(b)) }
                }
            ))
            .padding(.horizontal, 40)

            // Hiệu ứng
            Picker("Hiệu ứng", selection: $selectedEffect) {
                ForEach(BulbEffect.allCases) { effect in
                    Text(effect.displayName).tag(effect)
                }
            }
            .onChange(of: selectedEffect) { newValue in
                Task { bulbState = try! await service.setEffect(newValue) }
            }
            .padding(.horizontal, 40)

            Spacer()
        }
        .padding()
        .task {
            bulbState = try! await service.getState()
        }
    }
}
