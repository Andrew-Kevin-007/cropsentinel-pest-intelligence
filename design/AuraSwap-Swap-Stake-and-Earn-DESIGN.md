---
version: "alpha"
name: "AuraSwap — Swap, Stake, and Earn"
description: "Auraswap Swap Dashboard Section is designed for demonstrating application workflows and interface hierarchy. Key features include clear information density, modular panels, and interface rhythm. It is suitable for product showcases, admin panels, and analytics experiences."
colors:
  primary: "#5FE3B0"
  secondary: "#A88BFF"
  tertiary: "#62BFEA"
  neutral: "#E7EEF7"
  background: "#E7EEF7"
  surface: "#5FE3B0"
  text-primary: "#E7EEF7"
  text-secondary: "#5FE3B0"
  border: "#E5E7EB"
  accent: "#5FE3B0"
typography:
  display-lg:
    fontFamily: "Gloock"
    fontSize: "64.172px"
    fontWeight: 400
    lineHeight: "65.4554px"
    letterSpacing: "-0.022em"
  body-md:
    fontFamily: "IBM Plex Mono"
    fontSize: "12.5px"
    fontWeight: 300
    lineHeight: "23.75px"
  label-md:
    fontFamily: "IBM Plex Mono"
    fontSize: "10.5px"
    fontWeight: 500
    lineHeight: "15.75px"
    letterSpacing: "1.89px"
    textTransform: "uppercase"
rounded:
  full: "9999px"
spacing:
  base: "4px"
  sm: "3.85px"
  md: "4px"
  lg: "4.54px"
  xl: "8px"
  gap: "8px"
components:
  button-primary:
    textColor: "#04070E"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "14px"
  button-secondary:
    textColor: "{colors.neutral}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: "14px"
  card:
    rounded: "0px"
    padding: "24px"
---

## Overview

- **Composition cues:**
  - Layout: Grid
  - Content Width: Full Bleed
  - Framing: Glassy
  - Grid: Strong

## Colors

The color system uses light mode with #5FE3B0 as the main accent and #E7EEF7 as the neutral foundation.

