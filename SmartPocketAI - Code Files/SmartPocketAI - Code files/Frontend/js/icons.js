/* ============================================================
   Smartpocket AI — Icon System
   A small, consistent stroke-icon set (Lucide-style paths) used
   everywhere instead of emoji, so the UI reads as a crafted
   product rather than a generic template.
   Usage: Icon("home", "ic") -> returns inline <svg> markup string
   ============================================================ */
const ICONS = {
  // Navigation
  dashboard: '<path d="M3 13h8V3H3v10Zm10 8h8V11h-8v10ZM3 21h8v-6H3v6ZM13 3v6h8V3h-8Z"/>',
  sofa: '<path d="M4 15v-3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"/><path d="M2 15h20v3a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-3Z"/><path d="M6 15V8a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v7"/><path d="M4 19v2M20 19v2"/>',
  party: '<path d="M12 2a5 5 0 0 1 5 5c0 3.5-2.5 6.5-4 8l-1 5-1-5c-1.5-1.5-4-4.5-4-8a5 5 0 0 1 5-5Z"/><path d="M12 15v1"/>',
  gem: '<path d="M6 3h12l4 6-10 12L2 9Z"/><path d="M11 3 8 9l4 12 4-12-3-6"/><path d="M2 9h20"/>',
  history: '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l3 3"/>',
  logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/>',
  menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
  close: '<path d="M18 6 6 18M6 6l12 12"/>',

  // UI / status
  arrowRight: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  chevronDown: '<path d="m6 9 6 6 6-6"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  checkCircle: '<circle cx="12" cy="12" r="9"/><path d="m9 12 2 2 4-4"/>',
  clipboard: '<rect x="6" y="4" width="12" height="16" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><path d="M9 11h6M9 15h6"/>',
  wallet: '<path d="M3 7a2 2 0 0 1 2-2h13a1 1 0 0 1 1 1v2"/><path d="M3 7v11a2 2 0 0 0 2 2h14a1 1 0 0 0 1-1v-4"/><path d="M17 12h3a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-3a2 2 0 0 1 0-4Z"/>',
  star: '<path d="m12 2 3.1 6.6 7.2.9-5.3 5 1.4 7.2L12 18.3 5.6 21.7 7 14.5l-5.3-5 7.2-.9L12 2Z"/>',
  sparkle: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="m5.6 5.6 2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  cog: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.9.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.9V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
  trash: '<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0-1 14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2L4 6"/><path d="M10 11v6M14 11v6"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  refresh: '<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v5h-5"/>',
  upload: '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
  camera: '<path d="M4 8a2 2 0 0 1 2-2h1.5l1-1.5h6l1 1.5H18a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8Z"/><circle cx="12" cy="13" r="3.5"/>',
  filter: '<path d="M4 5h16l-6 8v5l-4 2v-7L4 5Z"/>',
  lock: '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a8 8 0 0 1 16 0v1"/>',
  bulb: '<path d="M9 18h6M10 22h4"/><path d="M12 2a6 6 0 0 0-4 10.5c.6.5 1 1.3 1 2.1V15a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-.4c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 2Z"/>',
  fan: '<circle cx="12" cy="12" r="1.5"/><path d="M12 10.5c-1-2-2-6-.5-7.5S15 3.5 13.5 6a3 3 0 0 0-1.5 4.5Zm0 3c1 2 2 6 .5 7.5S9 20.5 10.5 18a3 3 0 0 0 1.5-4.5Zm-1.5-1.5c-2 1-6 2-7.5.5S3.5 9 6 10.5a3 3 0 0 0 4.5 1.5Zm3 0c2-1 6-2 7.5-.5S20.5 15 18 13.5a3 3 0 0 0-4.5-1.5Z"/>',
  table: '<path d="M3 8h18M6 8v11M18 8v11"/><path d="M3 8V6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2"/>',
  palette: '<circle cx="13.5" cy="6.5" r="1.2"/><circle cx="17.5" cy="10.5" r="1.2"/><circle cx="8.5" cy="7.5" r="1.2"/><circle cx="6.5" cy="12.5" r="1.2"/><path d="M12 22a10 10 0 1 1 8-16c1 1.5.4 3.5-1.5 3.9-1.2.2-2.5-.2-3.4.6-1 .9-.8 2.5.4 3.2.9.5 1.5 1.4 1.2 2.5-.4 1.6-2.5 2.3-4.7 2.1"/>',
  building: '<path d="M4 21V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v16"/><path d="M12 10h7a1 1 0 0 1 1 1v10"/><path d="M8 8v.01M8 12v.01M8 16v.01M15 14v.01M15 17v.01M2 21h20"/>',
  utensils: '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M9 3v18M17 3c-1.7 0-3 2.2-3 5s1.3 5 3 5v10"/>',
  balloon: '<path d="M12 2a5 5 0 0 1 5 5c0 3.5-2.5 6.5-4 8l-1 5-1-5c-1.5-1.5-4-4.5-4-8a5 5 0 0 1 5-5Z"/><path d="M12 15v1"/>',
  music: '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
  aperture: '<circle cx="12" cy="12" r="9"/><path d="m14.3 3.6 5.2 3-2.7 4.7M9.7 3.6 4.5 6.6l2.7 4.7M4.5 17.4l5.2 3 2.7-4.7M19.5 17.4l-5.2 3-2.7-4.7M2.7 9 6 12l-3.3 3M21.3 9 18 12l3.3 3"/>',
  gift: '<rect x="3" y="9" width="18" height="12" rx="1"/><path d="M3 14h18M12 9v12"/><path d="M12 9C9 9 8 7.5 8 6a2.5 2.5 0 0 1 5-1c.3-1.5 1.7-2.5 3-2a2.5 2.5 0 0 1 1 4.5c-.7.7-2 1.5-5 1.5Z"/>',
  link: '<path d="M9 15 15 9"/><path d="M14 6.5 15.5 5a3.5 3.5 0 0 1 5 5l-1.5 1.5"/><path d="M10 17.5 8.5 19a3.5 3.5 0 0 1-5-5l1.5-1.5"/>',
  ring: '<circle cx="12" cy="15" r="6"/><path d="m9 9 3-6 3 6"/>',
  necklace: '<path d="M4 4c0 6 3.5 10 8 10s8-4 8-10"/><circle cx="12" cy="17.5" r="2.5"/>',
  earring: '<circle cx="12" cy="6" r="2"/><path d="M12 8v4a3 3 0 1 0 3 3"/>',
  bracelet: '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="3"/>',
};

function Icon(name, cls = "ic", size = null) {
  const path = ICONS[name] || ICONS.sparkle;
  const style = size ? ` style="width:${size}px;height:${size}px"` : "";
  return `<svg class="${cls}"${style} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${path}</svg>`;
}
