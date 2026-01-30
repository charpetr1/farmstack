import styles from "./Sidebar.module.css";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <nav className={styles.nav}>
        <NavLink
          to="/lists"
          className={({ isActive }) =>
            isActive ? styles.active : undefined
          }
        >
          My Lists
        </NavLink>
      </nav>
    </aside>
  );
}
