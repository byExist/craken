# Deprecated plugins

Plugins retired from the craken marketplace catalog. The code is kept here for reference, but these plugins are **removed from the marketplace** and can no longer be installed via `/plugin install …@craken`.

| Plugin | Reason |
| --- | --- |
| [glyphfit](glyphfit/) | The platform's native-resolution cap already downsizes large images, so a text-aware shrink only saves tokens in a narrow window — small, cropped, or repeatedly-read images. For most screenshots, reading the original costs the same, making the shrink a no-op. |
