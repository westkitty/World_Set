# World_Set Forensic Uplift Ledger

Baseline: `3bfc7504ada6` on `main`. This ledger reconciles the substantive uplift introduced by `63c8f70` with the current forensic repair pass. Each mandatory item has one primary category only. `VERIFIED` means direct behavioral or production-path evidence exists; `IMPLEMENTED` means executable implementation exists and passed applicable static/integration gates but was not individually exercised visually.

## Corrections
- CORR-01 — Orientation-safe `teleportToView` synchronization — IMPLEMENTED.
- CORR-02 — Expansion-world collision bounds — IMPLEMENTED.
- CORR-03 — Expansion-biome footstep profiles — IMPLEMENTED.
- CORR-04 — Expansion lore entries integrated with the runtime — IMPLEMENTED.
- CORR-05 — Tropical-atoll `atollGeo` runtime crash repaired — VERIFIED in Chrome boot.
- CORR-06 — Undefined `currentViewMode` world-routing crash repaired — VERIFIED across all 16 destinations.
- CORR-07 — Settings/controls ghost modals repaired with an actual `.active` display path — VERIFIED at 390px.
- CORR-08 — Duplicate flashlight keyboard toggle removed — VERIFIED by singular production caller.
- CORR-09 — Scanner no longer attempts to parse narrative lore coordinates as world-space positions — VERIFIED.
- CORR-10 — Settings/session persistence now has load, apply, save, autosave, and resume paths — VERIFIED across reload.

## UI/UX — 20 required
| ID | Distinct improvement | Evidence | State |
| --- | --- | --- | --- |
| UIUX-01 | Dynamic compass tape | `updateCompassHUD` + compass HUD | IMPLEMENTED |
| UIUX-02 | Tactical minimap/radar | `updateRadarHUD` + radar canvas | IMPLEMENTED |
| UIUX-03 | Sprint stamina meter | stamina bar + `updateStamina` | IMPLEMENTED |
| UIUX-04 | Live coordinate breadcrumb | `updateCoordsBreadcrumb` | IMPLEMENTED |
| UIUX-05 | Biome entry title banner | `showBiomeTitleBanner` | IMPLEMENTED |
| UIUX-06 | Stacking severity-aware toast feedback | `showToast` + toast container | IMPLEMENTED |
| UIUX-07 | Per-biome environmental visor treatment | visor overlay state system | IMPLEMENTED |
| UIUX-08 | Flashlight battery status gauge | flashlight badge/bar | IMPLEMENTED |
| UIUX-09 | Context-sensitive interaction reticle | interaction prompt/reticle updates | IMPLEMENTED |
| UIUX-10 | Structured settings dialog | settings groups, sliders, toggles | VERIFIED |
| UIUX-11 | Keyboard/control field manual | controls modal/key badges | VERIFIED |
| UIUX-12 | Performance telemetry graph HUD | telemetry canvas/stats | IMPLEMENTED |
| UIUX-13 | Dedicated Codex header access | header Codex control | IMPLEMENTED |
| UIUX-14 | Dedicated Settings header access | header Settings control | IMPLEMENTED |
| UIUX-15 | Dedicated Controls header access | header Controls control | IMPLEMENTED |
| UIUX-16 | Stored settings hydrate into visible controls/readouts | `hydrateSettingsControls` | VERIFIED |
| UIUX-17 | Mobile header contains navigation in a touch-scroll lane | 390px overflow test | VERIFIED |
| UIUX-18 | Active-world HUD/portal color synchronization | `dialGateway` UI theming | IMPLEMENTED |
| UIUX-19 | Mobile quick-dial width compaction | `@media (max-width:540px)` | VERIFIED |
| UIUX-20 | Mobile radial launcher scaling without page overflow | radial media rule + 390px test | VERIFIED |

