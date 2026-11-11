import { createRoot } from "react-dom/client";
import { App } from "./ui/App.tsx";
import "./design/theme.css";
import "./design/app.css";

createRoot(document.getElementById("root")!).render(<App />);
