const english = new URLSearchParams(location.search).get("lang") === "en";
document.documentElement.lang = english ? "en" : "ja";

if (english) {
  for (const element of document.querySelectorAll("[data-video-en]")) {
    element.setAttribute(element.tagName === "IFRAME" ? "src" : "href", element.dataset.videoEn);
  }
}

for (const section of document.querySelectorAll("[data-ja], [data-en]")) {
  section.hidden = english ? section.hasAttribute("data-ja") : section.hasAttribute("data-en");
}

document.querySelector("#ja-link").setAttribute("aria-current", String(!english));
document.querySelector("#en-link").setAttribute("aria-current", String(english));
