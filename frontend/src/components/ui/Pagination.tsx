import styles from "./Pagination.module.css";
import type { FC } from "react";

interface PaginationProps {
  page: number;
  total: number;
  pageSize: number;
  onChange: (newPage: number) => void;
}

const Pagination: FC<PaginationProps> = ({ page, total, pageSize, onChange }) => {
  const totalPages = Math.ceil(total / pageSize);

  if (totalPages <= 1) return null;

  return (
    <div className={styles.pagination}>
      <button
        disabled={page === 1}
        onClick={() => onChange(page - 1)}
      >
        Prev
      </button>

      <span>
        Page {page} / {totalPages}
      </span>

      <button
        disabled={page === totalPages}
        onClick={() => onChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
