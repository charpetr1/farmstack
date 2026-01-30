import styles from "./Header.module.css";
import ThemeToggle from "../components/ThemeToggle";
import LogoutButton from "../components/LogoutButton";

export default function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.logo}>Lists App</h1>

      <div className={styles.actions}>
        <ThemeToggle />
        <LogoutButton />
      </div>
    </header>
  );
}