- **Primary (#5FE3B0):** Main accent and emphasis color.
- **Secondary (#A88BFF):** Supporting accent for secondary emphasis.
- **Tertiary (#62BFEA):** Reserved accent for supporting contrast moments.
- **Neutral (#E7EEF7):** Neutral foundation for backgrounds, surfaces, and supporting chrome.

- **Usage:** Background: #E7EEF7; Surface: #5FE3B0; Text Primary: #E7EEF7; Text Secondary: #5FE3B0; Border: #E5E7EB; Accent: #5FE3B0

## Typography

Typography pairs Gloock for display hierarchy with IBM Plex Mono for supporting content and interface copy.

- **Display (`display-lg`):** Gloock, 64.172px, weight 400, line-height 65.4554px, letter-spacing -0.022em.
- **Body (`body-md`):** IBM Plex Mono, 12.5px, weight 300, line-height 23.75px.
- **Labels (`label-md`):** IBM Plex Mono, 10.5px, weight 500, line-height 15.75px, letter-spacing 1.89px, uppercase.

## Layout

Layout follows a grid composition with reusable spacing tokens. Preserve the grid, full bleed structural frame before changing ornament or component styling. Use 4px as the base rhythm and let larger gaps step up from that cadence instead of introducing unrelated spacing values.

Treat the page as a grid / full bleed composition, and keep that framing stable when adding or remixing sections.

- **Layout type:** Grid
- **Content width:** Full Bleed
- **Base unit:** 4px
- **Scale:** 3.85px, 4px, 4.54px, 8px, 10px, 12px, 14px, 14.12px
- **Gaps:** 8px, 10px, 12px, 16px

## Elevation & Depth

Depth is communicated through glass, border contrast, and reusable shadow or blur treatments. Keep those recipes consistent across hero panels, cards, and controls so the page reads as one material system.

Surfaces should read as glass first, with borders, shadows, and blur only reinforcing that material choice.

- **Surface style:** Glass
- **Borders:** 0.8px #E5E7EB; 0.8px #5FE3B0; 0.8px #A88BFF
- **Shadows:** rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(95, 227, 176, 0.9) 0px 0px 10px 0px; rgba(76, 203, 155, 0.28) 0px 6px 20px 0px, rgba(255, 255, 255, 0.65) 0px 1px 1px 0px inset; rgba(0, 0, 0, 0.9) 0px 30px 80px -30px, rgba(231, 238, 247, 0.06) 0px 1px 0px 0px inset
- **Blur:** 14px

### Techniques
- **Gradient border shell:** Use a thin gradient border shell around the main card. Wrap the surface in an outer shell with 0px padding and a 0px radius. Drive the shell with linear-gradient(rgba(4, 7, 14, 0.52), rgba(0, 0, 0, 0)) so the edge reads like premium depth instead of a flat stroke. Keep the actual stroke understated so the gradient shell remains the hero edge treatment. Inset the real content surface inside the wrapper with a slightly smaller radius so the gradient only appears as a hairline frame.

## Shapes

Shapes rely on a tight radius system anchored by 16px and scaled across cards, buttons, and supporting surfaces. Icon geometry should stay compatible with that soft-to-controlled silhouette.

Use the radius family intentionally: larger surfaces can open up, but controls and badges should stay within the same rounded DNA instead of inventing sharper or pill-only exceptions.

- **Corner radii:** 16px, 9999px
- **Icon treatment:** Linear
- **Icon sets:** Solar

## Components

Anchor interactions to the detected button styles. Reuse the existing card surface recipe for content blocks.

### Buttons
- **Primary:** text #04070E, radius 9999px, padding 14px, border 0px solid rgb(229, 231, 235).
- **Secondary:** text #E7EEF7, radius 9999px, padding 14px, border 0.8px solid rgb(229, 231, 235).

### Cards and Surfaces
- **Card surface:** radius 0px, padding 24px, shadow none.

### Iconography
- **Treatment:** Linear.
- **Sets:** Solar.

## Do's and Don'ts

Use these constraints to keep future generations aligned with the current system instead of drifting into adjacent styles.

### Do
- Do use the primary palette as the main accent for emphasis and action states.
- Do keep spacing aligned to the detected 4px rhythm.
- Do reuse the Glass surface treatment consistently across cards and controls.
- Do keep corner radii within the detected 16px, 9999px family.

### Don't
- Don't introduce extra accent colors outside the core palette roles unless the page needs a new semantic state.
- Don't mix unrelated shadow or blur recipes that break the current depth system.
- Don't exceed the detected expressive motion intensity without a deliberate reason.

## Motion

Motion feels expressive but remains focused on interface, text, and layout transitions. Timing clusters around 350ms and 900ms. Easing favors ease and 1). Hover behavior focuses on shadow and stroke changes.

**Motion Level:** expressive

**Durations:** 350ms, 900ms, 800ms, 1000ms, 150ms, 1150ms

**Easings:** ease, 1), 1, cubic-bezier(0.16, 0.3, cubic-bezier(0.19

**Hover Patterns:** shadow, stroke, text

## WebGL

Reconstruct the graphics as a full-bleed background field using webgl, renderer, antialias, dpr clamp, custom shaders. The effect should read as technical, meditative, and atmospheric: dot-matrix particle field with black and sparse spacing. Build it from dot particles + soft depth fade so the effect reads clearly. Animate it as slow breathing pulse. Interaction can react to the pointer, but only as a subtle drift. Preserve reduced motion + dom fallback.

**Id:** webgl

**Label:** WebGL

**Stack:** ThreeJS, WebGL

**Insights:**
  - **Scene:**
    - **Value:** Full-bleed background field
  - **Effect:**
    - **Value:** Dot-matrix particle field
  - **Primitives:**
    - **Value:** Dot particles + soft depth fade
  - **Motion:**
    - **Value:** Slow breathing pulse
  - **Interaction:**
    - **Value:** Pointer-reactive drift
  - **Render:**
    - **Value:** WebGL, Renderer, antialias, DPR clamp, custom shaders

**Techniques:** Dot matrix, Breathing pulse, Pointer parallax, Shader gradients, Noise fields

**Code Evidence:**
  - **HTML reference:**
    - **Language:** html
    - **Snippet:**
      ```html
      <!-- WebGL aurora sky -->
      <div class="fixed inset-0 z-0 pointer-events-none">
        <canvas id="sky" class="w-full h-full block"></canvas>
      </div>
      ```
  - **JS reference:**
    - **Language:** js
    - **Snippet:**
      ```
      const d = new Date();
          utc.textContent = 'UTC ' + String(d.getUTCHours()).padStart(2,'0') + ':' +
                            String(d.getUTCMinutes()).padStart(2,'0') + ':' +
                            String(d.getUTCSeconds()).padStart(2,'0');
        };
        tick(); setInterval(tick, 1000);

        /* ---------- 3. 48h storm strip ---------- */
      …
      ```
  - **Animation loop:**
    - **Language:** js
    - **Snippet:**
      ```
      utc.textContent = 'UTC ' + String(d.getUTCHours()).padStart(2,'0') + ':' +
                          String(d.getUTCMinutes()).padStart(2,'0') + ':' +
                          String(d.getUTCSeconds()).padStart(2,'0');
      };
      tick(); setInterval(tick, 1000);

      /* ---------- 3. 48h storm strip ---------- */
      const strip = document.getElementById('strip');
      …
      ```

## ThreeJS

Reconstruct the Three.js layer as a full-bleed background field with layered spatial depth that feels technical. Use antialias, dpr clamp renderer settings, orthographic projection, plane geometry, shadermaterial materials, and ambient + key + rim lighting. Motion should read as slow orbital drift, with reduced motion + non-3d fallback.

**Id:** threejs

**Label:** ThreeJS

**Stack:** ThreeJS, WebGL

**Insights:**
  - **Scene:**
    - **Value:** Full-bleed background field with layered spatial depth
  - **Render:**
    - **Value:** antialias, DPR clamp
  - **Camera:**
    - **Value:** Orthographic projection
  - **Lighting:**
    - **Value:** ambient + key + rim
  - **Materials:**
    - **Value:** ShaderMaterial
  - **Geometry:**
    - **Value:** plane
  - **Motion:**
    - **Value:** Slow orbital drift

**Techniques:** Shader materials, Timeline beats, antialias, DPR clamp, Reduced motion + non-3D fallback

**Code Evidence:**
  - **HTML reference:**
    - **Language:** html
    - **Snippet:**
      ```html
      <!-- WebGL aurora sky -->
      <div class="fixed inset-0 z-0 pointer-events-none">
        <canvas id="sky" class="w-full h-full block"></canvas>
      </div>
      ```
  - **JS reference:**
    - **Language:** js
    - **Snippet:**
      ```
      const d = new Date();
          utc.textContent = 'UTC ' + String(d.getUTCHours()).padStart(2,'0') + ':' +
                            String(d.getUTCMinutes()).padStart(2,'0') + ':' +
                            String(d.getUTCSeconds()).padStart(2,'0');
        };
        tick(); setInterval(tick, 1000);

        /* ---------- 3. 48h storm strip ---------- */
      …
      ```
  - **Animation loop:**
    - **Language:** js
    - **Snippet:**
      ```
      utc.textContent = 'UTC ' + String(d.getUTCHours()).padStart(2,'0') + ':' +
                          String(d.getUTCMinutes()).padStart(2,'0') + ':' +
                          String(d.getUTCSeconds()).padStart(2,'0');
      };
      tick(); setInterval(tick, 1000);

      /* ---------- 3. 48h storm strip ---------- */
      const strip = document.getElementById('strip');
      …
      ```
