# Research Findings: Apple AR (Swift & RealityKit) Curriculum Architecture

## Current Understanding
Apple's AR ecosystem has completely shifted from legacy SceneKit/Metal wrappers to a unified **SwiftUI + RealityKit + ARKit** paradigm with native **Entity-Component-System (ECS)** architecture. Beginners must master 3D spatial math (`SIMD3<Float>`, Quaternions) and declarative UI before handling camera tracking sessions and raycasting.

## Key Synthesized Patterns
1. **Separation of Concerns:**
   - `ARKit`: World understanding, plane detection, face mesh tracking, image targets, LiDAR depth.
   - `RealityKit`: 3D rendering, physics simulation (`PhysicsBodyComponent`), collision detection (`CollisionComponent`), materials (`PBRMaterial`), and spatial sound (`SpatialAudioComponent`).
   - `SwiftUI`: App lifecycle, state management (`@Observable`, `@State`), flat 2D HUD/UI overlays, and `RealityView` container integration.
2. **Entity-Component-System (ECS) Shift:**
   - Entities hold no logic themselves; data resides in `Components` (`ModelComponent`, `CollisionComponent`, `InputTargetComponent`), and processing happens via `Systems`.
3. **Product-First Waterfall Sequence:**
   - Phase 0: Swift 6, SwiftUI & 3D Math Fundamentals
   - Phase 1: RealityKit Foundations & ECS Architecture
   - Phase 2: ARKit World Tracking, Raycasting & Gesture Interactions
   - Phase 3: Advanced AR (Face & Image Tracking, Spatial Audio, Occlusion)
   - Phase 4: Reality Composer Pro, Shader Graphs & Animations
   - Phase 5: Production Capstone Project (Furniture Placement / Interactive AR Game)

## Lessons & Constraints
- **Hardware Requirement:** Xcode Simulator cannot emulate camera tracking or LiDAR depth realistically; physical iOS/iPadOS devices (iPhone/iPad with A12+ or Pro LiDAR) are mandatory for Phase 2+.
- **Avoid Over-Engineering:** Game engines like Unity are only necessary for cross-platform titles (Meta Quest + iOS); for native Apple ecosystem, `RealityKit` provides superior frame-rate performance and seamless SwiftUI state binding.
