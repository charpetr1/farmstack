import styles from "./Card.module.css";
import type { PropsWithChildren } from "react";

type CardProps = PropsWithChildren<object>;

export default function Card({ children }: CardProps) {
  return <div className={styles.card}>{children}</div>;
}
