# Mobile Responsive CSS Developer Reference

## Quick Reference: Breakpoints

```css
/* Mobile First Approach - Stack your breakpoints */

/* 1. BASE STYLES (applies to ALL devices) */
.my-class {
  padding: 1rem;
  font-size: 1rem;
}

/* 2. MOBILE STYLES (small phones < 480px) */
@media (max-width: 479px) {
  .my-class {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
}

/* 3. TABLET STYLES (480px - 768px) */
@media (min-width: 480px) and (max-width: 767px) {
  .my-class {
    padding: 1rem;
    font-size: 0.95rem;
  }
}

/* 4. LARGE TABLET STYLES (768px - 1024px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .my-class {
    padding: 1.5rem;
    font-size: 1rem;
  }
}

/* 5. DESKTOP STYLES (1024px+) */
@media (min-width: 1024px) {
  .my-class {
    padding: 2rem;
    font-size: 1.1rem;
  }
}

/* 6. ORIENTATION-SPECIFIC (if needed) */
@media (orientation: landscape) and (max-height: 600px) {
  .my-class {
    padding: 0.5rem;
  }
}
```

## Common Breakpoints Quick Reference

| Name | Min | Max | Target Device |
|------|-----|-----|---|
| xsmall | 0 | 479px | iPhone SE, small Android |
| small | 480px | 767px | iPhone 12, larger Android |
| medium | 768px | 1023px | iPad, iPad Mini |
| large | 1024px | ∞ | Desktop, laptops |

## Touch-Friendly Sizing Checklist

```css
/* Always ensure touch targets are at least 44x44px */
.button,
.link,
.input,
.tab {
  /* Height */
  min-height: 44px;
  
  /* Width */
  min-width: 44px;
  
  /* Padding for easy clicking */
  padding: 12px 16px;
}

/* On mobile, increase the padding more */
@media (max-width: 767px) {
  .button,
  .link,
  .input {
    min-height: 48px;
    padding: 14px 18px;
  }
}
```

## Common Responsive Patterns

### 1. Grid Responsive (Multi-column → Single column)

**Desktop**: 4 columns
**Tablet**: 2 columns  
**Phone**: 1 column

```css
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

@media (max-width: 767px) {
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 479px) {
  .metric-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}
```

### 2. Font Size Responsive (Large → Small)

**Desktop**: 2.5rem
**Tablet**: 2rem
**Phone**: 1.5rem

```css
.page-title {
  font-size: 2.5rem;
}

@media (max-width: 767px) {
  .page-title {
    font-size: 2rem;
  }
}

@media (max-width: 479px) {
  .page-title {
    font-size: 1.5rem;
  }
}
```

### 3. Padding/Margin Scale Down

**Desktop**: 2rem
**Tablet**: 1.5rem
**Phone**: 1rem

```css
.card {
  padding: 2rem;
}

@media (max-width: 767px) {
  .card {
    padding: 1.5rem;
  }
}

@media (max-width: 479px) {
  .card {
    padding: 1rem;
  }
}
```

### 4. Hide/Show Elements

```css
/* Show on desktop, hide on mobile */
.desktop-only {
  display: block;
}

@media (max-width: 767px) {
  .desktop-only {
    display: none;
  }
}

/* Show on mobile, hide on desktop */
.mobile-only {
  display: none;
}

@media (max-width: 767px) {
  .mobile-only {
    display: block;
  }
}
```

### 5. Full-Width Buttons on Mobile

```css
.button {
  /* Desktop: inline sizing */
  padding: 0.75rem 1.5rem;
  width: auto;
}

@media (max-width: 479px) {
  .button {
    /* Mobile: full width */
    width: 100%;
    padding: 0.65rem 1rem;
  }
}
```

### 6. Horizontal Scroll on Small Screens

```css
.scroll-container {
  display: flex;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* Smooth scroll on iOS */
}

@media (max-width: 767px) {
  .scroll-container {
    margin: 0 -1rem;
    padding: 0 1rem;
  }
  
  .scroll-item {
    flex: 0 0 80vw; /* Take 80% of viewport width */
    margin-right: 1rem;
  }
}
```

## CSS Properties Reference

### Flex Layout on Mobile
```css
.container {
  display: flex;
  flex-direction: row;
}

@media (max-width: 479px) {
  .container {
    flex-direction: column;
    gap: 1rem;
  }
}
```

### Grid Layout on Mobile
```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

@media (max-width: 479px) {
  .container {
    grid-template-columns: 1fr;
  }
}
```

