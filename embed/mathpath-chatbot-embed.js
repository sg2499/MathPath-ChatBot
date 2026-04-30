(function () {
  const currentScript = document.currentScript;
  const chatbotUrl = currentScript?.getAttribute("data-chatbot-url") || "https://your-chatbot-frontend.vercel.app/?embed=1&open=1";
  const logoUrl = currentScript?.getAttribute("data-logo-url") || "https://your-chatbot-frontend.vercel.app/MathPath-Logo.png";
  const position = currentScript?.getAttribute("data-position") || "right";

  const existing = document.getElementById("mathpath-ai-chatbot-container");
  if (existing) return;

  const container = document.createElement("div");
  container.id = "mathpath-ai-chatbot-container";
  container.style.position = "fixed";
  container.style.bottom = "22px";
  container.style[position === "left" ? "left" : "right"] = "22px";
  container.style.zIndex = "2147483647";
  container.style.fontFamily = "Inter, Arial, sans-serif";

  const launcher = document.createElement("button");
  launcher.type = "button";
  launcher.setAttribute("aria-label", "Open MathPath AI chatbot");
  launcher.innerHTML = '<img src="' + logoUrl + '" alt="MathPath"/><span>Ask MathPath AI</span>';
  launcher.style.display = "flex";
  launcher.style.alignItems = "center";
  launcher.style.gap = "10px";
  launcher.style.border = "2px solid rgba(255, 63, 127, 0.25)";
  launcher.style.borderRadius = "999px";
  launcher.style.background = "#ffffff";
  launcher.style.color = "#292d63";
  launcher.style.padding = "10px 16px 10px 10px";
  launcher.style.boxShadow = "0 18px 48px rgba(41,45,99,0.24)";
  launcher.style.cursor = "pointer";
  launcher.style.fontWeight = "800";
  launcher.style.fontSize = "14px";

  const style = document.createElement("style");
  style.textContent = '#mathpath-ai-chatbot-container button img{width:54px;height:54px;object-fit:contain;border-radius:50%;background:white;padding:3px;} #mathpath-ai-chatbot-frame{display:none;width:min(440px,calc(100vw - 28px));height:min(720px,calc(100vh - 32px));border:0;border-radius:28px;background:transparent;box-shadow:0 22px 60px rgba(41,45,99,0.24);} @media(max-width:560px){#mathpath-ai-chatbot-container{right:10px!important;left:10px!important;bottom:10px!important;}#mathpath-ai-chatbot-frame{width:100%;height:calc(100vh - 20px);border-radius:22px;}#mathpath-ai-chatbot-container button span{display:none;}}';
  document.head.appendChild(style);

  const iframe = document.createElement("iframe");
  iframe.id = "mathpath-ai-chatbot-frame";
  iframe.title = "MathPath AI Chatbot";
  iframe.src = chatbotUrl;
  iframe.allow = "clipboard-write";

  launcher.addEventListener("click", function () {
    launcher.style.display = "none";
    iframe.style.display = "block";
  });

  container.appendChild(launcher);
  container.appendChild(iframe);
  document.body.appendChild(container);
})();
