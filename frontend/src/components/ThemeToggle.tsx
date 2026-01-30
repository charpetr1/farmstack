import { useTheme } from "../theme/useTheme";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

 return ( 
 <button onClick={toggleTheme} className={"theme-button"}> 
 {theme === "dark" ? "☀️ Light" : "🌙 Dark"} 
 </button> 
 );
}
