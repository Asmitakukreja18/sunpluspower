/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/**/*.html",
    "./frontend/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        "surface-bright": "#f8f9fb",
        "secondary-container": "#e2dfde",
        "tertiary": "#505b6d",
        "inverse-primary": "#ffb4ac",
        "on-primary-fixed": "#410003",
        "on-primary": "#ffffff",
        "error-container": "#ffdad6",
        "secondary-fixed": "#e5e2e1",
        "secondary": "#5f5e5e",
        "on-secondary-fixed-variant": "#474746",
        "primary-container": "#d9302f",
        "inverse-on-surface": "#f0f1f3",
        "on-background": "#191c1e",
        "inverse-surface": "#2e3132",
        "surface-variant": "#e1e2e4",
        "outline-variant": "#e4beb9",
        "surface-tint": "#bb171d",
        "on-tertiary-container": "#f9f9ff",
        "surface": "#f8f9fb",
        "on-secondary-container": "#636262",
        "secondary-fixed-dim": "#c8c6c5",
        "primary-fixed-dim": "#ffb4ac",
        "surface-container-low": "#f2f4f6",
        "on-error": "#ffffff",
        "surface-container-lowest": "#ffffff",
        "tertiary-container": "#697386",
        "primary": "#d9302f",
        "error": "#ba1a1a",
        "on-surface-variant": "#5b403d",
        "tertiary-fixed-dim": "#bdc7dc",
        "surface-container": "#edeef0",
        "on-secondary-fixed": "#1c1b1b",
        "on-secondary": "#ffffff",
        "surface-container-highest": "#e1e2e4",
        "on-tertiary-fixed-variant": "#3d4759",
        "on-surface": "#191c1e",
        "on-primary-fixed-variant": "#93000e",
        "background": "#f8f9fb",
        "surface-dim": "#d9dadc",
        "on-tertiary": "#ffffff",
        "tertiary-fixed": "#d9e3f9",
        "on-tertiary-fixed": "#121c2c",
        "primary-fixed": "#ffdad6",
        "on-primary-container": "#fff8f7",
        "outline": "#906f6c",
        "on-error-container": "#93000a",
        "surface-container-high": "#e7e8ea",
        "charcoal": "#191c1e",
        "navy-grey": "#2d3748"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "sm": "12px",
        "lg": "48px",
        "margin-desktop": "64px",
        "md": "24px",
        "margin-mobile": "16px",
        "base": "8px",
        "xs": "4px",
        "xl": "80px",
        "gutter": "24px"
      },
      fontFamily: {
        "label-bold": ["Inter", "sans-serif"],
        "headline-md": ["Inter", "sans-serif"],
        "display-lg": ["Inter", "sans-serif"],
        "body-md": ["Inter", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"],
        "headline-lg": ["Inter", "sans-serif"],
        "headline-lg-mobile": ["Inter", "sans-serif"],
        "label-sm": ["Inter", "sans-serif"]
      },
      fontSize: {
        "label-bold": ["14px", {"lineHeight": "20px", "letterSpacing": "0.05em", "fontWeight": "700"}],
        "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
        "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "800"}],
        "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
        "body-lg": ["18px", {"lineHeight": "28px", "fontWeight": "400"}],
        "headline-lg": ["32px", {"lineHeight": "40px", "fontWeight": "700"}],
        "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
        "label-sm": ["12px", {"lineHeight": "16px", "fontWeight": "500"}]
      }
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/container-queries")
  ],
}
