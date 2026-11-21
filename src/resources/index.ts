import siteData from "./site-data";
import themeList from "./themes.json";

export { siteData };
export const baseURL = siteData.baseURL;
export const person = siteData.person;
export const themes = themeList.themes;
export const defaultTheme = themeList.default;

/** The pages in the header, in order. */
export const nav = [
  { path: "/", label: "home" },
  { path: "/about", label: "about" },
  { path: "/work", label: "work" },
  { path: "/gallery", label: "gallery" },
  { path: "/github", label: "open source" },
];