### Responsive Sizing (rem-based)
```css
/* Base - all devices */
.element {
  font-size: 1rem;     /* 16px */
  padding: 1rem;       /* 16px */
  margin: 0.5rem;      /* 8px */
}

/* Mobile scaling */
@media (max-width: 479px) {
  .element {
    font-size: 0.9rem;  /* 14.4px */
    padding: 0.75rem;   /* 12px */
    margin: 0.375rem;   /* 6px */
  }
}
```

## Performance Tips

### 1. Media Query Organization
```css
/* Good: Group by breakpoint */
@media (max-width: 479px) {
  .card { ... }
  .button { ... }
  .header { ... }
}

/* Avoid: Scattered media queries */
.card { ... }
@media (max-width: 479px) { .card { ... } }
.button { ... }
@media (max-width: 479px) { .button { ... } }
```

### 2. Reuse Classes
```css
/* Good: Use utility classes */
.full-width-mobile { width: 100%; }
.hide-mobile { display: none; }
.stack-mobile { flex-direction: column; }

/* Apply to multiple elements */
<button class="button full-width-mobile">...</button>
<div class="card stack-mobile">...</div>
```

### 3. Min/Max Width Instead of Height
```css
/* Good: responsive to content */
.container {
  max-width: 1200px;
  min-height: auto;
}

/* Avoid: fixed heights that don't adapt */
.container {
  width: 1200px;
  height: 500px;
}
```

## Testing Your Changes

### 1. Add to a Single Component
```
1. Open frontend/src/styles/mobile-responsive.css
2. Find the media queries section
3. Add your class under the appropriate breakpoint
4. Save file (hot reload will apply)
5. Test in browser DevTools responsive mode
```

### 2. Test All Breakpoints
```bash
# Open in browser and test these widths:
- 375px (iPhone SE)
- 480px (breakpoint)
- 768px (iPad)
- 1024px (breakpoint)
- 1200px (desktop)
```

### 3. Verify Cascade
```
Chrome DevTools > Elements > Styles tab
1. Find your element
2. Check which styles are applied
3. Verify media query is active (blue highlight)
4. Check if overriding correctly
```

## Common Mistakes to Avoid

### ❌ Wrong: Nested media queries in CSS-in-JS
```css
/* This won't work in regular CSS */
.container {
  @media (max-width: 479px) {
    display: flex;
  }
}
```

### ✅ Right: Separate media query blocks
```css
.container {
  display: grid;
}

@media (max-width: 479px) {
  .container {
    display: flex;
  }
}
```

### ❌ Wrong: Typo in media query
```css
@media (max-width: 479ps) {  /* Wrong: ps instead of px */
  .item { ... }
}
```

### ✅ Right: Correct unit
```css
@media (max-width: 479px) {
  .item { ... }
}
```

### ❌ Wrong: Multiple conditions with OR (not supported in CSS)
```css
@media (max-width: 479px) or (min-width: 1024px) { /* Wrong */
  .item { ... }
}
```

### ✅ Right: Use AND for combined conditions
```css
@media (min-width: 768px) and (max-width: 1023px) {
  .item { ... }
}
```

## Debugging Tips

### Issue: Styles Not Applying
```
Debug:
1. Check selector spelling matches HTML class exactly
2. Verify media query condition is correct
3. Check CSS cascade - is another rule overriding?
4. Hard refresh browser (Ctrl+Shift+R)
5. Check browser console for CSS parse errors
```

### Issue: Sizing Looks Different in DevTools vs Real Device
```
Check:
1. Device zoom level (should be 100%)
2. Device pixel ratio (DevTools can simulate different DPR)
3. Real device orientation
4. For testing: Use Browser's actual responsive mode, not simulated phone
```

### Issue: Media Query Works in Desktop but Not Mobile
```
Check:
1. Viewport meta tag in index.html
2. Media query is targeting the right breakpoint
3. CSS file is loaded (check Network tab)
4. No CSS conflicts from inline styles
5. Parent element styles not restricting width
```

## File Edit Quick Start

To add responsive styles to a component:

1. **Open**: `frontend/src/styles/mobile-responsive.css`
2. **Find**: The section for your component
3. **Add**: Under the appropriate breakpoint
   ```css
   @media (max-width: 479px) {
     .my-new-class {
       /* mobile styles */
     }
   }
   ```
4. **Save**: Ctrl+S
5. **Test**: DevTools responsive mode

## Resources

- **MDN Media Queries**: https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries
- **CSS Tricks**: https://css-tricks.com/a-complete-guide-to-grid/
- **Apple HIG**: 44pt minimum touch target (https://developer.apple.com/design/human-interface-guidelines/)
- **Material Design**: 48dp minimum touch target (https://material.io/design/usability/accessibility.html)

---

**Save this file as a reference while developing!**
