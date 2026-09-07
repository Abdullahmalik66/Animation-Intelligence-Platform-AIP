# Animation Security Reference

Security rules for all frontend animation implementations.

---

## Core Rules

### Never

- ❌ Load animation assets (Lottie JSON, Rive files, GLTF models) from untrusted external URLs
- ❌ Inject SVG content into the DOM without sanitization
- ❌ Run remote scripts as part of an animation setup
- ❌ Expose API keys, tokens, or secrets in animation configuration
- ❌ Trust user-provided animation data without validation
- ❌ Install animation dependencies without verifying their origin and integrity

### Always

- ✅ Serve animation assets from your own origin or a trusted, verified CDN
- ✅ Use Subresource Integrity (SRI) for CDN-loaded library scripts
- ✅ Sanitize SVG before DOM injection
- ✅ Validate Lottie JSON structure before loading
- ✅ Use Content Security Policy (CSP) to restrict script and media sources

---

## SVG Injection Safety

SVG can contain `<script>` tags and event handlers. Never inject raw SVG from user input:

```typescript
// UNSAFE
element.innerHTML = userProvidedSvg;

// SAFE — use DOMPurify to sanitize
import DOMPurify from "dompurify";
element.innerHTML = DOMPurify.sanitize(userProvidedSvg, {
  USE_PROFILES: { svg: true, svgFilters: true },
});
```

---

## CDN Usage (SRI)

If loading libraries from a CDN, use Subresource Integrity:

```html
<script
  src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"
  integrity="sha512-..."
  crossorigin="anonymous"
></script>
```

---

## Lottie File Safety

Lottie JSON files should:
- Be loaded from your own origin or verified CDN
- Be validated for structure before rendering
- Not be generated from untrusted user input

---

## Content Security Policy

Animation CSP considerations:

```
Content-Security-Policy:
  script-src 'self';           # No remote scripts
  img-src 'self' data:;        # Lottie may use data URIs
  connect-src 'self';          # No external API calls
  media-src 'self';            # Video backgrounds from own origin only
```

---

## Dependency Safety

Before installing any animation library:
- Verify the package on npmjs.com (download count, maintainers)
- Check the GitHub repository for activity and issues
- Run `npm audit` after installation
- Pin versions in `package.json` — avoid `*` or `latest`