## Gameplay / interaction — 20 required
| ID | Distinct improvement | Evidence | State |
| --- | --- | --- | --- |
| GAME-01 | Central movement collision resolver | `resolvePlayerMovement` | IMPLEMENTED |
| GAME-02 | Reusable AABB collision primitive | `isPointInAABB` | IMPLEMENTED |
| GAME-03 | Reusable cylindrical collision primitive | `isPointInCylinder` | IMPLEMENTED |
| GAME-04 | Sprint stamina drain and recovery | `updateStamina` | IMPLEMENTED |
| GAME-05 | World-specific gravity profiles | `PLANETARY_GRAVITY` | IMPLEMENTED |
| GAME-06 | Sprint speed changes actual locomotion | movement speed multiplier | IMPLEMENTED |
| GAME-07 | Flashlight battery drain and automatic shutdown | `updateFlashlightTorch` | IMPLEMENTED |
| GAME-08 | Jump impulse and landing physics | `triggerPlayerJump` / `updateJumpPhysics` | IMPLEMENTED |
| GAME-09 | Crouch locomotion stance | `toggleCrouch` | IMPLEMENTED |
| GAME-10 | Motion-coupled walking head bob | `calculateHeadBob` / render loop | IMPLEMENTED |
| GAME-11 | Surface-aware procedural footsteps | `playSurfaceFootstep` | IMPLEMENTED |
| GAME-12 | Collision coverage for all ten expansion worlds | `isPlayerPositionBlocked` branches | IMPLEMENTED |
| GAME-13 | Thermal vision interaction mode | `cycleVisionMode` | IMPLEMENTED |
| GAME-14 | Night-vision interaction mode | `cycleVisionMode` | IMPLEMENTED |
| GAME-15 | World transitions reset transient zero-G locomotion state | `switchActiveEnvironment` reset | IMPLEMENTED |
| GAME-16 | Discovery milestones tied to biome entry | `checkBiomeDiscovery` | IMPLEMENTED |
| GAME-17 | Analog gamepad locomotion/look | `GamepadAPISubsystem.poll` | IMPLEMENTED |
| GAME-18 | Edge-triggered gamepad actions | `pressedOnce` state | VERIFIED |
| GAME-19 | Camera trauma/shake response | `CameraTrauma.update` | IMPLEMENTED |
| GAME-20 | Per-destination interaction state survives all 16 world switches | full world-transition sweep | VERIFIED |

## Backend / technical — 20 required
| ID | Distinct improvement | Evidence | State |
| --- | --- | --- | --- |
| BACK-01 | Safe namespaced local-storage wrapper | `LocalStorageEngine` | VERIFIED |
| BACK-02 | Biome procedural soundscape controller | `ProceduralSoundscape` production caller | VERIFIED |
| BACK-03 | Reusable temporary Vector3 pool | `StaticObjectPool` production caller | VERIFIED |
| BACK-04 | Three.js hierarchy/resource disposal | `AssetDisposalManager` codex caller | VERIFIED |
| BACK-05 | Clamped frame-delta governor used by render loop | `FrameRateGovernor.getClampedDelta` caller | VERIFIED |
| BACK-06 | World-to-screen coordinate transformer | scanner projection caller | VERIFIED |
| BACK-07 | Renderer/FPS telemetry logger | render-loop caller | VERIFIED |
| BACK-08 | Master/ambience/SFX mixer bus | settings/audio callers | VERIFIED |
| BACK-09 | WebGL context-loss boundary | live renderer canvas listener | VERIFIED |
| BACK-10 | Honest renderer capability profile | live `renderer.capabilities` detection | VERIFIED |
| BACK-11 | World-scoped spatial hash index | scanner `queryNear` path | VERIFIED |
| BACK-12 | Unified semantic input action bus | keyboard + gamepad callers | VERIFIED |
| BACK-13 | Adaptive update-budget scheduler | proximity + telemetry channels | VERIFIED |
| BACK-14 | Runtime memory-status monitor | telemetry HUD caller | VERIFIED |
| BACK-15 | Gamepad API subsystem | per-frame polling caller | VERIFIED |
| BACK-16 | Automatic quality degradation | 1Hz FPS decision caller | VERIFIED |
| BACK-17 | URL world/view router | transition caller + 16-world sweep | VERIFIED |
| BACK-18 | World event publisher/subscriber bus | `world:entered` emit/listen path | VERIFIED |
| BACK-19 | Deduplicated critical-asset warmup queue | scene-init caller | VERIFIED |
| BACK-20 | Session snapshot restore/apply/autosave engine | reload round-trip | VERIFIED |

