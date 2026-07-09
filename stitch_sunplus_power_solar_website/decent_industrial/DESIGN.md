---
name: Decent Industrial
colors:
  surface: '#f8f9fb'
  surface-dim: '#d9dadc'
  surface-bright: '#f8f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#edeef0'
  surface-container-high: '#e7e8ea'
  surface-container-highest: '#e1e2e4'
  on-surface: '#191c1e'
  on-surface-variant: '#5b403d'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f3'
  outline: '#906f6c'
  outline-variant: '#e4beb9'
  surface-tint: '#bb171d'
  primary: '#b5111a'
  on-primary: '#ffffff'
  primary-container: '#d9302f'
  on-primary-container: '#fff8f7'
  inverse-primary: '#ffb4ac'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#505b6d'
  on-tertiary: '#ffffff'
  tertiary-container: '#697386'
  on-tertiary-container: '#f9f9ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb4ac'
  on-primary-fixed: '#410003'
  on-primary-fixed-variant: '#93000e'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#d9e3f9'
  tertiary-fixed-dim: '#bdc7dc'
  on-tertiary-fixed: '#121c2c'
  on-tertiary-fixed-variant: '#3d4759'
  background: '#f8f9fb'
  on-background: '#191c1e'
  surface-variant: '#e1e2e4'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style
The design system moves away from high-intensity marketing toward an "engineering-grade" aesthetic. It prioritizes reliability, precision, and industrial trust. The brand personality is authoritative yet understated, reflecting the stability of power infrastructure. 

The style is **Corporate Modern** with a lean toward **Minimalism**. It utilizes a structured hierarchy where white space is treated as a functional tool for clarity rather than just an aesthetic choice. Visual weight is shifted from vibrant color to solid, structural neutrals, positioning the product as a professional utility.

## Colors
The palette is anchored by **Charcoal (#1a1a1a)** and **Navy Grey (#2d3748)**. These colors serve as the primary structural anchors for global navigation, headers, and footers, providing a sense of "heavy-duty" stability.

The **Primary Red (#d9302f)** is strictly reserved for strategic accents. It should be used for primary calls to action, critical status alerts, and the brand mark. It must never dominate the layout or be used for large surface areas.

**Section Backgrounds** should alternate between clean white and **Light Grey (#f8f9fb)** to create logical grouping without the need for heavy borders.

## Typography
The design system utilizes **Inter** exclusively to maintain a systematic, utilitarian feel. The type scale is optimized for legibility in technical contexts. 

Headlines use tighter letter spacing and heavier weights to convey strength, while body text maintains generous line heights for readability. Uppercase labels are used for technical metadata and secondary navigation elements to provide a clear distinction from narrative content.

## Layout & Spacing
This design system follows a **Fixed Grid** model for desktop, centered within the viewport. The layout is built on an 8px rhythmic scale.

- **Desktop:** 12-column grid with 24px gutters.
- **Tablet:** 8-column grid with 20px gutters.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

Spacing between major sections should be generous (80px - 120px) to reinforce the "industrial-trust" through clarity and lack of clutter. Components should use consistent internal padding based on multiples of 8px.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** rather than heavy shadows. The background uses light grey (#f8f9fb) to define specific content regions, while cards and interactive elements sit on pure white surfaces.

Where elevation is required for interactivity (e.g., dropdowns, modals), use **Low-Contrast Outlines** (1px solid #e2e8f0) paired with a very subtle, neutral ambient shadow (0px 4px 12px rgba(0,0,0,0.05)). This keeps the interface feeling flat, technical, and precise.

## Shapes
In alignment with the engineering focus, the design system utilizes a consistent **8px (0.5rem)** corner radius for buttons, input fields, and cards. This provides a balance between approachable modern design and the structured rigidity of industrial hardware. Smaller components like checkboxes or tags should scale down to 4px rounding to maintain visual harmony.

## Components
- **Buttons:** Primary buttons use the Primary Red (#d9302f) with white text. Secondary buttons use a Navy Grey (#2d3748) outline with a subtle hover state.
- **Input Fields:** Use a 1px solid border in light grey, shifting to Navy Grey on focus. Labels should be small, bold, and placed above the field.
- **Cards:** Cards should be flat with a 1px border (#e2e8f0). Use white backgrounds on light grey section backgrounds.
- **Status Indicators:** Use small, solid circular dots. Red is strictly for "Critical/Error," while Navy Grey or Dark Green is used for "Standard/Active" operations.
- **Lists:** Technical data should be displayed in structured lists with subtle horizontal dividers and monospaced-style alignment for numerical values.
- **Chips/Tags:** Small, rectangular with 4px rounding, using light grey backgrounds and dark grey text to stay unobtrusive.