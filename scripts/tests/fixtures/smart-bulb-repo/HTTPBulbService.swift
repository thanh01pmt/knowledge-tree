import Foundation

/// Service điều khiển đèn qua HTTP — gọi ESP32 REST API thật.
class HTTPBulbService: BulbServiceProtocol {
    private let baseURL: URL
    private let session: URLSession

    init(baseURL: URL = URL(string: "http://192.168.1.100")!) {
        self.baseURL = baseURL
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 5
        self.session = URLSession(configuration: config)
    }

    func getState() async throws -> BulbState {
        let url = baseURL.appendingPathComponent("api/state")
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(BulbState.self, from: data)
    }

    func setPower(_ isOn: Bool) async throws -> BulbState {
        let body = ["isOn": isOn]
        return try await post("/api/power", body: body)
    }

    func setBrightness(_ value: Int) async throws -> BulbState {
        let body = ["brightness": value]
        return try await post("/api/brightness", body: body)
    }

    func setColor(red: Double, green: Double, blue: Double) async throws -> BulbState {
        let body = ["red": red, "green": green, "blue": blue]
        return try await post("/api/color", body: body)
    }

    func setEffect(_ effect: BulbEffect) async throws -> BulbState {
        let body = ["effect": effect.rawValue]
        return try await post("/api/effect", body: body)
    }

    private func post(_ path: String, body: [String: Any]) async throws -> BulbState {
        let url = baseURL.appendingPathComponent(path)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode(BulbState.self, from: data)
    }
}
