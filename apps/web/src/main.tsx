import { createRoot } from "react-dom/client";
import { App } from "./ui/App.tsx";
import "./design/theme.css";
import "./design/app.css";
import "./design/workspace.css";
import "./design/parity.css";

createRoot(document.getElementById("root")!).render(<App />);