## Quality of life — 20 required
| ID | Distinct improvement | Evidence | State |
| --- | --- | --- | --- |
| QOL-01 | Previous-biome shortcut `[Z]` | global input hook | IMPLEMENTED |
| QOL-02 | Next-biome shortcut `[X]` | global input hook | IMPLEMENTED |
| QOL-03 | Emergency origin recall `[Home]` | portal recall handler | IMPLEMENTED |
| QOL-04 | Hold-right-click telescope zoom | mouse handlers | IMPLEMENTED |
| QOL-05 | Codex shortcut `[M]` | semantic input action | IMPLEMENTED |
| QOL-06 | Scanner shortcut `[Q]` | semantic input action | IMPLEMENTED |
| QOL-07 | Photo-mode shortcut `[P]` | semantic input action | IMPLEMENTED |
| QOL-08 | Telemetry shortcut `[T]` | semantic input action | IMPLEMENTED |
| QOL-09 | Settings shortcut `[O]` | semantic input action | IMPLEMENTED |
| QOL-10 | Control-manual shortcut `[?]` | global input hook | IMPLEMENTED |
| QOL-11 | Priority Escape closure for active utilities | modal close order | IMPLEMENTED |
| QOL-12 | One-action coordinate copy | `copyCoordinatesToClipboard` | IMPLEMENTED |
| QOL-13 | Graphics/audio/control preferences persist | reload test | VERIFIED |
| QOL-14 | Session autosave every 15 seconds and on page hide | `initAutosave` | VERIFIED |
| QOL-15 | Session resumes world, camera position and look direction | reload round-trip | VERIFIED |
| QOL-16 | Hidden-tab audio suspend/resume | visibility handler | IMPLEMENTED |
| QOL-17 | Debounced resize handling | resize timer | IMPLEMENTED |
| QOL-18 | Single-action settings reset | `resetUserSettings` | IMPLEMENTED |
| QOL-19 | Deep-link world/view state in URL hash | `UrlRouterEngine` | VERIFIED |
| QOL-20 | Telemetry visibility preference persists | control settings reload | VERIFIED |

## Features — 20 required
| ID | Distinct improvement | Evidence | State |
| --- | --- | --- | --- |
| FEAT-01 | Director photo/free-camera mode | `enterPhotoMode` | IMPLEMENTED |
| FEAT-02 | PNG screenshot export | `capturePhotoScreenshot` | IMPLEMENTED |
| FEAT-03 | Photo filter cycling | `cyclePhotoFilter` | IMPLEMENTED |
| FEAT-04 | Photo lens/FOV cycling | `cyclePhotoFOV` | IMPLEMENTED |
| FEAT-05 | Rule-of-thirds photo composition grid | `togglePhotoGrid` | IMPLEMENTED |
| FEAT-06 | 360-degree panorama viewer | `initPanoramaViewer` | IMPLEMENTED |
| FEAT-07 | Tactical AR sonar scanning | `triggerARScannerPulse` / scanner runtime | VERIFIED |
| FEAT-08 | Searchable lore Codex | `filterCodexEntries` | IMPLEMENTED |
| FEAT-09 | Procedural 3D Codex object previews | `buildCodex3DModel` | VERIFIED |
| FEAT-10 | Touch-control mode for mobile exploration | virtual joystick handlers | IMPLEMENTED |
| FEAT-11 | Explorable volcanic caldera world | `buildVolcanoWorld` | VERIFIED |
| FEAT-12 | Explorable bioluminescent world | `buildBiolumWorld` | VERIFIED |
| FEAT-13 | Explorable abyssal citadel world | `buildAbyssWorld` | VERIFIED |
| FEAT-14 | Explorable Mars world | `buildMarsWorld` | VERIFIED |
| FEAT-15 | Explorable crystal world | `buildCrystalWorld` | VERIFIED |
| FEAT-16 | Explorable swamp world | `buildSwampWorld` | VERIFIED |
| FEAT-17 | Explorable cavern world | `buildCavernWorld` | VERIFIED |
| FEAT-18 | Explorable acid-industrial world | `buildAcidWorld` | VERIFIED |
| FEAT-19 | Explorable taiga world | `buildTaigaWorld` | VERIFIED |
| FEAT-20 | Explorable sky-island world | `buildSkyWorld` | VERIFIED |

## WOW-ME — additional flagship
| ID | Capability | Evidence | State |
| --- | --- | --- | --- |
| WOW-01 | Context-aware Field Intelligence Loop: world-scoped AR scan locks a real interactable POI, projects it into the HUD, and hands the exact target directly into the searchable 3D Codex via the semantic input bus. | Chrome runtime locked `base_telemetry`; Codex opened on the identical title; all 16 worlds rebuild isolated POI indexes. | VERIFIED |

## Count gate
- UI/UX: **20 / 20**
- Gameplay / interaction: **20 / 20**
- Backend / technical: **20 / 20**
- Quality of life: **20 / 20**
- Features: **20 / 20**
- WOW-ME: **1 / 1 additional**

Count integrity rule: each row has one primary category; no row is repeated under another mandatory category.